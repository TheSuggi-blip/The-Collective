# Intel guidebook -- Levelling (levelling.md)

### What trains a scout
Status: proven. Updated: 2026-11-21. Evidence: catalog table skills (column training, 0.723.2); data/fleet/ships/ against data/routes/runs.jsonl (2026-11-17 15:19 to 15:45 UTC).

- Exploration: "Visit systems for the first time". It is the pilot's own
  first visit, a system flown through included, about 5 XP each, whoever
  read it first. A list a scout has not flown still trains it: rotate
  scouts between lists (the visits per scout and list: runs.jsonl,
  `system` per pilot).
- Navigation: every jump. A road or far read is 14 to 60 jumps out and
  back, a home read 2 to 6.
- Piloting: every route; missions pay 280 to 480 XP; tier 2 at 10.
- Scanning: survey_system only, 5 XP for a survey (not every survey pays:
  125 XP for 52 surveys on 2026-11-17); get_poi gives none.
- Xenobiology, Weapons, Gunnery: kills and shots on the hunt routes.
- Deep Core Mining and Mining rise on the gather fallback: they are not
  the class's, so gathering is the last resort, never the plan.

### Kinds of scout
Status: proven. Updated: 2026-11-21. Evidence: game/routes/templates/intel.json; the plan file (tool plan, show).

| Kind | About | Skills that matter | Work |
|---|---|---|---|
| Explorer | 10 | exploration, navigation | a road list of its own, then census-worked-far, then a far list it has flown least, then @explorer |
| Reader | 20 | navigation, piloting, scanning | the list First (home census), then @reader: the outpost watch, the places our routes use near and far, the frontier, the roads |
| Hunter | a reader with a hunt first | weapons, xenobiology | its own hunt route, one hunter a herd, then @reader |

### Readings of the levels
Status: proven. Updated: 2026-11-21. Evidence: hive.py levels Oracle (2026-11-21 19:48 UTC).

The levels are read by call, never copied here: `hive.py levels Oracle`
(the tool fleet, view=levels). At 2026-11-21 19:48 UTC it printed
Piloting 6 / 8 / 8 and 42 hours to Piloting 10 at the class's rate; the
fallback's skills (deep core mining, mining) still stand above the
class's own, so each turn moves scouts from gathering to reads.
