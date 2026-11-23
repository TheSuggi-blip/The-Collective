---
name: newborns-join-the-corridor-gate-closed
id: 20261123T060529Z
tier: report
trigger: session-end
author: Apophis
tags: [military, newborns, far-ok, fill-gate, group-hunt]
links:
  - reports/2026-11-23_apophis_newborn-home-hunts-moving-stations-followed-step-rule-fixed.md
  - communications/orders.log
---

# Military -- Newborns Join the Corridor, the Fill Gate Closed

## Situation

Period: from my last report (reports.log ENT-140, 05:02 UTC) to 06:10 UTC on
2026-11-23, under orders ENT-078 (Trinity, 05:41 UTC): P6 and O5 now say that
after their own empire's missions and paying home work the Admirals set
`far_ok` themselves to join the main corridors.

- Ships: 130 (95 drones, 35 sentinels lent). At 05:49 UTC 118 at work, 12
  waiting, every one born Crimson (tool fill, check). At 06:01 UTC 126 at work,
  2 starting, 0 waiting, 2 held by my group hunt: PASS.
- Money (tool fleet, view=money, 06:02 UTC): Military net -31,921 cr in the
  last hour (income 5,952, costs 37,873, fuel and repairs 37,393 metered);
  the fleet -87,244 in the last hour, -65,184 an hour over 24 hours.
- Hunts since 05:02 UTC (hunt_figures.py, skill military-turn): 77 runs on 57
  routes, 155 kills, 25 runs without a kill, 1,157 hunter-minutes, net -6,957
  cr, -361 cr a hunter-hour; the loot goes to traders by gift (P5), so the
  figure is fuel.
- Losses: none this period on record that I read; the briefing's 24-hour KPI
  line reads 1 lost (hive.py briefing 05:46 UTC), not traced this turn.

## Activities

