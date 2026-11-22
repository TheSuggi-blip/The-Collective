# Map and intel -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## systems

the map: every star system, its empire (NULL lawless), capital (home), stronghold and jumps from our home (station/map.json, else game/map/galaxy.tsv)

- Kind: snapshot
- Columns: id, name, x, y, empire, home, stronghold, jumps, src; one row per id
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `map`, station/map.json; while it is missing, the repository's chart game/map/galaxy.tsv stands in
- Systems within 3 jumps of home: `SELECT id, name, empire, jumps FROM systems WHERE jumps <= 3 ORDER BY jumps, id`
- The empires' capitals and strongholds: `SELECT id, name, empire, home, stronghold FROM systems WHERE home = 1 OR stronghold = 1`
- The nearest lawless systems: `SELECT id, jumps FROM systems WHERE empire IS NULL ORDER BY jumps LIMIT 10`

## lanes

the map: the jump lanes, one row per direction as the map lists them

- Kind: snapshot
- Columns: a, b, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `map`, station/map.json; while it is missing, the repository's chart game/map/galaxy.tsv stands in
- The neighbours of nexus_prime: `SELECT b FROM lanes WHERE a = 'nexus_prime'`
- Systems with the most lanes: `SELECT a, COUNT(*) FROM lanes GROUP BY a ORDER BY 2 DESC LIMIT 10`
- Lanes that cross a border: `SELECT l.a, x.empire, l.b, y.empire FROM lanes l JOIN systems x ON x.id = l.a JOIN systems y ON y.id = l.b WHERE COALESCE(x.empire, '') <> COALESCE(y.empire, '') LIMIT 20`

## places

now: every place (POI) of a system our census read: its kind, name, class and the base on it (scouting/<system>.json)

