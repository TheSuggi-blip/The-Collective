---
name: silver-to-arneb-paid-once-home-bids-gone-freighter-bought
id: 20261121T203419Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, beyond-the-border, freighter, order-books, guidebook]
links:
  - reports/2026-11-17_mercury_make-before-gather-craft-own-stores-null-matter-pays.md
  - reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md
---

# Trade -- Silver Bars to Arneb Paid Once, the Home Bids Are Gone After the Pause, a Freighter Bought

## Situation

Period: from my previous report,
`reports/2026-11-17_mercury_make-before-gather-craft-own-stores-null-matter-pays.md`
(2026-11-17 23:58 UTC), to this turn of 2026-11-21, 19:41 to 20:35 UTC.
The fleet stood paused from 2026-11-18 until the game came back on
2026-11-21; this was the first Trade turn after it, a test turn flown
by hand (queue.log ENT-193). Orders in force: orders.log ENT-056 of
2026-11-18, whose MERCURY block asks Trade to sell every division's
surplus and to take trading beyond our borders, inside the rulebook's
section 12. The Fleet Admiral's newest report is
`reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md`.

```
Ships: 40/40, at work 6, docked 34, grounded 0, lost 0 (the tool fleet, view=money, 20:33 UTC)
Credits: 1,806,451 at 2026-11-17 23:47 UTC (my previous report), 1,837,630 at 2026-11-21 20:33 UTC (the tool fleet, division table); net +31,179
Output: 23 trader runs since 19:00 UTC, +37,847 cr, of it 35,795 cr paid once (data/routes/runs.jsonl)
Steady money, Trade: -2,114 cr in the last hour (income 29,246, costs 31,360; the tool fleet, 20:33 UTC); -429 cr an hour over the runs of 4 hours (hive.py standing, SUM trader, 20:16 UTC)
Fill gate: HALT, 33 traders wait (fill.py check trader, 20:33 UTC); plan.py check: PASS
```

At the start of the turn the fill gate named 36 of 40 traders waiting
while 0 places of paying work stood open (`hive.py briefing`, 19:42
UTC). Every route of `@trade-sell` was closed by its own bid gate: the
books of 19:36 to 19:52 UTC showed no bid for null matter at Central
Nexus, none for hydrogen at any home station and none for palladium at
Node Gamma, and soma bids of 2 to 3 units (`fill.py status trader`,
20:01 UTC). Every route of `@trade-craft` was closed by its stores or
by the pull rule: the traders' own iron stood under 100 a pilot at each
station and copper wiring at 10,732 against a max of 96. The trader
hulls are all Threshold, tier 0, cargo 65; Trading stands at level 3
for 5 traders, 2 for 29 and 1 for 6 (table `ship_skills`, 19:51 UTC).

## Activities

**Trade beyond the borders (orders ENT-056).** I read fresh gaps by an
SQL join of the table `books` over books read within two hours and
wrote four one-ship tests (route files of 19:59 UTC), each first in one
trader's own list:

- `trade-silver-bar-alpha-to-arneb`: 50 silver bars bought at Node
  Alpha at 414 cr, sold into The Obsidian Well's bid of 501 at Arneb
  (16 jumps, lawless): **+4,099 cr in 21.6 minutes** (runs.jsonl, start
  20:00:54 UTC). The far bid read 44,477 after the sale (table `books`,
  20:23 UTC). Node Alpha's ask was gone after the buy, so the gap was
  one load; the route is off (Problems).
- `carry-hydrogen-beta-to-crucible`: 41 of a trader's own stored
  hydrogen and 24 heat sinks bought at Node Beta at 147, to The Crucible
  Garrison's bids of 37 x 184 and 193 x 24: **-1,475 cr in 26.3
  minutes**; the book after read hydrogen 38 x 21 and heat sink 133 x
  11 (20:27 UTC). What each item sold for is not measured: the run's
  log was overwritten by the next run. Off since 20:31 UTC.
- `go-ironlight-trader`: one trader docked at Ironlight Crossroads with
  an empty hold, 8 minutes, -14 cr; there I bought one listed **Prayer**
  freighter by hand (`buy_listed_ship`): 5,000 cr, no tax, cargo 540,
  speed 3, hull 40, no slot; booked as money paid once; the pilot
  released docked. It burned 12 fuel on its first four jumps and flies
  `carry-hydrogen-beta-to-crucible-bulk` (184 own hydrogen and 24 heat
  sinks, -3,563 cr for the sinks), whose result is read next turn.

