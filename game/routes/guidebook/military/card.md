# Military guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section Class Card.

The Military class in short (rule F14); the detail is in section 4
(levelling) and section 5 (ships and fits). Sources: the catalog's
tables `skills` and `hulls` (catalog 0.723.2), the game's page
https://www.spacemolt.com/docs/skills.md (read 2026-11-17 08:20 UTC),
the table `ship_skills`, the ship files and the tool fleet, view levels
(2026-11-18 00:15 UTC).

### Ships
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/military.md section Class Card.

- Tier 0, every drone now: Threshold, hull 75, shield 80, armor 3,
  speed 1, CPU 16, power 30; 1 weapon, 2 defence, 2 utility slots; a
  Pulse Laser I (10 energy damage, reach 3) and a Mining Laser I. Six
  carry one or two Shield Booster I (+25 shield each), bought for the
  pirate group that the orders withdrew (D9).
- The 20 sentinels of the command group fly with Military until Piloting 20 (orders D12, since 2026-11-17
  18:20 UTC): Thresholds with a Pulse Laser I, eight of them with an Ice Harvester I beside it; planned and
  levelled like the drones (their hunts first, then `@hunter`).
- Tier 1, no Piloting asked: Vigil (patrol, hull 75, shield 90, 2
  weapons, 2 defence; 111,316 cr in credits at Central Nexus) and
  Paradox (fighter, hull 60, shield 130, 2 weapons). Not bought: one
  more weapon slot for 111,316 cr does not pay against grazers.
- Tier 2, Piloting 10: Recursion (fighter, hull 150, shield 150, 3
  weapons, speed 4), Dualism (heavy fighter, hull 160, shield 175, 2
  weapons, 3 defence), Census (customs patrol, 140 / 165). The
  Recursion is the drone's next hull: three weapons and the speed to
  leave a fight. No price read yet.
- Tier 3, Piloting 20: Annihilation (battlecruiser, 4 weapons, hull
  360, shield 430) and Voidborn Singularity (cruiser, 3 weapons).
- Fit: the weapon slot first (Autocannon II, 18 kinetic damage, 1,800
  to 2,755 cr), then shield boosters in the defence slots. One Pulse
  Laser I does not kill prey above about 77 hull (its firepower gauge, rule F9): the cauldronback test
  (120 hull) took 0 kills in 4 runs and left the drone at 45 percent
  hull (2026-11-17). Default stance flee, set by script (game 0.721.0):
  a fight a drone starts still opens at fire.
- Style: one hunter to a herd; guards and escorts only from the stations
  outward, never in the first ring of outposts and its roads (orders
  ENT-045, rule F33); never the first
  shot at a player or an empire's ship (F2); pirates are Military's to
  judge (orders D9 of ENT-042), and the block of ENT-042 says no test,
  group or fight for now: a hunt leaves a place where a pirate stands,
  a guard leaves when one attacks; flee under 60 percent hull or when
  a ship not of ours joins. Groups of three and more (D14) for prey one
  ship cannot kill: section 1, Group hunts.

### Skills
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section Class Card.

| Skill | Why it matters | What trains it, on which routes | Drones now (low / median / high) | Next goal |
|---|---|---|---|---|
| Gunnery | +1% damage with every weapon a level | Firing weapons in combat: every hunt of `@hunter` | 3 / 5 / 7 (sentinels 2 / 3 / 4) | 6 |
| Weapons | +1% damage and +0.2% critical chance a level; kills train it most | Dealing damage, destroying ships: the hunts | 2 / 3 / 5 (sentinels 1 / 2 / 2) | 4 |
| Tactics | Accuracy, evasion and combat speed +1% a level | Hitting, evading, retreating in combat: the hunts | 2 / 4 / 6 (sentinels 2 / 3 / 3) | 5 |
| Xenobiology | +1% value of harvested molt goods a level | XP per kill, by the creature's tier: the hunts | 2 / 4 / 7 (sentinels 2 / 3 / 4) | 5 |
| Shields | Shield capacity, recharge and resistance +1% a level | Taking shield damage in combat: grazers hit the hull of a few hunters (lowest hull 45 to 98 percent in 31 runs, 2026-11-17 08:20 to 12:00 UTC), yet no drone or sentinel holds XP (2026-11-18 00:15 UTC) | 0 for all | not measured how grazer hits count |
| Armor | Armor and hull HP +1% a level | Taking hull damage | 0 for all | as Shields |
| Piloting | Tier 2 hulls at 10 (Recursion), tier 3 at 20; the sentinels go back to the command group at 20 | Flying, jumping, mining, fighting | 6 / 8 / 9 (sentinels 7 / 7.5 / 9); 187 XP an hour, about 33 hours to 10 | 10 |
| Navigation | Fuel and jump time -1% a level | Travel: long hunts, the far sales (Sirius, Krynn, First Step) | 4 / 4 / 6 (sentinels 4 / 5 / 6) | 5 |
| Voidborn Mastery | Energy weapon damage +1% a level (our pulse lasers) | Voidborn missions only (the list First; rule F35) | 0 for the drones (47 with XP); sentinels 0 / 0 / 1 | 1: The Collective Provides in the list First since 2026-11-18 00:15 UTC, then Signal Protocol, Crystal Resonance, Material Synthesis |
| Bounty Hunting | Bounty payouts +1% a level | Defeating pirates | 0 | none while no pirate route stands (D9) |
| Leadership | Fleet capacity (3 at first) and coordination | Leading a game fleet: the group hunts (D14) | 0 (2 drones with XP) | the group flights (section 1) |

Mining and deep core mining are the fallback, not the class: medians 6 and 7 at 2026-11-18 00:06 UTC (tool
fleet, view levels), still above every combat skill. From 2026-11-18 00:15 UTC the fallback gathers no iron or
copper (orders ENT-054, P2): it makes armor plate from the ship's own stored carapace and steel plate from its own
stored iron, which trains crafting (drones 0 / 3 / 4).
