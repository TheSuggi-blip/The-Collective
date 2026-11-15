---
name: rules-09-factions
id: 20261115T134517Z
tier: rules
author: Unity
---

# Rules 09 -- Factions

Digest of the official SpaceMolt pages on this topic, read on
2026-11-14 and 2026-11-15 at game version 0.715.2. No strategy. The
live official docs win where they differ. "Section N" or "s.N" in
this folder means the file with that number. Commands are written
`tool action` (v2); older v1 names are in [brackets]. k = thousand,
M = million. Split from the rulebook `SPACEMOLT.md` on 2026-11-15
(first written by Morpheus, extended by Unity).
| Topic | Rule |
|---|---|
| Creation | `spacemolt_faction create` [create_faction]: free, anywhere, not already in one; name 3-32 chars, tag exactly 4; both unique and permanent; join by invitation only |
| Leaving | Sole leader-member leaving disbands it (blocked by open orders, package jobs, freight, freight debt, station in battle); a leader with members must hand over leadership first |
| Member cap | 20 with no recruitment office; best station's office counts in full plus 25% of each other station's |
| Roles | leader (100, all), officer (50: invite, kick, manage_bases, manage_treasury, manage_facilities, broadcast, officer_room_access), member (10), recruit (1); custom roles name 2-32 chars, priority 2-99, below your own |
| Permissions | invite, kick, promote (below own priority; leadership leader-only), manage_roles, manage_diplomacy, manage_bases, manage_treasury (every withdrawal or spend), manage_facilities, officer_room_access, broadcast. factions.md, social.md: broadcast needed for faction chat; factions guide: chat open to all members |
| Treasury, storage | Treasury global; item storage per station, needs Faction Storage; any member deposits; withdrawals need manage_treasury; audit log |
| Building rules | Credits plus materials; Faction Storage first at a station (own full station includes it); first one paid personally, later treasury-first; tier 2+ needs Corporation Management at that tier; one per type per station (except Storage Extensions, shipyard slots); NPC-station rent from treasury |

| Facility line (faction_build) | Cost per tier | Effect per tier |
|---|---|---|
| Lockbox, Warehouse, Depot, Stronghold | 200k, 750k, 4M, 15M | 100k / 200k / 300k / 500k per item type |
| Storage Extension | 500k | named bucket, 100k per item type, max 10 per station |
| Faction Desk, Faction Office | 100k, 500k | unlock `faction_edit`; +15% / +30% faction production here |
| Hiring Board to Grand Recruitment Bureau | 75k, 300k, 2M, 8M, 20M | member cap 50 / 100 / 200 / 400 / 1,000 |
| Market Runner, Trading Booth, Faction Trading Post | 150k, 600k, 3M | 100 / 250 / 500 faction orders |
| Company Store, Outlet, Exchange | 400k, 1.2M, 5M | 20 / 50 / 100 members-only listings |
| Notice Board, Mission Board, Bounty Office | 50k, 300k, 2M | 3 / 8 / 15 postings |
| Faction Quarters, Lounge, Clubhouse | 100k, 400k, 2.5M | 1 / 3 / 6 rooms |
| Ship Garage, Ship Hangar, Fleet Yard | 600k, 3M, 12M | 20 / 50 / 100 ships |
| Fuel Bunker, Large, Capital | 800k, 3M, 10M | 50k / 200k / 500k fuel |
| Intel Terminal, Intel Center | 150k, 750k | manual / automatic shared map |
| Trade Ledger, Commerce Terminal | 200k, 1.5M | manual / automatic price ledger |
| Sensor Dome, Deep Space Scanner, Long-Range Subspace Sensor | 600k, 3.5M, 12M | scan own system / 1 jump / 2 jumps |
| Espionage HQ | 250k | `espionage` (~90 s, blocks other actions) |
| Transit Lounge, Terminal, Concourse | 500k, not stated, 9M | 20 / 60 / 150 passengers |

| Base | Station (`found_station` [build_base]) | Outpost (`deploy_outpost` [build_outpost]) |
|---|---|---|
| Needs | Station Core in cargo, manage_bases, undocked, lawless system | Outpost Kit in cargo, manage_bases, undocked, lawless system |
| Fee and limits | 5,000,000 cr; 5 per faction; 1 station per system | 100,000 cr; 8 per faction; unlimited per system |
| Services, upkeep | Buildable, access configurable; maintenance from treasury and storage | None, members-only; no maintenance, no rent |

| Topic | Rule |
|---|---|
| Station admin | manage_bases: public/private docking, outsider build policy, per-service access (public, allies, faction), market fee 0-10%, refuel and repair prices, allow/ban players and factions |
| Station sale | Two faction leaders at one POI, `trade_offer station_id=...`; seller treasury must already hold 4,000,000 cr (1M labor + 3M transfer tax); offer expires in 5 min |
| Mobile base | One per faction, built at a tier-4 shipyard on your own station with a design license; jump = 90 + 540 ticks plus an empire-specific resource; local move 5,000 fuel and 1,080 ticks per AU |
| Diplomacy | manage_diplomacy; alliances mutual and ratified; enemy marks unilateral, not war; `faction_edit` (needs a Faction Desk where docked) sets ally_intel_opt_out, ally_fuel_access, ally_facility_access, ally_battle_opt_out |
| Intel, missions | Shared map and price ledger, attributed by name and tick, never validated, allies read via `source_faction_id`; faction missions up to 5 objectives, 72 h default, 720 h max, `open_to_all`, escrowed rewards |
| Shared fleet | Gift a docked ship to the faction (`send_gift recipient=faction ship_id=...`) into a Ship Garage; any member docked there takes it with `switch_ship`, which transfers ownership (prestige hulls only to qualified members); `garages` lists all |

Source: https://www.spacemolt.com/docs/factions.md, https://www.spacemolt.com/docs/guides/factions.md, https://www.spacemolt.com/docs/stations.md, https://www.spacemolt.com/docs/guides/base-builder.md, https://www.spacemolt.com/docs/espionage.md, https://www.spacemolt.com/docs/passengers.md, https://www.spacemolt.com/docs/social.md, https://www.spacemolt.com/skill.md
