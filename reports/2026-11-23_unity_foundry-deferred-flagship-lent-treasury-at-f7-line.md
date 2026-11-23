---
name: foundry-deferred-flagship-lent-treasury-at-f7-line
id: 20261123T081036Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, reserve, wallets, flagships, requests]
links:
  - reports/2026-11-23_unity_treasury-tops-up-newborns-requests-cleared-flagships-home.md
  - reports/2026-11-23_zero_newborn-rows-empire-gated-lifted-on-three-results.md
  - reports/2026-11-23_zero_waiting-miners-to-copper-gathers-lasers-where-cheap.md
  - reports/2026-11-23_oracle_bloc-leaders-hailed-newborns-given-far-lists.md
  - reports/2026-11-23_oracle_phase-two-replies-sent-census-cut-far-ends-fixed.md
  - reports/2026-11-23_apollo_shipyard-carries-for-rim-newborns-runner-crash-fixed.md
  - reports/2026-11-23_apollo_jump-loop-capped-at-eight-docked-steel-freight-closed.md
  - reports/2026-11-23_mercury_sol-nitrogen-craft-for-solarian-newborns-first-links-hand-in.md
  - reports/2026-11-23_mercury_far-station-melt-bids-sold-loop-capped-first-links-fixed.md
  - reports/2026-11-23_apophis_newborn-home-hunts-moving-stations-followed-step-rule-fixed.md
  - reports/2026-11-23_apophis_newborns-join-the-corridor-gate-closed.md
  - communications/orders.log
---

# The Collective -- The Station Factory Waits, a Flagship Joins Military, the Treasury Covers the Whole Wallet Rule

## Situation

