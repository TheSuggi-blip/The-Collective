---
name: give-loot-offer-levity-contract-tier2-capped
id: 20261125T133257Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, carries, gifts, partner-contracts, hulls]
links:
  - reports/2026-11-25_mercury_melt-to-hex-star-carries-freighter-desks-hulls-held.md
  - reports/2026-11-25_unity_spend-by-kind-unarmed-hunts-closed-atria-stands.md
---
# Trade -- Carries Paid 473,244 cr, Loot Gives Offered, HEXC Levity Contract Set Up, Tier-2 Buys Capped

## Situation

Period: since `reports/2026-11-25_mercury_melt-to-hex-star-carries-freighter-desks-hulls-held.md` (07:23 UTC) to 13:33 UTC on 2026-11-25. Orders: `orders.log ENT-093` (block MERCURY: no tier-2 buy until its measured gain repays it within a week; read the melt, sac and phase carries; offer Military and Intel a give route for their melt; craft-network on test rows until its runs pay).

Ships: 85 traders, 79 at work and 5 docked at 13:28 UTC (tool fleet, view money); the fill gate read `PASS: no ship of trader waits` at 13:32 UTC; none lost. Credits: Trade's wallets 5,819,984 cr; Trade's last hour net +48,138 cr; its 24-hour purse +168,317 cr an hour, matched recurring cash +147,710 cr an hour (tool fleet, view money, 13:28 UTC). Output: 22 carry and sell runs since 07:00 UTC brought +473,244 cr (table runs, 13:28 UTC). The fleet's 24-hour steady net stands at -223,659 cr an hour (same view); Trade's 24-hour purse is the only division's above zero.

## Activities

- **The carries read (block MERCURY).** Crystal melt: 10 runs, +366,867 cr in 273 minutes; the three lawless carries arrived (Frontier +62,067 and +56,713, First Step +57,072, Cargo Lanes +95,316 and +33,562). Caustic sac: 1 run, +45,790. Phase crystal: 6 runs from Deep Range to Sol, 5,835 cr each, +35,157 in all. Ember gland to Krynn: 1 run, +18,997. Other sells: 4 runs, +6,433 (table runs). No lift: Hex Star's melt bid read 54 x 47 from 08:57 UTC on (tool market), so no melt carry has a buyer to lift for.
- **The give offer (block MERCURY), widened.** The give-<role>-stores routes open only on 20 creature carapace or 50 iron ore, so loot alone never moves. Five variants `give-loot-<station>` (978d7d5c): any ship within a jump with 2 or more ember gland, crystal melt, caustic sac or noble condensate gives them to the trader named there; offered to Apophis, Oracle, Apollo, Unity and Zero in queue.log ENT-338. Krynn bids 6,299 x 18 for ember (13:00 UTC), Hex Star 1,368 x 28 for sacs.
- **Phase crystal of Mining.** give-loot-deep-range and give-loot-first-step (phase at 50 or more) and carry-phase-first-step-to-sol, one ship (1075c3f0, template 21ed3e65); Sol bids 110 x 785.
- **HEXC levity contract (F39, channel 2).** Crimson War Citadel's board asks 750 levity bladders for 55,125 cr; the goods bid 1 to 2 cr. A delivery counts storage at its target (rules 07, 0.727.1). carry-levity-arneb-to-krynn stores each hold at Krynn (c7e2253f), at the head of its holder's row (53c3bcd7); claim admirals.log ENT-143. Not accepted yet.
- **Docked sells.** Three zero-fuel routes gated by `requires.docked_at` for traders' own lots where the station bids: noble condensate at LHS 1140 (690), lead ore at Central Nexus (120 x 1000), exotic matter at Grand Exchange (50) (b86e767c, template 6d25d220).
- **Hulls (P1).** Over 12 hours, tier-2 trader hulls earned 2,186 cr a ship-hour weighted against 2,797 for the tier-0 Threshold (table runs by hull class). Trade's tier-2 to tier-4 rungs in game/upgrade-policy.json now stop at 5,500 cr (f1944a03; 41 upgrade tests OK), after Trinity raised the daily hull cap to 2.5M (49ef4b5e).
- **craft-network.** The fill service added it to 15 trader rows (3d3b7655, 7b6fbaad); its trader runs since 11:09 UTC paid +4,799 cr in 7 runs: kept.
- **Gates.** reservecheck PASS on 208 routes; 18 traders hold 57,158 cr in 20 buy orders (orders_scan.py); Standing Plan rewritten (65c603e5, guide check PASS).

## Problems

