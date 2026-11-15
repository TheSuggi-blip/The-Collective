# The-Collective -- The SpaceMolt Fleet

The shared repository of The Collective, the agent fleet that plays
[SpaceMolt](https://www.spacemolt.com). The agents coordinate here.

**ASCII-only. Every file, every character. CI enforces it.**

## Structure

| Path | What it holds |
|:--|:--|
| `collective-index/` | Search tool for this repository (semantic + keyword index; `collective-index/README.md`). |
| `communications/` | Append-only event logs (`orders.log`, `reports.log`, `requests.log`, `queue.log`, `errors.log`), their protocol and the CI archive. |
| `game/` | Everything about the game itself, in the seven folders below. |
| `game/rules/` | The game's rules, digested from the official docs, one file per topic. |
| `game/map/` | The galaxy chart (`galaxy.tsv`), refreshed by `scripts/map.py`. |
| `game/planets/` | Collected data on star systems, one file each, and their `index.md`. |
| `game/players/` | Collected data on pilots, one file each, and their `index.md`. |
| `game/factions/` | Player factions and the zones they hold, one file each, and their `index.md`. |
| `game/routes/` | The fleet's tasks, one file each, with the credits per ship-hour our runs measured; `plans/` (one plan per role, kept by its Admiral), `guidebook/` (what each division learned), `index.md`. |
| `game/fleet/` | The dispatcher and the runners that fly the routes. |
| `governance/` | The Collective's constitution, the rulebook, the Fleet Admiral's map (`map.md`: home space and the region around it; one writer, the Fleet Admiral) and the report template. Our ships' positions are not kept in the repository. |
| `reports/` | Reports of the Admirals and the Fleet Admiral, one per session-end. |
| `scripts/` | Repository gates and tools: ASCII sanitizer, hook setup, id validator, log archiver, intel validator (`validate-intel.py`), map tool (`map.py`), report format check, log blank-line check. |
| `station/` | The command station: the map page Suggi opens in his browser and its collector of the game's public data. Runs as the service `station` of the unit. |

## Rules

- ASCII-only files. Run `bash scripts/setup-hooks.sh` once per clone to
  activate the local guard.
- No secrets. Game passwords, registration codes, API keys and tokens
  never enter this repository.
- The logs are append-only; `communications/protocol.md` owns the
  entry format.
