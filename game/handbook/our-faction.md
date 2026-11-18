# Our faction -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## faction

our faction, one row: tag, leader, members and their limit, treasury, bases owned, at war (empire/empire.json)

- Kind: snapshot
- Columns: id, name, tag, leader, member_count, members_limit, treasury, owned_bases, at_war, created, t, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `empire`, data/empire/empire.json
- Our faction: `SELECT tag, name, leader, member_count, members_limit, treasury, owned_bases, at_war FROM faction`
- Room for members: `SELECT member_count, members_limit, members_limit - member_count AS free FROM faction`
- Our faction beside the others by size: `SELECT f.tag, f.members, (SELECT COUNT(*) FROM factions g WHERE g.members > f.members) + 1 AS rank FROM factions f JOIN faction o ON o.tag = f.tag`

## faction_members

our faction's members and their roles (empire/empire.json)

- Kind: snapshot
- Columns: pilot, role, t, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `empire`, data/empire/empire.json
- Members per role: `SELECT role, COUNT(*) FROM faction_members GROUP BY role`
- Our ships that are no members: `SELECT pilot FROM ships WHERE pilot NOT IN (SELECT pilot FROM faction_members)`
- Members per division: `SELECT s.division, COUNT(*) FROM faction_members m JOIN ships s ON s.pilot = m.pilot GROUP BY s.division`

## bases

our faction's bases: base id, name, system, place, kind (empire/empire.json)

- Kind: snapshot
- Columns: base, name, system, poi, kind, t, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `empire`, data/empire/empire.json
- Our bases: `SELECT base, name, system, poi, kind FROM bases`
- Our bases and their jumps from home: `SELECT b.name, b.system, y.jumps FROM bases b LEFT JOIN systems y ON y.id = b.system ORDER BY y.jumps`
- Our ships docked at our bases: `SELECT b.name, COUNT(s.pilot) FROM bases b LEFT JOIN ships s ON s.base = b.base GROUP BY b.base`

## our_stations

view: the stations and outposts whose owner's tag is our faction's, joined to our bases

- Kind: view over stations, faction, bases
- Columns: name, kind, system, tag, faction, condition, services, wrecked, mobile, base, poi, base_kind
- Kept: nothing: a view stores no row
- Refreshed: computed when asked, from its tables
- Our stations and outposts: `SELECT name, kind, system, condition, base FROM our_stations`
- Our stations and their jumps from home: `SELECT o.name, o.system, y.jumps FROM our_stations o LEFT JOIN systems y ON y.id = o.system`
- Our stations that no base row of empire.json names: `SELECT name, system FROM our_stations WHERE base IS NULL`

## faction_facilities

our faction's facilities: type, level, base, status, rent per cycle (empire/empire.json)

- Kind: snapshot
- Columns: id, type, name, level, base, system, status, rent_per_cycle, t, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `empire`, data/empire/empire.json
- Our facilities and their rent: `SELECT name, type, level, base, status, rent_per_cycle FROM faction_facilities ORDER BY base`
- Rent per cycle in all: `SELECT SUM(rent_per_cycle) FROM faction_facilities`
- Facilities not active: `SELECT name, base, status FROM faction_facilities WHERE status <> 'active'`

## faction_storage

what the faction's storage holds per base (a station's id or our outpost's) and item, the fuel of a bunker as item `fuel`; t = when its place was viewed (empire/empire.json, empire.py collect)

- Kind: snapshot
- Columns: base, base_name, item, units, t, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `empire`, data/empire/empire.json
- What each faction storage holds: `SELECT base_name, base, item, units FROM faction_storage ORDER BY base_name, units DESC`
- The fuel in our bunkers: `SELECT base_name, units FROM faction_storage WHERE item = 'fuel'`
- Faction storage places and when they were read: `SELECT base, base_name, COUNT(*), datetime(MAX(t), 'unixepoch') FROM faction_storage GROUP BY base`

## inventory_faction

view: what the faction's storage holds per place (`faction:<base id>`) and item, with its base value and worth (units x base value), a bunker's fuel too; inventory and inventory_by_station count the same goods already (holdings, member `Faction`)

- Kind: view over faction_storage, items
- Columns: place, base, base_name, item, name, category, units, base_value, worth, t
- Kept: nothing: a view stores no row
- Refreshed: computed when asked, from its tables
- The worth of each faction storage: `SELECT place, base_name, SUM(worth) FROM inventory_faction GROUP BY place ORDER BY 3 DESC`
- Where steel_plate lies, our own storage and the faction's: `SELECT place, member, SUM(units) FROM holdings WHERE item = 'steel_plate' GROUP BY place, member`
- What the faction stores that no catalog item names: `SELECT place, item, units FROM inventory_faction WHERE name IS NULL`

## territory

the systems our faction claims (empire/empire.json)

- Kind: snapshot
- Columns: system, claim, note, t, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `empire`, data/empire/empire.json
- Our territory: `SELECT system, claim, note FROM territory`
- Our ships in our territory: `SELECT t.system, COUNT(s.pilot) FROM territory t LEFT JOIN ships s ON s.system = t.system GROUP BY t.system`
- Our territory and its jumps from home: `SELECT t.system, y.jumps FROM territory t LEFT JOIN systems y ON y.id = t.system ORDER BY y.jumps`

## sites

places our faction watches or plans for (empire/empire.json)

- Kind: snapshot
- Columns: system, poi, status, note, t, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `empire`, data/empire/empire.json
- The sites we watch: `SELECT system, poi, status, note FROM sites`
- Sites per status: `SELECT status, COUNT(*) FROM sites GROUP BY status`
- Stations in the systems of our sites: `SELECT si.system, si.poi, st.name, st.tag FROM sites si JOIN stations st ON st.system = si.system`
