# Logistics guidebook -- Topic: bases (topic-bases.md)

### The Fleet's Storage Home and the Faction Lockbox
Status: proven. Updated: 2026-11-15. Evidence: migrated from guidebook/logistics.md section 8.

Central Nexus, for everything the fleet keeps from here on:

- Every pilot's home and respawn base, and the dock of the route
  `park`: a ship waiting there can craft from its own storage at the
  workshop for free (section 7), and pays no fuel to reach its goods.
- The deepest list of bids of our inner stations: 440 items with a
  bid in the 21:26 UTC book (Node Beta 88, Node Alpha 45, Node Gamma
  43, Synchrony Hub 49; The Experiment 664, but three jumps out and on
  the border).
- One jump from Node Beta, where half of the stored ore lies: 48 cr a
  round trip if a use for that ore appears.
- Against it: Node Beta sells fuel 2 cr cheaper and sits one jump from
  the Acubens and GSC-0027 fields.

A Faction Lockbox, the first faction storage (catalog 0.717.0, facility
`faction_lockbox`): 200,000 cr, 200 steel plate and 50 circuit boards,
build time 50, labor 50, 100,000 units per item type. What we store
covers part of it (`ledger.py show all`, 2026-11-15 23:21 UTC):

- Steel: 2,000 iron ore make 200 plate at the free workshop; Logistics
  stores 11,671 iron ore, and one hauler held up to 1,122 at Node Beta.
  Bought, plate costs 18 cr a unit with depth at five stations: 3,600 cr.
- Circuits: none in Logistics storage. Three miners store 47 silicon
  ore and 113 energy crystal at Central Nexus: about 46 boards by
  `fabricate_circuit_boards`, free at the workshop (quote, section 7).
  Bought, 50 boards cost about 23,700 cr at the best asks of four
  stations, 25,144 cr at Central Nexus alone (`data/market/`, 23:39 UTC).
- The goods go to the builder by a deposit to that player (section 7).
  Who builds it and where is the Fleet Admiral's and Suggi's (orders
  F11); this is Logistics' advice.

The ore that lies at Node Beta and Synchrony Hub stays there: moving it
costs fuel and nothing buys it (orders.log ENT-007, block APOLLO).

### Base Building: the Builder's Work (orders.log ENT-031)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 15.

Logistics is the fleet's base builder from 2026-11-17 (rule F16): the Fleet Admiral chooses each site
and allocates its credits and materials (rule F33); the build, its supply and its upkeep are ours.

### What the game says
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 15.1.

Read 2026-11-17 07:58 UTC: the help of `spacemolt_facility` and the game's list of actions
(`get_commands`, 318); `game/rules/09-factions.md`; `governance/empire.md`, section 5; the tool
base_plan. A line marked "read" was not flown by us.

- A faction facility: `spacemolt_facility facility` with `action` `faction_build` and
  `facility_type`, docked at the station, permission manage_facilities. Faction storage (the
  Lockbox) comes first at every station. The materials come from the faction's store there (or a
  named Storage Extension bucket); the ship's cargo backfills a shortfall (read). The first Lockbox,
  at Node Beta, was built from the builder's own storage there (the Fleet Admiral, 2026-11-17 05:38
  UTC). A facility of tier N asks its builder for Corporation Management N; tier 1 asks none (read).
  The game's help names only the faction store and the cargo, so `build.py` moves the materials from the
  builder's own storage into the faction store first (2026-11-17 12:19 UTC, section 15.4).
- The fee: a faction build takes it from the treasury when the treasury holds it, else from the
  builder's wallet, as two builds show: the Lockbox at The Experiment from the wallet (200,000 cr, the
  treasury held 44,034, 09:45 UTC), the Hiring Board from the treasury (75,000 cr, the treasury fell
  from 82,999 to 7,723 and the wallet did not move, 12:19 UTC). The help of `found_station` and
  `deploy_outpost` says "faction treasury first, then your wallet". The treasury pays the rent, so a
  build waits for the Fleet Admiral's word whenever the treasury holds the fee (errors.log ENT-086).
- Rent at a station that is not ours: every 100 ticks (about 17 minutes), from the treasury: the
  Lockbox 69 cr a cycle, 5,962 cr a day (`governance/empire.md`, section 5). Paused while it is
  built; unpaid, the facility stops but storage stays reachable. None at our own station or outpost.
