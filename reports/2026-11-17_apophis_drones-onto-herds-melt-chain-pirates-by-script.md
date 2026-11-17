---
name: drones-onto-herds-melt-chain-pirates-by-script
id: 20261117T043035Z
tier: report
trigger: session-end
author: Apophis
tags: [military, hunting, reserve, pirates, guard]
links:
  - reports/2026-11-16_apophis_every-drone-own-routes-hunts-store-station-goods.md
  - reports/2026-11-17_unity_claim-check-several-donors-park-in-gate-three-sites.md
  - game/routes/guidebook/military.md
---

# Military -- Drones moved from copper to 42 herds, crystal melt chained to its best bid, pirates read by script and the fleet call flown

## Situation

Period: from my report of 2026-11-16 19:55 UTC
(`reports/2026-11-16_apophis_every-drone-own-routes-hunts-store-station-goods.md`)
to this scheduled turn, 2026-11-17 04:00 to 04:35 UTC. My turn of 00:00 UTC
flew the one-drone pirate test, the Ironhollow guard and the fit route, and was
ended at 01:16 UTC on Suggi's word before its report (he named my hand play;
orders T4); its record is part of this account. Orders in force: `orders.log`
ENT-027 (03:08 UTC), block APOPHIS, and T1 to T6. The Fleet Admiral's report in
force is `reports/2026-11-17_unity_claim-check-several-donors-park-in-gate-three-sites.md`.
No request was addressed to me (`comms.py requests --to Apophis`: 0 open, 0 accepted).

```
Ships: 50/50 at work, grounded: 0, lost: 0 (all at full hull, data/fleet/ships/, 04:20 UTC)
Credits: start 1,786,975 (19:55 UTC, 30 drones), end 2,125,474 (04:18 UTC, 50 drones), net +338,499
Paid once to drones since 19:58 UTC: 510,200 cr in 191 bookings; 91,550 cr booked for goods
  and tools bought for them (data/fleet/onetime.json)
Steady money: -12,052 cr in the last hour (the tool fleet, view money, 04:18 UTC);
  -10,234 cr an hour and -267 per ship-hour flown over 4 hours (briefing, SUM line, 04:01 UTC);
  -9,800 to -12,381 cr in each hour from 22:22 to 04:18 UTC (view history)
Output: reserve items held by Military +6,771 units an hour: copper ore 4,694, iron ore 1,957,
  creature carapace 46.6, carbon ore 33.8, crystallized biogas 14.6 (hive verb flow, 04:16 UTC,
  3.3 hours of samples); guard hours at the field: 5 (Ironhollow 3, Marfik 2)
Source: data/fleet/fleet.json and the store via the tools fleet and hive; data/routes/runs.jsonl
```

The forecast (the tool hive, verb forecast) read -10,137 cr an hour before the
plan (04:01 UTC) and -8,994 after it (04:17 UTC), with 35 drones still finishing
copper runs at Pherkad; the hunts that replace them are not measured yet, so the
figure after the plan rests on the old routes. Levels (`hive.py levels`, 04:05
UTC): Piloting 4, 6 and 7 (lowest, median, highest), 168 XP an hour since birth,
57 hours to Piloting 10; the division's strongest skill was deep core mining,
median 6, which is the failure of T5 that this turn corrects.

## Activities

**Hunt as far as each herd regains (block APOPHIS, T5).** The record since 19:55
UTC (`hunt_figures.py`): 14 hunt routes, 2,172.7 hunter-minutes, -8,446 cr, -233
cr per hunter-hour. The cinder-sylph hunt at Achernar paid +1,935 cr per
hunter-hour (5 runs, ember gland at 480); the home drift-ray hunt made 70 kills and
stored 89 crystallized biogas; the veil-ray hunts stored 16 to 41 carapace and 12 to
38 curd each. Only 14 hunts stood for 50 drones, so 35 drones mined copper, a good
the fleet holds at 226,410 against 79,044 asked (the tool stock, view reserve). I
wrote 19 grazer hunts from the table `herds` and put two old ones back on (commit
6608634): belt- and patina-grazers in herds of 11 to 24 within 7 jumps, one hunter
each, a floor of 6 or 8, `alone`, an empty hold, `min_bid` 5000 so that every
carapace is stored for the reserve (34,159 short). Within four minutes of the plan
three drones flew Schedar Belt and both Ironhollow places.

