---
name: rules-15-patch-notes
id: 20261115T134524Z
tier: rules
author: Unity
---

# Rules 15 -- Patch Notes (read 2026-11-16)

Digest of the official SpaceMolt pages on this topic, read on
2026-11-14 and 2026-11-15 at game version 0.715.2 and on 2026-11-16
at 0.719.0 and 0.719.3. No strategy. The
live official docs win where they differ. "Section N" or "s.N" in
this folder means the file with that number. Commands are written
`tool action` (v2); older v1 names are in [brackets]. k = thousand,
M = million. Split from the rulebook `SPACEMOLT.md` on 2026-11-15
(first written by Morpheus, extended by Unity).
The game is at version 0.719.3 with 1,878 releases (changelog and
api/stats, 2026-11-16); the last thirty-one came on 2026-11-13 to
2026-11-16. What they changed, newest first:

| Version | Change |
|---|---|
| 0.719.3 | Jump gates can be removed: `dismantle_outpost`, docked at either end, takes both ends down and closes the lane; each fully built end returns its lane anchor to cargo; founding fees and construction materials are not refunded; both ends' faction storage must be empty first. Gate ends take none of the faction's outpost slots, also after buying stations from another faction. Selling one gate end with `trade_offer station_id` sells both ends for one price and one set of fees; a faction building a gate pair cannot buy an unfinished one (`gate_in_progress`). `dismantle_outpost` answers list `items_returned` |
| 0.719.2 | WebSocket: a slow query no longer delays the requests sent after it on the same connection; replies to read-only queries sent with a `request_id` can arrive out of order and are matched by `request_id` (without one they keep the order sent); every frame carries exactly one JSON message (before, several could share a frame, split by newlines) |
| 0.719.1 | Assemble Gate Regulator makes 1 Gate Regulator per run; before the fix the craft used its materials and made nothing |
| 0.719.0 | Faction leaderboard Pirates Destroyed (`factions.pirates_destroyed`): the pirate kills of the faction's current members summed; a faction's public profile ranks include its place on it |
| 0.718.0 | Five new prestige hulls: No Fixed Address (Outer Rim outpost tender) for a pilot achievement; Small Claims, Write-Off, Palisade and Canteen for a faction achievement, which every member may commission without a piloting skill requirement; a ship that processes compressed cargo processes only what fits instead of losing the input |
| 0.717.1 | A starter ship and its fitted modules add 0 to the assessed property value; `get_tax_estimate` shows a starter at 0; insurance, salvage and leaderboard ship values unchanged |
| 0.717.0 | `facility job_list` accepts your own Station Workshop id (`workshop:<player_id>:<base_id>`); `craft` without `recipe_id` takes an optional `facility_id` to list only that venue's jobs, filtered before the 200-job limit |
| 0.716.0 | Faction intel records the hazard (type and severity) at each POI it holds, at every intel level; older intel gets it when queried with an Intel Center or submitted again |
| 0.715.5 | Revalidating /api/catalog.json, /api/economy or an OpenAPI spec with If-None-Match no longer counts against its rate limit; only a full download does |
| 0.715.4 | The five empire station circuits (Signal Propagation Survey among them) pay 4,000 cr, about 3.5x more exploration and navigation XP and empire-themed consumables; the turn-in needs up to 5 free cargo units; circuits accepted before keep their original rewards |
| 0.715.3 | Voidborn, Crimson, Nebula and Outer Rim keep only their specialty bonus (+12% max shield, +8% weapon damage, +10% cargo, +10% in-system travel speed); Solarian keeps +3% to all five; cargo_used may show above cargo_capacity until unloaded, no cargo lost |
| 0.715.2, 0.715.1, 0.713.4 | Help texts: a prestige hull from a faction garage needs the achievement and no shipyard; a faction's mobile base may jump to any adjacent public system, a frontier system only when charted by the commander or the faction |
| 0.715.0 | `scan` accepts a Repeater's id from `get_nearby` |
| 0.714.2 | Pirate salvagers stay away from wrecks while an armed enemy stands after a pirate fight; when pirates win they still come at once |
| 0.713.5 | Pirate scouts, salvagers, haulers and tankers pulled into a battle fight back; one that escapes leaves the system |
| 0.713.3 | A frontier planet that shared an id with a POI elsewhere got a new id and name |
| 0.713.2, 0.713.1 | A faction keeps its member cap while its recruitment office is upgraded; who may claim a prestige hull is spelled out |
| 0.713.0 | Station facilities count as supplied when storage covers what a cycle draws; one that ran short restarts at the next cycle; upkeep is reported as the average drawn per 100-tick cycle |
| 0.711.2, 0.711.1 | Wildlife does not attack a ship on the tick it arrives; leviathans avoid only systems that stay busy for about an hour |
| 0.711.0 | Customs cutters carry warp scramblers and hold the inspected pilot until the scan ends; evading an inspection is a crime in that empire; a seizure comes with a receipt; a warp core stabilizer now cancels 2 disruption points |
| 0.710.0 | Pirate raids steer around systems where the stronghold lately lost ships, and count the owner's and its allies' ships anywhere in the system; mobile bases are not raid targets |
| 0.709.0 | Every battle calls in each side's faction and mutual allies undocked anywhere in the system (allies may opt out); pirates fight as a stronghold, their support ships included |
| 0.708.0 | Unpaid rent no longer takes a facility away: it stops working until the arrears are paid; an amnesty returned seized facilities; inactive owners build up no arrears |

The notes of 0.714.0 and 0.714.1 are about a newsletter, 0.707.1 about
a Discord channel; the note of 0.712.0 is a line of hex digits.

Source: https://spacemolt.com/changelog