- An outpost: `spacemolt_facility deploy_outpost` (in the action list; its parameters are not in
  the help text): an Outpost Kit (30 units of hold) in the cargo of an undocked ship at a place of a
  lawless system without a station, permission manage_bases, a fee of 100,000 cr (the treasury
  first, then the wallet: `base_cost`). Eight per faction, any number per system. It comes with
  faction storage and a fuel bunker, serves members only, pays no rent and draws no maintenance;
  fuel deposited in its bunker refuels our ships free (read). `dismantle_outpost`, docked there,
  packs it back into a kit; the fee is lost and its storage must be empty first.
- A station of our own: `found_station` with a Station Core in the cargo, 5,000,000 cr, five per
  faction, one per system; then faction storage, power, life support and services by
  `faction_build`. Every service and infrastructure facility draws maintenance from faction storage
  each cycle and goes offline when undersupplied (help text). What each draws: not read; the card
  `facility types facility_type=<id>` answers it and is refused to a pilot on a run.
- The kit made by us: `assemble_outpost_kit` in an outpost frame assembler (level 2, 600,000 cr,
  800 steel plate, 300 circuit boards, 120 reinforced frames, 40 control nodes: base_plan, 07:54
  UTC). Bought: 74,010 cr at Ironlight Crossroads in LHS 1140, 2 listed (book of 07:55 UTC). The
  first kit is bought.

### The Lockbox at The Experiment (orders P5 and block APOLLO (2))
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 15.2.

