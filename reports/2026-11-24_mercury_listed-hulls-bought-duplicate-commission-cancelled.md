---
name: listed-hulls-bought-duplicate-commission-cancelled
id: 20261124T132930Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, hulls, missions, bursar]
links:
  - reports/2026-11-24_mercury_bursar-buy-lane-off-station-needs-gated-listed-apophenia.md
  - reports/2026-11-24_unity_posted-role-gates-five-answers-lift-commits-fixed.md
---

# Trade -- Listed Hulls Bought, a Duplicate Commission Cancelled, Finish Routes Kept to Their Holders

## Situation

Period: 13:01 to 13:30 UTC on 2026-11-24, since
`reports/2026-11-24_mercury_bursar-buy-lane-off-station-needs-gated-listed-apophenia.md`
(11:20 UTC). Orders: `orders.log ENT-087` (Suggi's strategy v2.5; the
PLAN and blocks of ENT-086 stand: block MERCURY asks standing work for
every waiting trader, `requires.posted` on the Station Need routes,
no bid against Logistics' steel, tier-2 hulls for the Piloting-10
traders).

Ships: 85 traders, none lost; fill gate for trader PASS at 13:03 and
13:23 UTC (`fill.py check`, tool `fill`). Money (tool `fleet`
view=money, 13:27 UTC): Trade's last hour reads net +680,113 cr,
income 50,859 cr and costs -629,254 cr; the negative cost is mostly
buy escrow coming back as bursars cancel their old orders, so it is
not earnings. Trade's 24-hour recurring figure rose from +12.0k to
+28.5k cr an hour and the division score from 71.6 to 73.9 (briefing
scorecard, 13:01 and 13:28 UTC). Treasury 9,121,178 -> 9,271,091 cr.
Open buy escrow over all traders: 1,421,250 cr at 11:33 UTC, 407,385
cr at 13:06 UTC (`orders_scan.py`, 85 pilots, 65 buy orders left).

## Activities

1. Tier-2 hulls (block MERCURY; rules F12, F17). The ship exchange
   (table `ship_listings`, 13:17 UTC) lists hulls far under a
   commission. Bought: one Baling Wire (tier 2, 275 cargo, speed 3)
   from an Empire Treasury listing at 26,284 cr (RESULT 13:19 UTC,
   booked once). Trade's tier-2 count went from 2 of 14 to 3 of 15
   Piloting-10 pilots (`hive.py upgrades trade`).
2. A duplicate commission found and cancelled. One trader that
   already flies a listed Apophenia had a second one commissioned at
   11:55 UTC (205,135 cr; my cancel of 11:00 UTC was lost, see
   Problems). Caught docked at 13:23 UTC: `cancel_commission`
   refunded 80,994 cr and returned the gathered build materials to its
   storage at The Experiment (55 silicate composite and 2 processing
   cores among them, both reserve needs).
3. Prayer batch (rule F17): five starter traders standing where a
   Prayer (540 cargo, speed 3) is listed got a buy script; one bought
   at 3,240 cr by 13:25 UTC, three wait for their runs to end, one was
   stopped because Frontier Station is a mobile capital.
4. Finish routes (errors.log ENT-187, requests ENT-514):
   `finish-prospectus-levy-haven` left Trade's list First and went to
   the head of the own rows of the 22 traders whose ship files hold
   Federation Trade Route Prospectus half done (46 of its 250 runs
   paid, all by holders; plan 13:14 UTC, commit a4fe9b11).
5. First Links (errors.log ENT-189): nickel limit 130 -> 185 and
   `requires.ask` at Market Prime (ask 170 x 875, book 13:15 UTC),
   commit 71224fc3.
6. Answered Apollo (admirals.log ENT-129): the seven stations where a
   trader receiver stands for the haulers' soma and ration lots, and
   the P0 and tier-2 listings for every division.

## Problems

- The upgrade queue lost my edits of 11:00 UTC (errors.log ENT-190):
  three cancels and four new entries. Cause, read from the code: the
  wallet service's serve pass saves the queue rows it loaded 70
  seconds earlier, with no lock. Cost: 124,141 cr of the duplicate
  commission now lies as build materials, not credits.
- All four Apophenia commissions at The Experiment stand at
  'sourcing' since 10:26 to 10:58 UTC, short of phase matrix and
  neural interface gel (`commission_status` 13:10 UTC).
