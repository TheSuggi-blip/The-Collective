#!/usr/bin/env python3
"""wallet.py -- no ship of ours goes broke: a ship whose wallet runs low is given credits by a rich ship of its division.

WHAT: every pilot pays its own fuel, repairs, fittings and tax from its own wallet. This script reads every wallet
      (data/fleet/fleet.json) and, for each pilot under LOW, has the richest ship of the same division give it
      credits up to TARGET (a credit gift: the game's storage `deposit` of item `credits` to the pilot's name; it
      works from anywhere, also while both ships fly). A division without a donor is helped by the command group.
      When no single ship can give the whole need, several give, each what it holds above KEEP; the receiver is
      read once after its gift, so that the fleet file and the dispatcher see it.
      Every gift is booked twice in data/fleet/onetime.json (`Wallet top-up`, minus for the giver, plus for the
      receiver), so it moves no division's steady money, and kept in data/fleet/gifts.jsonl.
      The dispatcher does its part (dispatch.py, FLOOR): a pilot under 5,000 cr is sent only on work that pays.
      The sweep fills the faction's treasury, the fleet's main purse: a ship holding SWEEP_AT or more gives what it
      holds above KEEP_SHIP to the faction's leader (empire.json faction.leader), a few ships a pass, and the leader
      deposits what it holds above KEEP_SHIP into the treasury (the same storage `deposit` of `credits`, target
      `faction`) once that is MIN_DEPOSIT or more. A gift is booked as a top-up is (gifts.jsonl, onetime.json), a
      deposit once in onetime.json under routes.TREASURY (minus for the leader): a move between two purses of ours,
      no cost (routes.deposits, station/fleet.py). What the sweep tried is kept in data/fleet/sweep.jsonl; a deposit
      is written there as `sent` before its call, so a pass the job cuts (its `timeout 200`) loses no deposit: the
      next pass reads the treasury and books it, with the time it was sent, or keeps it unsure. A gift is written the
      same way (sweep.jsonl kind `gift` for the sweep's, `topup` for a top-up, with both wallets read right before
      the call): the next pass settles a `sent` gift from the receiver's wallet (errors.log ENT-116, DECISIONS Q75).
RULES:
  - A donor keeps KEEP credits at least; one gift per pilot per COOLDOWN (the wallets are read every ten seconds,
    the game's answer can lag): a pilot is never given twice for one low reading.
  - Every gift is booked the moment the game took it, with its own time: a fault later in the pass never loses the
    record, and a run's figure leaves the gift out by that time (routes.moved). A gate that does not answer is no
    fault of the pass: the wallet is read again after WAIT seconds; a gift that shows is booked, one that does not
    is kept in gifts.jsonl with 0 credits (`unsure`), so its pilot is on cooldown and never given twice.
  - Gifts are not income for the game's tax. They go between our own pilots only, never to another player.
  - `check` prints one HALT line for every pilot under the floor of rule F7 (3,000 cr) and exits 1 then.
  - A real `topup` is the Fleet Admiral's or the five-minute job's; `--dry-run` is free.
  - The sweep gives at most PER_PASS gifts a pass, never from the leader, a builder (empire.json members, role
    Builder: it holds credits for a buy), a pilot of SKIP_PILOTS, a ship not connected, a ship whose loop fails in a
    fight, a pilot refused for a fight in the last BATTLE_WAIT (`in_battle`: asked again at a later pass), or a pilot
    given or giving in the last COOLDOWN. A gift or a deposit is booked only when the giver's wallet, read again, shows
    the money gone (SHOW_WAIT; for a gift also the call's own answer, which carries the giver's wallet after it:
    answer_shows); one that does not show is kept unsure (no booking, the pilot on cooldown; a deposit:
    none again for UNSURE_HOLD). A refused deposit is tried again at the next pass, never twice in one.
  - A gift left `sent` by a cut pass is settled once, at the start of the next pass of its kind: booked with the time
    it was sent when the receiver's wallet, read after the call, rose by most of it and the giver's did not keep it
    (it fell by half of it at least: the receiver's reading before the call can lag an earlier gift of the pass);
    kept unsure otherwise (no booking, both on cooldown from the time it was sent); left `sent` while the receiver
    has no reading after the call, and kept unsure after SENT_KEEP. Its pilots are on cooldown while it stands
    open, so a gift is never given twice and never booked twice.
  - The sweep acts only while SWEEP_ENABLED is on; `sweep --dry-run` says what it would do in any case.
  - A fund (orders ENT-063; autonomous division access Suggi 2026-11-23, rule F12) draws credits from the shared
    faction treasury for a pilot's buy (hull, fit, working capital):
      * Unity (Fleet Admiral) may fund any pilot, uncapped above FUND_FLOOR.
      * Division Admirals (Zero, Mercury, Apollo, Apophis, Oracle) may autonomously fund pilots of their own
        division uncapped per pilot and per 24 hours (rule F12, Suggi 2026-11-24), always keeping treasury
        >= FUND_FLOOR (500,000 cr) -- upgrade hulls and fits as fast as cash allows with no waiting on Unity.
      * Served at the start of every 5-minute sweep pass, up to FUND_BATCH (10) open funds in one batched
        withdrawal while the leader (or any Officer/treasurer role docked at an active Faction Lockbox) stands
        docked. The first fund ever withdraws 1 cr first and reads the treasury (rule F12). The withdrawal is
        booked once in onetime.json (FUND_TITLE, plus for the withdrawer: never steady income), the gift to each
        pilot as every gift is; for FUND_HOURS (or --hours) from its gift the sweep and top-ups leave the funded
        credits with the pilot, then the row ends by itself. A withdrawal whose gift failed stays withdrawn and
        is given at the next pass.
  - Credits withdrawn for a fund or a top-up and not given yet are no donor's to give (`owed`), and a pilot with a
    treasury top-up row standing gets no second gift. A top-up row whose pilot was topped since ends (the leader's
    deposit takes the credits back); one the leader can no longer pay ends, and a new row asks the treasury again.
WHY:  Suggi, 2026-11-16: "No ships can go broke, this is important." Standing work costs fuel and earns nothing, and
      the weekly tax takes a share of every wallet in one moment.

USAGE:
  wallet.py [check]            every wallet against the floors; HALT for a pilot under 3,000 cr
  wallet.py topup [--dry-run]  give each pilot under LOW credits up to TARGET from a rich ship of its division
  wallet.py sweep [--cash-only] [--dry-run]
                               parallel sweep: seated members deposit directly to treasury; unseated gift to leader -> treasury
  wallet.py serve [--dry-run]  serve funds (lockbox or P2P), top-ups, seat & officer auto-queues, errands, and upgrades
  wallet.py fund <pilot[,pilot2...]> <credits> --why "<text>" [--hours H]
                               the treasury pays one or more pilots for a buy (own division for Admirals, uncapped above
                               500k treasury floor; any pilot for Unity); served every 5 min
  wallet.py fund --show        the funds on record, their state, and rolling 24h division autonomous budgets
  --data <dir>                 the unit's data folder (default: the fleet's)

Stdlib only. ASCII only.
"""

import calendar
from concurrent.futures import ThreadPoolExecutor, as_completed
import fcntl
import json
import os
import signal
import sys
import threading
import time
from pathlib import Path

_WRITE_LOCK = threading.Lock()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dispatch                                   # noqa: E402  flagships, roles
import division                                   # noqa: E402  who asks, which roles are whose

FLOOR = 3000                   # rule F7: every pilot keeps this
LOW = 10000                    # a wallet under this is topped up
TARGET = 20000                 # ... to this
KEEP = 30000                   # a donor never goes under this
COOLDOWN = 30 * 60             # one gift per pilot in this many seconds
WAIT = 45                      # seconds until the fleet file shows a gift the gate did not answer for (15 were too few: 2026-11-16, a gift that landed was booked unsure)
BUDGET = 150                   # seconds a pass may give for: what is left waits for the next pass (the job runs every five minutes)
TITLE = "Wallet top-up"
MIN_GIFT = 1000                # a share smaller than this is not worth a call: what a donor holds above KEEP must reach it
# The sweep into the faction's treasury (Suggi, 2026-11-17: a ship keeps up to 50,000 cr, the part above goes into the
# treasury when it is convenient, a few ships a pass). It gives credits away by itself: off until the Fleet Admiral has
# read `wallet.py sweep --dry-run` on the live data and switched it on.
SWEEP_ENABLED = True    # on since 2026-11-17 20:20 UTC, after its dry run on live data
SWEEP_AT = 60000               # a trader/command ship holding this much gives what it holds above KEEP_SHIP
KEEP_SHIP = 50000              # what a trader or command ship keeps (buys cargo/fittings)
SWEEP_WORK = 40000             # a non-trading working ship holding this much gives what it holds above KEEP_WORK
KEEP_WORK = 30000              # what a miner/hauler/scout/drone/sentinel keeps (>= top-up donor KEEP)
FULL_PURSE_ROLES = frozenset(("trader", "command"))
MIN_DEPOSIT = 20000            # the leader deposits once it holds this much above KEEP_SHIP
MIN_DIRECT_DEPOSIT = 10000     # minimum excess for a seated member to deposit directly into the faction treasury
PER_PASS = 20                  # unseated gifts a sweep tries in parallel (distinct donors = independent 10s ticks)
DIRECT_DEPOSIT_PER_PASS = 20   # seated members depositing directly to target=faction in parallel (1 hop, proven 2026-11-24)
SWEEP_WORKERS = 8              # concurrent threads for distinct-pilot gifts, direct deposits, and P2P funding
LEADER = "Prime Directive"     # the faction's leader when empire.json names none
SKIP_PILOTS = set()            # pilots that never give in a sweep (one that holds credits for a buy the code does not know)
SHOW_WAIT = 45                 # seconds the sweep waits for the giver's wallet to show the money gone before it books
BATTLE_WAIT = 10 * 60          # a pilot refused `in_battle` is not asked again in this long
UNSURE_HOLD = 60 * 60          # after a deposit the wallet did not show, no new deposit in this long
DEPOSIT_FIRST = 100000         # the leader holding this much above KEEP_SHIP deposits before any gift of the pass: the gifts of
                               # about 80 s each used up DEPOSIT_BY in every pass and 1.2 million cr stood in its wallet (r24)
DEPOSIT_BY = 110               # seconds into the cash sweep phase after which the deposit waits for the next pass
DEPOSIT_TITLE = "Faction treasury: credits deposited (the Collective keeps them)"     # begins with routes.TREASURY
SENT_KEEP = 60 * 60            # a gift left `sent` whose receiver has no reading after its call is kept unsure after this long
FUND_FLOOR = 500000            # what the treasury keeps after a fund (the Fleet Admiral's line)
FUND_HOURS = 6                 # a funded pilot keeps its fund this long from the gift (the buy), then the sweep may take it
FUND_WAIT = 24                 # hours an open fund waits for a docked leader before it ends by itself
FUND_READ = 12                 # seconds between a withdrawal's call and the treasury's read after it (about one tick)
FUND_TITLE = "Treasury fund: credits withdrawn from the faction treasury for a buy"   # never begins with routes.TREASURY
ADMIRAL_MAX_SINGLE = None      # rule F12 (Suggi, 2026-11-24): per-pilot cap removed (None = unlimited above FUND_FLOOR)
ADMIRAL_DAY_CAP = None         # rule F12 (Suggi, 2026-11-24): rolling 24h cap removed (None = unlimited above FUND_FLOOR)
FUND_BATCH = 25                # max open funds withdrawn in a single batched pass
FUND_BUDGET = 120              # seconds of a pass fund gifts may take; any remaining withdrawn rows go next pass
P2P_FUND_ENABLED = True        # wire credits directly from rich flying ships to upgrading pilots when no Officer is docked
P2P_FUND_MAX = 400000          # max single-pilot amount filled via mid-flight P2P (larger buys use docked lockbox withdrawal)
P2P_MAX_DONORS = 8             # max parallel rich donors contributing to one P2P fund
P2P_MIN_SLICE = 10000          # minimum donor excess slice worth transferring in P2P funding
STORAGE_FACILITY_TYPES = frozenset(("faction_lockbox", "faction_warehouse", "faction_depot", "faction_stronghold"))
LOCKBOX_OFFICERS_PER_BASE = 4  # target seated Officers stationed/docked at each active Faction Storage base
MIN_OFFICERS_PER_DIVISION = 4  # minimum seated Officers per division (all 6 divisions covered for cross-division banking & ops)
MAX_AUTO_OFFICERS = 50         # global cap on total auto-promoted Officers + leader
# The treasury tops up a pilot no ship of its division or of the command group can give to (requests ENT-380, ENT-384,
# ENT-385, ENT-386, ENT-389: the newborns of 2026-11-22 were born with 100 to 250 cr while the sweep keeps every working
# ship at its line). The figures are the Fleet Admiral's (rule F7).
TREASURY_TOPUP = True          # on since 2026-11-23 after its dry run on live data (Unity's turn of 02:30 CET)
TREASURY_UNDER = LOW           # a stranded pilot under rule F7's line is topped up ... (5,000 until 2026-11-23 08:50 CET: the
TREASURY_LINE = 11000          # ... to this, from the treasury; the pilots between 5,000 and 10,000 HALTed every pass, Unity)
TREASURY_DAY = 400000          # at most this much from the treasury for top-ups in 24 hours
TREASURY_EVERY = 6 * 3600      # a pilot is topped up from the treasury at most once in this many seconds
TREASURY_BUDGET = 100          # seconds of a sweep pass the top-ups' gifts may take; the rest waits for the next pass
TOPUP_WHY = "top-up from the treasury: no donor in the division (rule F7)"
TOPUP_TITLE = "Treasury fund: credits withdrawn from the faction treasury for top-ups"  # never begins with routes.TREASURY


def wallets(data):
    """[(pilot, credits, division)] of every ship whose wallet was read."""
    named = dispatch.flagships(data)
    fleet = dispatch.read_json(Path(data) / "fleet" / "fleet.json", {})
    out = []
    for ship in fleet.get("ships") or [] if isinstance(fleet, dict) else []:
        name, credits = ship.get("name"), ship.get("credits")
        if name and isinstance(credits, (int, float)) and not isinstance(credits, bool):
            owner = division.ROLES.get(dispatch.role_of(name, named), "")
            out.append((name, int(credits), owner))
    return out


