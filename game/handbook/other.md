# Other -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## rival_snapshots

hourly time-series snapshots of rival factions and blocs (members, bases, all 11 leaderboard metrics, live SSE active_1h/24h, hull tiers, alliances) recorded automatically into intel/rival_history.jsonl

- Kind: snapshot
- Columns: t, tag, name, members, bases, wrecked, wealth, ship_value, storage_value, facility_inv, ore_mined, items_crafted, missions, damage_dealt, kills_pve, kills_pvp, active_1h, active_24h, max_tier, avg_tier, allies, base_systems, src; one row per t, tag
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `rival_snapshots`, data/intel/rival_history.jsonl
- Latest snapshot per top faction by wealth: `SELECT tag, name, members, bases, wealth, active_1h, datetime(t, 'unixepoch') AS at FROM rival_snapshots WHERE t = (SELECT MAX(t) FROM rival_snapshots) ORDER BY wealth DESC LIMIT 15`
- Wealth and member deltas across earliest vs latest stored snapshots: `SELECT a.tag, b.members - a.members AS d_members, b.wealth - a.wealth AS d_wealth, b.bases - a.bases AS d_bases FROM rival_snapshots a JOIN rival_snapshots b ON a.tag = b.tag WHERE a.t = (SELECT MIN(t) FROM rival_snapshots) AND b.t = (SELECT MAX(t) FROM rival_snapshots) ORDER BY d_wealth DESC LIMIT 15`
- Count of stored hourly snapshots and distinct factions tracked: `SELECT COUNT(DISTINCT t) AS snapshots, COUNT(DISTINCT tag) AS factions FROM rival_snapshots`