The builder is a hauler with crafting 4 and engineering 2, which made the boards. It carries the
Lockbox's goods into its own storage at The Experiment Research Station and waits there, docked and
held by my hand, until the Fleet Admiral takes it at 09:30 UTC (`holdfor.py` of the skill
logistics-stock: it keeps the hold fresh, stops the moment another hand or a runner takes the ship,
and lets go at 11:30 UTC). Loads, by `catch.py` and `stage.py` at the end of each pilot's gather run
(2026-11-17 from 07:52 UTC): the builder 45 boards and 20 plate; three donors 64, 65 and 51 plate and
1 board from Node Beta; one donor 4 boards from Central Nexus; each donor gives into the builder's
storage at The Experiment, one unit first. Done 08:41 UTC: the builder's storage there read 200 steel
plate and 50 circuit boards (the game's storage view); each donor took 6.5 to 10.1 minutes from the
end of its run, 0 cr but fuel, no run cut. A deposit into the storage of a pilot that is not at the
station landed (08:22 UTC). Built by the Fleet Admiral's hand at 09:45 UTC, after the builder joined
the faction with the role Builder (manage_facilities, manage_bases): the 200 plate and 50 boards came
out of the builder's own storage, the fee of 200,000 cr out of its wallet; active at 09:58 UTC; the
builder's Corporation Management went from 0 to 3 (queue.log ENT-159).

### The first outpost as routes
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/logistics.md section 15.3.

Founded 2026-11-17 16:36:45 UTC by `found.py` at the end of the kit's second run (log of the catch row):
CLTV Outpost GSC-0044, base `443f0c5b2a1fbbcea95d13b76a797fe9`, its own place `da9de8c360c46ffee15dee4e7d1b8476`
beside GSC-0044 Belt; the fee of 100,000 cr from the treasury (205,263 -> 105,263), the builder's wallet
unchanged; the kit left the hold. It came with a Faction Lockbox and a Faction Fuel Bunker (table
faction_facilities, rent 0). The kit's run and the founding: 148,663 cr for the kit (booked once), about
40 minutes from the second run's start to the deploy.

What a member hauler found there (outpost.py of the skill logistics-stock, 2026-11-17 20:26 to 20:28 UTC,
one hauler with 20 fuel cells bought at The Experiment at 100 cr, 4 jumps out):

| Step | What the game showed |
|---|---|
| dock | a member docks (the outpost serves members only) |
| own storage | refused: "That station does not offer storage" (no personal storage at an outpost) |
| faction storage | items: none; `faction_fuel_capacity` 50,000; the treasury is shown here as everywhere |
| `refuel` item_id fuel_cell at 91 of 95 | tank 91 -> 95, one cell gone: a cell burnt into less room than 20 loses the rest |
| `deposit` 1, then 18 fuel cells, target faction, source cargo | the store read 1, then 19 fuel cells: items, not bunker fuel |
| `deposit` item_id fuel, quantity 5, target faction | tank 95 -> 90, `faction_fuel_reserve` 0 -> 5: the bunker takes fuel from the tank |
| `refuel` | tank 90 -> 95 for 0 cr: drawn from the reserve |

So the bunker is filled from tanks. A fuel cell costs 100 cr for 20 fuel (5.05 cr a unit with the tax)
where station fuel costs 12 to 15 cr a unit all-in (census files, 2026-11-17 20:00 UTC): a hauler that
burns cells into its tank in steps of 20 and deposits the tank into the reserve fills the bunker at
about 5 cr a unit. A circuit stop unloads into the faction storage with `store_faction` (route_run.py,
commit 6d69c52). Mine routes still store into personal storage only.

The first bunker fill (2026-11-17, one member hauler, `outpost.py --bunker 15`): 65 cells bought at The
Experiment at 101 cr with the tax (6,565 cr, one unit first, 20:39 UTC); 4 jumps; docked at the outpost
20:44 to 21:17 UTC burning four cells at a time into the tank and depositing the tank above 15: 1,292 fuel
from 64 cells into the reserve, which read 1,276 of 50,000 after (21 fewer than 5 + 1,292: drawn by a
member's refuel there, likely the mine run that took the pilot at 21:10, not verified). About 5.1 cr a
unit of reserve; 41 minutes from catch to the end, about 1,890 fuel a ship-hour, slow because each burn
and each deposit is one call of 11 s. The dispatcher took the pilot at the 31st minute because the
script did not refresh its hold (errors.log ENT-100; fixed in outpost.py).

The bunker as a route (2026-11-18 00:12 UTC, requests.log ENT-251): `supply-bunker-gsc-0044` buys 65 fuel cells at The
Experiment (102 cr or less with the tax), docks at the outpost without its fuel (`refuel: false`) and runs the stop step
`bunker` with keep 30: one `refuel` call with item_id fuel_cell burns as many whole cells as the tank has room for (its
room / 20), one `deposit` puts the tank above 30 into the reserve, until no cell is left. First RESULT line (2026-11-18
00:32 UTC): 2 of 2 stops in 19.6 minutes, +1,361 fuel from 65 cells, reserve 2,602 after, -6,565 cr, about 4.8 cr a
unit of reserve; three cells burnt a cycle of about 40 seconds (tank 30 to 90). A refused deposit ends the step; the row notes the fuel moved and
the reserve read after (`view` target faction). The same burn on the road is `burn_cells: true`. Only members dock at
the outpost, so the route stands only in the rows of member haulers (table faction_members: haulers 1 to 34). No gate
reads the reserve yet: the route is a budget of three runs (`once`, `max_pilots` 3), raised each turn by what the
reserve's draw asks (the gate is asked, requests.log ENT-266). The draw so far: 1,276 at 21:17 UTC, 1,258 at 23:52 UTC,
with a seated miner's two refuels between; the cell asks 1,850 at Central Nexus and 3,724 at The Experiment (00:00 UTC
books), 1,856 and 3,733 at 21:34 UTC: no restock read.

The plan of 08:06 UTC, as it stood before the founding:

The site is GSC-0044 (the Fleet Admiral, 2026-11-17 09:59 UTC; `game/map/sites.tsv`). The kit's
price doubled before it was bought: Ironlight Crossroads asks 148,663 cr for its one kit since
10:02 UTC (book read again 11:23 UTC), where two stood at 74,010 at 07:55 UTC; the catalog's base
value of a kit is 150,000 cr. The Fleet Admiral gave her word at 13:49 UTC (requests.log ENT-227): the
kit at up to 150,000 cr, the founding fee from the treasury (`--treasury-ok` for this site). The route
went on at 15:55 UTC with `min_credits` 155,000 and `max_pilots` 1, so only the builder flies it, and
stands first in the builder's own routes. Its first run (16:04 UTC) bought nothing: a route's `max_price`
counts the buyer's 1% tax (route_run.py, `offer`), and 148,663 x 1.01 = 150,150 is over 150,000; the
limit is 150,150 from 16:08 UTC, the kit's price itself inside the allocation. No pirate on our record
on the road or at the site (data/intel/sightings.jsonl and observations kind pirate, 15:54 UTC); a guard
cannot follow a circuit yet. The founding is `found.py` of the skill logistics-stock, run by `catch.py`
at the end of the kit's run: base_cost read docked, the kit withdrawn, the flight to GSC-0044 Belt
(goals navigate-to-system and go-to-poi), base_cost read there, `deploy_outpost` with a name (the api's
`build_outpost(name)`; the help names no parameter), the kit's leaving the hold as the proof, treasury
and wallet read before and after; a kit still aboard goes back into storage at The Experiment. What
follows is the plan of 08:06 UTC.

The site was the Fleet Admiral's to choose. Mining and Intel name Garnet (admirals.log ENT-018,
ENT-021), two jumps beyond The Experiment through Achernar: by the table systems that is 2 systems
beyond our space (Garnet 5 jumps from home, our border 3), where rule F33 asks 3 or 4. At 3 or 4
beyond: GSC-0044 (Mining's earlier choice, reports.log ENT-057) and Atlas, 3 jumps from The
Experiment each; Felis, Intercrus, Botein and Acrux, 4 to 6. Distances (table lanes): Node Beta to
LHS 1140 6 jumps; LHS 1140 to The Experiment 4 (Antares, GSC-0041, Ironhollow, three of them
lawless); The Experiment to Garnet 2, to GSC-0044 3 (Achernar, Cedarhold), to Atlas 3 (Achernar,
Garnet); LHS 1140 to GSC-0044 5. The kit is staged at The Experiment whatever the site.

| Step | How | Cost | State |
|---|---|---|---|
| 1. The kit | `outpost-kit-ironlight-to-experiment`: one ship with an empty hold to Ironlight Crossroads, 1 kit at 75,000 cr or less (booked once), stored at The Experiment | 74,010 cr and about 10 jumps of fuel | written, off; a guard of Military for the 4 loaded jumps is asked before it is switched on |
| 2. The founding | The builder withdraws the kit at The Experiment, flies to the chosen place, stays undocked, `deploy_outpost`; the faction gives it manage_bases | 100,000 cr from the treasury | a first call: one flight by hand, then a script |
| 3. Fuel for its bunker | How fuel goes into a bunker is not read: the first test after the founding, one hauler. The good to carry is the fuel cell (a ship burns cells from its cargo where no station sells fuel: help of `refuel`), asked at 100 cr in depth at Central Nexus (1,911), Node Alpha (3,219) and The Experiment (3,842), the border station nearest the sites (Trade's readings, admirals.log ENT-022, books of 07:36 to 07:42 UTC); a fuel cell restores 20 fuel in one unit of hold (catalog), so a Threshold's 65 cells carry 1,300 fuel for 6,500 cr; the reserve keeps every fuel cell (game/reserve.tsv) | 6,500 cr a hold | open |
| 4. Stock in and out | Miners at the site's fields deposit ore into the outpost's faction storage; haulers carry loads to The Experiment's workshop (2 jumps from Garnet, 3 from GSC-0044 or Atlas) (an outpost has storage and fuel, no workshop and no market) | fuel | routes written once the outpost stands |

Credits for the whole at the asks of 07:55 UTC: 174,010 cr and the fuel; at today's ask 248,663 cr.
What it draws each cycle: nothing (read).

### The Hiring Board at Node Beta (orders.log ENT-036, P5 and block APOLLO (3))
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 15.4.

Built 2026-11-17 12:19 UTC by `build.py` of the skill logistics-stock, flown in a `catch.py` row at the
end of the builder's gather run (caught 12:13 UTC; the engine's mining loop ran on and was stopped a
minute later; docked at Node Beta about 12:18 UTC; done in 6.4 minutes):

| Step | What the game showed |
|---|---|
| The faction store at Node Beta before | 0 items; treasury 82,999 cr (`view` with target faction, a read) |
| 75 steel plate and 25 circuit boards from the builder's own storage into the faction store | `deposit` with target faction and source storage, one unit first, proved by the store; no hold needed |
| `faction_build` hiring_board | HTTP 200; faction_list: Hiring Board, level 1, faction_recruitment, under_construction, capacity 50, rent 26 cr a cycle paused while it is built |
| After | the store's 100 units gone; treasury 7,723 cr; the builder's wallet unchanged at 186,321 cr |
| The builder | Corporation Management 3 to 4 (354 of 900 XP toward 5) |

Rent at Node Beta after: 69 cr a cycle for the Lockbox, the board's 26 to come. The cap rises from 20
to 50 when the board is done (catalog: build time 20 ticks). Left in the builder's storage at Node
Beta: 40 circuit boards and 5 steel plate, the start of the Recruitment Desk's 100 boards and 200
plate; the Desk's other 60 boards are the gold boards of `craft-boards-gold-experiment` (section 1.2).

### The Recruitment Desk (orders.log ENT-037, block APOLLO (2))
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/logistics.md section 15.5.

Built 2026-11-17 20:25 UTC (build.py with `--upgrade` and `--treasury-ok`, the Fleet Admiral's word of requests.log
ENT-242): the builder's storage at Node Beta held 115 plate and 100 boards; another hauler gave it 85 plate by
script (20:14 to 20:16 UTC, 0 cr), `waitstore.py` saw 200 and 100, `build.py` moved both into the faction store
(one unit first) and called `faction_upgrade` on the Hiring Board. The treasury fell 363,931 -> 63,931 cr, the
wallet did not move; faction_list: Recruitment Desk, level 2, under construction, capacity 100, rent 39 cr a cycle
paused while it is built; active with a members limit of 100 by 20:35 UTC (table faction). The builder's Corporation
Management rose from 4 to 5. Rent after it: 69 + 39 cr a cycle at Node Beta and 69 at The Experiment, 177 cr a
cycle, about 15,200 cr a day; the treasury read 94,652 cr at 20:35 UTC, about six days of rent.

The Desk is an upgrade of the Hiring Board (catalog: `recruitment_desk`, level 2, upgrades_from
`hiring_board`, cap 100, 300,000 cr, 100 circuit boards, 200 steel plate), so the call is `faction_upgrade`
with the board's facility_id and the type, not `faction_build` (the game's help of `spacemolt_facility`).
`build.py --upgrade <facility_id>` does it with the same steps as a build. The goods (the tool stock and the
table holdings, 15:57 UTC): Logistics holds 236 boards (175 at Node Beta, 60 gold boards at The Experiment, 1
at Central Nexus) and, in one storage at Node Beta, 200 steel plate; 60 boards and 175 plate go into the
builder's storage at Node Beta by script, where it holds 40 boards and 25 plate. The fee waits for the Fleet
Admiral (requests.log ENT-234): the treasury read 205,591 cr at 15:57 UTC and the outpost takes 100,000 of
it. The next office, the Recruitment Center (cap 200), takes 2,000,000 cr, 500 boards, 1,000 plate and 300
flex polymer, and Corporation Management 3 of its builder.