def recent(data, now):
    """{pilot: the time of its last gift received} within COOLDOWN."""
    out = {}
    try:
        with open(Path(data) / "fleet" / "gifts.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict) and now - (row.get("at") or 0) < COOLDOWN:
                    out[row.get("to")] = row.get("at")
    except OSError:
        pass
    return out


def topup_view(rows, held, owes):
    """The rows plan_gifts reads: a fund for a buy (held) and credits withdrawn for others (owes) are no donor's to
    give, but they never make a receiver: a pilot is topped up on what it holds itself, under LOW. A fund spent on its
    hull stays held for its hours; read as a debt it refilled the buyer to the fund's size from donors and the
    treasury, and a second hull was commissioned on it (2026-11-24, errors.log)."""
    out = []
    for name, credits, owner in rows:
        kept = held.get(name, 0) + owes.get(name, 0)
        free = credits - kept
        out.append((name, free if free >= LOW or not kept else min(credits, LOW), owner))
    return out


def plan_gifts(rows, given):
    """[(donor, pilot, credits)]: for each pilot under LOW, lowest first, the richest ship of its division that keeps
    KEEP after giving the whole need (up to TARGET); else the richest of the command group. When no single ship can
    give the whole need, several give: the ships of its division, richest first, each what it holds above KEEP (at
    least MIN_GIFT), then the command group for the rest (requests ENT-176). Such a pilot may get less than TARGET."""
    purse = {name: credits for name, credits, _owner in rows}
    out = []
    for name, credits, owner in sorted(rows, key=lambda r: r[1]):
        if credits >= LOW or name in given:
            continue
        need = TARGET - credits
        whole = None
        for group in (owner, "Unity"):
            donors = sorted(((purse[n], n) for n, _c, o in rows if o == group and n != name and purse[n] - need >= KEEP), reverse=True)
            if donors:
                whole = donors[0][1]
                break
        if whole is not None:
            purse[whole] -= need
            purse[name] += need
            out.append((whole, name, need))
            continue
        for group in (owner, "Unity"):
            for _have, donor in sorted(((purse[n], n) for n, _c, o in rows if o == group and n != name), reverse=True):
                part = min(need, purse[donor] - KEEP)
                if part < MIN_GIFT:
                    break                                       # richest first: the rest can spare less
                purse[donor] -= part
                purse[name] += part
                need -= part
                out.append((donor, name, part))
                if need < MIN_GIFT:
                    break
            if need < MIN_GIFT:
                break
    return out


def send(donor, target, credits):
    """(True, text) when the game took a storage `deposit` of credits from the donor to the target: a pilot's name (a
    gift) or `faction` (the faction's treasury)."""
    import gate
    status, answer = gate.call("post", "/accounts/%s/raw" % gate.q(donor),
                               {"toolGroup": "spacemolt_storage", "action": "deposit", "params": {"item_id": "credits", "quantity": int(credits), "target": target}}, timeout=90)
    return status == 200 and '"error"' not in answer[:200], answer[:200]


def give(donor, pilot, credits):
    """(True, text) when the game took the gift."""
    ok, text = send(donor, pilot, credits)
    if ok:
        refresh(pilot)                                      # the receiver read at once: the next run starts from a wallet that holds the gift (Q67, ENT-220)
    return ok, text


def deposit(pilot, credits):
    """(True, text) when the game took a deposit of credits from the pilot into the faction's treasury: the same call as a
    gift, the target `faction` (fleet-ops references/faction.md); the pilot read again at once, as a receiver is."""
    ok, text = send(pilot, "faction", credits)
    if ok:
        refresh(pilot)
    return ok, text


def treasury_read(pilot):
    """The faction's treasury as the game answers it now (`spacemolt_faction info` through the pilot, a read), or None
    when the read does not answer. A deposit is checked here, where it lands: the leader's wallet also moves by gifts
    and runs inside the same seconds (2026-11-17 20:26 UTC: a deposit that landed was kept unsure)."""
    import gate
    try:
        status, answer = gate.call("post", "/accounts/%s/raw" % gate.q(pilot),
                                   {"toolGroup": "spacemolt_faction", "action": "info", "params": {}}, timeout=30)
        found = json.loads(answer) if status == 200 else None
    except Exception:
        return None
    stack = [found]
    while stack:                                                # the first `treasury` number anywhere in the answer
        item = stack.pop(0)
        if isinstance(item, dict):
            money = item.get("treasury")
            if isinstance(money, (int, float)) and not isinstance(money, bool):
                return int(money)
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
        elif isinstance(item, str) and item.lstrip().startswith("{"):
            try:
                stack.append(json.loads(item))
            except ValueError:
                pass
    return None


def deposit_landed(data, leader, have, part, before):
    """True when the deposit shows: the treasury, read again, rose by most of it (when it was read before), else the
    leader's wallet fell by most of it (shows)."""
    if before is None:
        return shows(data, leader, have, part)
    deadline = time.time() + SHOW_WAIT
    while True:
        after = treasury_read(leader)
        if after is not None and after >= before + part * 0.9:
            return True
        if time.time() >= deadline:
            return False
        time.sleep(min(5, max(0.0, deadline - time.time())))


def refresh(pilot):
    """One read of the receiver (`get_status`, a read: no ship is taken): the engine keeps the last wallet it read of a
    docked ship, and the fleet file and the dispatcher see the gift only after a read (requests ENT-183)."""
    import gate
    try:
        gate.call("post", "/accounts/%s/raw" % gate.q(pilot), {"toolGroup": "spacemolt", "action": "get_status", "params": {}}, timeout=30)
    except Exception:                                           # a read that does not answer costs nothing: the next one shows it
        pass


def landed(data, pilot, was, credits):
    """True when the pilot's wallet shows the gift after all: the gate did not answer in time, the game may have taken it."""
    time.sleep(WAIT)
    have = {name: credits_now for name, credits_now, _owner in wallets(data)}
    return have.get(pilot, was) >= was + credits * 0.9


def _log(msg):
    with _WRITE_LOCK:
        print(msg)


def unsure(data, donor, pilot, credits, now):
    """A gift the gate did not answer for and the wallet does not show: kept with 0 credits, so the pilot is on cooldown
    (recent) and no figure counts it (routes.moved)."""
    with _WRITE_LOCK:
        with open(Path(data) / "fleet" / "gifts.jsonl", "a", encoding="utf-8") as handle:
            handle.write(json.dumps({"at": int(now), "from": donor, "to": pilot, "credits": 0, "unsure": credits}) + "\n")


def book(data, gifts, now):
    """The gifts into gifts.jsonl and, twice each, into onetime.json (kept out of the steady money)."""
    folder = Path(data) / "fleet"
    with _WRITE_LOCK:
        with open(folder / "gifts.jsonl", "a", encoding="utf-8") as handle:
            for donor, pilot, credits in gifts:
                handle.write(json.dumps({"at": int(now), "from": donor, "to": pilot, "credits": credits}) + "\n")
        once = folder / "onetime.json"
        with open(str(once) + ".lock", "w") as lock:                # the lock the runners and gate.py book under
            fcntl.flock(lock, fcntl.LOCK_EX)
            rows = dispatch.read_json(once, [])
            rows = rows if isinstance(rows, list) else []
            for donor, pilot, credits in gifts:
                rows += [[int(now), donor, TITLE, -credits], [int(now), pilot, TITLE, credits]]
            tmp = "%s.%d.%d.tmp" % (once, os.getpid(), threading.get_ident())
            with open(tmp, "w", encoding="utf-8") as handle:
                json.dump(rows[-8000:], handle, separators=(",", ":"))
            os.replace(tmp, once)


def ships(data):
    """{pilot: its row of data/fleet/fleet.json} of every ship whose wallet was read."""
    fleet = dispatch.read_json(Path(data) / "fleet" / "fleet.json", {})
    return {s["name"]: s for s in (fleet.get("ships") or [] if isinstance(fleet, dict) else [])
            if isinstance(s, dict) and s.get("name") and isinstance(s.get("credits"), (int, float)) and not isinstance(s.get("credits"), bool)}


def leader_of(data):
    """The faction's leader, the pilot that deposits into the treasury: data/empire/empire.json faction.leader, else LEADER."""
    found = (dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}).get("faction") or {}
    return str(found.get("leader") or LEADER) if isinstance(found, dict) else LEADER


def seated_members(data):
    """{pilot: role_lower} of every pilot seated in the faction (empire.json members)."""
    members = (dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}).get("members") or []
    out = {}
    for m in members:
        if isinstance(m, dict):
            p = str(m.get("pilot") or m.get("username") or "").strip()
            if p:
                out[p] = str(m.get("role") or "member").strip().lower()
    return out


def storage_bases(data):
    """Set of station/base IDs with an active faction storage facility (lockbox, warehouse, depot, stronghold)."""
    emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
    facs = (emp.get("facilities") or []) if isinstance(emp, dict) else []
    return {str(f.get("base")) for f in facs if isinstance(f, dict)
            and str(f.get("type") or "").lower() in STORAGE_FACILITY_TYPES
            and str(f.get("status") or "").lower() == "active" and f.get("base")}


def builders(data):
    """The pilots whose faction role is the builder's (empire.json members): they hold credits for a buy."""
    return {p for p, role in seated_members(data).items() if "build" in role}


