#!/usr/bin/env python3
"""routes_hygiene.py -- automated structural legacy-route cleanliness (strictly honoring Rule F22).

WHAT: keeps `game/routes/` clean automatically without Admiral toil and WITHOUT ever banning or retiring a route for
      economics, losses, empty bids, or depleted fields (Rule F22: "Nothing is bad for good").
      A route is eligible for archiving to `game/routes/archive/` ONLY when ALL four structural conditions hold:
        1. `status == "off"` explicitly set by its author in the route JSON.
        2. Its `note` / `off_reason` explicitly declares structural replacement or permanent retirement (`replaced by`,
           `superseded by`, `retired:`), NEVER danger, pirate, bid, price, loss, or empty field.
        3. The route appears in `0` active division plans (`game/routes/plans/*.json`) and `0` templates (`game/routes/templates/*.json`).
        4. The file has not been modified for at least 24 hours.
      Archived JSONs stay intact in `game/routes/archive/` in git so any route can be restored in one command.
USAGE:
  python3 -I -B game/fleet/routes_hygiene.py [--root /srv/collective/the-collective] [--write]
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPLACED_RE = re.compile(r"\b(?:replaced\s+by|superseded\s+by|retired\s+for\s+good|obsolete\s+duplicate)\b", re.I)
FORBIDDEN_ECONOMIC_RE = re.compile(r"\b(?:pirate|danger|loss|losing|unprofitable|empty\s+bid|no\s+bid|depleted)\b", re.I)
MIN_AGE_S = 24 * 3600


def referenced_routes(game_dir):
    refs = set()
    for sub in ("plans", "templates"):
        d = Path(game_dir) / "routes" / sub
        if not d.is_dir():
            continue
        for fp in d.glob("*.json"):
            try:
                txt = fp.read_text(encoding="utf-8")
            except OSError:
                continue
            for m in re.finditer(r'"([a-z0-9][a-z0-9_-]{2,80})"', txt):
                refs.add(m.group(1))
    return refs


def scan_candidates(root, now=None):
    now = time.time() if now is None else now
    rroot = Path(root)
    game_dir = rroot / "game" if (rroot / "game" / "routes").is_dir() else rroot
    rdir = game_dir / "routes"
    refs = referenced_routes(game_dir)
    candidates = []
    for fp in sorted(rdir.glob("*.json")):
        if fp.name == "plan.json":
            continue
        rid = fp.stem
        if rid in refs:
            continue
        try:
            st = fp.stat()
            if now - st.st_mtime < MIN_AGE_S:
                continue
            doc = json.loads(fp.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(doc, dict) or doc.get("status") != "off":
            continue
        # HARD F22 INVARIANT: never inspect `measured`, `cph`, `credits`, or `runs`!
        note = " ".join(str(doc.get(k) or "") for k in ("note", "off_reason", "why_off"))
        if REPLACED_RE.search(note) and not FORBIDDEN_ECONOMIC_RE.search(note):
            candidates.append((rid, fp, note[:120]))
    return candidates


def run_hygiene(root, write=False, commit=True, now=None):
    rroot = Path(root)
    repo_root = rroot.parent if rroot.name == "game" else rroot
    cands = scan_candidates(repo_root, now=now)
    if not cands:
        print("ROUTES HYGIENE: clean (0 superseded off-routes due; F22 economic routes untouched)")
        return 0
    if not write:
        print("ROUTES HYGIENE (dry-run): %d superseded off-route(s) eligible for game/routes/archive/:" % len(cands))
        for rid, _fp, note in cands[:20]:
            print("  %s | %s" % (rid, note))
        return 0
    arch_dir = repo_root / "game" / "routes" / "archive"
    arch_dir.mkdir(parents=True, exist_ok=True)
    moved_rels = []
    for rid, fp, _note in cands[:25]:
        dest = arch_dir / fp.name
        os.replace(fp, dest)
        moved_rels.extend([str(fp.relative_to(repo_root)), str(dest.relative_to(repo_root))])
    # Rebuild routes index files so routes.py check stays green
    subprocess.run([sys.executable, "-I", "-B", str(repo_root / "game/fleet/routes.py"), "index", "--root", str(repo_root / "game")], check=False)
    for idx_name in ("master-index.md", "index.md"):
        ip = repo_root / "game" / "routes" / idx_name
        if ip.exists():
            moved_rels.append(str(ip.relative_to(repo_root)))
    if commit and moved_rels:
        subprocess.run(["git", "add", "-A", "--"] + moved_rels, cwd=repo_root, check=False)
        subprocess.run(["git", "-c", "user.name=Collective Hygiene", "-c", "user.email=fleet@suggi-workspace.dev",
                        "commit", "-m", "routes: auto-archive %d superseded off-routes (F22-safe)" % len(cands[:25]), "--"] + moved_rels,
                       cwd=repo_root, check=False, capture_output=True)
    print("ROUTES HYGIENE: archived %d superseded off-route(s) into game/routes/archive/" % len(cands[:25]))
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    root = args[args.index("--root") + 1] if "--root" in args and args.index("--root") + 1 < len(args) else str(Path(__file__).resolve().parents[2])
    return run_hygiene(root, write="--write" in args, commit="--no-commit" not in args)


if __name__ == "__main__":
    sys.exit(main())