### The Atria outpost, planned (orders.log ENT-052, P4 (b) and block APOLLO (2))
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/logistics.md section 15.6.

Atria is the north outpost (the Fleet Admiral's choice; Acrab dropped on Suggi's word). Planned 2026-11-18 00:20 UTC from
the tables lanes, fields and books; built once GSC-0044 runs by routes and the allocation stands (requests.log ENT-268).

| Step | How | Cost | State |
|---|---|---|---|
| 1. The kit | `outpost-kit-ironlight-to-node-beta`: one member hauler with an empty hold to Ironlight Crossroads (LHS 1140, 6 jumps from Node Beta), 1 kit at 150,150 cr or less with the tax (asked 148,663 x 1, book of 00:13 UTC), stored at Node Beta | the kit, booked once; about 12 jumps of fuel | written, off: no hauler holds the price (wallets stop at 50,000 cr, orders D11) |
| 2. The founding | found.py of the skill logistics-stock from Node Beta: the road GSC-0027, GSC-0050, Brachium, GSC-0049, Acrab, Atria (6 jumps); `deploy_outpost` at the place she names (proposed: Atria Belt) | 100,000 cr, the treasury first | waits for her word (`--treasury-ok`) |
| 3. Its bunker | the runner's `bunker` step, cells from Central Nexus (100 cr x 1,850, 7 jumps from Atria) | about 5 cr a unit of fuel | a route like `supply-bunker-gsc-0044` once it stands |