def touched(data, now):
    """{pilot: the time of its last gift given or received} within COOLDOWN (gifts.jsonl, the unsure rows too)."""
    out = {}
    try:
        with open(Path(data) / "fleet" / "gifts.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict) and isinstance(row.get("at"), (int, float)) and now - row["at"] < COOLDOWN:
                    for name in (row.get("from"), row.get("to")):
                        if name:
                            out[name] = max(out.get(name, 0), row["at"])
    except OSError:
        pass
    return out


def fighting(ship):
    """True when the ship's loop fails in a fight: the engine's last failure names `in_battle` (the fleet file carries no
    other sign of a fight)."""
    return bool(ship.get("loop_failures")) and "in_battle" in str(ship.get("loop_last_failure") or "").lower().replace(" ", "_")


def swept(data):
    """[row] of data/fleet/sweep.jsonl: what each sweep tried, {"at", "kind": gift|deposit, "from", "to", "credits", "state"}."""
    out = []
    try:
        with open(Path(data) / "fleet" / "sweep.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict) and isinstance(row.get("at"), (int, float)):
                    out.append(row)
    except OSError:
        pass
    return out


def note(data, kind, giver, taker, credits, state, text="", before=None, wallets=None, sent_at=None):
    row = {"at": int(time.time()), "kind": kind, "from": giver, "to": taker, "credits": int(credits), "state": state,
           "text": str(text)[:200].encode("ascii", "replace").decode("ascii")}
    if before is not None:
        row["before"] = int(before)                              # the treasury read before a deposit's call
    if wallets is not None:
        row["wallets"] = {str(k): int(v) for k, v in wallets.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}   # a gift's two wallets before its call
    if sent_at is not None:
        row["sent_at"] = int(sent_at)                            # the `sent` row of a gift this row ends
    with _WRITE_LOCK:
        with open(Path(data) / "fleet" / "sweep.jsonl", "a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())                              # written before the call it announces
    return row["at"]


def pending(log):
    """The deposit row written `sent` whose pass ended before any answer (the newest deposit row of the log), or None."""
    rows = [r for r in log if r.get("kind") == "deposit"]
    return rows[-1] if rows and rows[-1].get("state") == "sent" else None


def settle(data, row):
    """A deposit a cut pass left `sent`: booked once, with the time it was sent, when the treasury rose by most of it
    since the read before its call; kept unsure when the treasury does not show it; left `sent` when the treasury does
    not answer. 'booked', 'unsure' or 'open'."""
    leader, credits, before = row.get("from"), int(row.get("credits") or 0), row.get("before")
    after = treasury_read(leader)
    when = time.strftime("%H:%M", time.gmtime(row["at"]))
    if after is None:
        print("no deposit: the deposit of %s cr sent at %s UTC is not settled: the treasury did not answer; read again at the next pass"
              % (format(credits, ","), when))
        return "open"
    if isinstance(before, (int, float)) and after >= before + credits * 0.9:
        book_deposit(data, leader, credits, row["at"])
        note(data, "deposit", leader, "faction", credits, "booked", "settled at the next pass: the treasury %s -> %s" % (before, after))
        print("booked at the next pass: the deposit of %s cr sent at %s UTC landed (the treasury %s -> %s cr)"
              % (format(credits, ","), when, format(int(before), ","), format(after, ",")))
        return "booked"
    note(data, "deposit", leader, "faction", credits, "unsure", "the pass ended before its answer; the treasury %s -> %s" % (before, after))
    print("HALT: the deposit of %s cr sent at %s UTC is not booked: its pass ended before the answer and the treasury does not show "
          "it (%s before, %s now). Read `view` target faction: if it landed, book it once (wallet.book_deposit)"
          % (format(credits, ","), when, before, format(after, ",")))
    return "unsure"


def open_gifts(log, kind):
    """The gift rows of `kind` (gift: the sweep's, topup: a top-up's) written `sent` that no later row ends (no row of
    the same kind and pilots names its time in `sent_at`): what a pass the job cut left between the call and its
    booking (DECISIONS Q75, errors.log ENT-116)."""
    ended = {(r.get("from"), r.get("to"), r.get("sent_at")) for r in log if r.get("kind") == kind and r.get("sent_at") is not None}
    return [r for r in log if r.get("kind") == kind and r.get("state") == "sent" and (r.get("from"), r.get("to"), r.get("at")) not in ended]


def read_at(ship):
    """The epoch of a fleet file row's wallet reading (`state_at`, UTC), or None when the row does not say."""
    try:
        return calendar.timegm(time.strptime(str(ship.get("state_at"))[:19].replace("T", " "), "%Y-%m-%d %H:%M:%S"))
    except (TypeError, ValueError):
        return None


def settle_gift(data, row, fleet, now, dry=False):
    """A gift a cut pass left `sent`: 'booked' (once, with the time it was sent) when the receiver's wallet, read after
    the call, rose by most of it and the giver's did not keep it; 'unsure' when the readings do not show it (kept
    with 0 credits in gifts.jsonl from the time it was sent: both on cooldown, booked nowhere); 'open' while the
    receiver has no reading after the call (unsure after SENT_KEEP). A dry run writes nothing and says what it would."""
    giver, taker, credits, sent = row.get("from"), row.get("to"), int(row.get("credits") or 0), int(row["at"])
    was = row.get("wallets") or {}
    when = time.strftime("%H:%M", time.gmtime(sent))
    what = "the %s %s -> %s %s cr sent at %s UTC" % ("top-up" if row.get("kind") == "topup" else "gift", giver, taker, format(credits, ","), when)
    got, gave = fleet.get(taker) or {}, fleet.get(giver) or {}
    fresh = lambda ship: isinstance(ship.get("credits"), (int, float)) and (read_at(ship) is None or read_at(ship) > sent)
    if not (fresh(got) and isinstance(was.get(taker), int)):
        if now - sent < SENT_KEEP:
            print("open: %s: the receiver's wallet was not read since the call; settled at a later pass" % what)
            return "open"
        state, why = "unsure", "the receiver's wallet was not read in %d minutes" % (SENT_KEEP // 60)
    else:
        rose = got["credits"] - was[taker] >= credits * 0.9
        kept = fresh(gave) and isinstance(was.get(giver), int) and gave["credits"] > was[giver] - credits * 0.5
        state = "booked" if rose and not kept else "unsure"
        why = "the receiver %s -> %s, the giver %s -> %s" % (was.get(taker), got["credits"], was.get(giver), gave.get("credits"))
    if dry:
        print("would settle: %s: %s (%s)" % (what, state, why))
        return state
    if state == "booked":
        book(data, [(giver, taker, credits)], sent)
        note(data, row.get("kind"), giver, taker, credits, "booked", "settled at the next pass: " + why, sent_at=sent)
        print("booked at the next pass: %s landed (%s)" % (what, why))
        return "booked"
    unsure(data, giver, taker, credits, sent)
    note(data, row.get("kind"), giver, taker, credits, "unsure", "the pass ended before its answer: " + why, sent_at=sent)
    print("HALT: %s is not booked: its pass ended before the answer and the wallets do not show it (%s). Read both wallets: if it "
          "landed, book it once (wallet.book)" % (what, why))
    return "unsure"


def settle_gifts(data, kind, now, dry=False):
    """Every gift of `kind` left `sent` settled (settle_gift): ({pilot: the time of its open gift}, 1 when one is kept
    unsure, else 0). The pilots of a gift still open are on cooldown: given and giving nothing until it is settled."""
    fleet, waiting, failed = ships(data), {}, 0
    for row in open_gifts(swept(data), kind):
        state = settle_gift(data, row, fleet, now, dry)
        failed = 1 if state == "unsure" else failed
        if state == "open" or dry:
            for name in (row.get("from"), row.get("to")):
                waiting[name] = row["at"]
    return waiting, failed


def settle_direct_deposits(data, now, dry=False):
    """Settle any `direct_deposit` left `sent` by a cut pass: booked once when the pilot's refreshed wallet shows the
    credits gone, kept unsure otherwise. Returns ({pilot: sent_at}, failed_flag)."""
    fleet, waiting, failed = ships(data), {}, 0
    for row in open_gifts(swept(data), "direct_deposit"):
        pilot, credits, sent = row.get("from"), int(row.get("credits") or 0), int(row.get("at") or 0)
        was = (row.get("wallets") or {}).get(pilot)
        ship = fleet.get(pilot) or {}
        have = ship.get("credits")
        after = read_at(ship)
        what = "direct deposit %s -> faction %s cr sent at %s UTC" % (
            pilot, format(credits, ","), time.strftime("%H:%M", time.gmtime(sent)))
        if (after is None or after <= sent) and now - sent <= SENT_KEEP:
            state, why = "open", "no reading of %s since the call" % pilot
        elif isinstance(was, (int, float)) and isinstance(have, (int, float)) and have <= was - credits * 0.9:
            state, why = "booked", "%s %s -> %s" % (pilot, format(int(was), ","), format(int(have), ","))
        else:
            state, why = "unsure", "%s %s -> %s" % (pilot, was, have)
        if dry:
            print("would settle: %s: %s (%s)" % (what, state, why))
            waiting[pilot] = sent
            continue
        if state == "open":
            waiting[pilot] = sent
            continue
        if state == "booked":
            book_deposit(data, pilot, credits, sent)
            note(data, "direct_deposit", pilot, "faction", credits, "booked", "settled at the next pass: " + why, sent_at=sent)
            print("booked at the next pass: %s landed (%s)" % (what, why))
        else:
            note(data, "direct_deposit", pilot, "faction", credits, "unsure", "the pass ended before its answer: " + why, sent_at=sent)
            print("HALT: %s is not booked: its pass ended before the answer and the wallet does not show it (%s)" % (what, why))
            failed = 1
    return waiting, failed


def recent_direct_deposits(log, now):
    """{pilot: at} of pilots with a direct_deposit row in sweep.jsonl within COOLDOWN (prevents double-sweeps)."""
    out = {}
    for r in log:
        if r.get("kind") == "direct_deposit" and r.get("state") in ("sent", "booked", "unsure"):
            at = r.get("at") or 0
            p = r.get("from")
            if p and now - at < COOLDOWN:
                out[p] = max(out.get(p, 0), at)
    return out


def answer_shows(text, pilot, was, credits):
    """True when the gift's own answer shows the giver's wallet with the credits gone: the game answers a credit gift
    with the giver's player state (`username`, then `credits`), which the fleet file shows only once the engine read
    the pilot again (2026-11-22 00:45 UTC: drone-11's 11,168 cr to the leader answered `credits` 50,000 from 61,168,
    and the gift stood unsure while the engine's copy of a docked pilot was minutes old)."""
    import re
    text = str(text or "")
    name = re.search(r'"username"\s*:\s*"([^"]*)"', text)
    have = re.search(r'"credits"\s*:\s*(-?\d+)', text[name.end():]) if name else None
    if not have or name.group(1) != pilot or not isinstance(was, (int, float)) or isinstance(was, bool):
        return False
    return int(have.group(1)) <= was - credits * 0.9


def keep_for(name, named=None):
    """(keep, sweep_at) by role: traders and command keep KEEP_SHIP (sweep at SWEEP_AT); other working roles keep KEEP_WORK
    (sweep at SWEEP_WORK), keeping every ship at or above top-up donor KEEP while freeing excess cash for the treasury."""
    if dispatch.role_of(name, named or {}) in FULL_PURSE_ROLES:
        return KEEP_SHIP, SWEEP_AT
    return KEEP_WORK, SWEEP_WORK


def plan_direct_deposits(fleet, leader, skip, seated, named=None):
    """[(pilot, credits to deposit)]: seated faction members (non-leader) above their role's sweep_at that can deposit
    directly into the faction treasury in 1 hop (proven 2026-11-24)."""
    if DIRECT_DEPOSIT_PER_PASS <= 0 or not seated:
        return []
    found = []
    for name, ship in fleet.items():
        if name == leader or name not in seated or name in skip:
            continue
        if ship.get("status", "connected") != "connected" or fighting(ship):
            continue
        keep, sweep_at = keep_for(name, named)
        part = int(ship["credits"] - keep)
        if ship["credits"] >= sweep_at and part >= MIN_DIRECT_DEPOSIT:
            found.append((part, name))
    found.sort(reverse=True)
    return [(name, int(part)) for part, name in found[:DIRECT_DEPOSIT_PER_PASS]]


def plan_sweep(fleet, leader, skip, named=None):
    """[(pilot, credits to give)]: the ships at their role's sweep_at or more, the most above their keep first, at most
    PER_PASS; never the leader, a pilot of `skip`, a ship not connected or one whose loop fails in a fight."""
    found = []
    for name, ship in fleet.items():
        if name == leader or name in skip or ship.get("status", "connected") != "connected" or fighting(ship):
            continue
        keep, sweep_at = keep_for(name, named)
        if ship["credits"] >= sweep_at:
            found.append((ship["credits"] - keep, name))
    found.sort(reverse=True)
    return [(name, int(part)) for part, name in found[:PER_PASS]]


def shows(data, pilot, was, credits, wait=None):
    """True when the pilot's wallet, read again, shows `credits` gone from `was` within `wait` seconds (SHOW_WAIT)."""
    deadline = time.time() + (SHOW_WAIT if wait is None else wait)
    while True:
        have = (ships(data).get(pilot) or {}).get("credits")
        if isinstance(have, (int, float)) and have <= was - credits * 0.9:
            return True
        if time.time() >= deadline:
            return False
        time.sleep(min(5, max(0.0, deadline - time.time())))


def book_deposit(data, pilot, credits, now):
    """A deposit into the faction's treasury, once in onetime.json (minus for the pilot), under the title routes.deposits
    and the collector read as a move between two purses of ours."""
    once = Path(data) / "fleet" / "onetime.json"
    with _WRITE_LOCK:
        with open(str(once) + ".lock", "w") as lock:                # the lock the runners and gate.py book under
            fcntl.flock(lock, fcntl.LOCK_EX)
            rows = dispatch.read_json(once, [])
            rows = rows if isinstance(rows, list) else []
            rows.append([int(now), pilot, DEPOSIT_TITLE, -int(credits)])
            tmp = "%s.%d.%d.tmp" % (once, os.getpid(), threading.get_ident())
            with open(tmp, "w", encoding="utf-8") as handle:
                json.dump(rows[-8000:], handle, separators=(",", ":"))
            os.replace(tmp, once)


def funds_file(data):
    return Path(data) / "fleet" / "funds.json"


def funds(data):
    """[row] of data/fleet/funds.json: {"pilot", "credits", "why", "at", "hours", "state": open|withdrawn|given|ended, ...}."""
    rows = dispatch.read_json(funds_file(data), [])
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def write_funds(data, rows):
    path = funds_file(data)
    with _WRITE_LOCK:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = "%s.%d.%d.tmp" % (path, os.getpid(), threading.get_ident())
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(rows[-1000:], handle, indent=1)      # top-up rows too: bounded by the fleet size a day
        os.replace(tmp, path)


def funded(data, now):
    """{pilot: credits} the sweep and the top-ups leave with a pilot: each fund given within its hours."""
    out = {}
    for r in funds(data):
        if r.get("kind") != "topup" and r.get("state") == "given" and now - (r.get("given_at") or 0) < float(r.get("hours") or FUND_HOURS) * 3600:
            out[r["pilot"]] = out.get(r["pilot"], 0) + int(r.get("credits") or 0)
    return out


def withdrawn(data):
    """Credits the leader holds for a fund whose gift has not gone yet: kept out of its deposit."""
    return sum(int(r.get("credits") or 0) for r in funds(data) if r.get("state") == "withdrawn")


def owed(data):
    """{withdrawer: credits} it holds for a fund or a top-up withdrawn and not given yet: no donor's to give (a top-up
    is withdrawn by the leader; 2026-11-23 the top-up pass gave 182,310 cr withdrawn for 44 named pilots to others)."""
    leader, out = leader_of(data), {}
    for r in funds(data):
        if r.get("state") == "withdrawn":
            actor = str(r.get("withdrawer") or leader)
            out[actor] = out.get(actor, 0) + int(r.get("credits") or 0)
    return out


def awaiting_treasury(data):
    """{pilot} with a top-up row open, withdrawn or unsure: the treasury serves it, no ship gives it twice."""
    return {r.get("pilot") for r in funds(data) if r.get("kind") == "topup" and r.get("state") in ("open", "withdrawn", "unsure")}


def withdraw(leader, credits):
    """(True, text) when the game took a withdrawal of credits from the treasury into the leader's wallet."""
    import gate
    status, answer = gate.call("post", "/accounts/%s/raw" % gate.q(leader),
                               {"toolGroup": "spacemolt_storage", "action": "deposit",
                                "params": {"item_id": "credits", "quantity": int(credits), "source": "faction", "target": "self"}}, timeout=90)
    return status == 200 and '"error"' not in answer[:200], answer[:200]


def docked(data, pilot):
    return bool((ships(data).get(pilot) or {}).get("docked"))


def gate_book(pilot, title, amount):
    import gate
    gate.book_onetime(pilot, title, amount)


def withdrawers(data, leader):
    """Ordered list of faction members with manage_treasury rights: leader first, then any Officer/treasurer in empire.json."""
    out = [leader]
    emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
    for m in (emp.get("members") or []) if isinstance(emp, dict) else []:
        if not isinstance(m, dict):
            continue
        p = str(m.get("pilot") or "").strip()
        role = str(m.get("role") or "").strip().lower()
        if p and p not in out and (role in ("leader", "officer") or "treasur" in role):
            out.append(p)
    return out


def ready_withdrawer(data, leader, request_stop=True):
    """Return a docked treasury-authorized pilot (leader preferred, else any docked Officer/treasurer at an active
    faction storage base: lockbox/warehouse/depot/stronghold), or '' (optionally asking leader's run to stop)."""
    boxes = storage_bases(data)
    fleet = ships(data)
    for actor in withdrawers(data, leader):
        dock = str((fleet.get(actor) or {}).get("docked") or "")
        if dock and (not boxes or dock in boxes):
            return actor
    if request_stop:
        run_marker = Path(data) / "fleet" / "host" / "running" / (leader + ".json")
        if run_marker.exists():
            stop_p = Path(data) / "fleet" / "host" / "stop" / leader
            stop_p.parent.mkdir(parents=True, exist_ok=True)
            stop_p.touch()
    return ""


def _p2p_donor_pool(data, leader, now, excluded):
    """Sorted [(excess, pilot, was_credits)] of rich flying/docked ships eligible for P2P mid-flight funding."""
    fleet = ships(data)
    named = dispatch.flagships(data)
    log = swept(data)
    battle = {r.get("from") for r in log if r.get("state") == "battle" and now - r["at"] < BATTLE_WAIT}
    cool = set(touched(data, now)) | set(recent_direct_deposits(log, now))
    owes = owed(data)
    skip = ({leader} | SKIP_PILOTS | builders(data) | set(funded(data, now))
            | battle | cool | set(excluded))
    try:
        import upgrades as _upg
        skip |= _upg.protected_pilots(data)
    except Exception:
        pass
    pool = []
    for name, s in fleet.items():
        if name in skip or s.get("status", "connected") != "connected" or fighting(s):
            continue
        keep, _sweep_at = keep_for(name, named)
        avail = int(s["credits"] - owes.get(name, 0) - keep)
        if avail >= P2P_MIN_SLICE:
            pool.append((avail, name, int(s["credits"])))
    pool.sort(reverse=True)
    return pool


def serve_funds_p2p(data, leader, pending_open, rows, now):
    """When no Officer is docked at a storage base, fill open funds (<= P2P_FUND_MAX) directly from rich ships in
    parallel from anywhere in space. Returns (filled_count, changed, failed)."""
    if not P2P_FUND_ENABLED or not pending_open:
        return 0, False, 0
    targets = {r["pilot"] for r in pending_open}
    pool = _p2p_donor_pool(data, leader, now, targets)
    if not pool:
        return 0, False, 0
    used_donors, filled, changed, failed = set(), 0, False, 0
    start = time.time()
    for r in pending_open[:FUND_BATCH]:
        if time.time() - start > FUND_BUDGET:
            break
        amt = int(r["credits"])
        if amt <= 0 or amt > P2P_FUND_MAX:
            continue
        target = r["pilot"]
        picks, need = [], amt
        for avail, donor, was in pool:
            if donor in used_donors or donor == target:
                continue
            take_cr = min(avail, need)
            if take_cr < P2P_MIN_SLICE and take_cr < need:
                continue
            picks.append((donor, take_cr, was))
            need -= take_cr
            if need <= 0 or len(picks) >= P2P_MAX_DONORS:
                break
        if need > 0 or not picks:
            continue
        for donor, _c, _w in picks:
            used_donors.add(donor)

        def _send_slice(item):
            donor, slice_cr, was = item
            try:
                ok, text = give(donor, target, slice_cr)
            except Exception as err:
                return donor, slice_cr, was, None, "gate error: %s: %s" % (type(err).__name__, err)
            return donor, slice_cr, was, ok, text

        workers = min(SWEEP_WORKERS, len(picks))
        results = []
        if workers > 1:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                futs = [ex.submit(_send_slice, p) for p in picks]
                for f in as_completed(futs):
                    results.append(f.result())
        else:
            for p in picks:
                results.append(_send_slice(p))

        got, ok_cnt = 0, 0
        for donor, slice_cr, was, ok, text in results:
            if ok is False:
                if "in_battle" in str(text or "").lower().replace(" ", "_"):
                    note(data, "gift", donor, target, slice_cr, "battle", text)
                else:
                    note(data, "gift", donor, target, slice_cr, "refused", text)
                    failed = 1
                continue
            if (ok and answer_shows(text, donor, was, slice_cr)) or shows(data, donor, was, slice_cr, wait=5):
                book(data, [(donor, target, slice_cr)], time.time())
                note(data, "gift", donor, target, slice_cr, "booked", "p2p_fund: " + str(text)[:140])
                got += slice_cr
                ok_cnt += 1
            elif ok:
                book(data, [(donor, target, slice_cr)], time.time())
                note(data, "gift", donor, target, slice_cr, "booked", "p2p_fund: " + str(text)[:140])
                got += slice_cr
                ok_cnt += 1
            else:
                unsure(data, donor, target, slice_cr, time.time())
                note(data, "gift", donor, target, slice_cr, "unsure", text)
                failed = 1

        if got >= amt:
            r.update(state="given", via="p2p", given_at=int(time.time()),
                     note="p2p from %d donor(s)" % ok_cnt)
            filled += 1
            changed = True
            print("FUND given (P2P): %d donor(s) -> %s %s cr (%s); no lockbox wait"
                  % (ok_cnt, target, format(got, ","), r.get("why")))
        elif got > 0:
            r["credits"] = amt - got
            r["note"] = "p2p partial +%s cr (%d donor(s)); %s cr remaining" % (format(got, ","), ok_cnt, format(amt - got, ","))
            changed = True
            print("FUND partial (P2P): %d donor(s) -> %s +%s cr (%s cr still open)"
                  % (ok_cnt, target, format(got, ","), format(amt - got, ",")))
    if changed:
        write_funds(data, rows)
    return filled, changed, failed


def serve_funds(data, leader, now, dry):
    """Serve open and withdrawn treasury funds: up to FUND_BATCH open funds withdrawn in one batched withdrawal
    while the leader (or a docked Officer/treasurer at a faction storage base) stands docked and treasury keeps
    FUND_FLOOR; when no Officer is docked, falls back to mid-flight parallel P2P funding from rich ships.
    Returns 0, or 1 when a call failed."""
    rows, changed, start = funds(data), False, time.time()
    for r in rows:                                              # an open fund ends by itself after FUND_WAIT hours
        if r.get("state") == "open" and r.get("kind") != "topup" and now - (r.get("at") or 0) > FUND_WAIT * 3600:
            r.update(state="ended", note="no docked leader within %d hours" % FUND_WAIT)
            changed = True
            print("FUND ended: %s %s cr: the leader stood docked at no pass within %d hours" % (r["pilot"], format(int(r["credits"]), ","), FUND_WAIT))
    pending_give = [r for r in rows if r.get("state") == "withdrawn" and r.get("kind") != "topup"]
    pending_open = [r for r in rows if r.get("state") == "open" and r.get("kind") != "topup"]
    if (not pending_give and not pending_open) or dry:
        for r in pending_give + pending_open[:FUND_BATCH]:
            print("would fund: %s %s cr from the treasury (%s), state %s" % (r["pilot"], format(int(r["credits"]), ","), r.get("why"), r["state"]))
        if changed and not dry:
            write_funds(data, rows)
        return 0
    if pending_open and not pending_give:
        actor = ready_withdrawer(data, leader, request_stop=False)
        if not actor:
            filled, p2p_changed, p2p_failed = serve_funds_p2p(data, leader, pending_open, rows, now)
            changed = changed or p2p_changed
            still_open = [r for r in rows if r.get("state") == "open" and r.get("kind") != "topup"]
            if not still_open:
                return p2p_failed
            ready_withdrawer(data, leader, request_stop=True)
            first = still_open[0]
            print("FUND waits: %d open (%s %s cr first): %s is not docked at a lockbox (the game withdraws docked only)"
                  % (len(still_open), first["pilot"], format(int(first["credits"]), ","), leader))
            if changed:
                write_funds(data, rows)
            return p2p_failed
        before = treasury_read(actor)
        take, total = [], 0
        for r in pending_open[:FUND_BATCH]:
            amt = int(r["credits"])
            if before is not None and before - (total + amt) >= FUND_FLOOR:
                take.append(r)
                total += amt
        if not take:
            first = pending_open[0]
            print("FUND waits: %s %s cr: the treasury reads %s, it keeps %s" % (first["pilot"], format(int(first["credits"]), ","), before, format(FUND_FLOOR, ",")))
            if changed:
                write_funds(data, rows)
            return 0
        if not any(r.get("state") in ("withdrawn", "given") or (isinstance(r.get("probed"), dict) and r["probed"].get("ok")) for r in rows):     # rule F12: one unit first
            ok, text = withdraw(actor, 1)
            time.sleep(FUND_READ)
            after = treasury_read(actor)
            take[0]["probed"] = {"ok": ok, "text": text, "before": before, "after": after}
            write_funds(data, rows)
            if not ok or after is None or before - after < 1:
                print("HALT: FUND probe: 1 cr from the treasury was not taken (%s; the treasury %s -> %s): no fund is withdrawn" % (text, before, after))
                return 1
            gate_book(actor, FUND_TITLE + " (the 1 cr probe)", 1)
            before = after
        ok, text = withdraw(actor, total)
        time.sleep(FUND_READ)
        after = treasury_read(actor)
        if not (after is not None and before - after >= total * 0.9):
            for r in take:
                r.update(state="open" if ok is False else "unsure", note="withdraw: %s; the treasury %s -> %s" % (text, before, after))
            write_funds(data, rows)
            print("HALT: FUND %d pilot(s) %s cr: the withdrawal %s (the treasury %s -> %s)"
                  % (len(take), format(total, ","), ("was refused: " + text) if ok is False else "does not show", before, after))
            return 1
        label = take[0].get("why") or take[0]["pilot"] if len(take) == 1 else ("%d pilots" % len(take))
        gate_book(actor, "%s: %s" % (FUND_TITLE, label), total)
        for r in take:
            r.update(state="withdrawn", withdrawn_at=int(time.time()), withdrawer=actor, treasury=[before, after])
        write_funds(data, rows)
        print("FUND withdrawn: %s cr from the treasury by %s for %d pilot(s) (the treasury %s -> %s)"
              % (format(total, ","), actor, len(take), before, after))
        pending_give = take
    failed = 0
    for r in pending_give:
        if time.time() - start > FUND_BUDGET:
            break
        actor = str(r.get("withdrawer") or leader)
        pilot, credits = r["pilot"], int(r["credits"])
        if pilot == actor:
            r.update(state="given", given_at=int(time.time()),
                     note="officer self-withdrawal: funds already in pilot wallet")
            print("FUND given: %s %s cr (%s), by its own withdrawal; the sweep leaves it for %s hours"
                  % (actor, format(credits, ","), r.get("why"), r.get("hours") or FUND_HOURS))
            continue
        ok, text = give(actor, pilot, credits)
        if not ok:
            r["note"] = "gift: %s" % text
            failed = 1
            print("HALT: FUND gift %s -> %s %s cr refused: %s; %s keeps it and gives at the next pass"
                  % (actor, pilot, format(credits, ","), text, actor))
            continue
        book(data, [(actor, pilot, credits)], time.time())
        r.update(state="given", given_at=int(time.time()))
        print("FUND given: %s -> %s %s cr (%s); the sweep leaves it for %s hours"
              % (actor, pilot, format(credits, ","), r.get("why"), r.get("hours") or FUND_HOURS))
    write_funds(data, rows)
    return failed


def treasury_topups(data, stranded, now, dry):
    """{pilot} with a top-up from the treasury open or given now: each stranded pilot (no ship of its division or of
    the command group can give) under TREASURY_UNDER gets one row of data/fleet/funds.json (kind `topup`, the credits
    up to TREASURY_LINE), served by the sweep (serve_topups); never a second open row a pilot, never twice in
    TREASURY_EVERY, never more than TREASURY_DAY in 24 hours. Nothing while TREASURY_TOPUP is off."""
    rows = funds(data)
    tops = [r for r in rows if r.get("kind") == "topup"]
    busy = {r["pilot"] for r in tops if r.get("state") in ("open", "withdrawn", "unsure")}
    late = {r["pilot"] for r in tops if r.get("state") == "given" and now - (r.get("given_at") or 0) < TREASURY_EVERY}
    if not TREASURY_TOPUP:
        return set()
    spent = sum(int(r.get("credits") or 0) for r in tops if r.get("state") != "ended" and now - (r.get("at") or 0) < 86400)
    out, added = set(busy | late), []
    for name, credits in sorted(stranded, key=lambda pc: pc[1]):
        if credits >= TREASURY_UNDER or name in out:
            continue
        need = TREASURY_LINE - int(credits)
        if spent + need > TREASURY_DAY:
            print("HALT: %s is under %s cr; the treasury's top-ups reached their %s cr of 24 hours (wallet.py TREASURY_DAY, the Fleet Admiral's line)"
                  % (name, format(TREASURY_UNDER, ","), format(TREASURY_DAY, ",")))
            continue
        spent += need
        out.add(name)
        added.append({"pilot": name, "credits": need, "why": TOPUP_WHY, "hours": 0, "at": int(now), "state": "open", "kind": "topup"})
        print("%s: %s %s cr from the treasury (it holds %s cr, line %s)" % ("would fund" if dry else "FUND open", name, format(need, ","),
                                                                             format(int(credits), ","), format(TREASURY_LINE, ",")))
    if added and not dry:
        write_funds(data, funds(data) + added)
    return out


def leader_ready(data, leader):
    """True when any treasury-authorized Officer or the leader stands docked at an active faction storage base;
    else asks the leader's run to stop at its next stop and returns False."""
    return bool(ready_withdrawer(data, leader, request_stop=True))


def serve_topups(data, leader, now, dry):
    """The treasury's top-ups (kind `topup` of funds.json): the open rows in one withdrawal while the leader stands docked
    and the treasury keeps FUND_FLOOR, then each given within TREASURY_BUDGET seconds (a gift needs no dock; what is left
    stays `withdrawn`, out of the leader's deposit, and goes at the next pass). 0, or 1 when a call failed."""
    rows, start = funds(data), time.time()
    for r in rows:
        if r.get("kind") == "topup" and r.get("state") == "open" and now - (r.get("at") or 0) > FUND_WAIT * 3600:
            r.update(state="ended", note="no docked leader within %d hours" % FUND_WAIT)
    todo = [r for r in rows if r.get("kind") == "topup" and r.get("state") == "open"]
    if dry:
        if todo:
            print("would withdraw for top-ups: %s cr for %d pilots" % (format(sum(int(r["credits"]) for r in todo), ","), len(todo)))
        return 0
    actor = ready_withdrawer(data, leader, request_stop=True) if todo else ""
    if todo and actor:
        before = treasury_read(actor)
        take, total = [], 0
        for r in todo:
            if before is not None and before - (total + int(r["credits"])) >= FUND_FLOOR:
                take.append(r)
                total += int(r["credits"])
        if take:
            if not any(r.get("state") in ("withdrawn", "given") or (isinstance(r.get("probed"), dict) and r["probed"].get("ok")) for r in rows):
                ok, text = withdraw(actor, 1)                   # rule F12: one unit first
                time.sleep(FUND_READ)
                after = treasury_read(actor)
                take[0]["probed"] = {"ok": ok, "text": text, "before": before, "after": after}
                write_funds(data, rows)
                if not ok or after is None or before - after < 1:
                    print("HALT: TOP-UP probe: 1 cr from the treasury was not taken (%s; the treasury %s -> %s)" % (text, before, after))
                    return 1
                gate_book(actor, TOPUP_TITLE + " (the 1 cr probe)", 1)
                before = after
            ok, text = withdraw(actor, total)
            time.sleep(FUND_READ)
            after = treasury_read(actor)
            if not (after is not None and before - after >= total * 0.9):
                for r in take:
                    r.update(state="open" if ok is False else "unsure", note="withdraw: %s; the treasury %s -> %s" % (text, before, after))
                write_funds(data, rows)
                print("HALT: TOP-UP withdrawal of %s cr %s (the treasury %s -> %s)" % (format(total, ","), ("was refused: " + text) if ok is False else "does not show", before, after))
                return 1
            gate_book(actor, "%s: %d pilots" % (TOPUP_TITLE, len(take)), total)
            for r in take:
                r.update(state="withdrawn", withdrawn_at=int(time.time()), withdrawer=actor)
            write_funds(data, rows)
            print("TOP-UP withdrawn: %s cr from the treasury by %s for %d pilots (the treasury %s -> %s)" % (format(total, ","), actor, len(take), before, after))
        else:
            print("TOP-UP waits: %d pilots, the treasury reads %s, it keeps %s" % (len(todo), before, format(FUND_FLOOR, ",")))
    elif todo:
        print("TOP-UP waits: %d pilots: the leader %s is not docked (the game withdraws docked only)" % (len(todo), leader))
    failed = 0
    wallets_now = {name: int(row.get("credits") or 0) for name, row in ships(data).items()}
    for r in [r for r in rows if r.get("kind") == "topup" and r.get("state") == "withdrawn"]:
        if time.time() - start > TREASURY_BUDGET:
            break
        actor = str(r.get("withdrawer") or leader)
        if r["pilot"] == actor:                                 # the withdrawer's own top-up: the withdrawal itself landed with it ...
            if wallets_now.get(actor, 0) >= TREASURY_UNDER or (r.get("withdrawn_at") or 0) >= start - 60:
                r.update(state="given", given_at=int(time.time()), note="the leader's own top-up: given by the withdrawal")
                print("TOP-UP given: %s %s cr from the treasury, by its own withdrawal" % (actor, format(int(r["credits"]), ",")))
            else:                                               # ... unless it went elsewhere since: a new row asks again
                r.update(state="ended", note="the leader holds %s cr: the withdrawal went elsewhere; a new row asks again" % format(wallets_now.get(actor, 0), ","))
                print("TOP-UP ended: the leader %s holds %s cr; a new row asks the treasury again" % (actor, format(wallets_now.get(actor, 0), ",")))
            continue
        if wallets_now.get(r["pilot"], 0) >= TREASURY_UNDER:    # topped up by another gift since: the credits go back with the deposit
            r.update(state="ended", note="the pilot holds %s cr: topped up since; the leader's deposit takes the credits back" % format(wallets_now[r["pilot"]], ","))
            print("TOP-UP ended: %s holds %s cr now; %s cr go back with the leader's deposit" % (r["pilot"], format(wallets_now[r["pilot"]], ","), format(int(r["credits"]), ",")))
            continue
        ok, text = give(actor, r["pilot"], int(r["credits"]))
        if not ok and "insufficient_funds" in text:             # the withdrawer no longer holds it: the row ends, the pilot is asked for anew
            r.update(state="ended", note="gift: %s" % text[:160])
            print("TOP-UP ended: %s cannot pay %s %s cr (%s); a new row asks the treasury again"
                  % (actor, r["pilot"], format(int(r["credits"]), ","), text[:120]))
            continue
        if not ok:
            r["note"] = "gift: %s" % text
            failed = 1
            print("HALT: TOP-UP gift %s -> %s %s cr refused: %s; %s keeps it and gives at the next pass" % (actor, r["pilot"], format(int(r["credits"]), ","), text, actor))
            continue
        book(data, [(actor, r["pilot"], int(r["credits"]))], time.time())
        r.update(state="given", given_at=int(time.time()))
        print("TOP-UP given: %s -> %s %s cr from the treasury" % (actor, r["pilot"], format(int(r["credits"]), ",")))
    write_funds(data, rows)
    return failed


SEAT_BATCH = 20
SEAT_BUDGET = 80


def seats_file(data):
    return Path(data) / "fleet" / "seats.json"


def seat_rows(data):
    rows = dispatch.read_json(seats_file(data), [])
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def write_seats(data, rows):
    path = seats_file(data)
    with _WRITE_LOCK:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = "%s.%d.%d.tmp" % (path, os.getpid(), threading.get_ident())
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(rows[-500:], handle, indent=1)
        os.replace(tmp, path)


def pick_unseated(data, limit=None):
    """Rank unseated fleet ships by Rule F11 benefit: bring every division to >= 10 seated members first,
    then prioritize outpost-working haulers, miners and traders, then sentinels, drones and scouts."""
    emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
    fac = (emp.get("faction") or {}) if isinstance(emp, dict) else {}
    seated = {str(m.get("pilot")) for m in (emp.get("members") or []) if isinstance(m, dict) and m.get("pilot")}
    queued = {str(r.get("pilot")) for r in seat_rows(data) if r.get("state") == "open"}
    fleet = ships(data)
    named = dispatch.flagships(data)
    div_counts = {}
    for p in seated:
        d = (fleet.get(p) or {}).get("division") or "Other"
        div_counts[d] = div_counts.get(d, 0) + 1
    role_rank = {"command": 0, "hauler": 1, "miner": 2, "trader": 3, "sentinel": 4, "drone": 5, "scout": 6}
    cands = []
    for name, s in sorted(fleet.items()):
        if name in seated or name in queued:
            continue
        role = (named.get(name) or {}).get("role") or name.split("-", 1)[0]
        div = s.get("division") or "Other"
        cands.append((role_rank.get(role, 9), int(s.get("number") or 0), name, div))
    cands.sort()
    picked = []
    # Pass 1: ensure every division reaches >= 10 seated members (Suggi standing floor)
    rest = []
    for item in cands:
        _rr, _num, name, div = item
        if div_counts.get(div, 0) < 10:
            picked.append(name)
            div_counts[div] = div_counts.get(div, 0) + 1
        else:
            rest.append(name)
    picked.extend(rest)
    if limit is None:
        ml, mc = int(fac.get("members_limit") or 0), int(fac.get("member_count") or len(seated))
        limit = max(0, ml - mc - len(queued)) if ml else len(picked)
    return picked[:max(0, int(limit))]


def add_seats(data, pilots, now):
    rows = seat_rows(data)
    emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
    seated = {str(m.get("pilot")) for m in (emp.get("members") or []) if isinstance(m, dict) and m.get("pilot")}
    open_set = {str(r.get("pilot")) for r in rows if r.get("state") == "open"}
    fleet = ships(data)
    added = []
    for p in pilots:
        p = p.strip()
        if not p or p in seated or p in open_set or p not in fleet:
            continue
        rows.append({"pilot": p, "state": "open", "at": int(now)})
        open_set.add(p)
        added.append(p)
    if added:
        write_seats(data, rows)
    print("SEATS queued: %d added (%d open in queue); served automatically between runs by wallet.py sweep"
          % (len(added), sum(1 for r in rows if r.get("state") == "open")))
    return 0


def faction_raw(pilot, action, params):
    import gate
    return gate.call("post", "/accounts/%s/raw" % gate.q(pilot),
                     {"toolGroup": "spacemolt_faction", "action": action, "params": params}, timeout=90)


def order_hold_path(data, pilot):
    return Path(data) / "fleet" / "orders" / (pilot + ".json")


def try_hold_sweep(data, pilot, now):
    if division.order_of(pilot, data):
        return False
    p = order_hold_path(data, pilot)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"pilot": pilot, "what": "hand sweep", "since": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))}), encoding="utf-8")
    return division.order_of(pilot, data) == "hand sweep"


