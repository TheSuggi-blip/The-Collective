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
  - A fund (orders ENT-063: one Recursion for Military from the purse) is the Fleet Admiral's alone: a row of
    data/fleet/funds.json, served at the start of a sweep pass, one at a time, while the leader stands docked (the
    game takes a treasury withdrawal docked only: storage `deposit` of credits, source `faction`, target `self`,
    2026-11-22) and the treasury keeps FUND_FLOOR after it. The first fund ever withdraws 1 cr first and reads the
    treasury (rule F12). The withdrawal is booked once in onetime.json (FUND_TITLE, plus for the leader: money paid
    once, never steady income), the gift to the pilot as every gift is; for FUND_HOURS (or --hours) from its gift the
    sweep and the top-ups leave the funded credits with the pilot, then the row ends by itself. A withdrawal whose gift
    failed is given at the next pass and the leader keeps it from the deposit meanwhile.
WHY:  Suggi, 2026-11-16: "No ships can go broke, this is important." Standing work costs fuel and earns nothing, and
      the weekly tax takes a share of every wallet in one moment.

USAGE:
  wallet.py [check]            every wallet against the floors; HALT for a pilot under 3,000 cr
  wallet.py topup [--dry-run]  give each pilot under LOW credits up to TARGET from a rich ship of its division
  wallet.py sweep [--dry-run]  the part above KEEP_SHIP of the richest ships to the leader, the leader's into the treasury
  wallet.py fund <pilot> <credits> --why "<text>" [--hours H]
                               the treasury pays one pilot for a buy: the next pass the leader stands docked withdraws the
                               credits and gives them; the sweep and the top-ups leave that much with the pilot for H hours
  wallet.py fund --show        the funds on record and their state
  --data <dir>                 the unit's data folder (default: the fleet's)

