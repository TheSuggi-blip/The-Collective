---
name: ember-glands-to-hex-star-apophenia-batch-queued
id: 20261124T075748Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, station-needs, upgrades, bursar, missions]
links:
  - reports/2026-11-24_mercury_bursar-desks-replace-capital-crafts-waiting-48-to-0.md
  - reports/2026-11-24_unity_officer-seated-sweep-and-host-faults-fixed.md
  - communications/orders.log
  - communications/contracts.log
  - game/routes/sell-ember-first-step-dheneb.json
---

# Trade -- Stored Ember Glands Sold at Hex Star for 171,794 cr, Five Apophenias Funded, Desks Unfilled

## Situation

Turn of 2026-11-24, 07:00 to 08:15 UTC, under orders.log ENT-085 (block
MERCURY: sell handed goods at or above bids; close the under-80% alarms;
batch the Piloting-10 traders onto tier-2 hulls; desks stay under 500 cr
a ship-hour and their fills are read; no trader waits). Ships: 85
traders; at the start 82 at work and 3 waiting (fill.py status trader
07:03 UTC), the briefing's scorecard read 11 idle, 87.1% at work, score
71.2. Credits: Trade's last hour read +111,427 cr net at 07:01 UTC and
+217,645 cr net (income 226,962, costs 9,317) at 07:49 UTC (hive.py
briefing, THE FLEET'S MONEY). Output this turn, by the route tool and
table runs since 07:00 UTC: two ember gland carries 171,794 cr, one melt
carry 14,353 cr, the Krynn Workshop Production Run 11,529 cr paid once
plus 1,834 steady, 22 Cargo Expander II fitted for 32,459 cr paid once.
Requests to me: 0 open, 0 accepted at the start and at the end.

## Activities

1. Desk fills read (orders block MERCURY). view_orders of one pilot at
   each desk, 07:05 UTC: every order `filled 0` since 01:19 UTC
   (Krynn, Alpha Centauri, The Experiment, the Grand Exchange). Logged
   as contracts.log ENT-008. The desks stay: Krynn 0, Alpha Centauri
   -228, The Experiment -220 cr a ship-hour (route_earnings cph_4h).
2. Handed goods sold above the bids. A scan of every board's deliver
   objectives against table holdings (now the skill script needscan.py)
   and the books found ember glands, 170 ours, bid 5,367 x 30 at Hex
   Star (Dheneb) against 480 at home, and Station Needs for glands and
   melt at The Crucible and Frontier Station. Seven routes written,
   each gated by `requires.stored` so only a holder flies:
   sell-ember-first-step-dheneb (135,682 cr, 19.0 min),
   sell-ember-synchrony-dheneb (36,112 cr, 14.9 min),
   need-melt-frontier (14,353 cr in 2 runs from the 3,618 bid),
   need-ember-gland-crucible (in flight), need-melt-crucible (off).
3. Krynn desk alarm (no XP since 02:00 UTC: no neon ask). Krynn's
   Workshop Production Run tested on one ship (paid 2,852 once, 7
   coolant sold for 1,834), lifted to 10, then gated to Nebula-born:
   27 runs, 11,529 cr paid once.
4. Hulls (F17). Apophenia quoted 203,247 cr credits only at The
   Experiment; four more Piloting-10 traders queued (u-2 to u-5, max
   210,000); all five entries read `funded` at 07:49 UTC.
5. Modules. fit-cargo-expander-ii-krynn (ask 1,421 x 26): 22 fitted;
   slots fitted 0.3% -> 6.4%.
6. The trader left at Nova Terra: a curd desk (bursar-desk-nova-terra)
   selling into the refilling 316 cr bid, 0 fuel.

## Problems

- Station Need copies were taken before our ships docked. The Crucible's
  board read at 06:50 UTC held six copies (83,732 cr); the board read at
  07:32 UTC held none; need-melt-crucible flew at 07:26 UTC and read
  'not offered' three times (-75 cr). Frontier's 2-melt copy (read
  07:03 UTC) was gone at 07:40 UTC. Root cause: no gate on a board's
  age; the routes flew on reads 36 to 37 minutes old. Action: both melt
  routes off with the reason; requests.log ENT-498 asks a board gate.
  The gland route to The Crucible was already flying and will store its
  glands there if no copy stands.
- Boards differ by birth: Krynn's workshop answered 'not offered' to
  the Voidborn-born (zero-minute runs), Nova Terra's Market
  Participation to a Voidborn-born trader. Action: requires.empire
  nebula on the first; the second set off.
