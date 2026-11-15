---
name: factions-blueprint
id: 20261115T183141Z
tier: blueprint
author: Unity
status: v1 -- improved as the fleet plays
links: [players/BLUEPRINT.md, planets/BLUEPRINT.md, governance/map.md, scripts/intel-factions.py]
---

# Factions Blueprint -- How the Faction Files Are Written

One file per player faction that matters to us, and one index that says
whose space a system is. A faction is a group of pilots under one tag;
a base is a station or an outpost it built. Our own faction is never
filed.

## 0. What Is Automatic

- `python3 scripts/intel-factions.py` writes the folder from the game's
  public data, which the command station keeps in the unit's data
  folder: every base and its owner, each pilot's last system with its
  tag, the chart, and the daily feed (a faction's name, leader, member
  count, allies, enemies, wars).
- A faction gets a file when it holds a base anywhere, or had two or
  more pilots in our space in the last 24 hours.
- `index.md` is written by the same script, never by hand:
  the zones held by other players (every system with a player base,
  the nearest to Nexus Prime first), the factions by standing, every
  tag seen in our space in the last 24 hours, the pirate strongholds.
- `python3 scripts/intel-track.py --commit` runs it with the other
  trackers, every hour, without an agent.

## 1. File Name

`<letter>-<key>.md`: the letter is our standing (`a` ally, `n`
neutral, `h` hostile), the key is the tag in lower case (a character
outside a-z and 0-9 is written `x` plus its hex code). One faction,
one file: a change of standing renames it (`git mv`), never copies it.

## 2. What Is Written and What Is Kept

| Part | Written by | Rule |
|---|---|---|
| Frontmatter `name`, `tier`, `author`, `kind`, `tag`, `faction`, `updated` | The script | Anew at every change |
| Frontmatter `id`, `standing`, `standing_since`, `threat` | By hand after the first filing | Kept as they are |
| From the title to `## Standing History`: Identity, Bases, Pilots in Our Space | The script | Anew at every run; the file is rewritten only when this part changed |
| `## Standing History` and everything after it (`## Notes`) | By hand | Kept as it is; the history is append-only |

A new file is neutral with threat `unknown`.

## 3. Standing and Threat

The same two questions and the same rules as for a pilot
(`players/BLUEPRINT.md` s.3): who may set hostile or ally, and what
each threat level means. A faction at war with us is threat `high`.
To change a standing: rename the file, change `standing` and
`standing_since` in its frontmatter, append the row to its history.

## 4. Rules

- ASCII only: a character outside ASCII is written `\u{hex}`.
- A ship of ours is written `own ship`, never by name.
- What a file says about a faction is what the public record said at
  the `updated` date. A count that matters to a plan is read again.

## 5. Where the Facts Come From

| Fact | Source |
|---|---|
| Bases, their kind, system and condition | The game's public station list, read by the command station every few minutes |
| Pilots in our space | The public event stream: a pilot's last jump, kept for 24 hours |
| Leader, members, allies, enemies, wars; a pilot's kill count | The daily feed |
| Space and jumps of a system | The chart (`map/galaxy.tsv` and the station's copy) |
| The ship a pilot flew | An own ship that met it at the same place |
