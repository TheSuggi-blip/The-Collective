# Logistics guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-24. Evidence: plan.py show and check (2026-11-24 15:16 UTC); fill.py status and check hauler 14:41 to 15:20 UTC; runs.jsonl 2026-11-24; requests.log ENT-504, ENT-511, ENT-516, ENT-523; orders.log ENT-089 (block APOLLO).

A free hauler takes the first open route of First, its own routes, Then (`plan.py show`). Earnings: the tool fleet, view=standing, member Apollo.

- First: the once missions (`voidborn-*`, first hunts, `mission-*` of the five capitals; F34, F35), Sol's paid loop, the `finish-*` routes of missions held half done.
- Own: `finish-*` in the holders' rows only; `@newborn-nebula` (Grand Exchange's once lines, First Links with nickel bought there), `@newborn-rim`; `@outpost-supply`; `@stored-goods`, `@craft-reserve` (docked crafts, closed at the reserve max, F36); `@train-hauler`; receivers' `craft-steel-logistics-<station>` first in their rows. No give-to-hauler route in a hauler row (`Stored goods`).
- Then: `buy-steel-reserve-central-nexus` (docked buy that only stores, ENT-504, closed by `held_below` steel 88,000 of Logistics), `builder-home-node-beta` (the Builder home once), `buy-carbon-reserve-node-beta` (4 cr, `in_system` node_beta, three buy-and-store cycles a run so dispatch's stall rest does not idle its pilots, `held_below` carbon 50,000), the far joins (`skills_below` corporation_management 7 keeps the Builder home), `haul-network`, `park`.
- `haul-network` (haul.py, game/haul-policy.json): freight and supply only, its arbitrage lane out (orders ENT-089 block APOLLO; P5: a buy that feeds a sale is Trade's). Policed freight is scarce (the board's contracts end mostly at pirate strongholds), so most of its runs wait docked at no cost for a job; its runs are read each turn.
- Off: the officer steel route on the outpost's faction iron (an outpost's faction store gives nothing out, topic-bases). Buying iron for steel stays off while plate asks 18 cr.
- Hulls (F17): no bulk hull while no freight or carry fills it (Prayer flown: no pay).
- What would change it: Unity's word on the Atria kit (ENT-523: Arneb's kit or our own kit line), freight a hull can carry, the Grand Exchange missions without a route.
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
Status: proven. Updated: 2026-11-24. Evidence: runs table 2026-11-15 to 17; game/routes/templates/logistics.json; storage views of a Synchrony Hub receiver 2026-11-24 12:06 and 12:20 UTC (admirals.log ENT-127).

- Fit: none. Trains trading (each sale) and navigation (each jump).
- Steps: at the stop that sells, `withdraw` takes from the pilot's own storage what the bid takes at its best price and `sell` puts it in; the rest goes back by `store`. A carry withdraws at the storing station and sells one hop away.
- Opens: `requires.stored` (only the pilot that stores the good) and `requires.bid` (a book of the last hour shows the bid at its floor); `max_ships` 1: a pool bid takes one load.
- Closes: the bid gone; the good sold out of that pilot's storage.
- The bids, not the haulers, bound it: soma into pools of 1 to 4 at 559 to 694 cr, armor plate into pools of 3 to 6, 200 hydrogen gas made into 75 liquid hydrogen and 42 sold at 116 cr (+4,798 cr in about 20 minutes, 2026-11-16).
- A give route that hands stores to the station's hauler receiver never stands in a hauler's own row: two receivers at one station that both fly it give each other their stores, and each one's steel run then finds no iron (2026-11-24: 3,953 iron gone from one receiver in 14 minutes).

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
Status: proven. Updated: 2026-11-23. Evidence: RESULT lines and routes.py measure, 2026-11-15 23:28 UTC to 2026-11-16 13:03 UTC; requests.log ENT-071, ENT-149; mission-market-participation-frontier RESULT 2026-11-23 00:21 UTC.

The Voidborn missions each new pilot flies once (list First):
- `voidborn-signal-protocol` (3,500 cr): needs The Collective Provides.
- `voidborn-hardware-cargo` (1,500) and `voidborn-atmospheric-extraction` (2,000): a Cargo Expander I or a Gas Harvester I held in the HOLD at the hand-in (`have_item`): a fitted module does not count (four runs, -4,216 cr, ENT-149): hand in first, fit after (`handin_module.py`).
- `voidborn-resonance-finish` (about 15,000 less 15 energy crystals bought at Central Nexus).
- `voidborn-precedence` (4,000: Node Beta, Synchrony Hub, Node Alpha), `voidborn-selling` (1,000: ten units sold), `voidborn-first-hunt-nexus` (1,000, 50 Weapons XP: three belt-grazers with the Pulse Laser I), `voidborn-first-steps-board` (1,000: 15 carbon at Acubens Belt, taken from the Central Nexus board).
- `voidborn-concurrent` (3,000) and `voidborn-substrate`: the soma they need are handed over at the accept, so nothing is bought; Crystal Delivery hands nothing: read the hold after an accept.
- `voidborn-missions-1` (Synchrony Relay Run and Crystal Delivery, 8 jumps), `voidborn-mining-missions` (1,500 and 1,800).
- Haulers born in another empire fly their home board's once missions, never the Voidborn ones (rule F35): templates `@newborn-rim` (Frontier Station) and `@newborn-nebula` (Grand Exchange). `mission-market-participation-frontier` and `-grand`: Buying and Selling, 1,000 cr each, ten copper ore bought and sold back (first run +1,960 cr in 1 minute); `min_credits` 3,200, since the runner buys nothing under 3,000.