def release_sweep(data, pilot):
    if division.order_of(pilot, data) == "hand sweep":
        try:
            order_hold_path(data, pilot).unlink()
        except OSError:
            pass


def auto_queue_seats(data, now, dry=False):
    """Automatically queue unseated fleet ships up to open faction cap (Rule F11) so open seats
    never wait 6 hours for Unity's AI turn. Uses pick_unseated() benefit ranking."""
    emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
    fac = (emp.get("faction") or {}) if isinstance(emp, dict) else {}
    ml = int(fac.get("members_limit") or 0)
    mc = int(fac.get("member_count") or 0)
    if ml <= 0 or mc >= ml:
        return 0
    rows = seat_rows(data)
    open_now = sum(1 for r in rows if r.get("state") == "open")
    need = max(0, (ml - mc) - open_now)
    if need <= 0:
        return 0
    picks = pick_unseated(data, limit=need)
    if not picks:
        return 0
    if dry:
        print("would auto-queue seats: %d pilots (%d/%d cap, %d already queued)" % (len(picks), mc, ml, open_now))
        return len(picks)
    add_seats(data, picks, now)
    return len(picks)


def serve_seats(data, leader, now, dry):
    """Invite and join up to SEAT_BATCH idle queued pilots when both the leader and each target pilot stand free."""
    rows = seat_rows(data)
    todo = [r for r in rows if r.get("state") == "open"]
    if not todo:
        return 0
    if dry:
        print("would seat: %d pilots waiting in seats.json" % len(todo))
        return 0
    fleet = ships(data)
    inviter = ""
    for cand in withdrawers(data, leader):
        if not fighting(fleet.get(cand) or {}):
            inviter = cand
            break
    if not inviter:
        print("SEATS waits: leader %s (and all officers) are in combat" % leader)
        return 0
    held_inviter = try_hold_sweep(data, inviter, now)
    joined = 0
    t0 = time.time()
    try:
        emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
        fid = str(((emp.get("faction") or {}).get("id")) or "")
        st_i, txt_i = faction_raw(inviter, "info", {})
        if st_i == 200 and "{" in txt_i:
            try:
                sc = (json.loads(txt_i[txt_i.find("{"):]).get("structuredContent")) or {}
                fid = str(sc.get("id") or fid)
            except ValueError:
                pass
        if not fid:
            print("SEATS waits: faction id unread")
            return 0
        for r in todo[:SEAT_BATCH]:
            if time.time() - t0 > SEAT_BUDGET:
                break
            p = str(r.get("pilot") or "")
            if not p or fighting(fleet.get(p) or {}):
                continue
            held_p = try_hold_sweep(data, p, time.time())
            try:
                st_a, txt_a = faction_raw(inviter, "invite", {"player_id": p})
                st_b, txt_b = faction_raw(p, "join", {"faction_id": fid})
                comb = (txt_a + " " + txt_b).lower()
                if "faction_full" in comb:
                    faction_raw(inviter, "withdraw_invite", {"player_id": p})
                    r.update(state="full", note="faction_full")
                    break
                if (st_b == 200 and '"error"' not in txt_b[:240]) or "already_member" in comb or "already in" in comb:
                    r.update(state="joined", joined_at=int(time.time()))
                    joined += 1
                elif "in_battle" in comb:
                    break
                else:
                    r["note"] = txt_b[:160]
            finally:
                if held_p:
                    release_sweep(data, p)
    finally:
        if held_inviter:
            release_sweep(data, inviter)
    write_seats(data, rows)
    if joined:
        print("SEATS joined: %d pilots added to CLTV (%d still open)"
              % (joined, sum(1 for r in rows if r.get("state") == "open")))
    return 0


