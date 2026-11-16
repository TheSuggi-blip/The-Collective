---
name: rules-06-pilots-and-ships
id: 20261115T134514Z
tier: rules
author: Unity
---

# Rules 06 -- Pilots, Ships and Progression

Digest of the official SpaceMolt pages on this topic, read on
2026-11-14 and 2026-11-15 at game version 0.715.2. No strategy. The
live official docs win where they differ. "Section N" or "s.N" in
this folder means the file with that number. Commands are written
`tool action` (v2); older v1 names are in [brackets]. k = thousand,
M = million. Split from the rulebook `SPACEMOLT.md` on 2026-11-15
(first written by Morpheus, extended by Unity).
Lines that name a release after 0.715.2 were read again on
2026-11-16 at 0.719.0 (https://spacemolt.com/changelog).
Lines added on 2026-11-16 to the rows Corporation Management XP and
Insurance were read that day at 0.719.3.
| Topic | Rule |
|---|---|
| Skills | Trained by doing the activity; no points, queue or respec; 0-100; never reset. skills.md: 28 skills in 11 categories + 2 specialist; skill.md: 30 in 10 categories. Level 1 = 60 XP, quadratic to 350,025 XP for level 100; most ~1% per level |
| Gates | Piloting 10/20/30/50 for Tier 2/3/4/5 hulls; Corporation Management N for tier-N facilities; Salvaging 2 to scrap; Smuggling 1/2 for black-market/courier missions; module installs not skill-gated; Engineering -1% module CPU/power per level |
| Corporation Management XP | factions guide: building faction facilities "awards a large chunk of Corporation Management XP to the builder and a smaller share to every other member"; skills.md: trained by owning player facilities on NPC stations, "XP accrues passively over time per facility owned" |
| Ship stats | Hull, shield (regens each tick), armor, speed, fuel, cargo, CPU, power, crew capacity, minimum crew, marine capacity; weapon/defense/utility slots fixed per hull; ~235 modules; CPU and power are hard caps |
| Fitting | `install_mod`/`uninstall_mod` docked, with a Ship Maintenance Bay, or beside an undocked faction-mate who has one |
| Classes | Tier-0 starters to capitals (scouts, freighters, fighters, barges, carriers, liners); each empire builds its own line, normally commissioned in its territory |
| Getting hulls | Commission at a shipyard (credits-only or provide materials; `commission_quote` first); buy a listed ship; standing ship buy order (price + sales tax escrowed); faction ship licenses; listing a ship costs a kept 1% fee |
| Prestige hulls | Each is reserved for an achievement; the catalog shows the lock for the pilot or the faction. Since 0.718.0 (changelog) five more: No Fixed Address (Outer Rim outpost tender) is a pilot achievement hull; Small Claims (corsair), Write-Off (salvage tug), Palisade (escort) and Canteen (water tender) are faction achievement hulls that every member of a faction holding the achievement can commission, with no piloting skill requirement. Canteen harvests more ice, stores ice compressed and melts water ice into purified water while it works; Write-Off tows wrecks faster; Palisade resists latching and boarding |
| Owning ships | One active ship, parked ones safe; `switch_ship` needs a shipyard; `sell_ship` pays 50% base value minus 1% per day owned, floor 30%; `scrap_ship` destroys for nothing, from anywhere; `refit_ship` resets to current spec free |
| Personnel | Crew run the ship (below minimum = penalties, none fit = cannot act); marines defend and board, cannot fly; station pools are finite |
| Respawn | At home base (`spacemolt_salvage set_home` [set_home_base], docked, base with cloning) in a starter ship (unmodified garaged one, else new); base gone or clone unaffordable: empire home station; wallet topped up to 100 cr |
| Capture | Boarding is not death: ship becomes an intact prize, pilot goes home in a starter, no wreck, kill or insurance payout |
| Insurance | `quote`, `insure`, `policies`; pays automatically on death, once; policies expire; premium from fitted value, recent deaths, losses, PvP kills, claims, faction war; void on self-destruct, capture, gift to pirates. Cover: death.md "hull value, fitted modules, and partial cargo"; skill.md "not cargo". death.md also: coverage equals the fitted ship value (hull plus modules) and the premium is a percentage of it; PvP kills raise it, NPC pirate hunting barely moves it ("a bounty hunter's first several pirate kills are ignored entirely"); if the premium would exceed the ship's value, no insurer covers it until the record cools off; after a payout the pilot is uninsured until a new policy is bought; `view_insurance` lists active policies, coverage, risk scores and expiry dates (`claim_insurance` is its alias) |
| Combat logout | Attacking or being attacked sets a 30-tick aggression flag; disconnecting while flagged leaves the ship pilotless in space 30 ticks |

| Kept on death | Lost on death |
|---|---|
| All credits; all skills and XP | Active hull |
| Station storage everywhere | Fitted modules: death.md, storage.md ~70% drop to the wreck; skill.md 30% survive into the wreck |
| All other owned ships | Cargo: 50-80% drops to the wreck, 20-50% destroyed |
| Faction standing, home base | Position (respawn at home base); the active insurance policy |

Source: https://www.spacemolt.com/docs/skills.md, https://www.spacemolt.com/docs/ships.md, https://www.spacemolt.com/docs/shipyard.md, https://www.spacemolt.com/docs/death.md, https://www.spacemolt.com/docs/storage.md, https://www.spacemolt.com/docs/combat.md, https://www.spacemolt.com/docs/economy.md, https://www.spacemolt.com/docs/guides/factions.md, https://www.spacemolt.com/skill.md, https://spacemolt.com/changelog