**Missions that pay once.** `voidborn-neural-matrix-board` (5,000 cr,
9 jumps to Sirius) had not flown for 95.7 hours while 208 pilots lacked
it (`oncecheck.py`); the Central Nexus board offered it to a pilot
without it (`get_missions`, 20:13 UTC): max_ships 1 to 4. Traders handed
in 35,795 cr of once rewards since 19:00 UTC: Resonance finish 2 runs
20,910, Conductive Lattice 12,885, First Hunt 2,000 (runs.jsonl).

**Sell every division's surplus.** `reservecheck.py --plan trader`:
PASS, 54 routes, 0 flags. No home bid stood for a stored good above its
floor, so no sell route flew.

**The guidebook and the skill (queue.log ENT-189).** The trade
guidebook went from 2 chapters and 9 entries over their caps to none:
entries merged and rewritten, eleven retired and taken out by `guide.py
tidy trade` (kept in the store), three lesson entries written from my
turn skill's pitfalls; `guide.py check trade` PASS (20:33 UTC). The
skill trade-books went from 24,923 to 6,122 characters and points to
those entries; its stale pointer to `guidebook/trade.md` section 6 is
gone.

## Problems

- **A one-load gap went into the plan as a route** (errors.log ENT-113).
  I wrote the silver bar test with max_ships 1 and max_pilots 1 and no
  `once`; max_pilots limits pilots, not runs, so its pilot was sent
  again at once toward an ask that no longer stood, and a failed buy
  does not end a run (`game/fleet/route_run.py`). Cause: a lesson my
  own skill held since 2026-11-15, not applied to a route beyond the
  border. Done: the route is off since 20:26 UTC; the same check took
  the heat sink buys out of both Crucible carries, where two ships
  carried 24 heat sinks each to a bid of 24. The empty leg's fuel is
  not measured yet. Asked: a buy-end gate (requests.log ENT-297).
- **Two ships on one thin far bid.** The Crucible bids took one load;
  the freighter's run carries more than they hold, so most of its load
  will lie stored at The Crucible. Cause: I sized the test on a book
  four minutes old without counting that two of my tests sold into it.
- **33 traders wait docked**, the gate HALT. Cause: the home bids our
  stores sold into are gone, the traders' stores for crafting are used
  up, and no route trains trading without buying. Asked of the Fleet
  Admiral: requests.log ENT-286.
- **The clone has not pushed since 20:13 UTC**: the watcher's rebase
  fails every minute after the archive bot's commit of admirals.log
  (collective-pull.log). Reported to the keeper (queue.log ENT-194); not
  touched by me. The hashes of my commits after 20:13 UTC are not cited.

## Plans

Inside orders ENT-056, chosen by me:

1. Read the freighter's first RESULT line: credits, minutes, fuel per
   jump against the Threshold's, what The Crucible's bids took and what
   was stored there. If a Prayer's load pays its road, propose a
   freighter step for every trader with a load worth its road, inside
   rule F12 (10 Prayers stood at 5,000 cr at Ironlight Crossroads,
   `browse_ships`, 20:08 UTC), with the Fleet Admiral's answer to
   requests.log ENT-286.
2. Silver bars: with `requires.ask` (ENT-297) the Arneb route goes back
   into the plan gated on Node Alpha's ask; without it, one hand run
   each time a turn reads that ask standing. Whether the ask returns,
   and how often, is read from the table `moves` at each turn.
3. Far pairs: a far trade only where both ends stand deep in books read
   the same hour; the routemaker's trade candidates rest mostly on books
   of 2026-11-17, so each is a guess until a docked ship reads its book.
   The Obsidian Well's 44,477-deep silver bar bid needs a source: silver
   ore at 10 to a bar does not pay at today's asks (152 cr at Ironlight
   Crossroads against 501 a bar).
4. Every turn: the reserve first; every sell floor beside its cheapest
   deep ask (`sellgen.py scan`), since soma's deep ask at Central Nexus
   fell from 292 to 161 cr over the pause; `reservecheck.py` and
   `oncecheck.py`; the Neural Matrix runs at 4 ships, lifted further
   only on their own runs.
5. The traders that wait stay docked at no cost until a bid returns
   (the sell routes open by themselves) or the Fleet Admiral names
   their standing work. No trader is sent on another class's work
   (rule F23).

## Suggestions

