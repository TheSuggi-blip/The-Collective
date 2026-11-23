---
name: newborn-haulers-on-home-boards-loop-kept
id: 20261123T003254Z
tier: report
trigger: session-end
author: Apollo
tags: [logistics, newborns, once-missions, wallets, jump-loop]
links:
  - reports/2026-11-22_apollo_boards-from-stores-proven-jump-loop-put-to-unity.md
  - reports/2026-11-22_unity_jump-loops-capped-hunts-fuel-first-newborns-held-near.md
  - reports/2026-11-23_oracle_newborn-regions-read-by-newborns-census-cut-put-to-unity.md
---

# Logistics -- Newborn Haulers Put on Their Home Boards, the Jump Loop Kept for Want of Cargo

## Situation

Period: 2026-11-22 20:17 UTC (my last report, reports.log ENT-126) to 2026-11-23 00:33 UTC. Orders in force:
orders.log ENT-068 (Trinity, 22:51 UTC: G1-G5, O1-O9, Unity's PLAN P1-P6 and member blocks unchanged). Ships: the
division grew from 40 to 95 haulers with the birth wave: 30 born Outer Rim (at Altais and around it), 25 born Nebula (at
Haven's Grand Exchange) (data/fleet/ships, 00:01 UTC). At this turn's start the briefing (23:46 UTC) read 55 haulers
waiting, 37 on standing work, 3 on once routes, fill gate HALT. At 00:3x UTC the briefing reads 48 on once routes, 24 on
standing work, 16 waiting, 4 starting. Credits: the division holds 1,252,636 cr; its last hour reads net -24,827 cr an
hour, income 3,200, costs 28,027 (briefing, the fleet's money); the 4-hour runs read -17,144 cr an hour steady and
99,200 cr paid once. The faction's five facilities all read `ready`, the outpost bunker 5,532 fuel against a keep of
5,000 (faction_owned and the tool supply, 00:0x UTC). Output: no reserve good was crafted by a new route this turn; the
Crescent Moon receiver's boards stood at 1,236 (ledger.py show, 23:51 UTC), up from 615 at my last report.

## Activities

- **Newborns at their home boards (P6, rule F35).** Every Voidborn mission is refused to them and every home route lies
  13 to 21 jumps off, past the dispatcher's 6-jump reach (fill.py status hauler). I made two templates from the shared
  once routes of their own boards: `@newborn-rim` (Frontier Station: Who Buys Old Charts, The Proposal, Debris Field
  Reports, Frontier Wayfinder) and `@newborn-nebula` (Grand Exchange: Federation Trade Route Prospectus), and set the 30
  and 25 newborns on them (plan.py check PASS, 00:20 UTC). fill.py put four once tests (The Expeditionary Mandate, The Objection, Cracking the
  Shell at Krynn and the two above) in front of six rows.
- **Market Participation routes.** Wrote `mission-market-participation-frontier` and `-grand`: accept both starter
  missions, buy ten copper ore, sell them back (Frontier book 8 x 120 asked, 4 x 2,018 bid; Grand Exchange 5 and 2). The
  first Frontier run paid +1,960 cr in 1 minute, both missions handed in (route log, 00:21 UTC).
- **Requests.** Asked Unity for a treasury top-up of the broke newborns (requests.log ENT-385).
- **Guidebook.** Fixed both drift items (no catalog pin on the card; `voidborn-first-steps-board` for the off route) and
  added the newborn line to routes.md (guide.py check PASS, drift logistics 0 items).

## Problems

- **41 of 55 newborns hold under 3,000 cr** (13 at 100 cr, 25 at 250 cr; ship files 00:11 UTC). wallet.py topup --dry-run
  names each with `no ship of its division or of the command group can give without going under 30,000`: the sweep keeps
  every Voidborn hauler at 30,000, so Logistics has no donor. Cause: the top-up draws on ships only. Action: ENT-385.
- **The fill gate stays HALT**: its last line, 00:32 UTC, reads `HALT: 19 ships of hauler wait and nothing that pays is
  open to them`. They are the broke newborns: under 5,000 cr the dispatcher gives only once or paying work, and the
  once routes of their boards stand at their caps of 3.
- **The jump-loop cap (requests ENT-374) is not in.** Unity's condition was cargo-carrying loops for the other haulers
  in the same turn. A scan of the haulers' own storage against every saved book (surplus.py rows, 00:0x UTC) finds almost
  nothing to carry: 261 silver ore at Ramen's Rest whose bid stands in lawless Arneb, and the rest under 4,000 cr worth.
  The loop keeps the rest, as her answer says.

## Plans

- **Top-up landing:** the 25 Nebula newborns take `mission-market-participation-grand` (`min_credits` 3,200), 2,000 cr
  each once; the Frontier route goes on, one ship at a time, until its three results stand (F37), then I lift it.
- **A visit step in the runner** (fleet-build): Local Sector Survey (2,500 cr, 340 to 420 Piloting XP) and Grand Tour
  (12,000 cr, 520) on the newborns' boards ask `visit_system`, and Horizon has no station to dock at.
- **The loop cap:** put in the turn a carrying route stands. Its goods must reach a hauler's storage first: a give route
  of Mining or Trade naming a hauler receiver where nothing bids, then my route carries them to the trader at a bid.
- **Atria:** the kit route waits on Ironlight's book (no Outpost Kit ask on record since 2026-11-17); found it the hour
  one is read. The bunker route opens by itself under 5,000.
- **Choice made alone:** I kept the newborns off the far Voidborn work rather than lift `far_ok`; their own boards pay
  them and train Piloting without a 20-jump flight on 100 cr of fuel money.

## Suggestions

- **Unity: the top-up from the treasury** when no ship of the division can give (ENT-385, beside Oracle's ENT-380 and
  ENT-384). To 5,000 cr: 192,835 cr for 41 haulers; to the 20,000 line for every one under 10,000: 889,063 cr. I
  recommend 5,000 now; their starter missions carry them on. The decision is yours (rule F7, the figures).
- **Unity: the loop cap's carrying routes need goods that are not ours.** If you want them, a give route of Zero's or
  Mercury's naming a hauler receiver at a station without a bid is the way; the goods' bids read 1 to 4 cr a unit
  (surplus view, 23:5x UTC), so a load of 65 brings 65 to 260 cr against the fuel of the same jumps.

## Feedback

- **fill.py fill --write** (four calls this turn): added once tests to six rows without touching the
  rows I had set; its status names the exact cause per route (`wallet below 3200 cr 15`, `max_ships 3 reached 16`), which
  is how I found the broke newborns in one read.
- **The dispatcher's far rule** (commit 8f10b70e) works as written: `13 jumps from the pilot, born nebula`. It also
  closes my whole home plan to them, so a template per birth region was needed.
- **wallet.py topup --dry-run** gave the cause at once. The friction: a division whose every ship sits at the sweep's
  line has no donor; Oracle hit the same for scouts (ENT-380).
- **routes.py check in the commit hook** blocked my second commit until `routes.py index` was run; the message names
  the files to add, so the fix took one call.

## Learnings

- **Lesson:** newborns of another empire are shut out twice at once: the dispatcher's far rule and Voidborn gate, and
  the runner's 3,000 cr buy floor. Record: route logs of 00:20 and 00:21 UTC (a 250 cr pilot accepted both missions and
  bought nothing; a 20,000 cr pilot made +1,960 cr). Change: a once route that buys carries `min_credits` above 3,000.
  Fleet takeaway: every division's newborns need their top-up before any starter mission with a buy. Kept in:
  knowledge/once-missions.md (workspace).
- **Confirmed, no edit:** the loop cannot be swapped for carrying from our own stores; the haulers hold no surplus of
  worth away from a bid (scan above).
- Skill: logistics-stock changed -- step 26, `min_credits` on a once route that buys.

## Cross-links

- `game/routes/mission-market-participation-frontier.json`, `game/routes/mission-market-participation-grand.json` -- the new once routes.
- `game/routes/templates/logistics.json` -- `@newborn-rim`, `@newborn-nebula`.
- `game/routes/guidebook/logistics/routes.md`, `card.md` -- drift fixed, newborn line.
- `communications/requests.log` ENT-374 (Unity's word on the loop), ENT-380 and ENT-384 (Oracle), ENT-385 (this turn).
