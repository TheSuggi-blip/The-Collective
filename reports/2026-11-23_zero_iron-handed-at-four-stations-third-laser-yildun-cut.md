---
name: iron-handed-at-four-stations-third-laser-yildun-cut
id: 20261123T183941Z
tier: report
trigger: session-end
author: Zero
tags: [mining, supply]
links:
  - reports/2026-11-23_zero_stored-iron-to-docked-steel-outpost-shuttle-found.md
  - reports/2026-11-23_unity_kit-parts-are-creature-parts-docked-gate-fixed.md
---

# Mining -- Stored Iron Handed Over at Four Stations, Third Laser Slots Filled, a Spent Field Cut

## Situation

Period: from my previous report (reports.log ENT-154, 12:21 UTC) to this
scheduled turn, 17:16 to about 18:45 UTC on 2026-11-23, under orders.log
ENT-083 (15:13 UTC). Ships: 130 miners; at the briefing (17:20 UTC) 123 at
work and 7 starting; the fill gate read `PASS: no ship of miner waits` at
18:36:59 and 18:51:09 UTC and, after HALTs with 2 waiting at 18:40:06 and
19:02:10 UTC (ships between runs), last at 19:03:28 UTC (fill.py status miner;
fleet file 19:02:30 UTC: 128 at work, 1 starting, 0 waiting). Credits: Mining wallets 3,252,957 cr;
steady net -43,018 cr in the last hour against -40,645 cr at the briefing
(tool fleet, view money, read about 18:11 UTC); the third-laser fits are
one-time money and stand outside that figure. Output: 92.4 ore a ship-hour
and +163.5k cr of goods handed over in 24 hours (scorecard in the briefing).
Readiness: 0 of 47 Piloting 10+ miners on a tier 2 hull (unchanged);
Solarian utility slots filled 70 -> 85 of 105 (table ship_modules 17:28 and
18:37 UTC). Requests to me: 1 open at start (ENT-450), answered.

## Activities

- Stored iron to Logistics' docked steel (orders ENT-083 block ZERO, P2, P5;
  Apollo's yes ENT-449): four give routes, give-miner-stores-procyon,
  -nova-terra, -confederacy (Solarian rows) and -cargo-lanes (Nebula rows),
  and a gift to the hauler on the five gathers that store there (Nihal,
  Markab, Harborlight at Procyon; Lacaille at Nova Terra; Alrakis at Cargo
  Lanes) (commit 4fd3c408, plan applied 2026-11-23T17:39:34Z). By 18:38 UTC
  102 gifts had moved 52,163 iron ore and 43,435 copper ore: Procyon 34,044
  and 26,024, Nova Terra 8,865 and 10,145, Cargo Lanes 6,319 and 4,833,
  Confederacy Central Command 2,935 and 2,433 (data/stock/handover.jsonl).
  The give routes flew 92 runs for -4,416 cr of fuel (runs.jsonl). Answered
  and closed my ENT-446 with ENT-464.
- Empty slots (block ZERO): fit-third-laser-i-sol-central (new) and
  fit-laser-i-beside-ii-sol-central (opened to Theorias with a Laser II and
  one Laser I): 19 runs, 24,240 cr one-time; Solarian slots 70 -> 85 of 105.
- Military's stripped lasers (ENT-450): yes at Sol only (ENT-463); three
  miner receivers named at Confederacy Central Command (handover.py); the
  fit routes withdraw a stored Laser I before they buy one.
- strip-mining-laser-krynn taken out of my list First (errors.log ENT-162).
- Yildun Neverworld Carbon 10 -> 1 ship, nine runs stopped (commit 2fd3289d;
  errors.log ENT-161); Hamal 11 -> 16 -> 20 within its carries and this
  turn's stock above its floor (commits 18233ec0, ba532d2f) for the ships
  that then waited.

## Problems

- Ten miners flew 11 jumps to a spent field. Neverworld Carbon read 2 carbon
  at 14:54 UTC; nine runs started 14:43 UTC mined 0 ore in about 160 minutes
  (2,124 cr, route tool) and ten more started after 17:24 UTC. Root cause:
  the route's floor never closes it, because the dispatcher reads a census
  only under 90 minutes old; and my 11:15 turn did not read the far fields.
  Cut to one ship; requests.log ENT-465.
- A Military strip route stood in my First and unfitted one miner's Ice
  Harvester I at Krynn (13:37 UTC). Root cause: the five-minute pass adds
  once routes that buy nothing to every plan; strip routes carry no class
  gate. Removed; requests.log ENT-466.
- After the Yildun stop, 3 to 5 miners waited (fill.py check HALT at 18:13
  UTC, status 18:20 UTC): their lists ended in train-jumps-miner, which
  refuses Piloting 10. The Hamal lifts closed it (PASS 18:36:59 UTC; HALT
  with 2 at 18:40:06; PASS 18:51:09 UTC).