Stdlib only. ASCII only.
"""

import calendar
import fcntl
import json
import os
import sys
import time
from pathlib import Path

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
PER_PASS = 4                   # gifts a sweep tries at most: each takes about half a minute (the gift, the receiver's read)
LEADER = "Prime Directive"     # the faction's leader when empire.json names none
SKIP_PILOTS = set()            # pilots that never give in a sweep (one that holds credits for a buy the code does not know)
SHOW_WAIT = 45                 # seconds the sweep waits for the giver's wallet to show the money gone before it books
BATTLE_WAIT = 10 * 60          # a pilot refused `in_battle` is not asked again in this long
UNSURE_HOLD = 60 * 60          # after a deposit the wallet did not show, no new deposit in this long
DEPOSIT_FIRST = 100000         # the leader holding this much above KEEP_SHIP deposits before any gift of the pass: the gifts of
                               # about 80 s each used up DEPOSIT_BY in every pass and 1.2 million cr stood in its wallet (r24)
DEPOSIT_BY = 90                # seconds into a pass after which the deposit waits for the next pass: the job cuts a pass at
                               # 200 s, and a deposit's call, read and check take up to about 100 s (2026-11-21 21:08 UTC)
DEPOSIT_TITLE = "Faction treasury: credits deposited (the Collective keeps them)"     # begins with routes.TREASURY
SENT_KEEP = 60 * 60            # a gift left `sent` whose receiver has no reading after its call is kept unsure after this long
FUND_FLOOR = 500000            # what the treasury keeps after a fund (the Fleet Admiral's line)
FUND_HOURS = 6                 # a funded pilot keeps its fund this long from the gift (the buy), then the sweep may take it
FUND_WAIT = 24                 # hours an open fund waits for a docked leader before it ends by itself
FUND_READ = 12                 # seconds between a withdrawal's call and the treasury's read after it (about one tick)
FUND_TITLE = "Treasury fund: credits withdrawn from the faction treasury for a buy"   # never begins with routes.TREASURY


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


def unsure(data, donor, pilot, credits, now):
    """A gift the gate did not answer for and the wallet does not show: kept with 0 credits, so the pilot is on cooldown
    (recent) and no figure counts it (routes.moved)."""
    with open(Path(data) / "fleet" / "gifts.jsonl", "a", encoding="utf-8") as handle:
        handle.write(json.dumps({"at": int(now), "from": donor, "to": pilot, "credits": 0, "unsure": credits}) + "\n")


def book(data, gifts, now):
    """The gifts into gifts.jsonl and, twice each, into onetime.json (kept out of the steady money)."""
    folder = Path(data) / "fleet"
    with open(folder / "gifts.jsonl", "a", encoding="utf-8") as handle:
        for donor, pilot, credits in gifts:
            handle.write(json.dumps({"at": int(now), "from": donor, "to": pilot, "credits": credits}) + "\n")
    once = folder / "onetime.json"
    with open(str(once) + ".lock", "w") as lock:                    # the lock the runners and gate.py book under
        fcntl.flock(lock, fcntl.LOCK_EX)
        rows = dispatch.read_json(once, [])
        rows = rows if isinstance(rows, list) else []
        for donor, pilot, credits in gifts:
            rows += [[int(now), donor, TITLE, -credits], [int(now), pilot, TITLE, credits]]
        tmp = "%s.%d.tmp" % (once, os.getpid())
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


def builders(data):
    """The pilots whose faction role is the builder's (empire.json members): they hold credits for a buy."""
    members = (dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}).get("members") or []
    return {str(m.get("pilot")) for m in members if isinstance(m, dict) and "build" in str(m.get("role") or "").lower()}


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
    with open(Path(data) / "fleet" / "sweep.jsonl", "a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())                                  # written before the call it announces
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
    with open(str(once) + ".lock", "w") as lock:                    # the lock the runners and gate.py book under
        fcntl.flock(lock, fcntl.LOCK_EX)
        rows = dispatch.read_json(once, [])
        rows = rows if isinstance(rows, list) else []
        rows.append([int(now), pilot, DEPOSIT_TITLE, -int(credits)])
        tmp = "%s.%d.tmp" % (once, os.getpid())
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
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = "%s.%d.tmp" % (path, os.getpid())
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(rows[-200:], handle, indent=1)
    os.replace(tmp, path)


def funded(data, now):
    """{pilot: credits} the sweep and the top-ups leave with a pilot: each fund given within its hours."""
    out = {}
    for r in funds(data):
        if r.get("state") == "given" and now - (r.get("given_at") or 0) < float(r.get("hours") or FUND_HOURS) * 3600:
            out[r["pilot"]] = out.get(r["pilot"], 0) + int(r.get("credits") or 0)
    return out


def withdrawn(data):
    """Credits the leader holds for a fund whose gift has not gone yet: kept out of its deposit."""
    return sum(int(r.get("credits") or 0) for r in funds(data) if r.get("state") == "withdrawn")


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


def serve_funds(data, leader, now, dry):
    """One fund a pass (a withdrawn one first, else the oldest open one): withdrawn while the leader stands docked and
    the treasury keeps FUND_FLOOR, then given to its pilot. 0, or 1 when a call failed."""
    rows, changed = funds(data), False
    for r in rows:                                              # an open fund ends by itself after FUND_WAIT hours
        if r.get("state") == "open" and now - (r.get("at") or 0) > FUND_WAIT * 3600:
            r.update(state="ended", note="no docked leader within %d hours" % FUND_WAIT)
            changed = True
            print("FUND ended: %s %s cr: the leader stood docked at no pass within %d hours" % (r["pilot"], format(int(r["credits"]), ","), FUND_WAIT))
    todo = next((r for r in rows if r.get("state") == "withdrawn"), None) or next((r for r in rows if r.get("state") == "open"), None)
    if not todo or dry:
        if todo:
            print("would fund: %s %s cr from the treasury (%s), state %s" % (todo["pilot"], format(int(todo["credits"]), ","), todo.get("why"), todo["state"]))
        elif changed:
            write_funds(data, rows)
        return 0
    pilot, credits = todo["pilot"], int(todo["credits"])
    if todo["state"] == "open":
        if not docked(data, leader):
            run_marker = Path(data) / "fleet" / "host" / "running" / (leader + ".json")
            if run_marker.exists():
                stop_p = Path(data) / "fleet" / "host" / "stop" / leader
                stop_p.parent.mkdir(parents=True, exist_ok=True)
                stop_p.touch()
            print("FUND waits: %s %s cr: the leader %s is not docked (the game withdraws docked only)" % (pilot, format(credits, ","), leader))
            if changed:
                write_funds(data, rows)
            return 0
        before = treasury_read(leader)
        if before is None or before - credits < FUND_FLOOR:
            print("FUND waits: %s %s cr: the treasury reads %s, it keeps %s" % (pilot, format(credits, ","), before, format(FUND_FLOOR, ",")))
            if changed:
                write_funds(data, rows)
            return 0
        if not any(r.get("state") in ("withdrawn", "given") or r.get("probed") for r in rows):     # rule F12: one unit first
            ok, text = withdraw(leader, 1)
            time.sleep(FUND_READ)
            after = treasury_read(leader)
            todo["probed"] = {"ok": ok, "text": text, "before": before, "after": after}
            write_funds(data, rows)
            if not ok or after is None or before - after < 1:
                print("HALT: FUND probe: 1 cr from the treasury was not taken (%s; the treasury %s -> %s): no fund is withdrawn" % (text, before, after))
                return 1
            gate_book(leader, FUND_TITLE + " (the 1 cr probe)", 1)
            before = after
        ok, text = withdraw(leader, credits)
        time.sleep(FUND_READ)
        after = treasury_read(leader)
        if not (after is not None and before - after >= credits * 0.9):
            todo.update(state="open" if ok is False else "unsure", note="withdraw: %s; the treasury %s -> %s" % (text, before, after))
            write_funds(data, rows)
            print("HALT: FUND %s %s cr: the withdrawal %s (the treasury %s -> %s)" % (pilot, format(credits, ","), ("was refused: " + text) if ok is False else "does not show", before, after))
            return 1
        gate_book(leader, "%s: %s" % (FUND_TITLE, todo.get("why") or pilot), credits)
        todo.update(state="withdrawn", withdrawn_at=int(time.time()), treasury=[before, after])
        write_funds(data, rows)
        print("FUND withdrawn: %s cr from the treasury by %s for %s (the treasury %s -> %s)" % (format(credits, ","), leader, pilot, before, after))
    ok, text = give(leader, pilot, credits)
    if not ok:
        todo["note"] = "gift: %s" % text
        write_funds(data, rows)
        print("HALT: FUND gift %s -> %s %s cr refused: %s; the leader keeps it and gives at the next pass" % (leader, pilot, format(credits, ","), text))
        return 1
    book(data, [(leader, pilot, credits)], time.time())
    todo.update(state="given", given_at=int(time.time()))
    write_funds(data, rows)
    print("FUND given: %s -> %s %s cr (%s); the sweep leaves it for %s hours" % (leader, pilot, format(credits, ","), todo.get("why"), todo.get("hours") or FUND_HOURS))
    return 0


SEAT_BATCH = 20
SEAT_BUDGET = 80


def seats_file(data):
    return Path(data) / "fleet" / "seats.json"


def seat_rows(data):
    rows = dispatch.read_json(seats_file(data), [])
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def write_seats(data, rows):
    path = seats_file(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = "%s.%d.tmp" % (path, os.getpid())
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
    if fighting(fleet.get(leader) or {}) or not try_hold_sweep(data, leader, now):
        if (Path(data) / "fleet" / "host" / "running" / (leader + ".json")).exists():
            sp = Path(data) / "fleet" / "host" / "stop" / leader
            sp.parent.mkdir(parents=True, exist_ok=True)
            sp.touch()
        print("SEATS waits: leader %s is on a run (%s)" % (leader, division.order_of(leader, data) or "fighting"))
        return 0
    joined = 0
    t0 = time.time()
    try:
        emp = dispatch.read_json(Path(data) / "empire" / "empire.json", {}) or {}
        fid = str(((emp.get("faction") or {}).get("id")) or "")
        st_i, txt_i = faction_raw(leader, "info", {})
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
            if not try_hold_sweep(data, p, time.time()):
                if (Path(data) / "fleet" / "host" / "running" / (p + ".json")).exists():
                    sp = Path(data) / "fleet" / "host" / "stop" / p
                    sp.parent.mkdir(parents=True, exist_ok=True)
                    sp.touch()
                continue
            try:
                st_a, txt_a = faction_raw(leader, "invite", {"player_id": p})
                st_b, txt_b = faction_raw(p, "join", {"faction_id": fid})
                comb = (txt_a + " " + txt_b).lower()
                if "faction_full" in comb:
                    faction_raw(leader, "withdraw_invite", {"player_id": p})
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
                release_sweep(data, p)
    finally:
        release_sweep(data, leader)
    write_seats(data, rows)
    if joined:
        print("SEATS joined: %d pilots added to CLTV (%d still open)"
              % (joined, sum(1 for r in rows if r.get("state") == "open")))
    return 0


def add_fund(data, pilot, credits, why, hours, now):
    rows = funds(data)
    if any(r.get("pilot") == pilot and r.get("state") in ("open", "withdrawn", "unsure") for r in rows):
        print("REFUSED: %s has a fund open already" % pilot)
        return 1
    if pilot not in ships(data):
        print("REFUSED: %s holds no wallet reading in the fleet file" % pilot)
        return 1
    rows.append({"pilot": pilot, "credits": int(credits), "why": why, "hours": hours, "at": int(now), "state": "open"})
    write_funds(data, rows)
    print("FUND open: %s %s cr (%s); served at the next pass the leader stands docked" % (pilot, format(int(credits), ","), why))
    return 0


def sweep(data, now, dry):
    """One pass of the sweep: at most PER_PASS gifts to the leader, then the leader's deposit. 0, or 1 when a call failed."""
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
    failed = serve_funds(data, leader, now, dry) or failed or unsettled   # orders ENT-063: the treasury pays one pilot for a buy
    serve_seats(data, leader, now, dry)
    log = swept(data)
    battle = {r.get("from"): r["at"] for r in log if r.get("state") == "battle" and now - r["at"] < BATTLE_WAIT}
    held = [r for r in log if r.get("kind") == "deposit" and r.get("state") == "unsure" and now - r["at"] < UNSURE_HOLD]
    skip = {leader} | SKIP_PILOTS | builders(data) | set(funded(data, now))
    cool = dict(touched(data, now), **{name: at for name, at in flying.items() if name})
    named = dispatch.flagships(data)
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
    plan = plan_sweep(fleet, leader, skip | set(battle) | set(cool), named)
    fought = [r for r in log if r.get("kind") == "deposit" and r.get("state") == "refused" and now - r["at"] < BATTLE_WAIT
              and "in_battle" in str(r.get("text") or "").lower().replace(" ", "_")]
    if plan and not held and not pending(log) and not fought and fleet[leader]["credits"] - KEEP_SHIP >= DEPOSIT_FIRST:
        print("the leader's deposit first: %s cr above its line; the gifts wait for the next pass" % format(int(fleet[leader]["credits"] - KEEP_SHIP), ","))
        plan = []
    for pilot, credits in plan:
        if dry:
            print("would give: %s -> %s %s cr (keeps %s)" % (pilot, leader, format(credits, ","), format(keep_for(pilot, named)[0], ",")))
            continue
        if time.time() - now > BUDGET:
            print("the pass's %d seconds are used up: %s waits for the next pass" % (BUDGET, pilot))
            break
        was = fleet[pilot]["credits"]
        sent = note(data, "gift", pilot, leader, credits, "sent", "", wallets={pilot: was, leader: (ships(data).get(leader) or {}).get("credits")})
        try:                                                    # Q75: on disk before the call; a cut pass leaves it for settle_gift
            ok, text = give(pilot, leader, credits)
        except Exception as error:                              # the gate did not answer: the game may still have taken it
            ok, text = None, "the gate did not answer (%s: %s)" % (type(error).__name__, error)
        if ok is False:
            fight = "in_battle" in text.lower().replace(" ", "_")
            note(data, "gift", pilot, leader, credits, "battle" if fight else "refused", text, sent_at=sent)
            if fight:
                print("in a fight: %s gives nothing now; asked again after %d minutes" % (pilot, BATTLE_WAIT // 60))
            else:
                failed = 1
                print("HALT: the gift %s -> %s %s cr was refused: %s" % (pilot, leader, format(credits, ","), text))
            continue
        if (ok and answer_shows(text, pilot, was, credits)) or shows(data, pilot, was, credits):
            book(data, [(pilot, leader, credits)], time.time())
            note(data, "gift", pilot, leader, credits, "booked", text, sent_at=sent)
            print("given: %s -> %s %s cr" % (pilot, leader, format(credits, ",")))
        else:
            unsure(data, pilot, leader, credits, time.time())
            note(data, "gift", pilot, leader, credits, "unsure", text, sent_at=sent)
            failed = 1
            print("HALT: the gift %s -> %s %s cr is not booked: %s; the wallet of %s does not show it gone after %d s (kept unsure, the pilot on cooldown)"
                  % (pilot, leader, format(credits, ","), "answered" if ok else text, pilot, SHOW_WAIT))
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
    elif time.time() - now > DEPOSIT_BY:
        print("the pass used %d seconds: the deposit waits for the next pass" % int(time.time() - now))
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
    verb = "seat" if "seat" in args else "fund" if "fund" in args else "topup" if "topup" in args else "sweep" if "sweep" in args else "check"
    now = time.time()
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
            for r in funds(data):
                print("FUND %s %s cr | %s | %s | opened %s UTC%s" % (r.get("pilot"), format(int(r.get("credits") or 0), ","), r.get("state"), r.get("why"),
                      time.strftime("%Y-%m-%d %H:%M", time.gmtime(r.get("at") or 0)), (" | " + str(r["note"])) if r.get("note") else ""))
            return 0
        kind, who = division.member()
        if who != "Unity":
            sys.exit("REFUSED: a fund from the treasury is the Fleet Admiral's alone (rule F11: the purse)")
        rest = [a for a in args if a != "fund"]
        why = rest[rest.index("--why") + 1] if "--why" in rest else ""
        hours = float(rest[rest.index("--hours") + 1]) if "--hours" in rest else FUND_HOURS
        plain = [a for i, a in enumerate(rest) if not a.startswith("--") and (i == 0 or rest[i - 1] not in ("--why", "--hours", "--data"))]
        if len(plain) != 2 or not plain[1].isdigit() or not why:
            sys.exit('USAGE: wallet.py fund <pilot> <credits> --why "<text>" [--hours H]')
        return add_fund(data, plain[0], int(plain[1]), why, hours, now)
    if verb == "sweep":
        dry = "--dry-run" in args
        if not dry and not SWEEP_ENABLED:
            sys.exit("REFUSED: the sweep is off (wallet.py SWEEP_ENABLED = False) until the Fleet Admiral has read its dry run and "
                     "switched it on; `wallet.py sweep --dry-run` says what it would do")
        kind, who = division.member()
        if not dry and not (who == "Unity" or kind == "service"):
            sys.exit("REFUSED: a real sweep is the Fleet Admiral's or the five-minute job's; use --dry-run")
        return sweep(data, now, dry)
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
    held = funded(data, now)                                    # a fund for a buy is no donor's to give
    gifts = [(d, p, c) for d, p, c in plan_gifts([(n, c - held.get(n, 0), o) for n, c, o in rows], given) if d not in flying]
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
    stranded = [name for name, credits, _o in low if name not in {p for _d, p, _c in gifts}]
    for name in stranded:
        if name not in recent(data, now):
            print("HALT: %s is under %s cr and no ship of its division or of the command group can give without going under %s" % (name, format(LOW, ","), format(KEEP, ",")))
    return 1 if failed or unsettled else 0


if __name__ == "__main__":
    sys.exit(main())