- Two funded listed buys did not start: `wallet.py fund` answered
  'no_storage' twice (the fund is withdrawn only while the pilot docks
  at a lockbox). I stopped both scripts, released the held pilot and
  left the two funds open.
- One Prayer script named Frontier Station at a fixed place; it is a
  mobile capital. Stopped before it moved the ship.

## Plans

- Next turn: read `commission_status` of the three remaining
  Apophenia commissions; if still sourcing, cancel them and buy
  listed tier-2 hulls (Analysis 89,229 cr, Meridian Freighter 91,039,
  Bulk Terms 97,194, Apophenia 141,529 at Node Gamma; table
  `ship_listings` 13:17 UTC), with the money taken where the pilot
  docks at a lockbox.
- Read the first runs of the new Baling Wire and Prayers (fuel per
  jump, minutes a run) before a second Prayer batch for the starters
  at the other listing stations.
- Read the runs of `finish-prospectus-levy-haven` by the 22 holders
  (4,000 cr each once) and of First Links under its new gate.
- The HEXC levity bladder contract at Krynn (750 for 55,125 cr; we
  hold 705, 455 of them at Arneb) waits for a 240-cargo hull: a
  starter carries 65.
- Choices made alone: the finish route in holders' rows only; the
  duplicate commission cancelled; Prayers bought where listed.

## Suggestions

- To Trinity and Unity (errors.log ENT-190): a lock around every
  load-modify-save of `data/fleet/upgrade_queue.json`, or a save that
  merges by entry id. Cost: one lock file in `upgrades.py`; owner
  Trinity. Without it any hand edit inside a five-minute serve pass
  is lost.
- To Unity: `fill.py fill --write` could leave `finish-*` routes (no
  accept) out of a list First; Apophis's requests ENT-514 asks a
  `requires.mission` gate, which would also cover Trade.
- To Unity: a fund served by a gift when the pilot is far from a
  lockbox, as `P2P_FUND_MAX` suggests; two funds of this turn waited.

## Feedback

- `buy_listed_hull.py` (Apophis, copied into my skill) bought the
  Baling Wire and a Prayer unchanged, with travel, refuel, booking and
  release; it is the right tool for every listed hull.
- `browse_ships` with `can_fly` from a docked trader answered for an
  Outer Rim hull in one free read: a Voidborn pilot at Piloting 10 may
  fly it.
- `wallet.py fund` printed 'served at the next 5m pass while docked at
  a lockbox' and then 'no_storage' in `--show`: the condition is
  printed, but a turn cannot tell when a far pilot will meet it.
- `comms.py post` refused my first errors entry because it named
  pilots; the message said what to change. Good gate.
- `plan.py note` printed nothing on a first call through the shell;
  the tool `plan` action=note wrote it at once.

## Learnings

- Lesson: a listed hull costs a fraction of a commission (Baling Wire
  26,284 cr, Prayer 3,240 cr, against about 203,000 cr for an
  Apophenia commission), and a commission can wait hours on its yard's
  materials. Record: `ship_listings` 13:17 UTC; RESULT lines 13:19 and
  13:25 UTC; `commission_status` 13:10 UTC. Change: listings with
  `can_fly` first, `commission_status` before any queue entry. Fleet
  takeaway: read the exchange before any commission. Kept in:
  `LEARNINGS.md` (unpromoted), linked to `knowledge/voidborn-order-books.md`.
- Lesson: a finish route without an accept pays only its holders.
  Record: runs.jsonl, 46 of 250 runs paid. Change: such routes only in
  holders' own rows. Kept in: `LEARNINGS.md`, linked to
  `knowledge/voidborn-delivery-missions.md`.
- Skill: trade-books changed -- pitfalls on the unlocked upgrade queue,
  the mobile Frontier Station and `pkill -f`.

## Cross-links

- `game/routes/finish-prospectus-levy-haven.json` -- the finish route.
- `game/routes/mission-first-links-store-grand.json` -- nickel gate.
- `game/fleet/upgrades.py` -- the queue and its serve pass.
- `communications/errors.log` ENT-187, ENT-189, ENT-190.
- `communications/admirals.log` ENT-127, ENT-129.
- `communications/requests.log` ENT-514.
- `game/routes/guidebook/trade/routes.md` -- Standing Plan.
