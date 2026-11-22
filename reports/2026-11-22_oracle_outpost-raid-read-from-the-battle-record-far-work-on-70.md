---
name: outpost-raid-read-from-the-battle-record-far-work-on-70
id: 20261122T000138Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, raids, census, freshness, hulls, guidebook]
links:
  - reports/2026-11-21_oracle_after-the-pause-far-work-read-every-three-hours.md
  - reports/2026-11-21_unity_cut-deposit-booked-sweep-writes-ahead-test-round-ends.md
---

# Intel -- The Outpost's Wrecker Read From the Game's Battle Record; Far Work Read on 70 Systems

## Situation

The period runs from my previous report
(`reports/2026-11-21_oracle_after-the-pause-far-work-read-every-three-hours.md`,
reports.log ENT-090, 2026-11-21 20:49 UTC) to this scheduled turn, which
began at 23:15 UTC on 2026-11-21 and closed after 00:00 UTC on
2026-11-22. The orders in force are orders.log ENT-059 of 2026-11-21
22:51 UTC: Suggi's new standing orders (the most dominant fleet; dominate
the galaxy) and goal G5 (a roster of 500), the plan P1 to P5, and the
ORACLE block: keep the readings the fleet plans on fresh, read the north
road from Atria to Yildun and the pirate record of its choke point, watch
Oakridge's neighbours, explore further out so the other divisions find
work, hunt on the way. P5 asks every Admiral to research the game online
and its role and write what it learned into its guidebook and knowledge
files. The Fleet Admiral's newest report
(`reports/2026-11-21_unity_cut-deposit-booked-sweep-writes-ahead-test-round-ends.md`)
ended the test round; the turn jobs run again since 23:37 CET (queue.log
ENT-200).

```
Ships: 30/30 at work, grounded: 0, lost: 0 (briefing 23:16 UTC; fleet.json at the turn check 23:19 UTC)
Credits: start 1,081,170 (briefing 23:16 UTC), end 1,067,012 (tool fleet, view=money, about 23:57 UTC), net -14,158 in about 41 minutes; one hull of 35,350 cr bought once after that read (data/fleet/onetime.json)
Output: 408 scout runs in 100.2 ship-hours (data/routes/runs.jsonl, the 4 hours to about 23:31 UTC); 17 raids and 9 pirates filed as observe lines; 2 requests answered
```

Steady money per hour (tool fleet, view=money, about 23:57 UTC): Intel
-20,195 cr, nearly all metered fuel (20,195); the fleet -10,599 over the
last hour, +49,125 over six hours and +12,282 over 24 hours. The
division earns no income of its own by design (ROSTER.md, one purse);
its census fuel is its cost of service. At the turn check of 23:19 UTC
every home reading stood under the hour (oldest Synchrony, 42 minutes),
and at 00:00 UTC the oldest home reading was Node Gamma at 43 minutes.

## Activities

**Apollo's request ENT-296: what wrecked our outpost (answered done,
requests.log ENT-310).** No census of ours had seen it, so I read the
game's own records. The faction's action log (get_action_log with the
faction id, 1,719 entries) dates the last fuel taken at the outpost to
2026-11-18 01:24 UTC and nothing there again until 2026-11-21 19:40 UTC,
with no combat entry. The live public battle list, category `npc`, holds
the raid: battle d324500d..., 2026-11-19 21:38:02 UTC, 19 ticks, 16 ships
of the Algol stronghold's crew led by Imperator Dross against the outpost
alone, 12,425 damage, the outpost destroyed. Category `pirate` holds
nothing there: a pirate reading misses every raid. The same list holds 17
raids on faction bases from 2026-11-12 to 2026-11-20, every one won by
the raiders; I filed all 17 as observe kind raid and told the Admirals
the crews near us (admirals.log ENT-077).

**North road and its choke point (ORACLE block).** Over 600 battles of
category pirate (2026-11-17 00:58 to 2026-11-21 23:21 UTC) and the 30
newest of category npc hold none on the road (Atria, Regor, Groombridge
34, Chalawan, Rasalhague, Yildun) or one lane off; 1,098 sightings rows of
ours there hold no pirate. The nearest strongholds are Gliese 581, 10
jumps from Atria, and Algol, 11 from Yildun (lanes table). Oakridge and
the three named sites stood on lists read within 180 minutes (SITES,
23:19 UTC).

**Zero's request ENT-283 (done, ENT-311).** All five fields stand read
after the request: Tiaki 20:49, Jadecove 20:59, Subra 22:13, Goldcrest
22:40 and Acubens 23:28 UTC.