def division_fund_spent(data, who, now):
    """Rolling 24h non-topup, non-ended credits funded by `who`."""
    return sum(int(r.get("credits") or 0) for r in funds(data)
               if r.get("kind") != "topup" and r.get("state") != "ended"
               and str(r.get("by") or "") == who and now - (r.get("at") or 0) < 86400)


def add_fund(data, pilot, credits, why, hours, now, who="Unity"):
    credits = int(credits)
    if credits <= 0:
        print("REFUSED: credits must be positive")
        return 1
    rows = funds(data)
    if any(r.get("pilot") == pilot and r.get("state") in ("open", "withdrawn", "unsure") for r in rows):
        print("REFUSED: %s has a fund open already" % pilot)
        return 1
    if pilot not in ships(data):
        print("REFUSED: %s holds no wallet reading in the fleet file" % pilot)
        return 1
    admiral = bool(who and who != "Unity" and who in division.MEMBERS)
    if admiral:
        owner = division.owner(pilot, data)
        if owner != who:
            print("REFUSED: %s belongs to %s, not %s (rule F12: own division only)" % (pilot, owner, who))
            return 1
        if ADMIRAL_MAX_SINGLE and credits > ADMIRAL_MAX_SINGLE:
            print("REFUSED: %s cr exceeds autonomous single-pilot cap of %s cr (rule F12); escalate to Unity (Scope: capital)"
                  % (format(credits, ","), format(ADMIRAL_MAX_SINGLE, ",")))
            return 1
        spent = division_fund_spent(data, who, now)
        if ADMIRAL_DAY_CAP and spent + credits > ADMIRAL_DAY_CAP:
            print("REFUSED: %s autonomous 24h treasury budget exceeded (%s + %s > %s cr, rule F12); escalate to Unity (Scope: capital)"
                  % (who, format(spent, ","), format(credits, ","), format(ADMIRAL_DAY_CAP, ",")))
            return 1
        emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
        tr_now = (emp.get("faction") or {}).get("treasury") if isinstance(emp, dict) else None
        if isinstance(tr_now, (int, float)):
            open_sum = sum(int(r.get("credits") or 0) for r in rows if r.get("kind") != "topup" and r.get("state") == "open")
            if int(tr_now) - open_sum - credits < FUND_FLOOR:
                print("REFUSED: treasury %s cr minus %s cr open funds minus %s cr would fall below %s cr floor (rule F12)"
                      % (format(int(tr_now), ","), format(open_sum, ","), format(credits, ","), format(FUND_FLOOR, ",")))
                return 1
    rows.append({"pilot": pilot, "credits": credits, "why": why, "hours": hours, "at": int(now), "state": "open", "by": who or "Unity"})
    write_funds(data, rows)
    print("FUND open: %s %s cr by %s (%s); served at the next 5m pass while docked at a lockbox"
          % (pilot, format(credits, ","), who or "Unity", why))
    return 0