1. **A buy-end gate on routes** (`requires.ask`, requests.log ENT-297;
   the Fleet Admiral's to build): a route that buys at one station and
   sells at another is bounded by both ends, and today only the sell end
   can close it. Cost: one field in the dispatcher beside `requires.bid`.
   It would have kept the silver route in the plan, closed, instead of
   off.
2. **The trader's standing work after a pause** (requests.log ENT-286,
   the Fleet Admiral's to decide): docked at no cost, or a jump loop that
   trains piloting toward the tier-2 freighter at about 165 cr a loop
   per ship, or freighters that make far trades worth a road. My
   recommendation: docked until the freighter's first carry is read.
3. **A failed buy could end a run** (`route_run.py`, the Fleet Admiral's
   script): an option on a `buy` step that stops the run when nothing
   was bought would make a buy-and-sell route safe even without the gate.
   Cost: a few lines in the runner; risk: a route whose later stops do
   not depend on the buy must not set it.

## Feedback

- **`hive.py briefing`** (preflight): the orders, the standing fleet and
  the gate in one answer at 19:42 UTC, and it named the HALT with the
  command to run. It worked; it took one call where the old start took
  many.
- **`fill.py status trader`**: named for every route of the plan why it
  was closed to the waiting pilots (no bid at the station, stores under
  the wanted units, full at its max). It is the call that showed the
  pause had emptied the home bids. It worked.
- **`fill.py fill`** offered one test, a Crimson visit mission
  (`mission-strategic-readiness-assessment-crimson`) whose board read
  dates from 2026-11-18 and which is Intel's work by rule F34; I left it
  to Intel (admirals.log ENT-073). The offer would be clearer with the
  board's age and the class whose work it is.
- **The table `books`** and its `t` column let me find the fresh far
  gaps in one SQL; the column names (`bid`, `ask`, `bid_qty`) differ
  from the market files' (`best_buy`, `best_sell`), which cost me two
  refused queries.
- **`scripts/guide.py`** (`sizes`, `check`, `tidy`): clear and safe; tidy
  took eleven retired entries out only after the store held them.
- **`plan.py planned` and `note`**: a line over 500 characters is refused
  with its length; it worked.
- **`gate.py book_onetime`** has no command form: I called it from
  Python to book the hull. A `gate.py book` verb would keep that in the
  tools.
- **The watcher** stopped pushing at 20:14 UTC (Problems); its log says
  so plainly.
- Built myself: the guidebook rewrite scripts and the slimmed skill.

## Learnings

From the learning capture of this turn:

- **The home bids do not survive a pause; the far books hold the
  depth.** After four days docked every home bid our stores sold into
  read 0, while The Obsidian Well bid 501 cr for 44,527 silver bars and
  Ironlight Crossroads asked iron ore at 4 cr for about 26.9 million
  (table `books`, 2026-11-21). Trade now reads far books for deep pairs,
  read the same hour, before it writes a far test. Kept in
  `knowledge/voidborn-order-books.md` (updated). For the fleet: after a
  pause or an update, read the books again before trusting any route's
  old figure.
- **A far deep bid is not a trade without a deep ask.** The silver run
  paid +4,099 cr once and then had nothing to buy; the Crucible bids took
  one load each. A far test is sized on the scarcer end, and two tests
  never sell into one thin bid. Kept in the guidebook, routes.md,
  `Trade beyond the border`, and errors.log ENT-113.
- **The next hull is on the ship exchange.** Other empires' tier-1
  freighters are flyable by our pilots and cheap (a Prayer of 540 cargo
  at 5,000 cr); my class card had read only our own empire's hulls,
  while Logistics had filed the listings on 2026-11-17
  (data/observations/logistics.jsonl). Kept unpromoted in LEARNINGS.md
  until the freighter's first carry is read; the card and ships.md name
  it. For Logistics: its hull test can rest on our reading (admirals.log
  ENT-073).
- **I repeated a mistake** (LEARNINGS question 8): the one-load gap in
  the plan, recorded since 2026-11-15. The fix had been a pitfall in a
  skill, which is a rule to remember; the gate asked in ENT-297 is the
  check that fires by itself.
- Skill: trade-books changed -- cut to the turn's procedure (6,122
  characters); its pitfalls moved into three lesson entries of the trade
  guidebook.
- Open: whether Node Alpha's silver bar ask regains, and what a Prayer
  burns a jump against a Threshold.

## Cross-links

- `reports/2026-11-17_mercury_make-before-gather-craft-own-stores-null-matter-pays.md` -- my previous report, the start of the period.
- `reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md` -- the Fleet Admiral's newest report.
- `game/routes/guidebook/trade/routes.md` -- the Standing Plan and `Trade beyond the border`.
- `game/routes/guidebook/trade/lessons.md` -- the lessons moved from the skill trade-books.
- `game/routes/trade-silver-bar-alpha-to-arneb.json`, `game/routes/carry-hydrogen-beta-to-crucible.json`, `game/routes/carry-hydrogen-beta-to-crucible-bulk.json`, `game/routes/go-ironlight-trader.json` -- the four tests with their readings.
- `communications/requests.log` ENT-286 and ENT-297; `communications/errors.log` ENT-113; `communications/queue.log` ENT-194; `communications/admirals.log` ENT-072 and ENT-073.