The place: Atria Belt holds aluminum 1,134 and gold 754; Atria Ice Fields water 45,824, nitrogen 50,000 and deuterium
5,000; Atria Emission Nebula argon 49,999, neon 50,000 and hydrogen 13,568 (table fields, 23:39 UTC). Atria lies 7 jumps
from home and 6 from Node Beta (table lanes); Intel reads its nearest station with fuel and a market 6 jumps away
(admirals.log ENT-063) and no pirate line
on our record within two jumps of the north road. Whether an outpost takes a faction office, which
decides where the big recruitment offices stand (orders P5 (2)), is read at GSC-0044 this turn (section 10).

Felis, the south outpost (orders.log ENT-054, block APOLLO (2): Atria, then Felis), planned 2026-11-18 00:40 UTC from the
tables lanes, fields and books. Road: from Synchrony Hub by Pherkad, Wolf 1061, GSC-0012 and GSC-0021 (5 jumps); from
Node Beta by Acubens, Hamal, Okab, Coldwater and Tanglewood (6); the kit from Ironlight Crossroads by Antares, GSC-0041,
Pherkad, Wolf 1061, GSC-0012, GSC-0021 (7). Felis lies 7 jumps from home; its belts hold about 100,000 iron and 100,000
copper each (Belt A, Belt B, Dim Lattice, Dark Residue, with 577 null matter at Dark Residue), its Frost Ring water
39,481, nitrogen 50,000 and deuterium 1,528 (table fields, 2026-11-17 23:35 UTC). Its bunker's cells would come from
Synchrony Hub (asked 47 cr x 30 at 00:37 UTC, the cheapest ask read) or Node Alpha (100 x 3,201). The same three steps
as Atria; its kit route is written when Atria's kit is bought, since Ironlight Crossroads lists one kit at a time.
