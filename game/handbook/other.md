# Other -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## division_pnl_24h

view: trailing 24h and 6h division cashflow per hour (steady, once, total Net Purse/h, and fuel) from stats_money_hour

- Kind: view over stats_money_hour
- Columns: division, hrs_24h, steady_24h, once_24h, purse_24h, fuel_24h, steady_6h, once_6h, purse_6h
- Kept: nothing: a view stores no row
- Refreshed: computed when asked, from its tables
- 24h and 6h Net Purse/h, steady, once and fuel per division: `SELECT * FROM division_pnl_24h ORDER BY purse_24h DESC`
- Divisions with negative 24h steady cashflow vs positive Net Purse/h: `SELECT division, steady_24h, once_24h, purse_24h FROM division_pnl_24h WHERE steady_24h < 0 ORDER BY purse_24h DESC`
- Trailing 6h vs 24h Net Purse/h momentum per division: `SELECT division, purse_6h, purse_24h, fuel_24h FROM division_pnl_24h WHERE division != 'Fleet' ORDER BY purse_6h DESC`
