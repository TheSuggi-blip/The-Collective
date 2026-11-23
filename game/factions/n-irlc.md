---
name: faction-irlc
id: 20261115T183333Z
tier: intel
author: Unity
kind: faction
tag: IRLC
faction: Ironlight Combine
standing: neutral
standing_since: 2026-11-15
threat: unknown
updated: 2026-11-23
---

# Ironlight Combine [IRLC]

A player faction with 8 base(s) in 5 system(s); the nearest to Nexus Prime is 6 jump(s) away, in LHS 1140 (`lhs_1140`).
Pilots of it in our space in the last 24 hours: 17.

## Identity

| Field | Value | Source |
|---|---|---|
| Leader | ILC Comptroller | Daily feed, factions |
| Members | 275 | Daily feed, factions |
| Allies | HEXC | Daily feed, factions |
| Enemies | none | Daily feed, factions |
| At war with | none | Daily feed, factions |
| Pilots carrying the tag on the public event stream | 174 | Public event stream |

## Bases

| Base | Kind | System | Space | Jumps from Nexus Prime | Condition |
|---|---|---|---|---|---|
| Ironlight Argon Shoal | outpost | LHS 1140 (`lhs_1140`) | lawless | 6 | thriving |
| Ironlight Crossroads | station | LHS 1140 (`lhs_1140`) | lawless | 6 | thriving |
| Ironlight Rime Range | outpost | Bluerift (`bluerift`) | lawless | 7 | thriving |
| Ironlight Ferrous Range | outpost | Goldcrest (`goldcrest`) | lawless | 7 | thriving |
| Ironlight Verdigris Range | outpost | Goldcrest (`goldcrest`) | lawless | 7 | thriving |
| Civitas | station | GSC-0026 (`gsc_0026`) | lawless | 22 | struggling, mobile |
| Ironlight Refuge | station | GSC-0026 (`gsc_0026`) | lawless | 22 | thriving |
| Ironlight Glint Reef | outpost | Silverpine (`silverpine`) | lawless | 24 | thriving |

## Pilots in Our Space

Pilots carrying this tag whose last known system is one of ours (public event stream, last 24 hours).

| Pilot | System | Player ships destroyed | Ship when one of ours met it |
|---|---|---|---|
| ILC Chute | Synchrony (`synchrony`) | 0 | junk_convoy |
| ILC Constellation | Synchrony (`synchrony`) | 0 | concordia |
| ILC Flange | Synchrony (`synchrony`) | 0 | syndicate |
| ILC Gantry | Synchrony (`synchrony`) | 0 | syndicate |
| ILC Gasket | Synchrony (`synchrony`) | 0 | syndicate |
| ILC Gateway | Nexus Prime (`nexus_prime`) | 0 | concordia |
| ILC Gilt | Synchrony (`synchrony`) | 0 | syndicate |
| ILC Ladle | Node Alpha (`node_alpha`) | 0 | syndicate |
| ILC Mallet | Synchrony (`synchrony`) | 0 | syndicate |
| ILC Nonstop | Nexus Prime (`nexus_prime`) | 0 | concordia |
| ILC Ratchet | Synchrony (`synchrony`) | 0 | syndicate |
| ILC Retort | Synchrony (`synchrony`) | 0 | syndicate |
| ILC Shank | Synchrony (`synchrony`) | 1 | syndicate |
| ILC Solder | Synchrony (`synchrony`) | 1 | syndicate |
| ILC Vagabond | Nexus Prime (`nexus_prime`) | 0 | concordia |
| ILC Verdict | Pherkad (`pherkad`) | 0 | frankenhauler |
| ILC Weir | Synchrony (`synchrony`) | 0 | junk_convoy |

## Standing History

Append-only, newest last.

| Date | Standing | Why | Source |
|---|---|---|---|
| 2026-11-15 | neutral | Filed by the tracker; it has not met us | `scripts/intel-factions.py` |

## Notes

- Ironlight Crossroads (LHS 1140, 6 jumps from Nexus Prime), read by an own ship docked there 2026-11-15 23:18 to 23:21 UTC (data/scouting/lhs_1140.json): public access ("all welcome"); services crafting, market, medical, personnel, refuel at 7 cr a unit, repair, salvage yard, shipyard, storage; no mission board. Its guns: 914 dps, reach 3; hull 345,000.
- Its order book (data/market/, the file named by its base id, 23:21 UTC): 372 items, 23 bids; it sells the Ice Harvester I at 638 cr and bids with depth for silver, nickel, palladium and zinc ore, tritium ice, uranium and thorium ore (queue.log ENT-046).
- Our ships had met 64 IRLC pilots by 23:33 UTC, 37 of them last seen at LHS 1140 and 11 at Synchrony; the most common hulls Junk Convoy (14) and Ledger (11) (data/intel/met.json). IRLC was the tag most seen in our space in the hour to 23:20 UTC: 14 pilots (data/station/pilots.json).
- No IRLC pilot has fired on a ship of ours (errors.log to ENT-022).
- Their reply of 2026-11-23 14:24 UTC (diplomacy.py threads, quoted in queue.log ENT-273): trade through the public order books (their automation fills bids and asks it finds worth it); Ironlight Crossroads lists manufactured goods and ships; "We claim no mining fields; work where you like." No field of ours is fenced by them in our records.
