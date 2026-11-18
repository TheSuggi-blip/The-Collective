# Intel guidebook -- the Class Card (card.md)

### Ships
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/intel.md section Class Card.

- Tier 0, every scout today: the starter Threshold (cargo 65, fuel 95,
  hull 75, shield 80, two utility slots), its mining laser and pulse
  laser, the default stance flee on all 30 (set by script, 2026-11-17).
- Fit next: Survey Scanner I in the second utility slot: three scouts
  carry it (2026-11-17 23:20 UTC); Central Nexus now asks 11,000 cr for
  its last one and The Experiment 4,911 for 2 (books of about 23:20 UTC),
  so `fit-survey-scanner-central-nexus` (max_price 5,000) buys nothing
  and the three readers still on it take their next route. The game's
  help for survey_system: each extra scanner module adds 50% of the one
  before, and a survey probe or an anomaly detector adds its power. A
  survey reads every field of a system and its wildlife in one action and
  is the only census action that trains scanning; since census.py 7540393
  a ship with a scanner surveys every system it reads. 12 surveys beyond
  the border revealed no hidden deposit; two (Homam, The Telescope) found
  "1 faint signature(s) that your scanner cannot resolve": a Mining Survey
  Probe (+30 survey power for 10 ticks, 180 cr) or Survey Scanner II
  (about 23,000 cr in Solarian books) is the next step. Ship Scanner I
  after it.
- Next hull: tier 2 at piloting 10 (45 hours away at the division's rate,
  `fleet` view=levels, 2026-11-17 23:27 UTC); a tier-1 hull for a scout
  is not read yet.
- Style: fly light and empty beyond the border (rule F13), read and leave,
  never fire first (F2), hunt where a herd lies on the way what passes both
  gauges of rule F9 (firepower and toughness), and pirates only by orders D9.

### Skills
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/intel.md section Class Card.

In the order a scout levels them (catalog, table `skills`; levels from
the table `ship_skills`, 30 scouts, 2026-11-17 23:28 UTC, lowest / mean /
highest; at 19:38 UTC in brackets where it moved):

| Skill | Why it matters | What trains it, and our route | Now | Next goal |
|---|---|---|---|---|
| exploration | survey power (+1% a level); the class's own skill | the pilot's own first visit to a system, about 5 XP each, a system flown through counts too; every census list a scout has not flown trains it, so the explorers rotate between lists (census-north, census-south, census-far-1 to 5) | 3 / 3.07 / 4, two scouts at 4 (2 / 3.0 / 3) | median 4 |
| navigation | -1% fuel, jump fuel and jump time a level; Signal Fragments opens at 3 | every jump: every census | 5 / 5.33 / 6 (5 / 5.2 / 6) | median 6 |
| piloting | hull tiers 2 to 5 at 10, 20, 30, 50 | every route; missions pay piloting XP (280 to 480) | 6 / 7.13 / 8 (6 / 7.0 / 8) | 10, the tier 2 hulls |
| scanning | scanner effectiveness (+1% a level) | survey_system (census.py surveys with a scanner aboard since 7540393), 5 XP a survey; a link of the Voidborn chain paid 20 XP to 15 scouts; get_poi gives none | 0 / 0.14 / 1 (0 / 0.1 / 1); the three scanner scouts hold 60, 35 and 30 XP: 125 XP for 52 surveys of 46 systems (wildlife/history.jsonl `surveyed`, to 23:22 UTC), so not every survey pays 5 | which surveys pay: a pilot's first of a system or every one |
| xenobiology, weapons, gunnery | molt value, damage | the hunt routes of the plan | xenobiology 0 / 1.22 / 5, gunnery 0 / 1.41 / 4, weapons 0 / 1.0 / 3 | not set |
| deep core mining, mining | not the class's: the gather fallback | gathering when nothing is due | 4 / 6.4 / 8 | none |
