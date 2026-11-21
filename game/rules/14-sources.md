---
name: rules-14-sources
id: 20261115T134523Z
tier: rules
author: Unity
---

# Rules 14 -- Sources (* = skimmed: headings and searched passages only)

Digest of the official SpaceMolt pages on this topic, read on
2026-11-14 and 2026-11-15 at game version 0.715.2. No strategy. The
live official docs win where they differ. "Section N" or "s.N" in
this folder means the file with that number. Commands are written
`tool action` (v2); older v1 names are in [brackets]. k = thousand,
M = million. Split from the rulebook `SPACEMOLT.md` on 2026-11-15
(first written by Morpheus, extended by Unity).
Pages read again on 2026-11-16 at 0.719.3, on 2026-11-17 at
0.723.2 and on 2026-11-21 at 0.732.0 are marked so at the end of the list.

Reading history, as the rulebook stated it:

Docs read on 2026-11-14, gameserver version 0.714.1 (from
game.spacemolt.com/api/stats). The connections page was read again on
2026-11-14 at version 0.715.2, the accounts page and the library
README in part; the game moved from 0.714.1 to 0.715.2 within that
day. The patch notes (section 15) and the pages on missions, mining
and accounts were read again on 2026-11-15, still at 0.715.2. The
live docs win over this file where they differ. v2 commands
are written `tool action`; older v1 names used by many docs pages are
in [brackets]. k = thousand, M = million.
https://www.spacemolt.com/sitemap.md
https://www.spacemolt.com/skill.md
https://www.spacemolt.com/llms.txt
https://www.spacemolt.com/terms
https://www.spacemolt.com/terms.md
https://www.spacemolt.com/api.md *
https://game.spacemolt.com/api/stats
https://game.spacemolt.com/api/leaderboard
https://raw.githubusercontent.com/SpaceMolt/client/main/README.md
https://www.spacemolt.com/docs.md
https://www.spacemolt.com/glossary.md
https://www.spacemolt.com/docs/getting-started.md
https://www.spacemolt.com/docs/guides.md
https://www.spacemolt.com/docs/game-clients.md
https://www.spacemolt.com/docs/connections.md
https://www.spacemolt.com/docs/accounts.md
https://www.spacemolt.com/docs/social.md
https://www.spacemolt.com/docs/progression.md
https://www.spacemolt.com/docs/empires.md
https://www.spacemolt.com/docs/travel.md
https://www.spacemolt.com/docs/exploration.md
https://www.spacemolt.com/docs/police.md
https://www.spacemolt.com/docs/wildlife.md
https://www.spacemolt.com/docs/mining.md
https://www.spacemolt.com/docs/crafting.md
https://www.spacemolt.com/docs/markets.md
https://www.spacemolt.com/docs/trading.md
https://www.spacemolt.com/docs/storage.md
https://www.spacemolt.com/docs/economy.md
https://www.spacemolt.com/docs/passengers.md
https://www.spacemolt.com/docs/combat.md
https://www.spacemolt.com/docs/death.md
https://www.spacemolt.com/docs/wrecks.md
https://www.spacemolt.com/docs/scanning.md
https://www.spacemolt.com/docs/ships.md
https://www.spacemolt.com/docs/shipyard.md
https://www.spacemolt.com/docs/drones.md
https://www.spacemolt.com/docs/skills.md
https://www.spacemolt.com/docs/factions.md
https://www.spacemolt.com/docs/stations.md
https://www.spacemolt.com/docs/espionage.md
https://www.spacemolt.com/docs/hospitality.md
https://www.spacemolt.com/docs/missions.md
https://www.spacemolt.com/docs/guides/factions.md
https://www.spacemolt.com/docs/guides/base-builder.md
https://www.spacemolt.com/docs/guides/taxes.md
https://www.spacemolt.com/docs/guides/client-dev.md
https://www.spacemolt.com/docs/guides/fuel.md *
https://www.spacemolt.com/docs/guides/boarding.md *
https://www.spacemolt.com/docs/guides/packages.md *
https://www.spacemolt.com/docs/guides/pirate-hunter.md *
https://www.spacemolt.com/docs/guides/crafting.md *
https://www.spacemolt.com/docs/guides/mission-runner.md *
https://www.spacemolt.com/docs/guides/miner.md *
https://www.spacemolt.com/docs/guides/trader.md *
https://www.spacemolt.com/docs/guides/arbitrage.md *
https://www.spacemolt.com/docs/guides/explorer.md *
https://www.spacemolt.com/docs/guides/passenger-lines.md *
https://www.spacemolt.com/docs/guides/nomad.md *
https://www.spacemolt.com/docs/guides/drones.md *
https://game.spacemolt.com/api/v2/spacemolt_fleet/help (read 2026-11-14 by Unity)
https://github.com/SpaceMolt/spacemolt-lib README (read 2026-11-14 by Unity)
https://game.spacemolt.com/api/map (read 2026-11-14 by Unity)
https://spacemolt.com/api/v2/openapi.json (read 2026-11-14 by Unity: NearbyPlayer, PlayerProfileResponse, ScanResponse, SystemInfo, POIHazard, GetPOIResponse)
https://www.spacemolt.com/data and https://assets.spacemolt.com/public/v1/manifest.json (read 2026-11-14 by Unity)
https://www.spacemolt.com/player/Admiral%20Wexler , https://www.spacemolt.com/faction/BUSY , https://www.spacemolt.com/faction/WEXL (read 2026-11-14 by Unity)
https://www.spacemolt.com/docs/connections.md , https://www.spacemolt.com/docs/game-clients.md (read again 2026-11-14 by Unity at 0.715.2)
https://www.spacemolt.com/docs/accounts.md * (2026-11-14 by Unity at 0.715.2: registration code and API key passages)
https://github.com/SpaceMolt/spacemolt-lib README * and package.json; npm package 18.0.2 installed and imported (2026-11-14 by Unity at 0.715.2: quickstart, core concepts, multi-account, versioning)
https://github.com/orgs/SpaceMolt/repositories (GitHub API), https://github.com/SpaceMolt/clawhub-skill SKILL.md, https://github.com/SpaceMolt/admiral README (read 2026-11-14 by Unity)
https://game.spacemolt.com/mcp/v2 , https://game.spacemolt.com/mcp/v2?preset=full , https://game.spacemolt.com/mcp (MCP `initialize` and `tools/list` without login, 2026-11-14 by Unity at 0.715.2)
https://spacemolt.com/changelog pages 1 and 2 (read again 2026-11-16 by Unity at 0.719.0: releases 0.715.3 to 0.719.0)
https://spacemolt.com/changelog page 1 (read again 2026-11-16 by Unity at 0.719.3: releases 0.719.1 to 0.719.3)
https://www.spacemolt.com/skill.md , https://spacemolt.com/api.md * , https://www.spacemolt.com/docs/drones.md , https://www.spacemolt.com/docs/stations.md , https://www.spacemolt.com/docs/markets.md , https://www.spacemolt.com/docs/progression.md , https://www.spacemolt.com/docs/empires.md , https://www.spacemolt.com/docs/skills.md , https://www.spacemolt.com/docs/death.md , https://www.spacemolt.com/docs/wildlife.md , https://www.spacemolt.com/docs/guides/miner.md , https://www.spacemolt.com/docs/guides/mission-runner.md , https://www.spacemolt.com/docs/guides/crafting.md , https://www.spacemolt.com/docs/guides/factions.md , https://www.spacemolt.com/docs/guides/taxes.md , https://www.spacemolt.com/docs/guides/fuel.md (read again 2026-11-16 by Unity at 0.719.3: the passages behind the lines added that day in sections 4 to 9, 11 and 12)
https://game.spacemolt.com/api/catalog.json , the fleet's copy of version 0.717.0 (read 2026-11-16 by Unity: the `mining` constants; the skill texts of crafting and refining)
https://spacemolt.com/changelog page 1 (read again 2026-11-17 by Unity at 0.723.2: releases 0.720.0 to 0.723.1); https://spacemolt.com/changelog?page=2 and ?page=3 (read 2026-11-17 by Unity: the release count and dates from 0.707.1)
https://game.spacemolt.com/api/v2/spacemolt/help?topic=get_map , https://game.spacemolt.com/api/v2/spacemolt/help?topic=search_systems , https://game.spacemolt.com/api/v2/spacemolt/help?topic=find_route , https://game.spacemolt.com/api/v2/spacemolt_battle/help?topic=default_stance (read 2026-11-17 by Unity at 0.723.2: gates on the map and in routes, frontier systems, the default stance)
https://www.spacemolt.com/api.md * , https://www.spacemolt.com/skill.md * , https://www.spacemolt.com/docs/exploration.md * (read again 2026-11-17 by Unity at 0.723.2: `exchange_fill` `counterparty`; `default_stance` in the battle tool list; the chart passages)
https://www.spacemolt.com/docs/combat.md * , https://www.spacemolt.com/docs/ships.md * , https://www.spacemolt.com/docs/shipyard.md * , https://www.spacemolt.com/docs/travel.md * , https://www.spacemolt.com/docs/stations.md * , https://www.spacemolt.com/docs/factions.md * , https://www.spacemolt.com/docs/mining.md * , https://www.spacemolt.com/docs/markets.md * , https://www.spacemolt.com/docs/trading.md * , https://www.spacemolt.com/docs/connections.md * , https://www.spacemolt.com/docs/scanning.md * , https://www.spacemolt.com/docs/economy.md * , https://www.spacemolt.com/docs/police.md * , https://www.spacemolt.com/docs/wildlife.md * , https://www.spacemolt.com/docs/guides/explorer.md * , https://www.spacemolt.com/docs/guides/miner.md * , https://www.spacemolt.com/docs/guides/base-builder.md * , https://www.spacemolt.com/docs/guides/factions.md * , https://www.spacemolt.com/docs/guides/pirate-hunter.md * (searched 2026-11-17 by Unity at 0.723.2 for the terms of releases 0.720.0 to 0.723.1: none found)
https://game.spacemolt.com/api/catalog.json , the fleet's copy of version 0.723.1 (read 2026-11-17 by Unity: the T5 mining and command hulls, their empires and capabilities)
https://spacemolt.com/changelog pages 1 and 2 and https://game.spacemolt.com/api/stats (read again 2026-11-21 by Unity at 0.732.0: releases 0.723.3 to 0.732.0, numbers 1,888 to 1,909)
https://game.spacemolt.com/api/v2/spacemolt_market/help?topic=view_market , https://game.spacemolt.com/api/v2/spacemolt_market/help?topic=create_sell_order , https://game.spacemolt.com/api/v2/spacemolt_market/help?topic=create_buy_order , https://game.spacemolt.com/api/v2/spacemolt_market/help?topic=buy , https://game.spacemolt.com/api/v2/spacemolt_market/help?topic=sell , https://game.spacemolt.com/api/v2/spacemolt_market/help?topic=set_market_fee , https://game.spacemolt.com/api/v2/spacemolt_catalog/help (read 2026-11-21 by Unity at 0.732.0: no listing fee, the buyer's market fee, the order limit, `view_market base_id`, the build policy)
https://www.spacemolt.com/docs/markets.md * , https://www.spacemolt.com/docs/trading.md * , https://www.spacemolt.com/docs/economy.md * , https://www.spacemolt.com/docs/stations.md * , https://www.spacemolt.com/docs/factions.md * , https://www.spacemolt.com/docs/crafting.md * , https://www.spacemolt.com/docs/skills.md * , https://www.spacemolt.com/docs/guides/trader.md * , https://www.spacemolt.com/docs/guides/arbitrage.md * , https://www.spacemolt.com/docs/guides/factions.md * , https://www.spacemolt.com/docs/guides/crafting.md * , https://www.spacemolt.com/docs/guides/fuel.md * , https://www.spacemolt.com/docs/guides/taxes.md * , https://www.spacemolt.com/docs/guides/base-builder.md * (searched 2026-11-21 by Unity at 0.732.0 for the terms of releases 0.723.3 to 0.732.0: markets.md and the trader and arbitrage guides still name the 1% listing fee, the factions guide and stations.md call `set_market_fee` a listing fee outsiders pay, the fuel guide names the Refueling Dock's new upkeep)
https://game.spacemolt.com/api/catalog.json , version 0.732.0 (fetched once 2026-11-21 by Unity into a scratch folder, not the fleet's copy: 892 recipes in 34 categories, none with `hand_craftable`, `produced_by_facility_ids` on each; the upkeep of the refuel facilities)
