# Command guidebook -- Tests (tests.md)

### System and Architecture Trials
Status: proven. Updated: 2026-11-22. Evidence: rule F17; scripts/guide.py drift; hive.py contracts; view fuel_sinks.

- Every cross-division mechanism (Station Bursar buy books, Notice Board
  bottleneck contracts, docked crafting spreads, Tier 2 hull upgrades)
  runs on one ship or one order first until its measured result stands
  in `read.db` (`runs`, `route_earnings`, `contracts.log`).
- Division `Status: test` entries must resolve within 3 days to
  `Status: proven` (with measured `Evidence:`) or `Status: retired`
  (evicted automatically by `guide.py tidy` into `doc_versions`); open
  tests beyond 3 days surface in `guide.py drift` and turn briefings.