ERRAND_WAIT = 24                 # hours an open leader errand waits before expiring by itself
ERRAND_BATCH = 15                # max open errands executed in a single docked pass (promotes full officer slate cleanly)
ERRAND_ACTIONS = {
    "promote": "spacemolt_faction_admin",
    "post_mission": "spacemolt_faction_admin",
    "cancel_mission": "spacemolt_faction",
    "write_room": "spacemolt_faction_admin",
    "create_role": "spacemolt_faction_admin",
    "edit_role": "spacemolt_faction_admin",
    "delete_role": "spacemolt_faction",
    "set_station_policy": "spacemolt_faction_admin",
}
ERRAND_DEFAULT_ROLES = ("recruit", "member", "officer", "leader")


def errands_file(data):
    return Path(data) / "fleet" / "leader_errands.json"


def errands(data):
    rows = dispatch.read_json(errands_file(data), [])
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def write_errands(data, rows):
    path = errands_file(data)
    with _WRITE_LOCK:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = "%s.%d.%d.tmp" % (path, os.getpid(), threading.get_ident())
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(rows[-200:], handle, indent=1)
            handle.write("\n")
        os.replace(tmp, path)


def validate_errand(action, params):
    """Validate a queued leader-only faction errand. Returns (toolGroup, clean_params, error_str)."""
    act = str(action or "").strip()
    if act not in ERRAND_ACTIONS:
        return None, None, "action %r is not on the leader errand allowlist (%s)" % (act, ", ".join(sorted(ERRAND_ACTIONS)))
    if not isinstance(params, dict):
        return None, None, "params must be a JSON object"
    p = dict(params)
    if act == "promote":
        pid = str(p.get("player_id") or "").strip()
        rid = str(p.get("role_id") or "").strip().lower()
        if not pid:
            return None, None, "promote requires player_id"
        if rid == "leader":
            return None, None, "transferring faction leadership (role_id=leader) is forbidden in the errand queue"
        if rid not in ("recruit", "member", "officer"):
            return None, None, "promote role_id must be one of recruit, member, officer"
        p = {"player_id": pid, "role_id": rid}
    elif act == "post_mission":
        for req in ("title", "description", "type"):
            if not isinstance(p.get(req), str) or not p[req].strip():
                return None, None, "post_mission requires non-empty string `%s`" % req
        if not isinstance(p.get("objectives"), list) or not p["objectives"]:
            return None, None, "post_mission requires a non-empty `objectives` list"
        if not isinstance(p.get("rewards"), dict):
            return None, None, "post_mission requires a `rewards` object"
    elif act == "cancel_mission":
        if not isinstance(p.get("template_id"), str) or not p["template_id"].strip():
            return None, None, "cancel_mission requires template_id"
    elif act == "write_room":
        for req in ("name", "description"):
            if not isinstance(p.get(req), str) or not p[req].strip():
                return None, None, "write_room requires non-empty `%s`" % req
        if p.get("access") not in ("public", "members", "officers"):
            return None, None, "write_room access must be public, members, or officers"
    elif act == "create_role":
        if not isinstance(p.get("name"), str) or not p["name"].strip():
            return None, None, "create_role requires name"
    elif act == "edit_role":
        if not isinstance(p.get("role_id"), str) or not p["role_id"].strip():
            return None, None, "edit_role requires role_id"
    elif act == "delete_role":
        rid = str(p.get("role_id") or "").strip().lower()
        if not rid or rid in ERRAND_DEFAULT_ROLES:
            return None, None, "delete_role requires a custom (non-default) role_id"
    elif act == "set_station_policy":
        if not p:
            return None, None, "set_station_policy requires at least one policy field"
    return ERRAND_ACTIONS[act], p, ""


def add_errand(data, action, params, why, station="", now=None, who="Unity"):
    """Queue a docked leader-only faction errand (Unity-only, rule F11). Returns 0 on success, 1 on refusal."""
    now = time.time() if now is None else now
    if who != "Unity":
        print("REFUSED: leader faction errands are the Fleet Admiral's (rule F11; caller=%s)" % who)
        return 1
    why_s = str(why or "").strip()
    if not why_s:
        print("REFUSED: --why is required when queueing a leader errand")
        return 1
    group, clean, err = validate_errand(action, params)
    if err:
        print("REFUSED: %s" % err)
        return 1
    rows = errands(data)
    eid = "err-%d-%d" % (int(now), len(rows) + 1)
    row = {
        "id": eid,
        "at": int(now),
        "by": who,
        "action": str(action).strip(),
        "group": group,
        "params": clean,
        "station": str(station or "").strip(),
        "why": why_s,
        "state": "open",
    }
    rows.append(row)
    write_errands(data, rows)
    st_msg = (" at station " + row["station"]) if row["station"] else " (any docked station)"
    print("ERRAND queued: %s | %s%s | %s" % (eid, row["action"], st_msg, why_s))
    return 0


def cancel_errand(data, eid, now=None, who="Unity"):
    """Cancel an open leader errand by id (Unity-only). Returns 0 if cancelled, 1 otherwise."""
    now = time.time() if now is None else now
    if who != "Unity":
        print("REFUSED: cancelling leader errands is the Fleet Admiral's (rule F11)")
        return 1
    rows = errands(data)
    for r in rows:
        if r.get("id") == eid and r.get("state") == "open":
            r.update(state="cancelled", done_at=int(now), note="cancelled by %s" % who)
            write_errands(data, rows)
            print("ERRAND cancelled: %s (%s)" % (eid, r.get("action")))
            return 0
    print("REFUSED: no open errand with id %r" % eid)
    return 1


def format_errands(data):
    """Human-readable summary of leader_errands.json."""
    rows = errands(data)
    n_open = sum(1 for r in rows if r.get("state") == "open")
    n_done = sum(1 for r in rows if r.get("state") == "done")
    lines = ["ERRANDS | open: %d | done: %d | total: %d | allowlist: %s"
             % (n_open, n_done, len(rows), ", ".join(sorted(ERRAND_ACTIONS)))]
    for r in rows[-25:]:
        st = (" @ " + r["station"]) if r.get("station") else ""
        note = (" | " + str(r["note"])[:120]) if r.get("note") else ""
        lines.append("  %s | %-14s | %-9s%s | %s%s"
                     % (r.get("id", "?"), r.get("action", "?"), r.get("state", "?"), st, r.get("why", ""), note))
    return "\n".join(lines)


def errand_raw(pilot, group, action, params):
    """Send one validated leader-only faction call through the gate; (ok, text)."""
    import gate                                 # as every other caller in this file: no module-level import (2026-11-24 02:13 UTC NameError)
    status, answer = gate.call("post", "/accounts/%s/raw" % gate.q(pilot),
                               {"toolGroup": group, "action": action, "params": params}, timeout=60)
    try:
        body = json.loads(answer)
    except ValueError:
        return False, "HTTP %s %s" % (status, str(answer)[:160])
    if status not in (200, 201) or body.get("error"):
        return False, str(body.get("error") or ("HTTP %s" % status))[:220]
    res = body.get("result")
    if isinstance(res, dict) and res.get("error"):
        return False, str(res.get("error"))[:220]
    sc = body.get("structuredContent") if isinstance(body.get("structuredContent"), dict) else {}
    if sc.get("error"):
        return False, str(sc.get("error"))[:220]
    txt = res if isinstance(res, str) else json.dumps(res if res is not None else sc, separators=(",", ":"))
    return True, str(txt)[:220]


def auto_queue_officers(data, now, dry=False):
    """Self-healing Officer staffing (Suggi, 2026-11-24): automatically queues `promote -> officer` errands for:
      1. Every seated Command/Division flagship (gives every Admiral + Unity manage_treasury/manage_facilities/invite).
      2. Up to LOCKBOX_OFFICERS_PER_BASE (2) seated docked ships at each active Faction Storage base (lockbox/warehouse/
         depot/stronghold), preferring Trade Bursars first, then haulers, then others -- guaranteeing 24/7 docked
         treasury withdrawal access across all bases with zero manual intervention.
    Capped at MAX_AUTO_OFFICERS total officers+leader; deduplicates against open and recent (<1h) done promotes."""
    emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
    if not isinstance(emp, dict) or not (emp.get("faction") or {}).get("id"):
        return 0
    seated = seated_members(data)
    if not seated:
        return 0
    existing_errands = errands(data)
    pending_or_recent = set()
    for r in existing_errands:
        if r.get("action") != "promote":
            continue
        st = r.get("state")
        pid = str((r.get("params") or {}).get("player_id") or "").strip()
        if not pid:
            continue
        if st == "open" or (st == "done" and now - float(r.get("done_at") or r.get("at") or 0) < 3600):
            pending_or_recent.add(pid)
    officers = {p for p, role in seated.items() if role in ("leader", "officer")} | pending_or_recent
    room = MAX_AUTO_OFFICERS - len(officers)
    if room <= 0:
        return 0
    named = dispatch.flagships(data)
    fleet = ships(data)
    to_queue = []

    # Priority 1: all seated division/command flagships currently at role 'member'
    for fg in sorted(named):
        if room <= 0:
            break
        if seated.get(fg) == "member" and fg not in officers:
            to_queue.append((fg, "auto-officer: division/command flagship treasury & facility access"))
            officers.add(fg)
            room -= 1

    # Priority 2: docked bankers (Bursar traders first, then haulers, then others) at each active storage base
    role_prio = {"trader": 0, "hauler": 1, "command": 2, "miner": 3, "scout": 4, "sentinel": 5, "drone": 6}
    for base in sorted(storage_bases(data)):
        if room <= 0:
            break
        docked_officers = [p for p in officers if str((fleet.get(p) or {}).get("docked") or "") == base]
        need = LOCKBOX_OFFICERS_PER_BASE - len(docked_officers)
        if need <= 0:
            continue
        cands = []
        for p, role in seated.items():
            if role != "member" or p in officers:
                continue
            s = fleet.get(p) or {}
            if str(s.get("docked") or "") != base or s.get("status", "connected") != "connected":
                continue
            r_cls = dispatch.role_of(p, named)
            cands.append((role_prio.get(r_cls, 9), p))
        cands.sort()
        for _prio, p in cands[:min(need, room)]:
            to_queue.append((p, "auto-officer: docked lockbox banker at %s" % base))
            officers.add(p)
            room -= 1

    # Priority 3: guarantee every division holds at least MIN_OFFICERS_PER_DIVISION seated Officers
    role_to_div = {
        "command": "Command", "miner": "Mining", "trader": "Trade",
        "hauler": "Logistics", "drone": "Military", "sentinel": "Military", "scout": "Intel",
    }

    def _div_of(pilot_name):
        s = fleet.get(pilot_name) or {}
        d = str(s.get("division") or "").strip()
        if d:
            return d
        return role_to_div.get(dispatch.role_of(pilot_name, named), "")

    div_counts = {}
    for p in officers:
        d = _div_of(p)
        if d:
            div_counts[d] = div_counts.get(d, 0) + 1
    for div_name in ("Command", "Mining", "Trade", "Logistics", "Military", "Intel"):
        if room <= 0:
            break
        need = MIN_OFFICERS_PER_DIVISION - div_counts.get(div_name, 0)
        if need <= 0:
            continue
        cands = []
        for p, role in seated.items():
            if role != "member" or p in officers:
                continue
            if _div_of(p) != div_name:
                continue
            s = fleet.get(p) or {}
            if s.get("status", "connected") != "connected":
                continue
            is_docked = 0 if str(s.get("docked") or "") else 1
            cands.append((is_docked, p))
        cands.sort()
        for _dk, p in cands[:min(need, room)]:
            to_queue.append((p, "auto-officer: %s division officer & treasury access" % div_name))
            officers.add(p)
            div_counts[div_name] = div_counts.get(div_name, 0) + 1
            room -= 1

    if not to_queue:
        return 0
    if dry:
        print("would auto-queue officers: %d pilot(s): %s" % (len(to_queue), ", ".join(p for p, _ in to_queue[:15])))
        return 0
    for p, why in to_queue:
        add_errand(data, "promote", {"player_id": p, "role_id": "officer"}, why, now=now, who="Unity")
    return 0


def serve_errands(data, leader, now, dry):
    """Execute open docked-leader errands while the leader stands docked (Q75 (12)). Returns 0, or 1 on call error."""
    rows, changed = errands(data), False
    for r in rows:
        if r.get("state") == "open" and now - float(r.get("at") or 0) > ERRAND_WAIT * 3600:
            r.update(state="ended", done_at=int(now), note="leader did not dock at required station within %d hours" % ERRAND_WAIT)
            changed = True
            print("ERRAND ended: %s (%s): timed out after %dh" % (r.get("id"), r.get("action"), ERRAND_WAIT))
    open_rows = [r for r in rows if r.get("state") == "open"]
    if not open_rows or dry:
        for r in open_rows[:ERRAND_BATCH]:
            print("would errand: %s %s (%s)" % (r.get("id"), r.get("action"), r.get("why")))
        if changed and not dry:
            write_errands(data, rows)
        return 0
    fleet = ships(data)
    dock_base = str((fleet.get(leader) or {}).get("docked") or "")
    if not dock_base:
        print("ERRAND waits: %d open (%s %s first): %s is not docked"
              % (len(open_rows), open_rows[0].get("id"), open_rows[0].get("action"), leader))
        if changed:
            write_errands(data, rows)
        return 0
    ready = [r for r in open_rows if not r.get("station") or str(r.get("station")) == dock_base]
    if not ready:
        need_st = open_rows[0].get("station")
        print("ERRAND waits: %d open (%s needs station %s; %s docked at %s)"
              % (len(open_rows), open_rows[0].get("id"), need_st, leader, dock_base))
        if changed:
            write_errands(data, rows)
        return 0
    if not try_hold_sweep(data, leader, now):
        print("ERRAND waits: %s holds an active order; trying next pass" % leader)
        if changed:
            write_errands(data, rows)
        return 0
    failed = 0
    try:
        for r in ready[:ERRAND_BATCH]:
            group, clean, err = validate_errand(r.get("action"), r.get("params"))
            if err:
                r.update(state="failed", done_at=int(time.time()), station_used=dock_base, note="invalid: " + err)
                write_errands(data, rows)
                failed = 1
                continue
            ok, text = errand_raw(leader, group, r["action"], clean)
            ascii_txt = str(text or "").encode("ascii", "replace").decode("ascii")[:220]
            if ok:
                r.update(state="done", done_at=int(time.time()), station_used=dock_base, note=ascii_txt or "ok")
                print("ERRAND done: %s | %s at %s | %s" % (r.get("id"), r["action"], dock_base, ascii_txt[:120]))
            else:
                r.update(state="failed", done_at=int(time.time()), station_used=dock_base, note=ascii_txt or "failed")
                print("HALT: ERRAND %s (%s) at %s failed: %s" % (r.get("id"), r["action"], dock_base, ascii_txt[:140]))
                failed = 1
            write_errands(data, rows)
    finally:
        release_sweep(data, leader)
    return failed