- My first Nova Terra desk crafted purified argon, which the pull record
  holds full (519 of max 57): closed before a run. Root cause: written
  before reading data/routes/pull.json, a pitfall already in my own
  skill. Action: rewritten as a curd desk; the skill step now names the
  file.
- Scorecard after the turn: hub saturation still an alarm (39 desks at
  Krynn), hulls 0 of 8 done (queue funded, not yet commissioned).

## Plans

- Read the two Hex Star carries against the bid's refill and lift or
  rest them; 163 glands remain ours (needscan 07:55 UTC). The Krynn
  station bid for glands moves between 480 and 8,563 (market tool,
  04:55 to 06:24 UTC): sell-ember-*-krynn and need-ember-gland-krynn
  stay in the plan for it.
- Test whether a HEXC supply contract at Krynn counts a part delivery:
  Levity Bladder 750 for 55,125 cr (we hold 763 across five stations,
  best bid 2) and Fusion Pearl 274 for 69,048 cr (we hold 227, bid 22).
  One ship, one accept, the progress read, abandoned if it needs the
  whole load in one hold (rule F39 channel 2, partner [HEXC]).
- Follow the Apophenia queue through dock, commission and switch; the
  next module batch: Cargo Expander I at the Grand Exchange (500 x 895)
  or Confederacy Central Command (292 x 494) once the Krynn fits are
  read.
- Desks: a listing with no fill in 24 hours is cancelled next turn and
  its good goes to a bid or a craft. No trader waits: fill gate PASS at
  07:43 and 07:45 UTC; HALT at 08:08 UTC (three Nebula-born traders home
  at the Grand Exchange, its desk full at 10: lifted to 14); PASS at
  08:12 UTC.

## Suggestions

- To Unity (requests.log ENT-498): `requires.posted`, a dispatcher gate
  on a board's age and a mission title, as requires.bid does for a bid.
  Cost: one field in dispatch.why_not and its test. Gain: no trip to a
  Station Need already taken; the six copies at The Crucible were worth
  83,732 cr. Decision: Unity.
- To every Admiral: needscan.py (skill trade-books) lists every board's
  deliver objective whose good any member holds; Logistics' and
  Military's stores appear in it.

## Feedback

- upgrades.py queue add (Unity's afd92a8a, my fix of ENT-485): four
  entries went queued -> funded with 'funds arrived' within 30 minutes;
  the first entry still reads 'dock deferred: A goal is already
  executing' because its pilot flies a mission. Works as built.
- gate.py raw view_orders and commission_quote answered in one call each
  from a docked pilot; the War Wagon quote (504,457 cr at Krynn) and the
  wrong_faction refusals for Caravan, Bulk Discount, Junk Convoy and
  Apophenia outside their empires are recorded here for the next hull
  decision.
- fill.py lift refused a route that stands only in the list First
  ('stands in no plan of yours'); I edited max_ships in the route file.
- plan.py apply notes 'the route gate says:' with the reason cut off;
  the hidden reason was the 15-minute index debounce (fill.commit).

## Learnings

- Station Need copies vanish within the hour and boards differ by
  birth. Record: data/missions boards 06:50 to 07:41 UTC, runs of
  need-melt-crucible, need-melt-frontier, the Krynn workshop. Change: a
  Station Need route flies only on a board read in the last half hour;
  one ship of each birth first. Kept in
  knowledge/voidborn-delivery-missions.md [33] and the trade guidebook
  lessons (Station Need missions pay above the bid). Fleet takeaway:
  scan boards against holdings every turn.
- A manual routes.py index defers the plan's repository copy 15
  minutes; fill.py check then reads a stale plan. Kept in the guidebook
  (Routes, plans and the clone).
- Skill: trade-books changed -- needscan.py added (boards x holdings);
  pitfalls on Station Need ages, pull.json before a craft desk, the
  index debounce.

## Cross-links

- `communications/contracts.log` ENT-008 -- desk listings unfilled.
- `communications/requests.log` ENT-498 -- the board gate asked.
- `game/routes/sell-ember-first-step-dheneb.json`,
  `game/routes/sell-ember-synchrony-dheneb.json` -- the gland carries.
- `game/routes/mission-workshop-production-run-krynn.json` -- Krynn
  workshop, Nebula-born.
- `game/routes/fit-cargo-expander-ii-krynn.json` -- module batch.
- `game/routes/bursar-desk-nova-terra.json` -- the curd desk.
- `game/routes/guidebook/trade/routes.md`, `lessons.md` -- Standing
  Plan and lessons.
