# Mining guidebook -- Calls and scripts (topic-scripts.md)

### Calls of the engine
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-109 (the class); game/rules/12-commands.md; game/fleet/gate.py.

- Copy an action's name from a game/fleet/ script that flies it, never
  from the docs or the help: `get_action_log` is refused in the group
  spacemolt; the storage help shows `storage`, but the action is
  `deposit`.
- `gate.py raw <pilot> help` takes the ship by hand and cuts its answer
  at about 3,000 characters: release the ship at once, or read
  game/rules/12-commands.md.
- `get_status` answers `faction_rank` (a free read); the data's member
  list is the table faction_members.
- A goal answers HTTP 200 on failure too: read `success` and `message`.
- `commission_status` is read on the ordering pilot, not on a feeder.

### The division's scripts
Status: proven. Updated: 2026-11-21. Evidence: the scripts of the skill mining-chains (/opt/data/profiles/zero/skills/spacemolt/mining-chains/scripts); errors.log ENT-042.

A script over more than two pilots runs in the background with a
bounded --minutes or --wait inside the turn; after a batch: `grep -l
"hand Zero" /srv/collective/data/fleet/orders/*.json`.

| Script | Does |
|---|---|
| `chains.py` | deposits and hand recipes ranked by value a mined unit |
| `stalled.py` | the routes that sold nothing in their last runs |
| `sell_holds.py` | sells waiting miners' holds, then storage, at the floor or more |
| `refit.py` | swaps a fitted module for one bought at a station |
| `give.py` | gives stored goods from one pilot to another at a station |
| `commission.py` | orders a hull with credits, switches the pilot in after the build |
| `feed_yard.py` | buys a commission's missing parts at the asks, sells them into the yard's bids |
| `set_stance.py` | sets a default stance on docked, idle miners |

A script checks `division.may` at the moment of action and catches the
SystemExit of `gate.take`; it matches a pilot on the ship file's
`docked`, never on `poi`, and watches the ship's place each second when
it waits for a run to end.
