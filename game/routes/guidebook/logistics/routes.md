# Logistics guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-22. Evidence: plan.py show --brief (applied 2026-11-22 15:55 UTC); fill.py check; orders.log ENT-064 (block APOLLO, P2, P4, P5); requests.log ENT-350, ENT-358; data/fleet/receivers.json; the tool stock, view=reserve; rules F8, F23, F37.

A free hauler takes the first open route of First, its own routes, Then (`plan.py show`). Earnings: the tool fleet, view=standing, member Apollo.

- First: the once missions (`voidborn-*`, first hunts, `mission-*`; F34, F35); a mission test whose runs reach none of its stops leaves the list.
- Own, members: `@outpost-supply` (GSC-0044's repair stock and bunker); the builder first `outpost-kit-ironlight-to-node-beta` (on `requires.ask`); the receiver at The Crescent Moon first `craft-boards-crescent-moon` (a test).
- Own, every hauler: `@stored-goods`, `@craft-reserve` (boards from stored silicon and carbon, gold wiring, cells, steel, piping: each opens on the pilot's own stored inputs), `@train-hauler` (piloting toward the freighter at 10, a cost of fuel).
- Receivers (strict classes on): several haulers a station where many give (`handover.py receivers`); each crafts docked what it is given. Silicon binds the boards; copper ore lies far beyond any recipe we need.
- Then: `park`, which none should reach.
- What would change it: a kit at Ironlight (the builder flies); Piloting 10 (the freighter, then far hauls); silicon given in quantity (more board crafters); a paid carry found (tests.md) in place of the loop.

### Route Templates
Status: proven. Updated: 2026-11-21. Evidence: game/routes/templates/logistics.json (2026-11-21); plan.py templates; Suggi 2026-11-16 and rule F22.

A template is a named list of routes in the order a ship tries them, with the skills it trains and, in its note, the fit (`game/routes/templates/logistics.json`). A ship's row names it as `@<name>`: one word switches a ship.

| Task | How |
|---|---|
| See them and their ships | `plan.py templates` (the tool plan, action=templates) |
| Make or change one | `plan.py template <name> <routes> --title "..." --trains <skills> --note "..."` |
| Put ships on one | `plan.py use <ships> <name>` |
| Take one away | `plan.py template <name> none`, once no ship names it |

The templates: `outpost-supply`, `train-hauler`, `stored-goods` (Trade's sell and carry routes of hydrogen, soma, null matter, palladium, plasma and liquid hydrogen; trading, navigation) and `craft-reserve` (fuel cells, four steel crafts, then piping; crafting, refining). `gas-harvest` and `gather-reserve` are gone (rule F23).

No list of routes that did not pay (rule F22): a credits figure here is a dated reading, never a verdict.

### Stored goods sold or carried (template `stored-goods`)
Status: proven. Updated: 2026-11-21. Evidence: runs table 2026-11-15 to 17; game/routes/templates/logistics.json.

- Fit: none. Trains trading (each sale) and navigation (each jump).
- Steps: at the stop that sells, `withdraw` takes from the pilot's own storage what the bid takes at its best price and `sell` puts it in; the rest goes back by `store`. A carry withdraws at the storing station and sells one hop away.
- Opens: `requires.stored` (only the pilot that stores the good) and `requires.bid` (a book of the last hour shows the bid at its floor); `max_ships` 1: a pool bid takes one load.
- Closes: the bid gone; the good sold out of that pilot's storage.
- The bids, not the haulers, bound it: soma into pools of 1 to 4 at 559 to 694 cr, armor plate into pools of 3 to 6, 200 hydrogen gas made into 75 liquid hydrogen and 42 sold at 116 cr (+4,798 cr in about 20 minutes, 2026-11-16).

### Crafting what we build with (template `craft-reserve`, and hand chains)
Status: proven. Updated: 2026-11-21. Evidence: route files and RESULT lines 2026-11-17 00:03 to 2026-11-18 00:12 UTC; queue.log ENT-128; admirals.log ENT-065; requests.log ENT-190, ENT-200.

- Fit: none; the pilot stays docked while the workshop runs. Trains crafting and refining.
- Steel: `craft-steel-logistics-experiment`, `-node-beta`, `-synchrony-hub`, `-central-nexus` (from Trade's `craft-steel-own-node-beta`) ask `basic_iron_smelting` in halving sizes, 128 to 1 runs: the runner quotes each and makes nothing where the store falls short, so a pilot smelts all of its own iron there (up to 2,550) in one visit. Opens on 100 iron stored there. The older 50-run routes for any role (ENT-190) need 550 stored.
- Piping: `craft-piping-plate-node-beta`, 15 runs of `draw_copper_piping` (180 copper, 30 plate: 60 piping, one hold); opens on 130 plate and 180 copper, so each storage keeps 100 plate.
- In a public facility: `craft-steel-refine-node-beta` (refine_steel, `venue: "facility"`, `max_fee` 36): 500 iron into 200 plate for 2,900 cr, a plate for 2.5 iron and 14.5 cr against 10 iron and 0 cr by hand; in no plan while the Fleet Admiral weighs the fee (ENT-200).
- Boards: `craft-boards-*` (topic-station.md).
- Hand chains: catch.py, craftchain.py and stage.py of the skill logistics-stock.

### Beyond the border (a test)
Status: test. Updated: 2026-11-21. Evidence: buy-gold-ironlight-boards, RESULT line 2026-11-17 00:35 UTC; requests.log ENT-172; runs table 2026-11-16; orders.log ENT-056.

- `buy-gold-ironlight-boards`: one ship with an empty hold to Ironlight Crossroads (LHS 1140, lawless, police 0, six jumps), 3 gold ore at 145 cr or less (booked once, craft inputs), then `fabricate_gold_circuit_boards` at Node Beta from the pilot's own copper and crystal: 3 of 3 stops in 20.6 min, -561 cr, 2 boards. Out of the plan since 2026-11-17 04:05 UTC.
- Our hunters sold at that station 14 times on 2026-11-16 without a loss. The orders now ask Logistics to carry and supply beyond our borders too (ENT-056).

### Missions that pay once (the list First)
Status: proven. Updated: 2026-11-21. Evidence: data/missions and the tool candidates, kind mission, 2026-11-17 11:53 UTC; RESULT line 12:41 UTC; queue.log ENT-157.

Board missions of the hauler's class (rule F34: deliveries, crafting, station needs). Read a once route's runs by role before it enters the plan: one measured on another role may refuse a hauler.

- Workshop Production Run (Central Nexus, Node Beta): "Craft 5 items using any recipe", 3,500 cr, 25 crafting XP, 20 Piloting XP. `mission-workshop-production-run-node-beta` accepts, smelts 5 plates from the pilot's own iron and hands in: 3 stops in 6.9 minutes. In First at 4 ships: each hauler that stores 60 iron at Node Beta flies it once.
- Shipyard Supply at Node Beta (deliver_item: Mining Laser I, Void Nanite Suspension, Shield Emitter): station-made mission ids (`procurement_<hash>_<item>`), no template id, so the runner's accept cannot take them until route_run.py accepts by mission id (a fleet-build of mine).
- Not flown: Procyon Station Upgrade (10 boards for 1,960 cr; boards are reserve); the smuggling deliveries of Central Nexus, 20 to 42 jumps.

### Missions That Pay Once
Status: proven. Updated: 2026-11-21. Evidence: RESULT lines and routes.py measure, 2026-11-15 23:28 UTC to 2026-11-16 13:03 UTC; requests.log ENT-071, ENT-149.

The Voidborn missions each new pilot flies once (list First):
- `voidborn-signal-protocol` (3,500 cr): needs The Collective Provides.
- `voidborn-hardware-cargo` (1,500) and `voidborn-atmospheric-extraction` (2,000): a Cargo Expander I or a Gas Harvester I held in the HOLD at the hand-in (`have_item`): a fitted module does not count (four runs, -4,216 cr, ENT-149): hand in first, fit after (`handin_module.py`).
- `voidborn-resonance-finish` (about 15,000 less 15 energy crystals bought at Central Nexus).
- `voidborn-precedence` (4,000: Node Beta, Synchrony Hub, Node Alpha), `voidborn-selling` (1,000: ten units sold), `voidborn-first-hunt-nexus` (1,000, 50 Weapons XP: three belt-grazers with the Pulse Laser I), `voidborn-first-steps` (1,000: 15 carbon at Acubens Belt).
- `voidborn-concurrent` (3,000) and `voidborn-substrate`: the soma they need are handed over at the accept, so nothing is bought; Crystal Delivery hands nothing: read the hold after an accept.
- `voidborn-missions-1` (Synchrony Relay Run and Crystal Delivery, 8 jumps), `voidborn-mining-missions` (1,500 and 1,800).
