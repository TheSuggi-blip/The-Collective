# Other -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## tourism_snapshots

hourly snapshots of galactic station tourism appeal and cumulative tourism revenue leaderboards

- Kind: snapshot
- Columns: bucket_h, station, system, board, rank, value, t, src; one row per bucket_h, station, board
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `leaderboards`, data/station/leaderboard.json
- No example is written for it yet (store.EXAMPLES).