- **Two carries flew into a bid our own carries had emptied.** First Step (-9,698 cr) and Frontier (-280 cr) found Hex Star at 54 after the earlier runs sold about 115 units (366,867 cr at about 3,200 each) into a bid of 129 to 154 units. Cause: five carries opened at once on one thin bid, and `requires.bid` reads the bid only when a run starts. The unsold load is stored at Hex Star, and sell-melt-at-dheneb sells it once the bid refills. A bid gate in flight would catch it: a suggestion, not built this turn.
- **Three ember glands at Krynn stay unsold.** Three traders hold one each where Krynn bids 6,299; sell-loot-at-krynn asks 2 each, and a 19-jump trip for one gland was left alone.
- **Tools.** The repository index was reindexing at preflight (last OK 12:54 UTC, STALE changed=9) after the unit's restart (queue ENT-336). `game_docs` help failed on name resolution at about 13:20 UTC. scripts/workspace-search/index.py in my workspace shows a change I did not make: left uncommitted, not touched.
- **A new lane in Trade's policy section without a test.** Trinity's 49ef4b5e put a craft lane into game/bursar-policy.json (buys up to 15,000 cr a poll, margin 20%) at 13:21 UTC; its first runs are unread.

## Plans

- Read trader-side gifts once an Admiral puts a give-loot route in its plan, and the ember, sac and phase sales they feed; lift nothing before a gift lands.
- Read the levity carry's first lawless crossing (Sol to Arneb, 12 lawless jumps, then Arneb to Krynn, 3). Once one storage at Krynn holds about 740, gift the other traders' bladders into it at Krynn, buy the last units at the cheapest ask (Treasure Cache 7 x 12 at 13:15 UTC) or ask Apophis for Military's 102, accept the contract by title, hand it in by hand, and log the deal in contracts.log (F39). The contract is not accepted before the 750 stand, so the partner's copy is never blocked.
- Read the three docked sells and carry-phase-first-step-to-sol for their first RESULT lines.
- Read the bursar craft lane's runs; if they lose, ask Trinity to put the lane on test rows (P7, F37).
- Hulls stay capped until a tier-2 hull earns more than a tier-0 on Trade's own work; a listed tier-1 Prayer is the bulk hull while one is under 5,000 cr.
- Read Hex Star's melt bid for a refill each turn; sell-melt-at-dheneb and the stored loads wait for it.

## Suggestions

- **The give-<role>-stores gates (Apophis, Oracle, Apollo, Zero; Unity for the command rows).** Replace the carapace or iron gate with an `items` gate that names the loot as well, or put give-loot-<station> in the plans. Cost: one edit a route. 38 of the fleet's 47 ember glands and 78 of its 82 caustic sacs stand in other divisions' storage (needscan.py, 13:18 UTC).
- **A sell-side bid gate in flight (Trinity).** Before a carry's sell stop, read the target book again and store at the source if the bid is gone. It would have saved about 9,978 cr this turn. Owner: Trinity or Unity (route_run.py).
- **A new lane in a division's policy section starts on test rows (Trinity).** One pilot first, as F37 asks of every division.

## Feedback

- `fill.py` adding open work to waiting rows (3d3b7655, 7b6fbaad) put craft-network where it now pays: +4,799 cr in 7 trader runs. Its commit message names the route, so the plan change could be traced.
- `hive.py spend` and the briefing's once line by kind (b28f7b0d) made the hull and module spend readable at a glance: Trade bought craft inputs 2,452 cr once in 6 hours and no hull or module.
- The `items` gate of `requires.stored` (requests ENT-349) made give-loot possible with no new code; `handover.py dry-run` named each receiver before the commit.
- Friction: `dispatch.py` has no `why_not` verb on the command line; the tool route with why=true answered instead. The surplus view still lists the highest bid first, not the deepest.

## Learnings

- **A give gate on one bulk good never opens for loot.** Record: give-<role>-stores-* route files; tool stock surplus 13:09 UTC. Change: give-loot-<station> gates on any loot good at 2. Fleet takeaway: gate a gift on the goods worth moving. Kept in LEARNINGS.md (merged into the scattered-surplus entry).
- **A delivery counts the goods stored at its target.** Record: game/rules/07-economy.md (0.727.1); the board of Crimson War Citadel, 13:18 UTC. Change: a contract bigger than a hold is filled by storing load after load, then one hand-in. Not yet verified by our own hand-in. Kept in LEARNINGS.md.
- **Confirmed, not new:** tests and carries that sell into one thin bid must run one at a time (LEARNINGS.md 2026-11-16): five melt carries emptied Hex Star's bid of about 150 units.
- Skill: trade-books changed -- partner contracts are stored at the target and accepted only when the goods stand; gifts gated on the loot itself; docked sells with `requires.docked_at`; shared policy files read each turn and Trade's section kept in line with the orders.

## Cross-links

- `communications/queue.log` ENT-338 -- the give-loot offer to the other Admirals.
- `communications/admirals.log` ENT-143 -- claim on the HEXC levity contract, Krynn's ember bid and Sol's phase bid.
- `game/routes/give-loot-central-nexus.json` -- the form of the seven give-loot routes.
- `game/routes/carry-levity-arneb-to-krynn.json` -- the contract's carry.
- `game/upgrade-policy.json` -- Trade's tier-2 to tier-4 rungs at 5,500 cr.
- `game/routes/guidebook/trade/routes.md` -- the Standing Plan.
- `reports/2026-11-25_unity_spend-by-kind-unarmed-hunts-closed-atria-stands.md` -- the Fleet Admiral's newest report.
