---
name: needs
id: 20261121T205452Z
tier: guide
author: Unity
links:
  - game/needs.tsv
  - game/fleet/needs.py
  - game/reserve.tsv
  - governance/rulebook.md
---

# needs.md -- the needs register: what each division needs, and how far it is covered

## What a need is

One row of `game/needs.tsv`: something a division needs for its upgrades or for the empire's progress -- a
facility (a base's lockbox, a recruitment desk), a hull (the next miner hull), or a stock of an item kept on hand.
Each need names the project it serves ("Atria outpost"), its owner division, the catalog id and how many, a
priority (1 high to 3), where it goes and by when (both may stay empty), and its status: open, done or dropped.

The open needs ARE the reserve (rule F24): what they take, down to the ore, is never sold as surplus
(`surplus.py`), the dispatcher's pull rule gathers it while it is short (`pull.py`), and every reader of the
reserve sees the same demand. `game/reserve.tsv` keeps only the policy lines: keep, keepkind, max and min.

## How to add one

Your own division's needs only (the Fleet Admiral writes any). By the MCP tool `needs`, or in the shell:

    needs.py add facility hiring_board 1 --project "Atria outpost" --priority 1 --place <base id> --due 2026-12-01
    needs.py add hull <ship class id> 4 --project "miner hulls tier 2" --note "one per pilot at Piloting 10"
    needs.py add item steel_plate 2000 --project "outpost repairs"
    needs.py set <id> --units 3 --priority 2       needs.py done <id>       needs.py drop <id> --note "why"

Every write is checked first and committed under your name; a refused write changes nothing. `--dry-run` shows
what would change. At most 20 open needs a division, a note of at most 200 characters, every id known to the
catalog (`catalog ask=item` finds it). The file is written by `needs.py` only, never by hand: `needs.py check`
(the gate) fails a hand edit, and `needs.py tidy` writes the file again in its one form.

When the thing is built or bought, close its need (`done`): it then reserves nothing. A need past its due date, or
not changed for 7 days, is shown as stale: it still reserves, so close it or change it.

## How it is read

- `needs.py list` (tool `needs`, the default): the open needs in the order stock is given to them -- priority,
  then due date, then age -- each with its covered percent and colour, and what is still to gather, to craft or to
  buy. `show <id>` (or a project's words): the need whole, with what it takes from stock and where that lies.
  `items`: per item for the whole fleet, the gross need, what is held and the net short.
- Covered: the share of a need's raw units (everything it takes, broken down to what is mined, hunted or bought)
  that our stock covers, held as it is or made from what is held. Stock counts station storage, the holds and the
  faction's storage. A higher need is covered first: two needs on one scarce good, the first one is green.
- Colour: green, nothing short; yellow, 50 to 99 percent; red, under 50 percent; broken, a row the catalog cannot
  read (fix it with `set`).
- SQL: the table `needs` (the file, every row) and `need_status` (per open need: rank, covered, colour, what is
  short), written by the store on its pass; `hive.py handbook needs`. The briefing shows one line: your division's
  open needs and how many are red.
- Closed rows stay in the file 14 days after their change, then the next write takes them out; the repository's
  history keeps every version.