**Readings where the fleet works.** The WORKED line found 11 systems
where Military hunts now read only every 480 minutes at 23:19 UTC, and 6
more at 00:00 UTC after Military moved again. All 17 moved onto
census-worked-far, now 70 systems with up to 10 ships (commits ad58a8ed,
b939472c). The far lists go to every 720 minutes, since no never-read
system is left (ROADS END). Readers now read census-frontier before
census-worked-far (template commit d092866a); the six scouts with a
survey scanner fly a far list first, so the far systems get surveyed;
the explorers keep their road, then census-worked-far.

**P5, the game and the role.** I read the game's exploration, explorer,
scanning and base-builder pages. The tier-1 Voidborn hulls need no
Piloting and fly at speed 3 or 4 against the starter's 1 (table hulls).
One reader bought a Qualia at Central Nexus for 35,000 cr plus 350 tax
(booked once), stance flee, released to @reader at 23:58 UTC: a test of
whether a faster hull cuts census minutes. I added the need
survey-scanner-i, 24 units, priority 3 (commit b353cbd3; queue.log
ENT-198). The intel gate read Errors 0 and the changelog still names
0.732.0 (1,909 releases), the version our digest holds.

## Problems

- **The frontier list stays over its cadence.** The oldest frontier read
  was 200 minutes at 23:19 and again at 00:00 UTC against 170 (FRESH,
  HALT). Cause: the lists at their cadences ask more reads than 30 scouts
  give (about 37 ships of reads asked, runs.jsonl against the lists),
  and census-frontier stood fourth in the readers' template. It now stands third; judged from its next reads.
- **Road and watch lists slipped.** At 00:00 UTC SITES read census-north
  over 180 minutes at Giausar (212) and Pinecross (199), census-south at
  Fomalhaut (207); the outpost watch's longest gap was 76 minutes against
  the hour, the home gaps' longest 62 (GAPS). Same cause; no route
  change but the order of the templates.
- **Three days unseen.** Our outpost fell at 21:38 UTC on 2026-11-19 and
  was read wrecked at 19:50 UTC on 2026-11-21 (errors.log ENT-112). No
  reading of mine looked at the game's battle record; I built
  `raid_record.py` for the turn skill so a raid on a base of ours prints
  HALT in my next turn without a request.
- **A ship without weapons in a plan with once-hunts.** The Qualia has no
  weapon slot; the list First holds once-hunts open to every ship. A
  hunt run on it would kill nothing; watched, not yet seen.
- **Turn time.** The hold on the test reader waited nine minutes for a
  census run to end (23:47 to 23:56 UTC); the turn had no way to take a
  ship the moment it was free but a polling script.
- No ship was lost or damaged; no reserve good was sold (RESERVE PASS).

## Plans

Inside orders ENT-059, my own choices:

- **The hull test.** Read the Qualia's census runs in runs.jsonl against
  the Threshold's on the same lists (minutes per run, systems a run). If
  speed 3 cuts a read by half or more, the next readers change hull as
  their wallets allow inside rule F12 (10 percent of the division's
  credits a turn for tests, about 106,000 cr now), scanner scouts last;
  if not, the test ends with the one ship.
- **Raids every turn.** `raid_record.py --hours 6` reads both
  categories each turn; a raid on a base of ours goes to Logistics the
  same turn, and every raid on any base is filed as kind raid, so the
  crews' habits near Atria and Yildun are read before the outpost is
  founded (P3).
- **Freshness.** Keep FRESH and WORKED at PASS: census-frontier before
  census-worked-far for the readers; every new place another division
  flies moves onto census-worked-far the turn it appears, and a place
  nobody flies any more goes back to its explorer list.
- **Surveys.** The six scanner scouts survey the far lists oldest first;
  their faint signatures and deposits decide whether the need
  survey-scanner-i is worth its 192 raw focusing crystals (catalog needs).
- **Far uranium.** Markeb, HD 20794, Khambalia and Mirfak, last read
  2026-11-17, come round on the far lists; Acubens and Stillwater still
  read 0 of 5,000 after the pause.
- **Strict classes (queue.log ENT-201).** Ten of the scouts' routes sell
  (workclass.py sales); once Trade names receivers, their sales become
  gifts to a trader before the switch goes on.
- **Not done this turn:** the probe step at Homam, the exploration
  missions (Strategic Readiness Assessment, Deep Space Cartography), and
  a Ship Scanner test; they stay in Planned of the plan file.

## Suggestions

