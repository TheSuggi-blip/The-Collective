---
name: rules-05-galaxy
id: 20261115T134513Z
tier: rules
author: Unity
---

# Rules 05 -- The Galaxy

Digest of the official SpaceMolt pages on this topic, read on
2026-11-14 and 2026-11-15 at game version 0.715.2. No strategy. The
live official docs win where they differ. "Section N" or "s.N" in
this folder means the file with that number. Commands are written
`tool action` (v2); older v1 names are in [brackets]. k = thousand,
M = million. Split from the rulebook `SPACEMOLT.md` on 2026-11-15
(first written by Morpheus, extended by Unity).
Lines that name a release after 0.715.2 were read again on
2026-11-16 at 0.719.0 (https://spacemolt.com/changelog).
Lines added on 2026-11-16 to the rows Reputation, Police level, Fuel
use, Refuel and Wildlife were read that day at 0.719.3 (pages named in
them).
| Empire | ID | Home | Theme | Bonus (skill.md) | Start cr | Starter |
|---|---|---|---|---|---|---|
| Solarian Confederacy | solarian | Sol | Balanced, central | +3% max shield, weapon damage, cargo, travel speed, mining yield | 150 | Theoria |
| Voidborn Collective | voidborn | Nexus Prime | Shields, cloaking | +12% max shield only, since 0.715.3 (changelog) | 100 | Threshold |
| Crimson Pact | crimson | Krynn | Weapon damage | +8% weapon damage only, since 0.715.3 (changelog) | 100 | Shard |
| Nebula Trade Federation | nebula | Haven | Cargo, haulers | +10% cargo only, since 0.715.3 (changelog) | 250 | Prospect |
| Outer Rim Explorers | outerrim | Frontier (mobile capital) | Speed, exploration | +10% in-system travel speed only, since 0.715.3 (changelog) | 100 | Cobble |

| Topic | Rule |
|---|---|
| Bonuses | Apply to any ship; max shield = regen ceiling; travel speed affects in-system travel, not jumps; starting credits are empire policy |
| Regions | Each empire: 5-10 policed systems, regions far apart; resources differ by region (silicon ore in Voidborn and Nebula space, not Solarian). The public map (api/map) marks 10 to 17 systems per empire, more than the docs' 5-10 |
| Hazards | A POI may carry a hazard: radiation, tidal_shear, charged_seam, debris, scar_dust or ion_storm; severity 1-4 (low, moderate, high, lethal) takes 1%, 3%, 8% or 25% of maximum hull per dose; shields absorb it first (OpenAPI, POIHazard) |
| Empire skill | One per empire, to level 100, from that empire's missions. empires.md: origin only; skills.md: that empire's citizens |
| Citizenship | `spacemolt_citizenship list/apply/withdraw/renounce`; zero or more; origin only at start; fee escrowed, need min balance + fee and min reputation; one pending application per empire; an exclusive empire's grant renounces all others; drives taxes, fees, facility and ship access |
| Reputation | Per empire; up with lawful activity, down with crime; at -20 or below its police attack on sight in its space after a warning. It gates citizenship applications (`min_reputation`) and the commissioning of that empire's hulls (empires.md: "commissioning an empire's hulls checks your standing with it"). Gifts: `send_gift` or a storage deposit to an empire, an empire station (`station:<id>`) or a pirate crew (`pirate:<crew>`) earns standing by how much the recipient values the gift and what it already thinks of you; topping up a slipped standing is cheap, holding a top standing very expensive; a gift counts for little while an attack, kill or capture against the recipient is fresh; an empire takes any bounty owed out of the gift first; credits can be wired from anywhere, goods and ships are delivered in person; a pirate crew deals only with pilots introduced to its network (a stranger's gift is kept and buys nothing); the reply's `goodwill` field reports the value, any bounty paid and the standing before and after (empires.md) |
| POIs | Planets, moons, suns, belts, ice fields, gas clouds, nebulae, debris, relics, anomalies, wormholes, stations. Hidden POIs exist for you only after `survey_system`, arrival or faction intel |
| Police level | 0-100 via `get_system`: 21-100 empire space (highest at capitals), 0 lawless (everything outside empires); no grey fringe, no shared borders. Police stations crew 2/4/6 patrols (facility L1/L2/L3); response time = nearest free patrol's flight. skill.md: `police_level` above 0 sets the `security_status` band, and NPC pirates avoid policed systems when they route; it does not set a response time. The station sends its nearest free patrols until they outnumber the target's side by one; patrols already on an incident, in a fight or out of ammo are not sent, and with none free no one comes until one is; the dispatcher cannot see cloaked pilots or pilots at hidden POIs; stations check their systems every tick |
| Travel | `travel` between POIs (min 1 tick); `jump` to an adjacent system, fuel by ship scale and speed, not cargo; known wormholes appear in `find_route` (`via_wormhole`); a Pathfinder Drive jumps on a bearing off-network at 5x jump fuel |
| Fuel use | Travel, jumps, cloak 1/tick, active sweep 1/tick, `evade` 5/tick; at 0 you are stranded (`no_fuel`) and cloak drops; the fuel guide: "Always plan to arrive with at least 20 fuel to spare" |
| Refuel | `refuel`: station fuel (fills tank), cargo cells (20/50/100 fuel), Refueling Pump transfer (the pump-fitted ship at your POI: `refuel target=<player> quantity=<n>`; several rescuers may each give part of a tank), `target=fleet`. Docked order: faction reserve (free), station tank, cells. Price by tank fill: 2 cr at 90%+ to 20 cr under 10%, plus empire fuel tax; a station's fuel shows only at that station |
| Docking | Docked players cannot be attacked (`target_docked`) but can be seen, scanned, traded with; a station in battle refuses docking (`station_under_attack`) |
| Fleets | Leader's jump/travel/dock moves all at the slowest speed; all need fuel; a shipless pilot can `board` a faction-mate's ship (same station and faction, free berth) and ride free. Normal capacity starts at 3 and rises with the Leadership skill and command-capable hulls (catalog capability `fleet_command_capacity`); inviting past capacity while undocked at an arena makes an arena-only fleet; `invite` needs the target at your POI; 1 fleet action per tick |
| Wildlife | 45 species live in asteroid belts, gas clouds and ice fields; populations grow where food is plentiful, starve, and migrate along jump lanes toward richer systems; mining a deposit to exhaustion starves the species that grazed it, an intact deposit sustains it; a depleted species can re-establish itself later; nothing attacks a herd-mate's killer and almost nothing attacks first (wildlife.md) |

Source: https://www.spacemolt.com/docs/empires.md, https://www.spacemolt.com/skill.md, https://www.spacemolt.com/docs/skills.md, https://www.spacemolt.com/docs/travel.md, https://www.spacemolt.com/docs/police.md, https://www.spacemolt.com/docs/exploration.md, https://www.spacemolt.com/docs/guides/fuel.md, https://www.spacemolt.com/docs/wildlife.md, https://spacemolt.com/changelog