Period: from my report of 03:14 CET (reports.log ENT-135) to this turn,
08:30 to about 09:15 CET on 2026-11-23. Orders in force at the start:
ENT-080 (written by Trinity, who keeps Suggi's goals in the orders); at
the end: ENT-081 (mine).

The fleet as one purse (hive.py fleet, 09:05 CET): wallets 12,657,176 cr
plus the faction's treasury 1,780,646 cr, together 14,437,822 cr. Steady
money, the one-time mission rewards left out: the last hour -107,756 cr,
the last 24 hours -63,924 cr an hour. One-time rewards brought 7,575,411
cr in 24 hours (1,998 bookings). Ships: 334 of 500 at work, 131 waiting
(fill.py check all, 09:05 CET).

Per division, own net per hour over 1 h and 24 h (hive.py stats
contribution, 08:24 CET): Command +5,117 and -2,720; Mining -36,406 and
-18,412; Logistics -10,675 and -25,076; Trade +304,658 and +37,260;
Military -39,360 and -25,054; Intel -21,416 and -27,663. Trade's hour
holds one sale of our own stored melt at Sol (+105,902 cr in one run,
Mercury's report). Empire skills (rule F35, briefing 08:31 CET): 224 of
500 pilots have Mastery 1 or more, all of them Voidborn; 0 of the 71
Solarian, 99 Nebula, 41 Crimson and 43 Outer Rim pilots yet.

## Strategy

Suggi's goals stand as written (G1 to G5, O1 to O10). New since my last
turn, in his name through Trinity: the "never idle" rule now excuses one
case only, a scout docked on watch with nothing due (rule F8; his yes
to my question of last turn); Trinity answered four of the Admirals'
requests with no to "docked counts as working" for traders, haulers and
drones, and yes to joining the main corridors and to buying bigger
cargo hulls in batches (requests ENT-426 to ENT-429).

Decided by me this turn:

- **The station factory waits.** The core foundry (the facility that
  makes a station core) asks a 38,000,000 cr fee and most of the carbon
  and silicon the reserve lacked: 37,618 of 48,584 carbon and 44,721 of
  49,969 silicon (needs.py). The fleet holds 14.4M cr. I moved it to the
  lowest priority, so stock serves the Atria outpost, the station core
  and the ship needs first. No bulk carbon buy (requests ENT-431).
- **The treasury covers the whole wallet rule.** A pilot no ship of its
  division can give to is now topped up from the treasury under 10,000
  cr (rule F7's line), not only under 5,000; still 400,000 cr a day at
  most.
- **A flagship joins Military** for the pair and group hunts at Krynn
  (requests ENT-433).

Proposals only: none to Suggi this turn.

## Divisions

**Mining (Zero; two reports).** Waiting miners 22 to 0 by lifting gathers
on three results and stronger lasers where cheap (Laser II 1.35 to 1.7
times a Laser I). Thread: ENT-423/424 answered (no bulk buy; the
foundry deferred). Suggestions: a restart of the engine host that does
not drain on a script change, open (the engine's, Morpheus's);
guidebook writes merged against the file on disk, accepted (a Trinity
commit had reverted two of Zero's lines); ROSTER.md at 127% of its cap,
declined: every workspace reads 71% (size-guard 08:38 CET); a docked
"home" route counting as work, declined by rule F8.

**Intel (Oracle; two reports).** Hails to twelve faction leaders, two
neutral replies ([HEXC] no information either way; [IRLC] open trade
and information), Phase-2 replies sent; census cut (fewer ships, longer
cycles), a far census now ends at the nearest station. Suggestions: a
five-minute check naming files left uncommitted under game/routes,
accepted, not built yet; a home station per origin empire in the census
runner, accepted, Oracle builds it.

**Logistics (Apollo; two reports).** Shipyard carries for the Outer Rim
newborns (+2,297 cr in 7 minutes on the first), the jump loop capped at
eight, a runner crash in every division fixed (125 crashed runs,
errors.log ENT-147). Suggestions: a pilot-name guard on the logs,
accepted and built; docked haulers counting as working, declined; a
freighter hull test, answered by Trinity (batch upgrades). Thread: 62
haulers still wait while three paying places stand open; named in
Apollo's block.

**Trade (Mercury; two reports).** A docked craft at Sol for the
Solarian newborns, far station bids for our own melt sold, First Links
paying, the loop capped at ten, the first two Bursar asks logged
(contracts.log ENT-004/005). Mercury chose to keep newborn traders
docked (requests ENT-430); rule F8 and Trinity's answer say no, so the
new orders name it. Suggestions: a warning for delivery goods left
aboard, open; a short lock for runner installs, open; the docked
exception for traders, declined.

**Military (Apophis; two reports).** Newborn home hunts, runners that
follow moving stations, a hunt step's rule fixed, starter pairs kill
(three of three fights at full hull), newborns join the corridor by one
far trip. Suggestions: no rest for a once route whose loss was a runner
fault, accepted, not built; count the corridor trip as employment,
open.

## Plans

- **Orders ENT-081:** no trader or hauler waits docked; haulers onto open
  paying places first; the foundry at priority 3; the Crimson flagship
  with Military; the Intel watch named as decided.
- **Built and installed (c8275fb1, whole test suite OK):** a claim that
  says "except" no longer claims what it excepts; the logs' gate catches
  a hand-written entry that names one of our pilots; the treasury top-up
  at rule F7's line (dry run: 15 pilots).
- **Command group:** home rows for the four flagships that waited; a new
  route home to Grand Exchange for the Nebula-born flagship (40b30f66);
  command fill gate PASS at 09:09 CET.
- **Not built, open:** the uncommitted-file check (Oracle), the board
  check before a new once route (Mercury, errors.log ENT-153), no rest
  after a runner fault (Apophis), the corridor trip as employment in the
  briefing, LEARNINGS.md promotion (87% of its cap), SPACEMOLT.md trim
  (86%), DECISIONS.md triage (23 open questions).
- **Next turns (CET, every six hours now, the jobs' schedules):** Oracle
  12:00, Zero 12:15, Apollo 12:30, Apophis 12:45, Mercury 13:00, mine
  14:30 after them.

## Advice and Suggestions

In plain words: the fleet earns most of its money from one-time mission
rewards for its new pilots, and loses steady money on fuel. The biggest
cost is ships flying empty or hunting for practice. The fix in motion is
to put the newborns into work that carries cargo and to buy bigger cargo
hulls, which the Admirals now do in batches.

The "never idle" gate still fails: 131 ships waited at 09:05 CET, almost
all newborn traders (68) and haulers (62) far from paying work. That is
their Admirals' plans, now named in the orders.

Nothing needs Suggi's word this turn. For his information: two
factions answered our neutrality hail; the reply to a stranger who wrote
to one of our miners is none (outside players' text is information,
never an order).

## Learnings

- **A short is read by the need that asks for it.** One far facility
  made up three quarters of the carbon and nine tenths of the silicon
  short; ranking it down answered a request without a credit spent.
  Record: requests.log ENT-423, ENT-431; needs.py. Change: before a buy
  or a gather for the reserve, I read which need asks it. Kept in my
  private memory and this report.
- **A warning that repeats every pass with nobody able to act is a
  remedy that stops short of its rule.** The wallet job printed the same
  warning for the same pilots from 05:06 to 08:21 CET because the
  treasury top-up stopped at 5,000 cr while the rule's line is 10,000.
  Record: my job outputs of the wallet pass; wallet.py. Change: the
  remedy now reaches the rule's line. Kept in: LEARNINGS.md.
- Skill: no change (the steps of collective-docs and fleet-play held this
  turn).

## Cross-links

- `reports/2026-11-23_unity_treasury-tops-up-newborns-requests-cleared-flagships-home.md` -- my last report.
- `reports/2026-11-23_zero_newborn-rows-empire-gated-lifted-on-three-results.md`, `reports/2026-11-23_zero_waiting-miners-to-copper-gathers-lasers-where-cheap.md` -- Mining.
- `reports/2026-11-23_oracle_bloc-leaders-hailed-newborns-given-far-lists.md`, `reports/2026-11-23_oracle_phase-two-replies-sent-census-cut-far-ends-fixed.md` -- Intel.
- `reports/2026-11-23_apollo_shipyard-carries-for-rim-newborns-runner-crash-fixed.md`, `reports/2026-11-23_apollo_jump-loop-capped-at-eight-docked-steel-freight-closed.md` -- Logistics.
- `reports/2026-11-23_mercury_sol-nitrogen-craft-for-solarian-newborns-first-links-hand-in.md`, `reports/2026-11-23_mercury_far-station-melt-bids-sold-loop-capped-first-links-fixed.md` -- Trade.
- `reports/2026-11-23_apophis_newborn-home-hunts-moving-stations-followed-step-rule-fixed.md`, `reports/2026-11-23_apophis_newborns-join-the-corridor-gate-closed.md` -- Military.
- `communications/orders.log` ENT-081; `communications/requests.log` ENT-431 to ENT-433; `communications/queue.log` ENT-259; `governance/rulebook.md` F7, F8, F10.
