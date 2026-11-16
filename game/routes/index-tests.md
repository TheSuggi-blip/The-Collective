---
name: routes-index-tests
id: 20261116T174325Z
tier: intel
author: Unity
---

# index-tests.md -- Tests

Written by `python3 -B game/fleet/routes.py index`, never by hand. Work that repeats and has no measured figure yet: one ship until its first RESULT line is read.
A route is a task one pilot carries out by itself; its file is `game/routes/<id>.json`
(`BLUEPRINT.md`). The figures are what our own runs measured. Home space first, then by
kind and name. Up: [master-index.md](master-index.md).

Routes: 11.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [carry-liquid-hydrogen-node-beta-central](carry-liquid-hydrogen-node-beta-central.json) | circuit | home space | Liquid hydrogen made at the Node Beta workshop carried one jump to the Central Nexus bid | up to 1 ships, with 10 liquid_hydrogen stored at node_beta_industrial_station, while central_nexus bids 110 cr for liquid_hydrogen | TBD | TBD | TBD | TBD | -- |
| [carry-soma-node-beta-node-alpha](carry-soma-node-beta-node-alpha.json) | circuit | home space | Stored neural soma carried one jump from Node Beta to the Node Alpha soma bid | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_alpha_processing_station bids 500 cr for voidborn_neural_soma | TBD | TBD | TBD | TBD | -- |
| [carry-soma-node-beta-node-gamma](carry-soma-node-beta-node-gamma.json) | circuit | home space | Stored neural soma carried one jump from Node Beta to the Node Gamma soma bid | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 500 cr for voidborn_neural_soma | TBD | TBD | TBD | TBD | -- |
| [carry-soma-synchrony-node-alpha](carry-soma-synchrony-node-alpha.json) | circuit | home space | Stored neural soma carried one jump from Synchrony Hub to the Node Alpha soma bid | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 500 cr for voidborn_neural_soma | TBD | TBD | TBD | TBD | -- |
| [carry-soma-synchrony-node-gamma](carry-soma-synchrony-node-gamma.json) | circuit | home space | Stored neural soma carried one jump from Synchrony Hub to the Node Gamma soma bid | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_gamma_relay_station bids 500 cr for voidborn_neural_soma | TBD | TBD | TBD | TBD | -- |
| [drain-ice-node-alpha](drain-ice-node-alpha.json) | circuit | home space | Stored water ice sold where it lies, at node_alpha_processing_station, into the bid there | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | TBD | TBD | TBD | TBD | -- |
| [sell-soma-node-beta](sell-soma-node-beta.json) | circuit | home space | Stored neural soma sold where it lies, at Node Beta, into the station's soma bid | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 500 cr for voidborn_neural_soma | TBD | TBD | TBD | TBD | -- |
| [sell-soma-synchrony](sell-soma-synchrony.json) | circuit | home space | Stored neural soma sold where it lies, at Synchrony Hub, into the station's soma bid | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 500 cr for voidborn_neural_soma | TBD | TBD | TBD | TBD | -- |
| [mine-the-experiment-haze-synchrony](mine-the-experiment-haze-synchrony.json) | mine | home space | The Experiment Haze: hydrogen_gas; sold at Synchrony Hub | up to 1 ships, needs gas_harvester_i, while synchrony_hub bids 28 cr for hydrogen_gas | TBD | TBD | TBD | TBD | -- |
| [hunt-test-amberfall-chlorophage](hunt-test-amberfall-chlorophage.json) | hunt | beyond the border, 5 jumps | Yield test: chlorophage at Amberfall Emission Nebula (lawless); does a kill drop caustic sac | up to 1 ships, empty hold | TBD | TBD | TBD | TBD | -- |
| [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) | mine | beyond the border, 8 jumps | Nova Terra Ice Shelf: water_ice, deuterium_ice, helium_ice; sold at Node Beta Industrial Station | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | TBD | TBD | TBD | TBD | -- |
