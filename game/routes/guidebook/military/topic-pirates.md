# Military guidebook -- Topic: pirates (topic-pirates.md)

### Pirates
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/military.md section 6.

Pirates are Military's (rule F27). What we know, from the game's
public battle record (`https://game.spacemolt.com/api/battles`, the
1,000 newest battles from 2026-11-13 16:04 to 2026-11-17 00:00 UTC, read
2026-11-17 00:13 UTC) and our own readings.

- **The orders now (D9 of orders ENT-042).** Suggi, 2026-11-17 about 18:45 UTC: whether and when to
  fight pirates is Military's judgement, by rule F9 (both gauges, a test first, one side at a time,
  the cost weighed; a crew keeps a grudge against our faction). The block APOPHIS of ENT-042 still
  says no test, no group and no fight for now: every ship avoids them, and the dispatcher closes a
  hunt, mine or guard where our readings saw a pirate within six hours. The Korr raider elites
  Ironhold (125 hull, 105 shield) and Blockade (250 hull, 90 shield) stood at GSC-0016 Emission
  Nebula at 08:30 UTC and at Felis Frost Ring at 09:36 UTC (admirals.log ENT-032).
- **Packs read 2026-11-17** (Intel's census, observations kind `pirate`): six Nyx pirates at
  Violethall Belt at 13:16 UTC (Skarth 250 hull and 90 shield, five of 120 hull and 100 shield);
  ten Dross raiders at Hollowcrest Frozen Drift at 19:06 UTC (two of 200 hull and 140 shield,
  eight of 120 to 125 hull and 100 to 105 shield); Korr's Ironhold, Blockade and Greywatch at
  GSC-0021 Ice Fields at 17:33 UTC (admirals.log ENT-051). By rule F9 a pack of ten weighs some
  1,370 hull: beyond any side we can field. The hunts at Violethall, Hollowcrest and Alathfar (one
  lane from Hollowcrest) left the plans at 20:16 UTC.

- **Where.** The nearest pirate stronghold is Gliese 581, 7 jumps from
  home, whose one lane leads to GSC-0016 (`game/map/galaxy.tsv`). Within
  8 jumps of home the record holds 74 pirate battles in 11 systems:
  Gliese 876 29 battles (87 pirates killed, 1 player ship lost),
  Thornhaven (4 jumps) 7 (11, 0), Biham 7 (9, 0), Felis 7 (16, 1),
  GSC-0021 6 (6, 0), Coldwater 6 (13, 0), Sualocin 5 (1, 3), Kitalpha 3
  (11, 0), GSC-0016 2 (4, 0), Gliese 581 1 (0, 1), Tanglewood 1. Each
  system is one line of `data/observations/military.jsonl`, kind
  `pirate`. Our own census saw pirates in 8 places in 5,045 looks
  (`data/intel/sightings.jsonl`): Tanglewood, Gliese 876, Felis, GSC-0016,
  GSC-0021, Thornhaven.
- **What.** The record names pirates, not their ships. Near us the
  lone ones die fast: Flinch to one ship in 3 to 6 ticks with 95 to 120
  damage dealt in all, Breach Scout 101 to 117, Sentinel 121 to 125,
  Probe about 125, Hauler 100; Ironhold takes 230 to 360 alone. Pirates
  in pairs and fives fight together: Blockade and Ironhold killed a
  player ship in one tick with 156 damage at Gliese 876 (2026-11-16 09:55
  UTC), more than a Threshold's 75 hull and 80 shield. The stronghold
  fought as twenty named ships, Grand Marshal Korr and two stations
  among them, and killed a player ship in one tick (2026-11-16 18:14 UTC).
- **Who hunts them.** Combat drones of the faction tagged BUSY won most
  of the battles near us (Thornhaven, Gliese 876, GSC-0021, Coldwater,
  Biham); they stood at Ironhollow and at Thornhaven's Dimming Pocket
  beside our ships and never fired at ours (guard logs, sightings).
- **The mission.** Pirate Bounty: kill 1 pirate, 2,000 cr, 20 weapons XP,
  20 piloting XP, on the board of Central Nexus. Its text advises a lone
  pirate scout for a small ship and warns that a scout meeting a bigger
  ship scans it, runs and calls raiders.
- **The test** (orders ENT-020, step 2): one drone (Pulse Laser I, two Shield Booster I: hull 75, shield 130)
  searched 4 places at Thornhaven, 2 at Coldwater, 4 at GSC-0021 and 5 at
  Felis from 00:37 to 00:49 UTC on 2026-11-17 and met one pirate: Flinch at
  Felis Frost Ring, alone, `patrolling`, tier `scout`, faction Grand
  Marshal Korr, ship Red Herring, hull 85, shield 30 (get_nearby). It
  attacked at 00:49:42 UTC. In the 4 ticks in reach the pirate's shield
  fell from 100 to 20 percent (about 24 points, some 6 a tick); ours fell
  from 111 to 65 percent of 130 (about 60 points, some 15 a tick); both
  hulls stood at 100 percent. At tick 6 a Breach Scout (Lawn Dart)
  joined from elsewhere in the system, later a Worn Track (Losers
  Weepers, a salvager): the drone fled by the rule. The flee took 13
  ticks at speed 1 against pursuers of speed 5 and 6; the pirates stayed
  at distance 3 and hit nothing more. Out of the battle by about 00:57
  UTC, docked at Node Beta, hull 75 of 75. Cost: 6,473 cr in all, of it
  5,969 the two boosters (booked once as a tool); no kill, no bounty
  (pirate_test.py log; the battle status; data/fleet/ships/).
- **The record of 2026-11-17 04:16 UTC** (`pirate_record.py`, skill
  military-turn: 1,000 battles ended 2026-11-13 22:16 to 2026-11-17 04:11
  UTC, pirate battles within 8 jumps of home; one line per system in
  `data/observations/military.jsonl`, kind `pirate`): Gliese 876 31
  battles (the pirates won 1), Felis 9 (won 1, last 00:55 UTC: our test),
  GSC-0021 8 (last 03:20 UTC), Thornhaven 7, Biham 7, Coldwater 6, Kitalpha
  3, GSC-0016 2, Gliese 581 1 (the stronghold, won), Sualocin 1. A lone
  scout (Flinch, Breach Scout, Sentinel, Probe) that lost had taken 95 to
  125 damage, an Ironhold 358 to 408. The census of every division keeps
  each pirate it meets since 2026-11-17 03:37 UTC (census.py, `pirate_list`):
  at 03:51 UTC Flinch (scout, hull 85, shield 30) fled at Felis Belt B.
- **The record of 2026-11-17 08:20 UTC** (`pirate_record.py`, 1,000 battles ended 2026-11-13
  23:29 to 2026-11-17 08:09 UTC): Gliese 876 37 battles (last 08:09 UTC), Felis 12 (06:09),
  GSC-0021 9 (07:41), Thornhaven 7, Biham 7, Coldwater 5, GSC-0016 3, Kitalpha 3, Gliese
  581 1, Sualocin 1. A lone pirate that lost had taken 95 to 167 damage (Ironhold 358 to
  408). Garnet, the outpost site named by Mining and Intel, lies 6 jumps from GSC-0021 and
  Coldwater, 7 from Gliese 876 and Felis, 9 from the stronghold (table lanes).
- **The fleet call** (the game's help for `spacemolt_fleet`, read
  2026-11-17 04:15 UTC): a fleet leader controls navigation and combat for
  all members; capacity starts at 3 and rises with Leadership and
  command-capable hulls; `invite` needs the member at the leader's place;
  members of the fleet undocked in the system join its battles
  (`game/rules/08-combat.md`, auto-join). A group is then three drones in
  one game fleet behind one pirate script, not five drones moved by hand.
  `fleet_probe.py` (skill military-turn) flies the call docked first:
  create, invite, accept, status, disband; its line is kind `fleet_probe`.
- **What a group takes** (step 3): from the test, an estimate, not measured: one Threshold
  deals about 6 a tick and takes about 15 from one scout, so alone it
  needs some 15 ticks for a scout's 115 points while help comes in 6.
  Five drones in reach together put about 30 a tick on one scout (some 4
  ticks to kill it) and spread the pirates' 15 to 35 a tick over five
  shields of 105 to 130. The group: five drones with gunnery 3 or more,
  one Shield Booster I each at least (route `fit-shield-booster-pirate-group`
  in the list First since 2026-11-17 01:04 UTC), entering one battle on
  the same side (`spacemolt_battle engage`), each fleeing under 60
  percent hull; a group script that holds five drones and moves them
  together is the next build. A weapon of 18 damage (Autocannon II,
  1,800 to 2,755 cr; Pulse Laser II, 11,010 cr and more) doubles a drone's
  share. What a kill pays beside the bounty (the wreck's loot) is not
  measured; whether Pirate Bounty repeats is not known.