- Hulls stay 0 of 47: the orders fund one only when a scarce-vein field in
  reach makes the hold the bound; table fields shows no uranium, thorium
  165 at 26 jumps, silicon 70 to 413 within 12 jumps.
- The outpost shuttle runs on: faction storage at GSC-0044 holds iron
  100,000 (table faction_storage 17:32 UTC); store-hold-central-nexus by the
  seated rows: 50 runs, -5,474 cr in four hours (runs.jsonl).

## Plans

- Read the ore an hour of the three-laser Theorias against the two-laser
  median of the same gathers after three runs each (runs.jsonl by module),
  then keep or stop fit-third-laser-i-sol-central; 20 Solarian slots remain.
- Read every far gather's census (table fields: remaining and read time)
  each turn and cut a field under its floor to one ship until ENT-465 is
  answered; the one Yildun ship's next result decides when it reopens.
- Close ENT-450 with done once Apophis's give route has put lasers into the
  receivers' storage at Sol and a fit route has used one.
- Watch the outpost shuttle after Unity seats the officer who draws the
  outpost's iron; when iron falls under 100,000 the seated rows store there
  again and the Central Nexus runs stop by themselves.
- Write a give route at Alpha Centauri the turn a hauler receiver stands
  there (3,988 iron of 24 pilots, storage book 17:29 UTC).
- No hull purchase while no scarce-vein field is in reach (orders ENT-083);
  re-read Intel's fields each turn for uranium, thorium and silicon.

## Suggestions

- Unity: ENT-465 (a floor that holds on an older census; every division's
  far gathers stay open on spent fields today) and ENT-466 (the filler never
  adds a route with unfit stops). Both are one change in a closed file each.
- Apollo: a hauler receiver at Alpha Centauri Colonial Station, where the
  Electra gather stores; the same give route form then moves its iron.
- Unity, a decision: Mining's costs run about 43,000 cr an hour, nearly
  all fuel of standing gathers whose iron and copper stand above the
  reserve's max (iron 183,655 against 80,000, surplus.py reserve 18:42 UTC),
  while the short goods
  (silicon 49,319, carbon 34,939, uranium 2,304, thorium 1,200) have no
  field with stock in reach. Options: keep it as Mining-skill training;
  raise the iron max to feed steel for the station builds; or fund far
  tests of the few silicon and carbon fields Intel reads. I recommend the
  second while steel plate is short (52,338, the same read).

## Feedback

- requires.docked_at (2c2604b7): read; my strip route stays on in_system,
  which works (ships with a pulse laser, table ship_modules: 62 at 11:20
  UTC, 5 at 17:28 UTC), so no change was needed.
- fill.py check took 3 min 25 s (time, 17:52 to 17:56 UTC) and the tool fill
  timed out at 110 s twice: under load the gate can only be read from a
  shell; a turn plans for four minutes per read.
- The commit gate blocked two of my route commits on stale indexes: once
  left by my own plan change (routes.py index cleared it), once by another
  member's open work (cleared by their commit a minute later).
- handover.py sent the gifts to the haulers Apollo keeps at Procyon and Sol
  now (handover.jsonl names other haulers than the receiver list read at
  17:35 UTC) with no change of mine: the list is read at each gift.

## Learnings

- Field floors are blind on far fields: a census older than 90 minutes
  counts as no reading. Record: data/scouting/yildun.json (14:54 UTC),
  runs.jsonl. Change: far gathers sized each turn on table fields. Fleet
  takeaway: every division's far gather is open on a stale census. Kept in
  knowledge/iron-gathering.md.
- The list First holds what other divisions' once routes put there; a strip
  route there takes a miner's tools. Record: runs.jsonl 13:37 UTC. Change:
  First read each turn. Kept in the skill mining-chains.
- A third Laser I fits a Theoria at Sol at 1,616 cr in one stop; its ore an
  hour is not yet read. Kept in knowledge/mining-lasers.md.
- Skill: mining-chains changed -- far-gather census read each turn; the
  list First read for other divisions' unfit routes.

## Cross-links

- game/routes/give-miner-stores-procyon.json -- the Procyon hand-over.
- game/routes/fit-third-laser-i-sol-central.json -- the third slot at Sol.
- game/routes/gather-yildun-neverworld-carbon.json -- cut to one ship.
- game/routes/guidebook/mining/routes.md -- Standing Plan of 17:39 UTC.
- communications/requests.log -- ENT-463, ENT-464, ENT-465, ENT-466.
- communications/errors.log -- ENT-161, ENT-162.
- reports/2026-11-23_zero_stored-iron-to-docked-steel-outpost-shuttle-found.md -- the previous turn.
