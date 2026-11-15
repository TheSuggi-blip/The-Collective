---
name: orders
id: 20261115T143031Z
tier: orders
author: Unity
links:
  - governance/the-collective-constitution.md
  - governance/rulebook.md
---

# orders.md -- The Orders in Force

What the fleet and each division are ordered to do now. One writer:
the Fleet Admiral, on Suggi's decisions. Every agent reads this file
at session start (preflight). It ranks below the constitution, an
agent's AGENTS.md and SOUL.md and the rulebook
(`governance/rulebook.md`), and above the task at hand.

- An order names its goal, its owner, its limits and what changes it.
- An Admiral carries out the orders of its division and decides inside
  them. It proposes a change in its report or with an `@Unity` entry
  in `communications/queue.log`; it does not edit this file.
- This file is public. Where our ships are, and which place or route
  an order uses, is not written here: the places of the running turn
  are in the unit's data folder
  (`/srv/collective/data/fleet/dispatch.json`).
- An order is never edited away. When it ends, its row moves to
  section 4 with the date and the reason.

## 1. The Fleet

| # | Order | Goal | Changes when |
|---|---|---|---|
| F1 | The Fleet Admiral commands every ship. No Admiral commands a ship until an order here hands its division over | One hand on the fleet while it is built | Suggi hands a division to its Admiral |
| F2 | Posture HOLD toward every player and every NPC ship, for every division: never initiate; flee, dock or brace (rulebook 8.2). Wildlife of the role grazer may be hunted in Voidborn space by the ships a turn names | No loss while every ship is a starter; hunting is legal everywhere and grazers are prey | An order here sets TIGHT or FREE for a division and a region |
| F3 | Every ship stays in policed Voidborn space | The same | A written order here sends one ship out: insured, hold empty (rulebook 8.3) |
| F4 | No pilot of ours writes to another player. A contact is passed to the Fleet Admiral | Diplomacy has one voice | Approved templates exist |
| F5 | No new pilot and no faction without Suggi's word | Permanent choices are Suggi's | Suggi's word |
| F6 | A turn lasts four hours. An order gives its ships work for the whole turn. A ship without paying work stays docked | No ship burns fuel for nothing: fuel is the fleet's running cost | -- |
| F7 | Every pilot keeps 2,000 cr in its wallet | The weekly tax is taken from the wallet: Voidborn takes 6% of the week's income and 0.75% of the ship's value; a pilot that cannot pay becomes a debtor of the empire. Next assessment about 2026-11-16 12:00 UTC | The tax is prepaid, or the rates change |

## 2. The Turn in Force

| Turn | From (UTC) | To (UTC) | Order | Goal | Owner | Done when |
|---|---|---|---|---|---|---|
| T2 | 2026-11-15 14:30 | 2026-11-15 18:30 | Find the first income that repeats. Test ships only: hunters at the grazing grounds of our space, prospectors at the ice fields and gas clouds not read yet, one trader that checks a price gap at both stations before it buys. Every other ship stays docked at the capital | A measured figure, credits per ship per hour, for each way of earning tried | Unity, by script | Each way tried has its figure in the turn's record, and the best one is the order of T3 |

## 3. The Divisions

No division has an order of its own yet: every ship flies the turn in
force. A division's row is filled when it gets its first order.

| Division | Admiral | Order in force | Measure it should move |
|---|---|---|---|
| Mining | Zero | The turn in force | -- |
| Trade | Mercury | The turn in force | -- |
| Logistics | Apollo | The turn in force | -- |
| Military | Apophis | The turn in force | -- |
| Intel | Oracle | The turn in force | -- |

## 4. Ended Orders

Append-only, newest last.

| # | Order | In force (UTC) | Why it ended |
|---|---|---|---|
| T0 | Every ship fills its starter mining missions at the first belt chosen | 2026-11-15 13:10 to 13:25 | That belt was almost empty: 50 units for 28 ships in nine minutes. A scout had read a full one; the turn was restarted there as T1 |
| T1 | Every ship fills its own two starter mining missions (Iron Supply Run, Copper Requisition) at a full belt two jumps out, hands them in at the capital and stays docked | 2026-11-15 13:30 to 14:15 | Done: all 55 pilots handed both in, 181,500 cr of one-time money. The hour cost the fleet about 8,800 cr of fuel and earned nothing that repeats |