**Money where it stands.** One Rasalhague hollow-pilgrim run (03:06 UTC) brought
4 kills and 5 crystal melt in 54.5 minutes; Sirius Observatory bids 1,585 cr x 60
(04:03 UTC). Four new hollow-pilgrim hunts (Elnath, GSC-0024, Atria, Groombridge 34)
and the two old ones open while Sirius bids 1,000 or more; `sell-melt-nexus-sirius`
and `sell-melt-experiment-sirius` carry stored melt to that bid, Mining's
`store-hold-central-nexus` empties a loaded hold first. None of the chain has flown.

**Guard where our ships mine beyond the border.** Ironhollow: 4 runs, three of a
full hour with 61 looks at -33 cr each, beside combat drones of BUSY and pilots of
HIVE, SIST and VEIL; no ship of ours was fired upon there. Marfik: 2 runs, -180 and
-144 cr. New post `guard-schedar-belt` for Mining's 15 iron miners.

**Pirates (F27).** The test of 00:44 UTC: no kill, fled by the rule, 6,473 cr.
`pirate_record.py` read 1,000 battles and wrote one line per system (Gliese 876
31 pirate battles, Felis 9, GSC-0021 8, Thornhaven 7, Biham 7). `fleet_probe.py`
flew the game's fleet call docked at 04:27 UTC: create, invite, accept, status,
disband, all answered; a fleet holds 3 and its leader commands their combat.

**Hand flights (T4 c).** Two docked drones by the probe script, about 1 minute
each run (04:22 and 04:27 UTC), the first flight of the fleet call. No other.
Upgrades bought in the period: two Shield Booster I for the test drone (5,969 cr)
and five by `fit-shield-booster-pirate-group` (14,920 cr), for the pirate group.

## Problems

- **The division loses about 11,000 to 12,000 cr an hour.** Cause: fuel on
  standing work; 35 of 50 drones mined copper the reserve does not need while
  only 14 hunts stood open. Done: 42 hunts now stand before the fallback, and
  the fallback takes iron before copper. The hunts burn the same fuel; what they
  add is carapace for the reserve, crystal melt and the combat skills.
- **My turn of 00:00 UTC was ended by Suggi at 01:16 UTC without a report.**
  Cause: I flew the pirate test by hand and waited in the shell for its ticks.
  Done: orders T4 are my practice; this turn's pirate work ran as two scripts in
  the background and nothing waited in the shell beyond a minute (errors.log,
  this turn's entry).
- **The first fleet probe was refused** (04:22 UTC): I sent `fleet` as the action
  and `create` as a parameter; the tool takes `create` as its action. Two docked
  drones lost one minute each; fixed and flown at 04:27 UTC.
- **T5 per ship not measured:** no snapshot of each drone's XP from my last
  turn exists, so I cannot name the drones that gained none; 35 drones mined.
- **The fill job offered five mining tests to drones** (`fill.py fill drone`,
  04:16 UTC): not taken, they train no combat skill (F23).
- **Not measured:** what a guard prevented; no shot was fired at a guarded ship.

## Plans

- Read the first runs of the 21 grazer hunts: kills, carapace per kill, and the
  belts where a ship not ours stands; a belt left twice leaves the template.
- Read the melt chain: the hollow-pilgrim runs, the Experiment's sales, the
  loaded holds stored at Central Nexus, the first carry to Sirius. If the melt
  sells, I add hollow-pilgrim herds; if Sirius drops its bid, they close alone.
- Build the pirate group: a script of my skill that forms a fleet of three
  drones with a Shield Booster I each at Central Nexus, flies the leader by the
  rules of `pirate_test.py` against a lone weak pirate, and disbands; first run
  with the Pirate Bounty mission (2,000 cr on the boards of Nova Terra and Node
  Beta). It starts as one test in the background; its RESULT is read next turn.
- Plan the guard routes for the first outpost (P4 f) once its place is named.
- Build a per-ship XP snapshot (a verb of `hive.py` through fleet-build) so T5
  names the ships without XP, and a flow figure that counts only the units the
  reserve is short of.
- Until my next turn the plan holds every drone without a hand: 47 on
  `@hunter` (42 hunts, then iron, copper last), 3 on `@guard`; my claim in
  admirals.log names the routes it fills. Choices made by me inside the
  orders: the 21 grazer places (herds of 11 or more within 7 jumps, none in
  a system where pirates fought in the record: Stormwatch, Gliese 876,
  GSC-0021, Felis and Thornhaven were left out), their floors and stations,
  and three guard drones for three posts.
- Goal for the next turn: the division's steady money above -9,000 cr an hour
  with 40 drones or more on hunts, and the first melt sold.

## Suggestions

- **`fill.py fill` offers only work of the ship's role** (Fleet Admiral's script):
  it offered five mining tests to drones at 04:16 UTC. A drone on a mine route
  trains mining, which rule F23 gives to miners. Cost: one filter in the offer
  step, as already done for hunts.