def served(name, step, *args, result=True):
    """One served step of the sweep (funds, top-ups, seats, errands): an exception is printed as a HALT line and fails
    the pass instead of ending it, so the steps after it, the gifts and the deposit still run (errors.log ENT-173: a
    NameError in the errand step and a timeout of a seat's join each ended whole passes on 2026-11-24).
    1 on an exception; else the step's own answer (`result`) or 0."""
    try:
        out = step(*args)
    except Exception as error:
        print("HALT: the sweep's %s step failed: %s: %s" % (name, type(error).__name__, str(error)[:200]))
        return 1
    return (out or 0) if result else 0


def _acquire_serve_lock(data):
    """Non-blocking exclusive flock on data/fleet/wallet-serve.lock so concurrent serve passes never race."""
    lock_p = Path(data) / "fleet" / "wallet-serve.lock"
    lock_p.parent.mkdir(parents=True, exist_ok=True)
    fh = open(lock_p, "a+", encoding="ascii")
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        fh.close()
        return None
    return fh


def serve(data, now, dry):
    """Run all non-sweep service queues in isolation (funds/P2P, top-ups, seat & officer auto-queues, seats,
    errands, upgrades) so slow admin steps never starve cash sweeping or deposits."""
    lock_fh = None if dry else _acquire_serve_lock(data)
    if not dry and lock_fh is None:
        return 0
    try:
        fleet, leader = ships(data), leader_of(data)
        if leader not in fleet:
            print("SERVE | the leader %s holds no wallet reading in the fleet file" % leader)
            return 1
        failed = 0
        failed = served("fund", serve_funds, data, leader, now, dry) or failed
        failed = served("top-up", serve_topups, data, leader, now, dry) or failed
        failed = served("seat queue", auto_queue_seats, data, now, dry, result=False) or failed
        failed = served("officer queue", auto_queue_officers, data, now, dry, result=False) or failed
        failed = served("seat", serve_seats, data, leader, now, dry, result=False) or failed
        failed = served("errand", serve_errands, data, leader, now, dry) or failed
        try:
            import upgrades as _upg
            _upg.serve_upgrades(data, now=now, dry=dry)
        except Exception as error:
            print("HALT: the upgrade queue's step failed: %s: %s" % (type(error).__name__, str(error)[:200]))
            failed = 1
        return failed
    finally:
        if lock_fh is not None:
            try:
                fcntl.flock(lock_fh, fcntl.LOCK_UN)
                lock_fh.close()
            except OSError:
                pass


def serve_daemon(data, every=60, dry=False):
    """Lightweight persistent service loop for wallet.py serve (zero idle CPU, single-instance lock)."""
    every = max(15, int(every or 60))
    stop_flag = []

    def _on_sig(_sig, _frame):
        stop_flag.append(1)

    signal.signal(signal.SIGTERM, _on_sig)
    signal.signal(signal.SIGINT, _on_sig)
    print("wallet: serving every %d s (pid %d)" % (every, os.getpid()), flush=True)
    while not stop_flag:
        if not (Path(data) / "fleet" / "STOP").exists():
            try:
                serve(data, time.time(), dry)
            except Exception as error:
                print("wallet: pass error: %s: %s" % (type(error).__name__, str(error)[:200]), flush=True)
            sys.stdout.flush()
        end_wait = time.time() + every
        while not stop_flag and time.time() < end_wait:
            time.sleep(min(1.0, max(0.05, end_wait - time.time())))
    print("wallet: stopped cleanly", flush=True)
    return 0

