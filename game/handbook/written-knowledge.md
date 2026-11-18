# Written knowledge -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## docs

now: the fleet's written knowledge by section (docs.py): the rulebook (each rule F<n> of section 12 its own section), the newest entry of communications/orders.log (head, each S/G/D/P line, each block and member's block), governance/strategy.md and empire.md, the guidebooks and templates of each division, game/rules/*.md row by row: kind, owner, section id, n (its place in the file), title, text, sha, chars, t (the file's mtime); hive.py docs

- Kind: snapshot
- Columns: path, kind, owner, section, n, title, text, sha, chars, t, src; one row per path, section
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `docs`, the files of every kind of docs.KINDS (The kinds, in game/handbook/written-knowledge.md)
- The sections of the rulebook in their order: `SELECT section, chars, title FROM docs WHERE path = 'governance/rulebook.md' ORDER BY n`
- One rule whole: `SELECT title, text FROM docs WHERE path = 'governance/rulebook.md' AND section = 'F8'`
- The sections that name a word: `SELECT path, section, title FROM docs WHERE text LIKE '%wallet%' ORDER BY path, n`

## doc_versions

history: every version of every section of docs, kept for good: a new row when a section's sha is new (version rises), first_seen, last_seen (the last pass it stood; a section that left its file keeps its rows); hive.py changes, docs --history

- Kind: history
- Columns: version, path, section, sha, title, text, first_seen, last_seen; one row per version
- Kept: for good: no step of the code deletes its rows
- Refreshed: the store's pass (every 60 s), by docs.keep
- Sections changed in the last 24 hours (a section's first version is no change): `SELECT v.path, v.section, v.title, datetime(v.first_seen, 'unixepoch') AS changed FROM doc_versions v WHERE v.first_seen >= strftime('%s', 'now') - 86400 AND v.version > (SELECT MIN(w.version) FROM doc_versions w WHERE w.path = v.path AND w.section = v.section) ORDER BY v.first_seen DESC`
- Every version of rule F8: `SELECT version, sha, datetime(first_seen, 'unixepoch'), datetime(last_seen, 'unixepoch'), LENGTH(text) FROM doc_versions WHERE path = 'governance/rulebook.md' AND section = 'F8' ORDER BY version`
- Sections that left their file: `SELECT v.path, v.section, MAX(v.title), datetime(MAX(v.last_seen), 'unixepoch') FROM doc_versions v WHERE NOT EXISTS (SELECT 1 FROM docs d WHERE d.path = v.path AND d.section = v.section) GROUP BY v.path, v.section`

## The kinds

What docs.py mirrors into the tables docs and doc_versions (docs.KINDS); the files stay the source.

| Kind | Files | Owner | Ask |
|---|---|---|---|
| rulebook | `governance/rulebook.md` | Fleet | docs doc=rulebook (hive.py docs rulebook) |
| orders | `communications/orders.log` | Unity | docs doc=orders (hive.py docs orders); comms view=orders |
| strategy | `governance/strategy.md` | Fleet | docs doc=strategy (hive.py docs strategy) |
| empire | `governance/empire.md` | Fleet | docs doc=empire (hive.py docs empire) |
| guide | `game/routes/guidebook/*/*.md` | the division its file's name or folder names | docs doc=guide (hive.py docs guide) |
| guidebook | `game/routes/guidebook/*.md` | the division its file's name or folder names | docs doc=guidebook (hive.py docs guidebook); docs view=division |
| template | `game/routes/templates/*.json` | the division its file's name or folder names | docs doc=template (hive.py docs template) |
| rules | `game/rules/*.md` | Fleet | docs doc=rules (hive.py docs rules) |
| metrics | `game/metrics.md` | Fleet | docs doc=metrics (hive.py docs metrics); fleet view=<figure> |
| handbook | `game/handbook.md`, `game/handbook/*.md` | Fleet | docs doc=handbook (hive.py docs handbook); docs view=handbook (hive.py handbook) |
| plan | `data/plans/plan-*.md` | the division its file's name or folder names | docs doc=plan (hive.py docs plan); plan action=show; docs view=division |
| report | `reports/*.md` | the division its file's name or folder names | docs doc=report (hive.py docs report) |
| log | `communications/archive/requests-*.log`, `communications/requests.log`, `communications/archive/queue-*.log`, `communications/queue.log`, `communications/archive/admirals-*.log`, `communications/admirals.log`, `communications/archive/errors-*.log`, `communications/errors.log`, `communications/archive/reports-*.log`, `communications/reports.log` | each entry's author's division | docs doc=log (hive.py docs log); comms view=requests, view=digest |
| member | `data/docs/members/**/*.md` | the division its file's name or folder names | docs doc=member (hive.py docs member); docs view=division |
