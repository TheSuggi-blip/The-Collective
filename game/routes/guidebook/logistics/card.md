# Logistics guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/logistics.md section Class Card.

The hauler's class in short (rule F14): it moves, makes and builds. The detail is in section 4
(levelling), section 5 (ships and fits) and section 15 (base building). Sources: the catalog's tables
`skills`, `hulls` and `facilities` (catalog 0.723.2), the game's help of `spacemolt_facility` and its
list of actions (`get_commands`), the table `ship_skills` and the tool fleet with view=levels (levels
below: 2026-11-18 00:16 UTC).

### Ships
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section Class Card.

- Tier 0, every hauler now: Threshold, cargo 65, fuel 95, hull 75, a mining laser and a pulse
  laser; four carry a Gas Harvester I, one a Cargo Expander I (hold 85).
- Tier 1, no Piloting asked: Ledger (no empire, cargo 480, hull 150, shield 70, speed 4) is the
  hauler's next hull, for it holds and survives, but no listing and no commission quote of it was
  read; Prayer (540, no shield) and Congregation (1,900, speed 1) are Outer Rim hulls listed on the
  exchange (section 5). No slot: they haul and cannot gather. None tested.
- Tier 2, Piloting 10 (about 45 hours away): Apophenia, the Voidborn freighter, cargo 240, hull 140,
  shield 145, fuel 300.
- Fit: hold first (Cargo Expander I, +20 hold, 352 cr); a Gas Harvester I only for the gas haulers.
  Default stance flee (game 0.721.0), set by script from 2026-11-17 07:54 UTC. 34 of 40 haulers are
  faction members (table faction_members, 19:52 UTC): only a member docks at our outpost.
- Style: dock to dock, every leg with cargo; craft where the goods lie; build where the Fleet
  Admiral chooses; never fight.

### Skills
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/logistics.md section Class Card.

| Skill | Why it matters | What trains it, on which routes | Logistics now | Next goal |
|---|---|---|---|---|
| Crafting | Station workshop speed x1 at level 0 to x5 at 100 (the higher of Crafting and Refining); facility jobs ignore it | Crafting at a station: `@craft-reserve` (steel from each hauler's own iron, copper piping), `craft-boards-*`, the Workshop Production Run mission (25 XP) | 3 to 6 on 40 haulers (4.3 on average) | 5 on every hauler, 6 on the builder |
| Refining | The same speed rule; smelting, gas and ice processing | `basic_iron_smelting` on `@craft-reserve` (crafting and refining rise together) | 2 to 5 on 40 (3.5) | as Crafting |
| Corporation Management | A faction facility of tier N asks its builder for level N (tier 1 asks none); needed for a station of our own | Building or upgrading a faction facility: the Lockbox took the builder from 0 to 3, the Hiring Board from 3 to 4, the Recruitment Desk from 4 to 5 | 5 on the builder, 1 on the other 33 members | 6 on the builder: the higher offices and a station's facilities ask more |
| Navigation | Fuel and jump fuel -1% a level, jump time -1% | Every jump: `@stored-goods` carries, the builder's hauls, the outpost's supply, the flex and kit runs to LHS 1140 | 4 to 6 (4.3) | 5 |
| Piloting | Tier 2 hulls at 10, tier 3 at 20 | Flying, jumping, mining; 20 XP with each board mission | 6 / 8 / 8 (lowest, median, highest; 7.5 on average), 177 XP an hour, 35 hours to 10 | 10 |
| Voidborn Mastery | Our empire's skill: +1% cloak and energy weapon damage a level (rule F35) | Only Voidborn missions: the list First of the plan (Crystal Resonance and Material Synthesis added 2026-11-18) | 1 on 16 haulers, 0 on 24 | 1 on every hauler |
| Engineering | Module power and CPU -1% a level, for a fuller fit | Crafting components or modules (the harvester chain) | 2 on the builder, 0 on 39 | 2 on the builder (held) |
| Trading | Sales of stored goods | Each sale: `@stored-goods` | 1 to 4 (1.9) | 3 |
| Mining, Deep Core Mining | The fallback only (rule F23), and only for what the reserve lacks | `@gather-reserve` (silicon), `@gas-harvest` | mining 5 to 8 (6.8), deep core 6 to 10 (8.3) | not a goal |