- Kind: snapshot
- Columns: system, poi, kind, name, class, base, x, y, t, src; one row per system, poi
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `scouting`, data/scouting/*.json
- The stations among the places we read: `SELECT system, poi, name, base FROM places WHERE base IS NOT NULL`
- Places per kind: `SELECT kind, COUNT(*) FROM places GROUP BY kind ORDER BY 2 DESC`
- The places of node_beta: `SELECT poi, kind, name FROM places WHERE system = 'node_beta'`

## fields

now: what is left in each resource field of a place, by the newest census (scouting/<system>.json)

- Kind: snapshot
- Columns: system, poi, resource, remaining, max_remaining, richness, t, src
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `scouting`, data/scouting/*.json
- Where iron_ore is left: `SELECT system, poi, remaining, max_remaining, datetime(t, 'unixepoch') FROM fields WHERE resource = 'iron_ore' AND remaining > 0 ORDER BY remaining DESC`
- What is left in all fields, per resource: `SELECT resource, SUM(remaining), COUNT(*) FROM fields GROUP BY resource ORDER BY 2 DESC`
- Fields within 3 jumps of home: `SELECT f.system, f.poi, f.resource, f.remaining, y.jumps FROM fields f JOIN systems y ON y.id = f.system WHERE y.jumps <= 3 AND f.remaining > 0 ORDER BY y.jumps, f.remaining DESC`

## herds

now: the creatures at a place by species, counted by the newest census (wildlife/<system>.json)

- Kind: snapshot
- Columns: system, poi, creature, name, role, count, t, src
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `wildlife`, data/wildlife/*.json
- The largest herds: `SELECT system, poi, creature, count FROM herds ORDER BY count DESC LIMIT 10`
- Where cauldronbacks live: `SELECT system, poi, count FROM herds WHERE creature = 'cauldronback'`
- Animals per system: `SELECT system, SUM(count) FROM herds GROUP BY system ORDER BY 2 DESC`

## readings

history: one row per census count of a field (units left) or a herd (animals) at a place, the raw rows of --keep-days days

- Kind: history
- Columns: system, poi, what, kind, amount, t; one row per system, poi, what, t
- Kept: 7 days (store.py KEEP_DAYS, --keep-days), then deleted by whole days
- Refreshed: the store's pass (every 60 s): the new whole lines of data/wildlife/history.jsonl
- The newest field counts in node_beta: `SELECT poi, what, amount, datetime(t, 'unixepoch') FROM readings WHERE system = 'node_beta' AND kind = 'field' ORDER BY t DESC LIMIT 20`
- Herds counted at 0: `SELECT system, poi, what, datetime(t, 'unixepoch') FROM readings WHERE kind = 'herd' AND amount = 0 ORDER BY t DESC LIMIT 20`
- Readings per system: `SELECT system, COUNT(*) FROM readings GROUP BY system ORDER BY 2 DESC`

## reading_day

history: per place, field or herd and UTC day the first and the last count; kept for good while retention.py is off (on: 400 days)

- Kind: history
- Columns: system, poi, what, kind, day, first, last, t_first, t_last; one row per system, poi, what, day
- Kept: for good while retention.py RETAIN_ENABLED is off; on: 400 days by `day`, then deleted (hourly, at most 5000 rows a table and pass)
- Refreshed: the store's pass (every 60 s): summed again for the days that got new rows of readings
- How the fields changed per day: `SELECT system, poi, what, date(day, 'unixepoch') AS day, first, last, last - first AS change FROM reading_day WHERE kind = 'field' ORDER BY day DESC, change LIMIT 20`
- Herds that shrank in a day: `SELECT system, poi, what, date(day, 'unixepoch'), first, last FROM reading_day WHERE kind = 'herd' AND last < first ORDER BY day DESC`
- Days on record per system: `SELECT system, COUNT(DISTINCT day) FROM reading_day GROUP BY system ORDER BY 2 DESC`

## stations

every station and outpost of the galaxy: kind, system, its owner's faction tag and name, condition, services (station/stations.json)

- Kind: snapshot
- Columns: name, kind, system, tag, faction, empire, condition, services, wrecked, mobile, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `stations`, data/station/stations.json
- Which stations and outposts lie within 3 jumps of our home, and who owns them: `SELECT s.name, s.kind, s.system, y.jumps, s.tag, s.faction FROM stations s JOIN systems y ON y.id = s.system WHERE y.jumps <= 3 ORDER BY y.jumps, s.system, s.name`
- Stations per faction: `SELECT tag, faction, COUNT(*) FROM stations GROUP BY tag, faction ORDER BY 3 DESC`
- Wrecked or mobile stations: `SELECT name, system, kind, wrecked, mobile FROM stations WHERE wrecked = 1 OR mobile = 1`

## factions

every faction of the game: tag, name, members, leader, allies, enemies, wars as comma text (station/feed.json)

- Kind: snapshot
- Columns: tag, name, members, leader, allies, enemies, wars, src; one row per tag
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `factions`, data/station/feed.json
- The largest factions: `SELECT tag, name, members, leader FROM factions ORDER BY members DESC LIMIT 10`
- Factions at war: `SELECT tag, name, wars FROM factions WHERE wars <> ''`
- The owners of stations within 5 jumps: `SELECT DISTINCT f.tag, f.name, f.members FROM stations s JOIN systems y ON y.id = s.system JOIN factions f ON f.tag = s.tag WHERE y.jumps <= 5`

## met

the pilots of OTHER players our ships met: faction, ship class, where last seen, first and last seen (t), times met (intel/met.json)

- Kind: snapshot
- Columns: name, faction, class, system, poi, first, t, times, in_combat, src; one row per name
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `met`, data/intel/met.json
- Pilots of others seen in the last hour: `SELECT name, faction, class, system, datetime(t, 'unixepoch') FROM met WHERE t >= strftime('%s', 'now') - 3600 ORDER BY t DESC`
- The factions we meet most: `SELECT faction, COUNT(*), SUM(times) FROM met GROUP BY faction ORDER BY 3 DESC LIMIT 10`
- Pilots seen in combat: `SELECT name, faction, system, datetime(in_combat, 'unixepoch') FROM met WHERE in_combat IS NOT NULL ORDER BY in_combat DESC`

## observations

history: one row per observation a member wrote with observe.py (observations/<division>.jsonl): division, member, kind, subject, when it was seen (t, at), note; `fields` is JSON text, one field read by json_extract(fields, '$.<key>'); kept 30 days at least

- Kind: history
- Columns: division, member, kind, subject, t, at, fields, note, digest; one row per division, kind, subject, t, digest
- Kept: 30 days (store.py KEEP_TABLES), then deleted by whole days
- Refreshed: the store's pass (every 60 s): the new whole lines of data/observations/<division>.jsonl (6 records)
- The newest observations of every division: `SELECT at, division, member, kind, subject, fields, note FROM observations ORDER BY t DESC LIMIT 20`
- Every kind on record: its rows, its newest time, which division: `SELECT kind, division, COUNT(*) AS n, datetime(MAX(t), 'unixepoch') AS newest FROM observations GROUP BY kind, division ORDER BY n DESC`
- Prices seen at stations we read no book of (kind price): fields read by json_extract: `SELECT at, subject AS station, json_extract(fields, '$.item') AS item, json_extract(fields, '$.bid') AS bid, json_extract(fields, '$.ask') AS ask FROM observations WHERE kind = 'price' ORDER BY t DESC LIMIT 20`
