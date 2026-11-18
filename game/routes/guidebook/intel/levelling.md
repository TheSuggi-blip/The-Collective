# Intel guidebook -- Levelling (levelling.md)

### Levelling Guide
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/intel.md section 4.

Which skills a scout levels and on which work (rule F23): a scout scans
and explores; gathering ore is the fallback when nothing is due. The
readings are from `hive.py levels` and `data/fleet/ships/`.

The skills of the class, by the game's catalog (table `skills`, column
`training`, catalog 0.723.2, read 2026-11-17 07:20 UTC), with the route of
ours that trains each:

| Skill | How the game trains it (catalog) | What a level gives (catalog) | Our route that trains it | Scouts now (min / mean / max, table ship_skills, 07:20 UTC) |
|---|---|---|---|---|
| exploration | "Visit systems for the first time" | +1% survey power a level, added to scanning's; survey_system reveals a hidden place when the survey power reaches its reveal difficulty | every census and every circuit that takes a pilot to a system it has not been in, about 5 XP a system (2026-11-17 15:45 UTC); the pilot's second visit gives none | 2 / 2.1 / 3 |
| navigation | "Travel between systems and POIs" | -1% fuel, jump fuel and jump time a level | every census (a road read is 14 to 30 jumps out and back, a home read 2 to 6) | 3 / 3.8 / 5 |
| piloting | "Fly ships: travel, jump, mine, or fight"; a bonus for surveying new places or stale faction ore readings, completed missions and freight | +1% travel speed inside a system; piloting 10, 20, 30, 50 open hull tiers 2 to 5 | every route; the most by the census and the missions | 4 / 5.8 / 7 |
| scanning | "Query POI details or survey systems to reveal mineral deposits" | +1% scanner effectiveness a level | none yet: no scout holds a survey scanner, and get_poi in the census has given no scanning XP (0 on all 30); the test is fit-survey-scanner-central-nexus | 0 / 0 / 0 |
| deep core mining | "Mine with advanced equipment (power 3+), or reveal deep core deposits with survey_system" | +5% yield from hidden deep core deposits a level | today the gather fallback (Mining Laser I has power 5); for a scout, survey_system once a survey scanner is fitted | 3 / 6.0 / 8 |
| xenobiology, weapons, gunnery, tactics | a kill of a creature (by its tier); damage dealt; a weapon fired; hitting or evading | the value of molt goods; damage; accuracy and evasion | the five hunt routes of the plan (rule F16) | xenobiology 0 / 1.1 / 3 |
| stealth | "Activate cloaking devices or evade customs inspections" | cloak and scan evasion | none: no cloak fitted | not trained |

What our scouts farm: readings first (fields, herds, books, boards,
pilots, pirates) and caustic sac from the Amberfall chlorophages; ore only
on the fallback. The next fits of the class: Survey Scanner I (utility,
cpu 3, power 4, survey power 30; Central Nexus asked 4,892 cr, The
Experiment 4,911, books of 2026-11-17 07:14 to 07:18 UTC), Ship Scanner I
(utility; counts the ships at every place of a system and scans another
place; 1,481 cr at Central Nexus), and the consumable Mining Survey Probe
(+30 survey power for 10 ticks, 180 cr). A Threshold has two utility
slots and the mining laser takes one (catalog: hull threshold, cpu 16,
power 30). The next hull: tier 2 at piloting 10, 62 hours away at the
division's rate (fleet view=levels, 07:24 UTC).

| Kind of scout | Skill that matters | What raises it | What the next level opens | Template |
|---|---|---|---|---|
| Explorer | exploration, navigation, then piloting | a never-read system (exploration), jumps (navigation) | navigation 3 opens Signal Fragments (7,000 cr once, list First); piloting 10 opens the tier 2 hulls | @explorer |
| Reader | navigation, piloting; scanning once a survey scanner is fitted | every census: jumps flown, places read | piloting 10, 20, 30 and 50 open hull tiers 2 to 5 | @reader |
| Hunter | weapons, xenobiology | kills of grazers (rule F9) | not measured for a scout yet | own hunt route, then @reader |

Readings:

- 2026-11-17 07:24 UTC (`fleet` view=levels): 30 scouts, 36 hours played
  (median); piloting 4, 6 and 7 (lowest, median, highest), 143 piloting
  XP an hour since birth, 62 hours to piloting 10; median deep core
  mining 7 (160 XP an hour), mining 5 (86), navigation 4 (51), trading 2
  (7), exploration 2 (12). Against 03:23 UTC: navigation's median rose
  from 3 to 4 and deep core mining's from 6 to 7; exploration stayed at
  2, because the explorers' list held no never-read system from about
  04:33 UTC and 24 of 30 scouts were gathering at 07:17 UTC.

- 2026-11-17 03:23 UTC (`fleet` view=levels): 30 scouts, 32 hours played
  (median); piloting 3, 6 and 7 (lowest, median, highest), 141 piloting
  XP an hour since birth, 70 hours to piloting 10; median deep core
  mining 6 (139 XP an hour), mining 5 (73), navigation 3 (49), trading 2
  (9), exploration 2 (12). The division's strongest skill is still the
  fallback's (deep core mining), not a scout's: the scout runs that
  started from 2026-11-16 23:15 to 2026-11-17 03:20 UTC flew 49 hours of
  gathering (Hamal 43.7, the prism scatter 5.5) and 32 of census
  (`data/routes/runs.jsonl`).
- 2026-11-16 23:28 UTC (`hive.py levels`): 30 scouts, 28 hours played
  (median); piloting 2, 5 and 7 (lowest, median, highest), 137 piloting
  XP an hour since birth, 78 hours to piloting 10 at that rate; median
  navigation 3 (45 XP an hour), exploration 2 (12 XP an hour), mining 4
  (69), deep core mining 6 (126). Deep core mining and mining lead
  because gathering was the work most scouts flew; exploration rises
  slowest.
- The same hour (`data/fleet/ships/`): the ten scouts born on
  2026-11-16 stand at navigation 2 and piloting 2 or 3; of the twenty
  older ones, ten stand at navigation 4 or 5 and ten at 3.
- 2026-11-16 12:22 UTC: piloting 3, 5 and 5; 91 piloting XP an hour;
  131 hours to piloting 10. 2026-11-15 23:44 UTC: in ten minutes twenty
  scouts gained 55 exploration XP, 235 navigation XP and 456 piloting
  XP on census reads.
- First Hunt gives 50 weapons, 15 xenobiology and 20 piloting XP once.
