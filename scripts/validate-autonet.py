#!/usr/bin/env python3
"""Structural AutoNet invariant validator (CI + pre-commit hook).

Ensures Admirals adapt and tune AutoNet parameters or stack P3 strategies ON TOP
rather than disabling engines, deleting core lanes (e.g. arbitrage), choking all
belts, or stripping *-network routes out of division plans.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

REQUIRED_POLICIES = (
    "game/haul-policy.json",
    "game/haul-policy-trade.json",
    "game/mine-policy.json",
    "game/hunt-policy.json",
    "game/bursar-policy.json",
    "game/craft-policy.json",
    "game/fit-policy.json",
    "game/census-policy.json",
)

REQUIRED_HAUL_LANES = ("active_freight", "internal_supply", "public_freight", "arbitrage")

REQUIRED_PLAN_ROUTES = {
    "game/routes/plans/miner.json": ("mine-network", "fit-network"),
    "game/routes/plans/drone.json": ("hunt-network", "fit-network"),
    "game/routes/plans/sentinel.json": ("hunt-network", "fit-network"),
    "game/routes/plans/hauler.json": ("haul-network", "fit-network"),
    "game/routes/plans/trader.json": ("bursar-network", "haul-network-trade", "fit-network"),
    "game/routes/plans/scout.json": ("fit-network", "census-network"),
}


def check_repo(repo_root=None):
    root = Path(repo_root) if repo_root else REPO
    errors = []

    for rel in REQUIRED_POLICIES:
        p = root / rel
        if not p.is_file():
            errors.append(f"MISSING policy: {rel}")
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"INVALID JSON in {rel}: {e}")
            continue
        if not isinstance(d, dict):
            errors.append(f"Policy {rel} must be a JSON object")
            continue
        if d.get("enabled", True) is False:
            errors.append(f"{rel}: enabled=false is forbidden (tune parameters or stack P3 strategies on top instead)")

        if rel == "game/haul-policy.json":
            lanes = d.get("lanes") or []
            missing = [ln for ln in REQUIRED_HAUL_LANES if ln not in lanes]
            if missing:
                errors.append(f"{rel}: required core lanes missing: {missing} (keep arbitrage, internal_supply, public_freight, active_freight)")

        elif rel == "game/mine-policy.json":
            if bool(d.get("policed_only", True)) and not bool(d.get("allow_lawless_for_deficit", True)) and int(d.get("lawless_min_tier") or 1) > 3:
                errors.append(f"{rel}: policed_only=true + allow_lawless_for_deficit=false + lawless_min_tier>3 starves miners of deficit belts")
            if float(d.get("min_left_pct") or 5) < 5.0:
                errors.append(f"{rel}: min_left_pct must stay >= 5% to stay safely above deposit_too_sparse")

        elif rel == "game/hunt-policy.json":
            if int(d.get("keep_herd", 1)) < 1:
                errors.append(f"{rel}: keep_herd must stay >= 1 to prevent herd extinction")
            if not bool((d.get("solo") or {}).get("enabled", True)):
                errors.append(f"{rel}: solo.enabled=false is forbidden")
            if not bool((d.get("escort") or {}).get("enabled", True)):
                errors.append(f"{rel}: escort.enabled=false is forbidden (tune threat gate instead)")
            if int((d.get("escort") or {}).get("min_escorts") or 3) < 3:
                errors.append(f"{rel}: escort.min_escorts must stay >= 3 (Suggi doctrine)")

        elif rel == "game/bursar-policy.json":
            if not bool((d.get("sell") or {}).get("enabled", True)):
                errors.append(f"{rel}: sell.enabled=false is forbidden")
            if not bool((d.get("buy") or {}).get("enabled", True)):
                errors.append(f"{rel}: buy.enabled=false is forbidden")

        elif rel == "game/fit-policy.json":
            specs = d.get("specialties") or {}
            req_fit_slots = {
                ("Mining", "ore"): ("utility", "defense"),
                ("Mining", "ice"): ("utility", "defense"),
                ("Mining", "gas"): ("utility", "defense"),
                ("Logistics", "freight"): ("utility", "defense"),
                ("Logistics", "passenger"): ("utility", "defense"),
                ("Military", "brawler"): ("weapon", "defense", "utility"),
                ("Military", "ewar"): ("weapon", "defense", "utility"),
                ("Military", "flak_tank"): ("weapon", "defense", "utility"),
                ("Military", "royal_guard_escort"): ("weapon", "defense", "utility"),
                ("Military", "royal_guard_utility"): ("weapon", "defense", "utility"),
                ("Intel", "covert_recon"): ("utility", "defense"),
                ("Intel", "sensor_survey"): ("utility", "defense"),
                ("Trade", "mobile"): ("utility", "defense"),
            }
            for (div_k, sp_k), req_slots in req_fit_slots.items():
                ld = ((specs.get(div_k) or {}).get("loadouts") or {}).get(sp_k) or {}
                for sl in req_slots:
                    if not (ld.get(sl) or []):
                        errors.append(f"{rel}: {div_k}.{sp_k}.{sl} loadout cannot be empty (Suggi mandate: always keep non-bursar fleet modules upgrading automatically)")

    for rel, req_routes in REQUIRED_PLAN_ROUTES.items():
        p = root / rel
        if not p.is_file():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"INVALID JSON in {rel}: {e}")
            continue
        routes = set(d.get("routes") or [])
        ships = d.get("ships") or {}
        for r in req_routes:
            if r not in routes:
                errors.append(f"{rel}: missing required AutoNet route '{r}' (stack P3 strategies on top, never strip AutoNet)")
            elif int(ships.get(r, 1)) <= 0:
                errors.append(f"{rel}: AutoNet route '{r}' ship cap cannot be 0")


    # Verify matrix_match module exists and hosting.json (when live) hosts every AutoNet *_net kind
    mm_path = root / "game" / "fleet" / "matrix_match.py"
    if not mm_path.is_file():
        errors.append("MISSING game/fleet/matrix_match.py (global optimal batch matching & mission-board gate)")
    live_hosting = Path("/srv/collective/data/fleet/hosting.json")
    if root == REPO and live_hosting.is_file():
        try:
            hk = set((json.loads(live_hosting.read_text(encoding="utf-8")) or {}).get("kinds") or [])
            for req_k in ("mine_net", "hunt_net", "fit_net", "craft_net", "salvage_net", "pirate_net", "census_net", "haul", "bursar"):
                if req_k not in hk:
                    errors.append(f"hosting.json missing required hosted kind '{req_k}' (causes SPAWN_MOST idle starvation)")
        except Exception as e:
            errors.append(f"INVALID /srv/collective/data/fleet/hosting.json: {e}")

    # Rule R6: hosted runner scripts MUST pass sys.argv[1:] to argparse (never bare .parse_args() which reads host argv)
    for _rname in ("route_run.py", "hunt.py", "census.py", "mine.py", "guard.py", "bursar.py", "haul.py",
                   "mine_net.py", "hunt_net.py", "fit_net.py", "craft_net.py", "salvage_net.py", "pirate_net.py", "census_net.py"):
        _rp = root / "game" / "fleet" / _rname
        if _rp.is_file() and ".parse_args()" in _rp.read_text(encoding="utf-8"):
            errors.append(f"game/fleet/{_rname}: bare .parse_args() reads runhost process argv instead of thread Facade sys.argv[1:]")

    return errors


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO
    errs = check_repo(root)
    if errs:
        print("AUTONET INVARIANT CHECK FAILED:")
        for e in errs:
            print("  -", e)
        return 1
    print("AUTONET INVARIANT CHECK: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
