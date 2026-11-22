# Military guidebook -- Topic: pirates, guards and escorts (topic-pirates.md)

### Pirates
Status: proven. Updated: 2026-11-21. Evidence: https://game.spacemolt.com/api/battles read by pirate_record.py (2026-11-17); observations kind pirate; this entry's versions (hive.py docs game/routes/guidebook/military/topic-pirates.md --section pirates --history).

Pirates are Military's call (rule F27, by F9: a test first, the cost
weighed; a crew keeps a grudge). Until a pirate route stands every ship
leaves or docks, and the dispatcher closes work where one was seen in six
hours.

- Where: the nearest stronghold is Gliese 581, 7 jumps out, one lane to
  GSC-0016. Most pirate battles near us: Gliese 876, Felis, GSC-0021,
  Thornhaven, Biham, Coldwater. The orders watch a pack at Merak.
- What: a lone scout (Flinch, Breach Scout, Sentinel, Probe) dies after 95
  to 167 damage; the elite Ironhold after 358 to 408. Pairs and packs fight
  together: Blockade and Ironhold killed a player ship in one tick with 156
  damage; packs of six to ten (Nyx at Violethall, Dross at Hollowcrest,
  Korr at GSC-0021) weigh 700 to 1,400 hull: beyond any side we field.
- Who hunts them: the combat drones of BUSY won most battles near us and
  never fired at ours.
- Read by script each turn: `pirate_record.py --write` and
  `pirate_places.py` (skill military-turn).

### Raids on bases
Status: proven. Updated: 2026-11-22. Evidence: spacemolt.com/docs/combat and /docs/guides/pirate-hunter (read 2026-11-22 00:35 UTC); observations kind raid (Intel) and pirate (pirate_record.py, categories pirate and npc); admirals.log ENT-077, ENT-082.

- The game files raids on bases under category `npc`, not `pirate`:
  `pirate_record.py` reads both since 2026-11-22.
- A raid on a faction base calls in the faction: every ship of ours
  undocked anywhere in that system joins the base's side. A wildlife hunt
  calls in nobody; a fight with one pirate brings its whole stronghold in
  the system.
- A raid fleet is 4 to 12 hulls with salvagers and haulers; it sits a few
  minutes in each system on its road and gives up after about three hours
  on target. Its chatter carries seven jumps in three stages over about an
  hour: rumour, target named, imminent.
- Kill the haulers first: they carry the ammunition, and a raid without
  it goes home. A crew mauled on the road turns back, and a stronghold
  that loses several ships in one system sends its next raids elsewhere.
- Our outpost fell in 19 ticks to 16 raiders (observations kind raid):
  far beyond a side of starters. Military meets a raid only with a side
  its tests size; until then the answer is to dock or leave.

### The pirate test
Status: proven. Updated: 2026-11-21. Evidence: pirate_test.py log 2026-11-17 00:37 to 00:57 UTC; data/fleet/ships/.

One drone (Pulse Laser I, two Shield Booster I: hull 75, shield 130)
attacked Flinch (scout, hull 85, shield 30) alone at Felis Frost Ring on
2026-11-17 00:49 UTC. In 4 ticks in reach it took the pirate's shield from
100 to 20 percent (about 6 a tick) and lost about 15 a tick of its own
shield. At tick 6 a Breach Scout joined: the drone fled by rule (13 ticks
at speed 1 against pursuers of speed 5 and 6), docked at 100 percent hull.
Cost 6,473 cr, 5,969 of it the boosters. No kill, no bounty.
`pirate_test.py` (skill military-turn) attacks only a lone pirate of its
weak list, never re-attacks one already fought (that summons the
stronghold's combat pirates), flees by F2.

### What a side takes against pirates
Status: test. Updated: 2026-11-21. Evidence: the pirate test above; tests.md (Group hunts, Weapon fits).

An estimate, not measured: one starter deals about 6 a tick to a scout
and takes about 15, so alone it needs some 15 ticks while help comes in 6.
Five in reach would kill a scout in about 4 ticks. A weapon of 18 or 28
damage changes this sum: the pirate group waits for the weapon test and a
group that kills a creature first. The Pirate Bounty (2,000 cr, 20 weapons
XP) is flown only with a pirate route.

### Guards and escorts
Status: proven. Updated: 2026-11-21. Evidence: guard.py; guard runs in table runs 2026-11-16 to 2026-11-17; requests.log ENT-217, ENT-226, ENT-248; the retired routes.md entry Guard (hive.py guide military --retired).

- `guard.py` keeps one drone at the place of a guarded mine or hunt route
  while a ship of ours flies it; it never fires, looks once a minute (who
  stands there, pirates), leaves under 60 percent hull or in a fight, and
  docks. One guard to a place: its look lists every pilot there.
- `guard.py --follow <pilot>` is the escort: it reads the pilot's place
  once a minute and jumps after it; it trails a moving ship by one jump and
  keeps the long stops (a buy, a founding).
- What a guard gives: the minute-by-minute reading of who comes and the
  first warning, at -30 to -200 cr a run. It is no match for a pirate pack
  and holds no walls.
- Orders ENT-045 and rule F33: no guard or escort in the first ring of
  outposts and its roads; `@guard` waits for a station of ours beyond it.