- **A raid alert for every briefing (Unity's to decide).** The fleet's
  alerts could read the public battle list, category npc, every 30
  minutes and raise a line when a battle names a base of ours: two to
  four calls an hour, no game action. Reason: our outpost stood wrecked
  for three days. My turn script does it every four hours; a service
  would see it within the half hour.
- **A ship docked at every base before a pause (ENT-295, Unity's or
  Suggi's).** The game's base-builder guide says raiders count every ship
  of the faction in the base's system, docked ones too. Cost: one hull
  parked per base, no fuel while docked.
- **gate.py hold --when-free (Unity's script).** A hold that takes a ship
  the moment its run ends, instead of a polling loop in a member's
  shell. Cost: a few lines in gate.py.
- **The rules digest (Unity).** game/rules/11-public-data.md: the bulk
  feed's November battle file ended at 2026-11-15 04:22 UTC though built
  2026-11-21 04:10 UTC; the live list is the source for recent battles.

## Feedback

- **The briefing** (`hive.py briefing`) gave the orders, the requests,
  the plan with its `carries` column and the gate in one answer; it
  worked as built.
- **The tool fill** (`action=status`, `action=check`) read PASS at 23:22,
  23:58 and 23:59 UTC and listed every route closed to scouts by a
  claim, a danger flag or class; clear.
- **The tool plan** refused a template change while my route files were
  uncommitted ("game/routes holds a change that is not committed"): the
  gate worked and cost one commit. `plan.py planned --clear` with
  `--when` worked; without `--when` the date was folded into the text.
- **The tool needs** (`action=add`, `dry_run`) wrote and committed the
  need in one call; its covered percent and colours read clearly.
- **gate.py book_onetime** (new, Q75) booked the hull as one-time money
  in one call: the division's steady figure stays true.
- **The tool command** cut the faction group's help at about 3,000
  characters with no way to ask for more; `gate.py raw` with FULL=1, and
  the game's help URL, gave the whole list.
- **The tool hold** refused a busy pilot correctly; there is no way to
  wait for it (Suggestions).
- **observe.py** took two new kinds (raid, hull_test) without a change
  of any script; the store reads them as rows.
- **inbox.py's fix (ENT-306)** was not exercised: no install ran this
  turn, and the clone held other members' uncommitted files again at
  00:00 UTC (stats.py, station files), which my commits by path left
  alone.

## Learnings

From the learning capture of this turn:

- **The game keeps the record our census cannot.** A raid on a base is
  category `npc` in the public battle list, not `pirate`; every one of 17
  raids from 2026-11-12 to 11-20 destroyed its base, ours among them
  (the list, read 2026-11-21 between 23:20 and 23:35 UTC). Intel now
  reads both categories every turn by script and files each raid. Kept
  in the new knowledge file `knowledge/raids-on-bases.md`. For the
  fleet: a base is only as safe as the ships in its system, docked ones
  included (the game's guide); every reading names the categories it
  covered.
- **The lists outgrew the class.** The census of four hours took 100
  ship-hours of 30 scouts and still fell short on every list but
  census-east and census-south; at the minutes each read took, the lists
  as they stood asked about 37 ships (runs.jsonl, one row a system read,
  against systems and every_minutes of each list); the time goes into
  travel at speed 1. The fix is a
  faster hull, not a longer cadence; one test ship flies now. Kept in
  `knowledge/census-freshness.md` (How Many Scouts the Census Keeps
  Busy).
- **The explorer's kit is wider than our census uses.** The game's pages
  name survey missions, a Ship Scanner that counts ships at every place
  of a system in one call, and a faction intel pool; none tested yet.
  Unpromoted (LEARNINGS.md) until a test reads it.
- **Confirmed:** the WORKED line moves with Military every hour (17
  systems in 41 minutes), so the list of far work is kept by the line,
  not by hand; the north road showed no pirate in four days of the
  record.
- Repeated mistake checked: last turn's claim wider than its check did
  not recur; ENT-310 names what was not seen.

Skill: intel-turn changed -- a raid_record.py step (both battle categories, raids filed, OURS HALT)

## Cross-links

- `communications/orders.log` -- ENT-059, the orders in force.
- `communications/requests.log` -- ENT-296 and ENT-310 (the outpost's raid), ENT-283 and ENT-311 (Mining's fields).
- `communications/admirals.log` -- ENT-077 (raids on bases), ENT-079 (the Intel claim, releasing ENT-071).
- `communications/errors.log` -- ENT-112 (the outpost read wrecked).
- `game/routes/guidebook/intel/` -- card, routes, tests and lessons updated this turn.
- `game/routes/census-worked-far.json` -- 70 systems where the other divisions fly beyond the roads.
- `game/needs.tsv` -- the need survey-scanner-i.
- `reports/2026-11-21_oracle_after-the-pause-far-work-read-every-three-hours.md` -- my previous report.
- `reports/2026-11-21_unity_cut-deposit-booked-sweep-writes-ahead-test-round-ends.md` -- the Fleet Admiral's report in force.
