# The store itself -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## source

snapshot bookkeeping: every file the snapshot tables were read from: size, mtime, when loaded (t), rows, and why not (note)

- Kind: bookkeeping
- Columns: name, loader, size, mtime, t, rows, note; one row per name
- Kept: not over time: store.Pass.fleet, store.Pass.forget, store.Pass.run delete rows, what stands is the newest
- Refreshed: the store's pass (every 60 s), by store.Pass.keep
- Which files could not be read, and why: `SELECT name, note FROM source WHERE note <> ''`
- How fresh is each loader's newest file: `SELECT loader, COUNT(*) AS files, datetime(MAX(mtime), 'unixepoch') AS newest_file, datetime(MAX(t), 'unixepoch') AS loaded FROM source GROUP BY loader`
- The largest files: `SELECT name, size, rows FROM source ORDER BY size DESC LIMIT 10`

## cursor

history bookkeeping: where each record (routes/runs.jsonl, market/history.jsonl, wildlife/history.jsonl, observations/<division>.jsonl) was read to, by byte

- Kind: bookkeeping
- Columns: record, offset, head; one row per record
- Kept: for good, bounded: one row per record the store reads (store.RECORDS), its place in the record (retention.py BOUNDED)
- Refreshed: the store's pass (every 60 s), by store.take_record
- Where is each record read to?: `SELECT record, offset FROM cursor ORDER BY record`
- How far is the run record read?: `SELECT offset FROM cursor WHERE record = 'routes/runs.jsonl'`
- How many records are read?: `SELECT COUNT(*) FROM cursor`

## meta

the store's settings: the sealed hour (day) of each raw table, the snapshot schema's version and its tables

- Kind: bookkeeping
- Columns: key, value; one row per key
- Kept: not over time: needs.setup deletes rows, what stands is the newest
- Refreshed: the store's pass (every 60 s), by docs.keep, docs.mark_baselines, needs.compute, needs.setup and 5 more
- Which hours and days are sealed?: `SELECT key, datetime(value, 'unixepoch') FROM meta WHERE key LIKE 'sealed.%'`
- Which snapshot schema is in use?: `SELECT value FROM meta WHERE key = 'snapshot.schema'`
- Every setting: `SELECT key, value FROM meta ORDER BY key`