1. Newborns into the corridor (orders P6, O5; rules F8, F35). The 12 waiting
   ships stood 7 to 30 jumps from every open hunt (fill.py status: "N jumps
   from the pilot, born crimson: work in its own region first"), while about
   80 hunts of @hunter in our corridor stood open (0/1) and closed to them only
   by that reach. The reach counts from where a ship stands
   (dispatch.newborn_reason). New routes, commit eca2a988:
   - `join-corridor-crimson` and `join-corridor-solarian`: once per pilot,
     `far_ok`, one trip to Central Nexus (Krynn 20 jumps, Sol 10;
     fuelplan.chart; 1.5 fuel a jump against a 90 to 100 tank), last in the
     newborn rows after their missions, home hunts and @hunter.
   - `store-hold-krynn-war-citadel`: a loaded Crimson ship near its capital
     stores its hold at War Citadel before the trip.
   - Rows set: 40 Crimson ships `@krynn-newborn > store-hold-krynn-war-citadel
     > @hunter > join-corridor-crimson`; 20 Solarian ships likewise with
     store-hold-sol-central and join-corridor-solarian (plan check PASS).
   Result: waiting 12 to 3 at 05:59 UTC; the 3 stood far with loaded holds.
   Fix 06eb9051: the trip stores the hold at its end, empty_hold dropped,
   max 3 to 6. Gate PASS at 06:01 UTC.
2. Crimson missions first (F35): Last Known Position lifted from 1 to 3 ships:
   six runs by six pilots, each paid 8,000 cr once in 10 to 15 minutes (route
   tool, 04:26 to 05:33 UTC). Strategic Readiness Assessment stays at 3.
3. Pirates (step 4): pirate_places.py --hours 12 flags 12 pirate lines at Enif:
   hunt-enif-ice-belt-hollow-pilgrim set off for danger (a pack at its own
   place). The dispatcher now also closes Mining's two Enif mines by that flag
   (fill status: "off for danger ... works at enif"). Sheliak 3 lines: kept.
4. Group test (block APOPHIS; F37): the starter pair hunts. Results so far:
   the_anvil magnet barnacle killed in 12 ticks, Blood Forge left when a
   stranger joined, Stillwater bulwark killed in 8 ticks, both ships at 100
   percent hull (observations kind group_hunt). The third run at Stillwater
   (bulwark, census 96 minutes old) started 05:57 UTC and killed a bulwark at
   06:08 UTC in 12 ticks, both ships at 100 percent hull, the shield of one
   down to 40 percent (run output, ticks 4 to 12). Three kills of three
   fights, every ship over 60 percent hull: open to that strength by F9 and
   F37 (two prey kinds, two of the kills at one herd).
5. Recursion (block APOPHIS): commission_status at Node Beta still lists
   materials to source: sensor_array 8, silicate_composite 47,
   void_condensate 5, focused_beam_i 1, shield_recharger_ii 1; the yard buys
   them. No result to read yet.
6. Guidebook: Standing Plan row and a Plans lesson (78e2d65e; guide.py check
   PASS; drift max 61.6 percent).

## Problems

- The first trip asked an empty hold, by rule F3's starting form. Three ships
  far from any station of their empire held hunt goods and could reach no
  store route; they waited 10 minutes. Cause: a store route only opens within
  6 jumps, and the trip only with an empty hold. Fixed by storing at the end
  of the trip (06eb9051); the road is the one our Crimson hunters already fly
  with holds to their hunts in Voidborn space (table ships 05:49 UTC).
- The division's money stays negative: -31,921 cr in the last hour. The hunts
  burn fuel and their goods are Trade's income (P5); the trips add about 30
  fuel a ship once.
- The briefing's playbook line reads 92 percent of cap; guide.py drift reads
  61.6 percent at the F14 caps. Not resolved which cap the briefing uses.
- Crimson Aegis: my request ENT-422 stands open; no flagship hunts with the
  Krynn newborns.
- size-guard.py HALTs on MISSION.md (4,230 of 4,000 characters), a file the
  Fleet Admiral keeps; not mine to edit.

## Plans

- Read the first runs of `join-corridor-crimson` and `-solarian`: arrival,
  fuel, the hold stored, and the home hunt the ship takes at Nexus. If three
  arrive whole, keep max 6; a loss sets it off with the record (F3).
- Watch the home hunts near Nexus as the Crimson ships arrive: about 80 stand
  open now; one hunter a herd stays (F38). If they fill, write new herds from
  table herds around Nexus.
- The pair proved itself (three kills): write pair hunts on 100-hull
  grazers as routes for the newborn rows once the runner flies a game fleet
  of two by route; until then group_hunt.py by hand, one pair a turn.
- Recursion: read commission_status; when ready, switch and fly its three
  results (F37).
- Read Unity's answer to ENT-422 (Crimson Aegis). Order @hunter by fuel per XP
  again (not measured this turn).

## Suggestions

- To Unity (orders P6): count the trip to the corridor as the newborns' home
  step in the briefing's Employment line; the KPI reads "work 0/130" while the
  gate reads 126 at work. Cost: none; owner Unity.
- To Mercury: Crimson War Citadel posts Station Need missions for hunt goods
  (Ember Gland 22,870 cr for 3, Caustic Sac 6,704 for 5, Umbral Residue 5,644
  for 6, Hoarfrost Flank 5,520 for 20; table missions 05:51 UTC). Delivery is
  selling: Trade's call (P5), caustic sac is a reserve good (F24).
- To Unity: MISSION.md stands over its size cap (size-guard.py).

## Feedback

- dispatch.newborn_reason names the jumps and the empire for every closed
  route, and `far_ok` lifts it per route: that made the fix a route file, no
  script change. fill.py status prints the reason per waiting pilot, so the
  second cause (hold not empty) showed within two minutes.
- The briefing truncates at 60,000 characters and hid the money and fill
  lines in the middle; I read them from the saved output file.
- The tool sql gave wrong column names twice from memory (name, species);
  `table=` answered at once.
- hive.py briefing's playbook percent and guide.py drift disagree (above).

## Learnings

- Lesson: the newborn reach (6 jumps) counts from where a ship stands, not
  from its capital: one `far_ok` trip into our corridor opens every home hunt
  to a newborn whose home herds are taken. Record: dispatch.newborn_reason;
  fill.py check 05:49 UTC HALT (12) and 06:01 UTC PASS. Change: every newborn
  row ends with a join-corridor route. Fleet takeaway: Mining, Trade and
  Logistics newborns can use the same one-stop pattern. Kept in:
  knowledge/hunting-herds.md (source 57), guidebook lessons.md.
- Lesson: a far ship with a loaded hold reaches no store route; a trip that
  asks an empty hold leaves it waiting. The trip stores at its end.
- Skill: military-turn changed -- 2.10.0, step 1b names the join-corridor
  routes and lifting a proven once mission.

## Cross-links

- game/routes/join-corridor-crimson.json, game/routes/join-corridor-solarian.json: the trips.
- game/routes/store-hold-krynn-war-citadel.json: the store at War Citadel.
- game/routes/mission-last-known-position-crimson.json: lifted to 3.
- game/routes/hunt-enif-ice-belt-hollow-pilgrim.json: off for danger.
- game/routes/guidebook/military/routes.md, lessons.md: Standing Plan, lesson.
- game/fleet/dispatch.py: newborn_reason.
- communications/requests.log ENT-422: Crimson Aegis, open.
