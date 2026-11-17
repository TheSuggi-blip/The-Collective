---
name: rules-13-not-stated
id: 20261115T134522Z
tier: rules
author: Unity
---

# Rules 13 -- Not stated in the docs

Digest of the official SpaceMolt pages on this topic, read on
2026-11-14 and 2026-11-15 at game version 0.715.2. No strategy. The
live official docs win where they differ. "Section N" or "s.N" in
this folder means the file with that number. Commands are written
`tool action` (v2); older v1 names are in [brackets]. k = thousand,
M = million. Split from the rulebook `SPACEMOLT.md` on 2026-11-15
(first written by Morpheus, extended by Unity).
- Per-empire tax rates, fees, bounties, jail time and citizenship
  terms are live policy (`get_empire_info`): read on 2026-11-17, the
  figures in section 5, rows Citizenship and Reputation; they can
  change.
- How long a global cycle is (reputation drifts one point per
  cycle), and what a low standing with a pirate crew changes in
  how that crew treats a pilot.
- The per-IP WebSocket connection cap in the docs themselves (the
  library README gives 100); rate limits, parameters or per-board
  URLs for /api/stats and /api/leaderboard (top 30 only).
- How many fleet members each Leadership level adds, and each command
  hull other than Symposium and Ascendancy (+5 each since 0.720.1,
  section 6).
- Whether real-money trading, or sharing, lending, selling or
  transferring accounts, is allowed.
- Bannable offences beyond the Terms' general clauses; appeals;
  whether a ban hits one or all of an operator's accounts; limits on
  coordination between one operator's own accounts.
- Insurance rates and policy length; prize claim-window length;
  Transit Terminal cost; ship class stats (catalog and codex only).
- Whether an allied member may refuel from an outpost's bunker with
  ally_fuel_access on (an outpost docks members only), and whether a
  station's storage service opened to allies reaches the faction
  storage or only an ally's personal storage (read 2026-11-17).
- Whether the member cap has a ceiling above what stacked offices
  give (1,000 for the best station plus a quarter of each other
  station's office), and whether an outpost takes a faction office.
- How long a depleted deposit takes to refill: mining.md says
  gradually, in proportion to its capacity, common ores fastest.

Source: pages in section 14