def sweep(data, now, dry, cash_only=False):
    """One pass of the sweep: parallel direct seated-member deposits to treasury, parallel unseated gifts to leader,
    then leader deposit into treasury. When cash_only=False (default), also runs service queues first with an
    isolated cash_start timer so admin queues never starve sweeping or deposits. Returns 0, or 1 on failure."""
    fleet, leader = ships(data), leader_of(data)
    if leader not in fleet:
        print("SWEEP | the leader %s holds no wallet reading in the fleet file: nothing given, nothing deposited" % leader)
        return 1
    log = swept(data)
    waiting, failed = pending(log), 0
    if waiting and not dry:
        state = settle(data, waiting)
        failed = 1 if state == "unsure" else 0
        log = swept(data)
    elif waiting:
        print("would settle: the deposit of %s cr sent at %s UTC" % (format(int(waiting.get("credits") or 0), ","), time.strftime("%H:%M", time.gmtime(waiting["at"]))))
    flying, unsettled = settle_gifts(data, "gift", now, dry)    # Q75: a gift a cut pass left `sent`, settled before any new one
    dd_flying, dd_unsettled = settle_direct_deposits(data, now, dry)
    failed = failed or unsettled or dd_unsettled
    _upg_skip = set()
    if not cash_only:
        failed = served("fund", serve_funds, data, leader, now, dry) or failed
        failed = served("top-up", serve_topups, data, leader, now, dry) or failed
        failed = served("seat queue", auto_queue_seats, data, now, dry, result=False) or failed
        failed = served("officer queue", auto_queue_officers, data, now, dry, result=False) or failed
        failed = served("seat", serve_seats, data, leader, now, dry, result=False) or failed
        failed = served("errand", serve_errands, data, leader, now, dry) or failed
        try:
            import upgrades as _upg
            _upg.serve_upgrades(data, now=now, dry=dry)
            _upg_skip = _upg.protected_pilots(data)
        except Exception as error:              # errors.log ENT-171: a step that fails on every pass is printed, never swallowed
            print("HALT: the upgrade queue's step failed: %s: %s" % (type(error).__name__, str(error)[:200]))
            failed = 1
    else:
        try:
            import upgrades as _upg
            _upg_skip = _upg.protected_pilots(data)
        except Exception:
            pass
    # Reset phase timer AFTER admin steps so slow seat/errand calls never starve cash sweeping or deposits!
    cash_start = time.time()
    fleet = ships(data)
    if leader not in fleet:
        return 1
    log = swept(data)
    battle = {r.get("from"): r["at"] for r in log if r.get("state") == "battle" and now - r["at"] < BATTLE_WAIT}
    held = [r for r in log if r.get("kind") == "deposit" and r.get("state") == "unsure" and now - r["at"] < UNSURE_HOLD]
    skip = {leader} | SKIP_PILOTS | builders(data) | set(funded(data, now)) | _upg_skip
    cool = dict(touched(data, now))
    cool.update({name: at for name, at in flying.items() if name})
    cool.update(recent_direct_deposits(log, now))
    cool.update({name: at for name, at in dd_flying.items() if name})
    named = dispatch.flagships(data)
    seated = seated_members(data)
    above = [(name, s["credits"], keep_for(name, named)[0]) for name, s in fleet.items()
             if name != leader and s["credits"] >= keep_for(name, named)[1]]
    print("SWEEP | leader %s holds %s cr | %d ships above role cap hold %s cr to sweep (traders/command keep %s, others %s) | the treasury read %s"
          % (leader, format(fleet[leader]["credits"], ","), len(above), format(sum(c - k for _n, c, k in above), ","),
             format(KEEP_SHIP, ","), format(KEEP_WORK, ","), treasury_text(data)))
    for name, _credits, _keep in sorted(above):
        why = ("a builder: holds credits for a buy" if name in builders(data) else "in SKIP_PILOTS" if name in SKIP_PILOTS
               else "funded by the treasury for a buy" if name in funded(data, now)
               else "not connected" if fleet[name].get("status", "connected") != "connected" else "its loop fails in a fight" if fighting(fleet[name])
               else "refused for a fight %d min ago" % ((now - battle[name]) // 60) if name in battle
               else "gave or got a gift %d min ago" % ((now - cool[name]) // 60) if name in cool else "")
        if why:
            print("  left out: %s (%s cr): %s" % (name, format(fleet[name]["credits"], ","), why))

    # Lane 1: Seated faction members deposit directly to target=faction (1 hop, bypasses leader completely!)
    direct_plan = plan_direct_deposits(fleet, leader, skip | set(battle) | set(cool), seated, named)
    direct_pilots = {p for p, _c in direct_plan}
    if dry:
        for pilot, credits in direct_plan:
            print("would deposit direct: %s -> faction %s cr (keeps %s)" % (pilot, format(credits, ","), format(keep_for(pilot, named)[0], ",")))
    elif direct_plan:
        def _do_direct(item):
            pilot, credits = item
            if time.time() - cash_start > BUDGET:
                _log("the pass's %d seconds are used up: direct deposit %s waits for the next pass" % (BUDGET, pilot))
                return 0
            was = fleet[pilot]["credits"]
            sent = note(data, "direct_deposit", pilot, "faction", credits, "sent", "", wallets={pilot: was})
            try:
                ok, text = deposit(pilot, credits)
            except Exception as error:
                ok, text = None, "the gate did not answer (%s: %s)" % (type(error).__name__, error)
            if ok is False:
                fight = "in_battle" in text.lower().replace(" ", "_")
                note(data, "direct_deposit", pilot, "faction", credits, "battle" if fight else "refused", text, sent_at=sent)
                if fight:
                    _log("in a fight: %s deposits nothing now; asked again after %d minutes" % (pilot, BATTLE_WAIT // 60))
                    return 0
                _log("HALT: direct deposit %s -> faction %s cr was refused: %s" % (pilot, format(credits, ","), text))
                return 1
            if (ok and answer_shows(text, pilot, was, credits)) or shows(data, pilot, was, credits):
                book_deposit(data, pilot, credits, time.time())
                note(data, "direct_deposit", pilot, "faction", credits, "booked", text, sent_at=sent)
                _log("deposited direct: %s -> faction %s cr" % (pilot, format(credits, ",")))
                return 0
            note(data, "direct_deposit", pilot, "faction", credits, "unsure", text, sent_at=sent)
            _log("HALT: direct deposit %s -> faction %s cr is not booked: %s; wallet of %s does not show it gone after %d s"
                 % (pilot, format(credits, ","), "answered" if ok else text, pilot, SHOW_WAIT))
            return 1

        workers = min(SWEEP_WORKERS, len(direct_plan))
        if workers > 1:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                for res in ex.map(_do_direct, direct_plan):
                    if res:
                        failed = 1
        else:
            for item in direct_plan:
                if _do_direct(item):
                    failed = 1

    # Lane 2: Unseated pilots gift in parallel to the leader, then leader deposits in one batch
    plan = plan_sweep(fleet, leader, skip | set(battle) | set(cool) | direct_pilots, named)
    fought = [r for r in log if r.get("kind") == "deposit" and r.get("state") == "refused" and now - r["at"] < BATTLE_WAIT
              and "in_battle" in str(r.get("text") or "").lower().replace(" ", "_")]
    if plan and not held and not pending(log) and not fought and fleet[leader]["credits"] - KEEP_SHIP >= DEPOSIT_FIRST:
        print("the leader's deposit first: %s cr above its line; the gifts wait for the next pass" % format(int(fleet[leader]["credits"] - KEEP_SHIP), ","))
        plan = []
    if dry:
        for pilot, credits in plan:
            print("would give: %s -> %s %s cr (keeps %s)" % (pilot, leader, format(credits, ","), format(keep_for(pilot, named)[0], ",")))
    elif plan:
        def _do_gift(item):
            pilot, credits = item
            if time.time() - cash_start > BUDGET:
                _log("the pass's %d seconds are used up: %s waits for the next pass" % (BUDGET, pilot))
                return 0
            was = fleet[pilot]["credits"]
            sent = note(data, "gift", pilot, leader, credits, "sent", "", wallets={pilot: was, leader: (ships(data).get(leader) or {}).get("credits")})
            try:                                                # Q75: on disk before the call; a cut pass leaves it for settle_gift
                ok, text = give(pilot, leader, credits)
            except Exception as error:                          # the gate did not answer: the game may still have taken it
                ok, text = None, "the gate did not answer (%s: %s)" % (type(error).__name__, error)
            if ok is False:
                fight = "in_battle" in text.lower().replace(" ", "_")
                note(data, "gift", pilot, leader, credits, "battle" if fight else "refused", text, sent_at=sent)
                if fight:
                    _log("in a fight: %s gives nothing now; asked again after %d minutes" % (pilot, BATTLE_WAIT // 60))
                    return 0
                _log("HALT: the gift %s -> %s %s cr was refused: %s" % (pilot, leader, format(credits, ","), text))
                return 1
            if (ok and answer_shows(text, pilot, was, credits)) or shows(data, pilot, was, credits):
                book(data, [(pilot, leader, credits)], time.time())
                note(data, "gift", pilot, leader, credits, "booked", text, sent_at=sent)
                _log("given: %s -> %s %s cr" % (pilot, leader, format(credits, ",")))
                return 0
            unsure(data, pilot, leader, credits, time.time())
            note(data, "gift", pilot, leader, credits, "unsure", text, sent_at=sent)
            _log("HALT: the gift %s -> %s %s cr is not booked: %s; the wallet of %s does not show it gone after %d s (kept unsure, the pilot on cooldown)"
                 % (pilot, leader, format(credits, ","), "answered" if ok else text, pilot, SHOW_WAIT))
            return 1

        workers = min(SWEEP_WORKERS, len(plan))
        if workers > 1:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                for res in ex.map(_do_gift, plan):
                    if res:
                        failed = 1
        else:
            for item in plan:
                if _do_gift(item):
                    failed = 1

    have = (ships(data).get(leader) or {}).get("credits", 0)
    part = int(have - KEEP_SHIP - withdrawn(data))             # a fund withdrawn and not given yet stays with the leader
    if pending(log) and not dry:
        pass                                                    # settle() said why: no second deposit on top of an open one
    elif held:
        print("no deposit: the deposit of %s cr at %s UTC answered but the leader's wallet did not show it; none again until %s UTC "
              "(read `view` target faction and book it by hand if it landed)"
              % (format(held[-1].get("credits", 0), ","), time.strftime("%H:%M", time.gmtime(held[-1]["at"])), time.strftime("%H:%M", time.gmtime(held[-1]["at"] + UNSURE_HOLD))))
    elif part < MIN_DEPOSIT:
        print("no deposit: the leader holds %s cr, under %s" % (format(have, ","), format(KEEP_SHIP + MIN_DEPOSIT, ",")))
    elif dry:
        print("would deposit: %s %s cr into the faction's treasury (keeps %s)" % (leader, format(part, ","), format(KEEP_SHIP, ",")))
    elif time.time() - cash_start > DEPOSIT_BY:
        print("the pass used %d seconds: the deposit waits for the next pass" % int(time.time() - cash_start))
    else:
        before = treasury_read(leader)
        note(data, "deposit", leader, "faction", part, "sent", "", before)    # first: a cut pass loses no deposit (settle)
        try:
            ok, text = deposit(leader, part)
        except Exception as error:
            ok, text = None, "the gate did not answer (%s: %s)" % (type(error).__name__, error)
        if ok is False:
            note(data, "deposit", leader, "faction", part, "refused", text)
            failed = 1
            print("HALT: the deposit of %s cr was refused: %s; tried again at the next pass" % (format(part, ","), text))
        elif deposit_landed(data, leader, have, part, before):
            book_deposit(data, leader, part, time.time())
            note(data, "deposit", leader, "faction", part, "booked", text)
            print("deposited: %s %s cr into the faction's treasury" % (leader, format(part, ",")))
        else:
            note(data, "deposit", leader, "faction", part, "unsure", text)
            failed = 1
            print("HALT: the deposit of %s cr is not booked: %s; neither the treasury nor the leader's wallet shows it after %d s. Read `view` target faction: "
                  "if it landed, book it once (wallet.book_deposit); no deposit again for %d minutes" % (format(part, ","), "answered" if ok else text, SHOW_WAIT, UNSURE_HOLD // 60))
    return failed


def treasury_text(data):
    """The faction's treasury as empire.py collect last read it: `N cr, H:M UTC`, or `not measured`."""
    state = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
    money = (state.get("faction") or {}).get("treasury") if isinstance(state.get("faction"), dict) else None
    if not isinstance(money, (int, float)) or isinstance(money, bool):
        return "not measured"
    return "%s cr at %s" % (format(int(money), ","), str(state.get("written_at") or "an unknown time").replace("T", " ").replace("Z", " UTC"))


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    data = args[args.index("--data") + 1] if "--data" in args else division.DATA
    verb = "errand" if "errand" in args else "seat" if "seat" in args else "fund" if "fund" in args else "serve" if "serve" in args else "topup" if "topup" in args else "sweep" if "sweep" in args else "check"
    now = time.time()
    if verb == "errand":
        rest = [a for i, a in enumerate(args) if a != "errand" and a != "--data" and (i == 0 or args[i - 1] != "--data")]
        if not rest or "--show" in rest or rest[0] == "show":
            print(format_errands(data))
            return 0
        kind, who = division.member()
        caller = who if kind == "member" else "Unity"
        sub = rest[0]
        if sub == "cancel" and len(rest) >= 2:
            return cancel_errand(data, rest[1], now=now, who=caller)
        if sub == "add" and len(rest) >= 2:
            act = rest[1]
            p_raw = rest[rest.index("--params") + 1] if "--params" in rest and rest.index("--params") + 1 < len(rest) else "{}"
            why_s = rest[rest.index("--why") + 1] if "--why" in rest and rest.index("--why") + 1 < len(rest) else ""
            st_s = rest[rest.index("--station") + 1] if "--station" in rest and rest.index("--station") + 1 < len(rest) else ""
            try:
                p_obj = json.loads(p_raw)
            except ValueError as e:
                print("REFUSED: invalid --params JSON: %s" % e)
                return 1
            return add_errand(data, act, p_obj, why_s, station=st_s, now=now, who=caller)
        sys.exit('USAGE: wallet.py errand [--show | add <action> --params "<json>" --why "<text>" [--station <base>] | cancel <id>]')
    if verb == "seat":
        if "--show" in args:
            rows = seat_rows(data)
            emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
            fac = (emp.get("faction") or {}) if isinstance(emp, dict) else {}
            print("SEATS | faction %s/%s | queued open: %d | joined via queue: %d"
                  % (fac.get("member_count", "?"), fac.get("members_limit", "?"),
                     sum(1 for r in rows if r.get("state") == "open"),
                     sum(1 for r in rows if r.get("state") == "joined")))
            for r in rows[-30:]:
                print("  %s | %s%s" % (r.get("pilot"), r.get("state"), (" | " + str(r["note"])) if r.get("note") else ""))
            return 0
        kind, who = division.member()
        if "--dry-run" not in args and who != "Unity":
            sys.exit("REFUSED: seating ships in the faction is the Fleet Admiral's (rule F11)")
        rest = [a for a in args if a != "seat"]
        if "--pick" in rest:
            idx_p = rest.index("--pick")
            lim = int(rest[idx_p + 1]) if idx_p + 1 < len(rest) and rest[idx_p + 1].isdigit() else None
            picks = pick_unseated(data, lim)
            if "--dry-run" in rest:
                print("would queue %d pilots: %s" % (len(picks), ", ".join(picks[:25]) + (" ..." if len(picks) > 25 else "")))
                return 0
            return add_seats(data, picks, now)
        pilots = []
        for a in rest:
            if a.startswith("--"):
                continue
            if a.startswith("@") and os.path.exists(a[1:]):
                pilots.extend([l.strip() for l in open(a[1:], encoding="utf-8") if l.strip()])
            else:
                pilots.append(a)
        if not pilots:
            sys.exit("USAGE: wallet.py seat [--show | --pick [N] [--dry-run] | <pilot>... | @<file>]")
        if "--dry-run" in rest:
            print("would queue %d pilots: %s" % (len(pilots), ", ".join(pilots[:25])))
            return 0
        return add_seats(data, pilots, now)
    if verb == "fund":
        if "--show" in args:
            emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
            tr_now = (emp.get("faction") or {}).get("treasury") if isinstance(emp, dict) else None
            cap_txt = (("%s cr/pilot, %s cr/24h" % (format(ADMIRAL_MAX_SINGLE, ","), format(ADMIRAL_DAY_CAP, ",")))
                       if (ADMIRAL_MAX_SINGLE or ADMIRAL_DAY_CAP) else "unlimited (own division)")
            print("TREASURY | balance: %s cr | floor: %s cr | Admiral cap: %s"
                  % (format(int(tr_now), ",") if isinstance(tr_now, (int, float)) else "?",
                     format(FUND_FLOOR, ","), cap_txt))
            for m in ("Zero", "Mercury", "Apollo", "Apophis", "Oracle"):
                used = division_fund_spent(data, m, now)
                if used:
                    if ADMIRAL_DAY_CAP:
                        print("  24h budget %-8s: %s / %s cr used" % (m, format(used, ","), format(ADMIRAL_DAY_CAP, ",")))
                    else:
                        print("  24h funded %-8s: %s cr (uncapped)" % (m, format(used, ",")))
            for r in funds(data):
                by_s = (" | by " + str(r["by"])) if r.get("by") else ""
                print("FUND %s %s cr | %s%s | %s | opened %s UTC%s"
                      % (r.get("pilot"), format(int(r.get("credits") or 0), ","), r.get("state"), by_s, r.get("why"),
                         time.strftime("%Y-%m-%d %H:%M", time.gmtime(r.get("at") or 0)),
                         (" | " + str(r["note"])) if r.get("note") else ""))
            return 0
        kind, who = division.member()
        if kind == "member" and who not in division.MEMBERS:
            sys.exit("REFUSED: unknown member %r cannot fund from the treasury" % (who,))
        caller = who if kind == "member" else "Unity"
        rest = [a for a in args if a != "fund"]
        why = rest[rest.index("--why") + 1] if "--why" in rest else ""
        hours = float(rest[rest.index("--hours") + 1]) if "--hours" in rest else FUND_HOURS
        plain = [a for i, a in enumerate(rest) if not a.startswith("--") and (i == 0 or rest[i - 1] not in ("--why", "--hours", "--data"))]
        if len(plain) != 2 or not plain[1].isdigit() or not why:
            sys.exit('USAGE: wallet.py fund <pilot[,pilot2...]> <credits> --why "<text>" [--hours H]')
        pilots_in = [p.strip() for p in plain[0].split(",") if p.strip()]
        if not pilots_in:
            sys.exit('USAGE: wallet.py fund <pilot[,pilot2...]> <credits> --why "<text>" [--hours H]')
        rc = 0
        for p_one in pilots_in:
            if add_fund(data, p_one, int(plain[1]), why, hours, now, who=caller) != 0:
                rc = 1
        return rc
    if verb == "serve":
        dry = "--dry-run" in args
        daemon = "--daemon" in args
        every = int(args[args.index("--every") + 1]) if "--every" in args and args.index("--every") + 1 < len(args) else 60
        kind, who = division.member()
        if not dry and not (who == "Unity" or kind == "service"):
            sys.exit("REFUSED: a real serve pass is the Fleet Admiral's or the five-minute job's; use --dry-run")
        if daemon:
            return serve_daemon(data, every=every, dry=dry)
        return serve(data, now, dry)
    if verb == "sweep":
        dry = "--dry-run" in args
        cash_only = "--cash-only" in args
        if not dry and not SWEEP_ENABLED:
            sys.exit("REFUSED: the sweep is off (wallet.py SWEEP_ENABLED = False) until the Fleet Admiral has read its dry run and "
                     "switched it on; `wallet.py sweep --dry-run` says what it would do")
        kind, who = division.member()
        if not dry and not (who == "Unity" or kind == "service"):
            sys.exit("REFUSED: a real sweep is the Fleet Admiral's or the five-minute job's; use --dry-run")
        return sweep(data, now, dry, cash_only=cash_only)
    rows = wallets(data)
    if not rows:
        print("wallet: no wallet read in %s" % data)
        return 1
    low = sorted(r for r in rows if r[1] < LOW)
    if verb == "check":
        poorest = min(rows, key=lambda r: r[1])
        print("WALLETS | %d pilots | poorest %s %s cr | under %s cr: %d | under the floor %s cr: %d"
              % (len(rows), poorest[0], format(poorest[1], ","), format(LOW, ","), len(low), format(FLOOR, ","), sum(1 for r in rows if r[1] < FLOOR)))
        bad = [r for r in rows if r[1] < FLOOR]
        for name, credits, owner in bad:
            print("HALT: %s holds %s cr, under the floor of %s (division of %s): `wallet.py topup` gives it credits" % (name, format(credits, ","), format(FLOOR, ","), owner))
        return 1 if bad else 0
    kind, who = division.member()
    if "--dry-run" not in args and not (who == "Unity" or kind == "service"):
        sys.exit("REFUSED: a real top-up is the Fleet Admiral's or the five-minute job's; use --dry-run")
    flying, unsettled = settle_gifts(data, "topup", now, "--dry-run" in args)    # Q75: a top-up a cut pass left `sent`, settled first
    given = dict(recent(data, now), **{name: at for name, at in flying.items() if name})
    given.update({name: now for name in awaiting_treasury(data) if name and name not in given})   # the treasury serves it
    held, owes = funded(data, now), owed(data)                  # a fund for a buy, and credits withdrawn for others, are no donor's to give
    gifts = [(d, p, c) for d, p, c in plan_gifts(topup_view(rows, held, owes), given) if d not in flying]
    done, failed = [], []
    for donor, pilot, credits in gifts:
        if "--dry-run" in args:
            print("would give: %s -> %s %s cr" % (donor, pilot, format(credits, ",")))
            continue
        if time.time() - now > BUDGET:                          # a gate that answers slowly: the rest waits for the next pass
            break
        purse = {name: credits_now for name, credits_now, _owner in wallets(data)}      # both wallets right before the call
        sent = note(data, "topup", donor, pilot, credits, "sent", "", wallets={donor: purse.get(donor), pilot: purse.get(pilot)})
        try:                                                    # Q75: on disk before the call; a cut pass leaves it for settle_gift
            ok, text = give(donor, pilot, credits)
        except Exception as error:                              # the gate did not answer (a timeout): the game may still have taken the gift
            was = next((have for name, have, _owner in rows if name == pilot), 0)
            ok, text = landed(data, pilot, was, credits), "the gate did not answer (%s: %s) and the wallet does not show the gift" % (type(error).__name__, error)
            if not ok:
                unsure(data, donor, pilot, credits, time.time())
        if ok:
            book(data, [(donor, pilot, credits)], time.time())  # at once and with its own time: a fault later in the pass never loses the record
            done.append((donor, pilot, credits))
        else:
            failed.append((donor, pilot, text))
        note(data, "topup", donor, pilot, credits, "booked" if ok else "unsure" if "did not answer" in text else "refused", text, sent_at=sent)
    for pilot in dict.fromkeys(p for _d, p, _c in done):          # once per receiver, after its last gift
        refresh(pilot)
    for donor, pilot, credits in done:
        print("given: %s -> %s %s cr" % (donor, pilot, format(credits, ",")))
    for donor, pilot, text in failed:
        print("HALT: the gift %s -> %s failed: %s" % (donor, pilot, text))
    stranded = [(name, credits) for name, credits, _o in low if name not in {p for _d, p, _c in gifts}]
    lent = treasury_topups(data, [(n, c) for n, c in stranded if n not in given], now, "--dry-run" in args)   # requests ENT-380 ff.: the treasury, when no ship can give
    for name, _credits in stranded:
        if name not in recent(data, now) and name not in lent:
            print("HALT: %s is under %s cr and no ship of its division or of the command group can give without going under %s" % (name, format(LOW, ","), format(KEEP, ",")))
    return 1 if failed or unsettled else 0


if __name__ == "__main__":
    sys.exit(main())
