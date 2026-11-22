# Logistics guidebook -- Topic: bases (topic-bases.md)

### The Fleet's Storage Home and the Faction Lockbox
Status: proven. Updated: 2026-11-21. Evidence: books of 2026-11-15 21:26 UTC; orders.log ENT-007; catalog 0.717.0 (faction_lockbox); the Lockbox at The Experiment, 2026-11-17 07:52 to 09:58 UTC (queue.log ENT-159).

- Central Nexus is every pilot's home and respawn base and the dock of `park`: a ship waiting there crafts from its own storage at the free workshop; the deepest bids of our inner stations; one jump from Node Beta, which sells fuel 2 cr cheaper. Stored ore stays where it lies: moving it costs fuel (ENT-007).
- A Faction Lockbox: 200,000 cr, 200 steel plate, 50 circuit boards, build time 50, 100,000 units an item type; faction storage comes first at every station. Ours stand at Node Beta (from the builder's own storage, 2026-11-17 05:38 UTC) and The Experiment.
- The Experiment's: three donors gave 200 plate and 50 boards into the builder's storage there (catch.py, stage.py, one unit first); holdfor.py held the builder docked until the Fleet Admiral built it (fee from its wallet: the treasury held less; Corporation Management 0 to 3).

### Base Building: the Builder's Work (orders.log ENT-031)
Status: proven. Updated: 2026-11-21. Evidence: rules F16, F33; orders.log ENT-056 (block APOLLO); errors.log ENT-086; build.py 2026-11-17 12:19 to 20:25 UTC.

Logistics is the fleet's base builder (rule F16): the Fleet Admiral chooses each site and allocates its credits and materials (rule F33); the build, its supply and its upkeep are ours. Now (ENT-059): Atria once GSC-0044 runs by itself (it does since 2026-11-21 23:48 UTC); the Recruitment Center when the purse holds its fee; the buildings G5 asks stand in the needs register.
- `build.py --treasury-ok` is her word that the TREASURY pays: it stops when the treasury holds less than the fee, as the game would take it all from the wallet. A wallet fee is booked once.
- The goods go into the faction store first (`deposit` target faction, source storage, one unit first, no hold needed).

### What the game says
Status: proven. Updated: 2026-11-21. Evidence: help of spacemolt_facility, get_commands, game/rules/09-factions.md, governance/empire.md section 5, base_plan (2026-11-17 07:58 UTC); builds of 09:45, 12:19 UTC. "Read": not flown.

- `spacemolt_facility` action `faction_build` (or `faction_upgrade` with the facility_id, for an office that `upgrades_from` another), docked, permission manage_facilities; materials from the faction store there, the cargo backfills (read). Tier N asks Corporation Management N, tier 1 none (read).
- The fee comes from the treasury whenever it holds it, else the wallet; the treasury pays the rent, so a build waits for the Fleet Admiral's word (ENT-086). Rent at a station not ours: every 100 ticks (about 17 min), paused while built; unpaid, the facility stops, storage stays.
- An outpost: `deploy_outpost`, an Outpost Kit (30 hold) in an undocked ship's cargo in a lawless system without a station, manage_bases, 100,000 cr (`base_cost`); eight per faction; storage and a fuel bunker, members only, no rent (read). `dismantle_outpost` packs it back (fee lost, storage empty).
- A station: `found_station` with a Station Core, 5,000,000 cr, five per faction, one per system; its facilities draw maintenance from faction storage and go offline undersupplied (each: `facility types facility_type=<id>`, refused on a run).
- A kit made: `assemble_outpost_kit` (assembler level 2: 600,000 cr, 800 plate, 300 boards, 120 reinforced frames, 40 control nodes).

### The first outpost as routes
Status: proven. Updated: 2026-11-21. Evidence: found.py 2026-11-17 16:36 UTC; outpost.py 20:26 to 21:17 UTC; RESULT line 2026-11-18 00:32 UTC; requests.log ENT-227, ENT-251, ENT-281.

- CLTV Outpost GSC-0044 (base `443f0c5b2a1fbbcea95d13b76a797fe9`), beside GSC-0044 Belt, 3 jumps from The Experiment: founded 2026-11-17 16:36 UTC by found.py; kit 148,663 cr at Ironlight Crossroads, fee 100,000 from the treasury (ENT-227). It came with a Faction Lockbox and a Faction Fuel Bunker (50,000).
- Only members dock; no personal storage, workshop or market. Fuel cells deposited are items; `deposit` item_id fuel, target faction moves tank fuel into the reserve, and `refuel` there draws it for 0 cr. A cell burnt into less room than 20 loses the rest.
- So the bunker is filled from tanks: a cell gives 20 fuel for about 100 cr, about 5 cr a unit, against 12 to 15 for station fuel.
- `supply-bunker-gsc-0044` buys 65 cells at The Experiment (102 cr or less with the tax), docks with `refuel: false`; its `bunker` step (keep 30) burns whole cells and deposits the tank above 30: +1,361 fuel, -6,565 cr, 19.6 min. Member haulers only. Three runs (`once`, `max_pilots` 3); ENT-281 offers `requires.reserve` (below 5,000) in their place.

### Keeping a base: raids and its repair stock
Status: proven. Updated: 2026-11-22. Evidence: the game's base-builder guide (read 2026-11-22 00:00 UTC); requests.log ENT-301, ENT-310; faction_owned 2026-11-21 23:48 UTC; routes supply-repair-gsc-0044-plate, -boards; needs gsc-0044-repair-plate, -boards.

- Pirate strongholds raid the faction bases of their region: GSC-0044 was wrecked 2026-11-19 by a crew of 16, and 17 raids from 11-12 to 11-20 wrecked every base they hit (ENT-310).
- A wrecked base repairs itself: every cycle it starts each repair its faction store there can pay, the fuel chain first; a repair costs 30% of the build's materials (GSC-0044: 180 plate, 45 boards, delivered by route; both facilities ready 2026-11-21 23:48 UTC). No command, no credits.
- Raiders count the guns and every ship of the faction in the system, docked or not; a stronghold that loses ships there skips it for days. Guns cost millions; the guide's cheap way: eat a raid, pay the bill.
- Our keeping (Apollo, ENT-301): each base's repair stock stands in its faction store (a need and a gated route), our ships work in its system while the fleet plays, and at a pause ships end docked there.

### The Recruitment Desk (orders.log ENT-037, block APOLLO (2))
Status: proven. Updated: 2026-11-21. Evidence: build.py 2026-11-17 12:19 and 20:25 UTC; table faction 20:35 UTC; orders.log ENT-036, ENT-056; requests.log ENT-242.

- The Hiring Board at Node Beta (ENT-036): build.py in a catch.py row, 6.4 minutes: 75 plate and 25 boards into the faction store, `faction_build hiring_board`; 75,000 cr from the treasury (82,999 -> 7,723), the wallet unchanged; cap 50, rent 26 cr a cycle; Corporation Management 3 to 4.
- The Recruitment Desk upgrades it (level 2, cap 100, 300,000 cr, 100 boards, 200 plate): `build.py --upgrade`. Built 20:25 UTC on the Fleet Admiral's word (ENT-242): a hauler gave the builder 85 plate, `waitstore.py` saw 200 and 100; the treasury fell 363,931 -> 63,931; active, limit 100, by 20:35 UTC; Corporation Management 4 to 5.
- Rent: faction_owned prints it (242 cr a cycle for all five, 2026-11-21 23:48 UTC); none at our own outpost.
- Next, the Recruitment Center (cap 200): 2,000,000 cr, 500 boards, 1,000 plate, 300 flex polymer, Corporation Management 3; when the purse holds its fee (ENT-056). Its flex: `buy-flex-ironlight-to-node-beta`.

### The Atria outpost, planned (orders.log ENT-052, P4 (b) and block APOLLO (2))
Status: test. Updated: 2026-11-22. Evidence: tables lanes, fields and books, 2026-11-17 23:35 to 2026-11-18 00:40 UTC; admirals.log ENT-063; requests.log ENT-268, ENT-272; orders.log ENT-059; need atria-outpost-kit.

Atria, the north outpost (the Fleet Admiral's choice), is founded once GSC-0044 runs by itself (ENT-056) on her allocation (ENT-268).
- The kit: `outpost-kit-ironlight-to-node-beta`, one member hauler with an empty hold to Ironlight Crossroads (6 jumps from Node Beta), 1 kit at 150,150 cr or less with the tax, stored at Node Beta. Off until the allocation is in the builder's wallet.
- The founding: found.py from Node Beta by GSC-0027, GSC-0050, Brachium, GSC-0049, Acrab, Atria (6 jumps), at the place she names (proposed: Atria Belt); 100,000 cr, the treasury first.
- Its bunker: cells from Central Nexus (7 jumps), a route like `supply-bunker-gsc-0044`.
- The place: Atria Belt aluminum and gold; Ice Fields water, nitrogen, deuterium; Emission Nebula argon, neon, hydrogen (table fields). Nearest station with fuel and a market: 6 jumps (ENT-063).