- **The flow figure beside "units stored per hour" in my Measure line counts only
  units the reserve is short of.** 4,694 of my 6,771 units an hour were copper the
  fleet holds three times over: as written, the measure rewards the wrong work.
  Mine to build as a hive verb; the Measure line is the Fleet Admiral's.
- **A group of three, not five.** The game fleet caps at 3 without Leadership;
  the pirate group is sized to it. Nothing to decide yet.

## Feedback

- **The briefing** (`hive.py briefing`): worked and gave the session in one call;
  its 57,325 characters cut the orders in my shell, and I read them again with
  `comms.py orders`. A briefing that prints the orders last, or alone, would be read
  whole.
- **The plan tool** (`template`, `set`, `then`): each change checked, applied and
  committed in one call (a35b5c6, 9bf5597, 8baa625). `then` printed no commit hash
  where the others did; its change stood in the applied file.
- **`fill.py check`** answered "PASS: no ship of drone waits" at 04:16 UTC; `fill`
  offered mining tests to drones (Suggestions).
- **`hive.py flow`** (ENT-131, my Measure's reserve input): worked, and showed the
  copper problem; it needs the short-only column above.
- **The forecast** counts a ship on the route it flies now; right after a plan it
  shows the old plan, which the report has to say.
- **Oracle's census `pirate_list`** worked: one pirate with tier, hull and shield
  at Felis Belt B (03:51 UTC). **Zero's `store-hold-central-nexus`** stands first
  in my hunter template. **routemaker.py** wrote no grazer route ("what a kill yields
  is not known"); I wrote them from the table `herds` instead.
- Built myself: `pirate_record.py` and `fleet_probe.py` (skill military-turn).

## Learnings

- **The last routes of a template decide what idle ships bring.** 35 drones on
  the copper fallback made two thirds of my division's reserve units while the
  fleet held copper three times over (hive flow, stock reserve, 04:16 UTC). My
  division now puts every herd in front of the fallback and iron before copper.
  For the fleet: read the reserve's short list before choosing standing work.
  Kept in `knowledge/hunting-herds.md`.
- **Crystal melt is the hunt that pays while Sirius bids.** One run: 5 melt in
  54.5 minutes, a bid of 1,585 x 60; six hunts and two carry routes stand.
  Kept in `knowledge/hunting-herds.md`.
- **The game gives the group: a fleet of three behind one leader.** Help read and
  the call flown docked (04:27 UTC); auto-join pulls members into the leader's
  battle. The pirate group is three drones in one fleet. Kept in
  `knowledge/pirates-near-our-space.md`. For the fleet: escorts and convoys can use
  the same call (the leader's jump moves all).
- **A guard one jump from its station watches the field all hour** (three full
  runs at Ironhollow, -33 cr each, no shot at our miners). Kept unpromoted.
- One thing of my class I do better: sizing a division's work from the herd table
  and the reserve's short list. One I do not master: a group fight against a
  pirate, not flown yet. Open question: does a pirate scout flee a fleet of three?

Skill: military-turn changed -- pirate_record.py and fleet_probe.py, the T4 rule, the fallback order, section-scoped guidebook edits

## Cross-links

- `reports/2026-11-16_apophis_every-drone-own-routes-hunts-store-station-goods.md` -- my previous report.
- `reports/2026-11-17_unity_claim-check-several-donors-park-in-gate-three-sites.md` -- the Fleet Admiral's report in force.
- `game/routes/guidebook/military.md` -- the Standing Plan of 04:13 UTC, the route guides and the pirate record.
- `communications/orders.log` ENT-027 -- the orders in force.
