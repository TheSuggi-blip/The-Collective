---
name: claims-hold-again-treasury-fund-built-two-asks-done
id: 20261122T141814Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, claims, treasury, strict-classes]
links:
  - reports/2026-11-22_unity_strict-classes-on-five-requests-built-hull-funding-next.md
  - reports/2026-11-22_zero_strict-classes-miners-gather-and-give-jump-loop-cut.md
  - reports/2026-11-22_oracle_census-roads-given-ships-unflown-line.md
  - reports/2026-11-22_mercury_nexus-melt-sales-and-docked-carapace-crafts.md
  - reports/2026-11-22_apollo_recruitment-center-raised-receivers-spread-gold-wiring.md
  - reports/2026-11-22_apophis_whale-group-proven-hunts-ordered-by-fuel-per-xp.md
---

# The Collective -- Claims Hold Again, the Treasury Can Pay One Ship, Two Asks Done

## Situation

Period: since `reports/2026-11-22_unity_strict-classes-on-five-requests-built-hull-funding-next.md` (11:05 CET) to 15:18 CET. Orders in force: `orders.log` ENT-064 (written this turn; ENT-063 before).

- **The purse** (`hive.py fleet`, 15:18 CET): wallets 8,058,575 cr plus the treasury 1,703,288 cr, 9,761,863 cr in all. At my last report it was 11.63 million. The 2,000,000 cr Recruitment Center fee left the treasury at 12:56 CET (Apollo, queue ENT-224), so the drop is that one payment, not a loss.
- **Steady money** (`hive.py stats kpi`, 15:16 CET; fuel and running costs in, one-time rewards out): -20,796 cr an hour over the last hour, -39,464 over 6 hours, +3,773 over 24 hours. One-time money (mission rewards less one-time buys) adds +80,138 an hour over the last hour. In plain words: since strict classes went on (10:35 CET), only traders sell, so every other division's work shows as fuel spent. Trade's sales grow (Trade earned +60,594 net in the last hour), but they do not cover the fleet's fuel yet.
- **Ships:** 246 of 246 working, none lost. The "never idle" check passed for every role at 15:12 CET (`fill.py check all`).
- **Per division, last hour** (`hive.py fleet`): Command -3,067; Intel -23,440; Logistics -17,047; Military -27,223; Mining -13,477; Trade +60,594 cr.
- **Faction seats** (briefing): 99 of 200. The Recruitment Center is under construction, which is why the cap reads 200.

## Strategy

The standing orders S1 to S5 and the goals G1 to G5 stand as Suggi set them. Only he changes them.

Decided this turn (the Fleet Admiral's own calls):
- **Claims count again for hunting grounds.** When one division claims a herd, no other division's plan may take it. Since strict classes went on, this rule had silently stopped working for hunts (cause below). The fix is in, and I took 29 claimed herds out of my own flagships' plan.
- **The treasury can now pay one ship for one purchase.** That was the missing piece for Military's first tier-2 warship, the Recursion. The game lets the faction leader take money out of the treasury only while docked, so the script waits for that moment. 320,000 cr are booked for it.
- **Orders ENT-064:** my block now asks for two figures two Admirals each asked for. P4 now reads "Recruitment Center raised". Apollo's block moved on from that build.

My proposal, not yet decided by anyone above me: the fleet should be judged on P1 ("pay for itself") only once the goods the hunters and miners hand over are valued. Today that value appears nowhere, so those divisions read as pure cost. Building that figure is my first task next turn.

## Divisions

- **Mining (Zero, reports.log ENT-111).** The miners now hand their ore to the receiving ships. A jump loop that only trains piloting fell from 14 ships to 5, and none waited. Suggestions: the "any one of several goods" gate, accepted and built (requests ENT-353). Stores that no hand-over route reaches, accepted: Mercury asked the same, so it is a missing tool and I build it next turn. The two disagreeing iron figures stay open; not worked on this turn.
- **Intel (Oracle, ENT-112).** A census list had flown no run for 10 hours. Oracle gave it ships of its own and a check that stops his turn when a list goes unflown. Suggestions: the filler's preview and its write named different hunts. Open: the cause I found today explains the claimed hunts, and his case had no claim; I read it next turn. Flag a standing route with no run in its cadence: open. Filter the route check's warnings by plan: open, small.
- **Trade (Mercury, ENT-113).** The first loot sales landed: 33,437 and 57,492 cr in two runs at Dheneb. Melt carries and carapace crafting started within 15 minutes. Suggestion: stores no route reaches, accepted (see Mining). His error ENT-134 (old drafts copied by a wildcard) was fixed in his own skill.
- **Logistics (Apollo, ENT-114).** He raised the Recruitment Center from the treasury in 5.3 minutes and named ten more receiving ships. Suggestion: warn when a one-time buy route is not marked standing work. Accepted, next turn; it is the class of three errors this day (ENT-128, ENT-132, ENT-135).
- **Military (Apophis, ENT-115).** A group of three ships killed pilot whales three times out of three at full hull, the first proven group play. Suggestions: a "group" route kind for the dispatcher, open (a build turn of its own, queued since DECISIONS Q72). Goods handed over at their worth per division: accepted, next turn. His requests ENT-352 (1) and (2) were done this turn (ENT-354).
- **Thread check:** the claimed-hunt fault I logged at 11:00 CET (errors ENT-131) is closed with its cause (ENT-136). The Recursion step I promised is built, but not paid yet.

## Plans

Next turns (CET): Zero 16:00, Oracle 16:15, Mercury 16:30, Apollo 16:45, Apophis 17:00, mine 18:30.

- **Builds for my next turn, in order:** (1) the goods each division hands over, valued at the bid they could sell for, as a figure in the store and in the "contribution" view; (2) a line per role for the stores no open route reaches; (3) the route check's warning on a one-time buy that is not standing work; (4) read Oracle's preview-against-write case.
- **The Recursion:** the five-minute pass serves the fund the first time it finds the leader docked. It tries 1 cr first, as rule F12 asks, then moves 320,000 cr. `wallet.py fund --show` reads its state (open at 15:14 CET: "the leader is not docked"). When it is paid, Military buys the hull at its next turn, and I close requests ENT-345.
- **Still not built** (DECISIONS): the group route kind (Q72/Q73), the two iron figures, the survey visit step (Q66), stored goods counted at their worth inside a run's figure (Q71).

## Advice and Suggestions

- What I decided and why, in plain words: hunting grounds are claimed one ship per herd so ships do not crowd and starve each other. The fault let anyone take a claimed herd, so I fixed the rule in code, not by reminding people.
- What to watch: the fleet's steady money is negative since strict classes started (-39,464 cr an hour over 6 hours). That is expected while the receivers learn to sell. If 24 hours from now it is still negative with the hand-over value counted, the order of work needs to change (fewer far hunts, more selling).
- Nothing waits on Suggi. No new pilot, war, alliance or message to another player is proposed. No pilot wrote to our ships (`inbox.py new` empty). My two jobs without AI printed nothing unusual since my last report.

## Learnings

- **Lesson:** a switch can change what a shared word means for every program that reads it. Strict classes made every hunt that gives its loot "standing work", and the claim reader trusted "standing work is never claimed". So claims went void for 4.5 hours without any error. Record: errors.log ENT-131, ENT-136; commit 17cb9c29. Change: before I switch something on, I search every reader of each property it flips and run their tests with the switch on. Kept in: `LEARNINGS.md` (unpromoted). Fleet takeaway: an Admiral adding a switch names every reader in its commit.
- **Game fact:** the treasury pays out only to a docked leader, through the storage call with source "faction" and target "self". Two other action names the engine does not know. Record: three refused probe calls 14:58 to 15:01 CET; the game's help of the storage tool. Kept in: skill fleet-ops, `references/faction.md`.
- Skill: fleet-ops changed -- treasury withdrawal call and its docked requirement.

## Cross-links

- `reports/2026-11-22_zero_strict-classes-miners-gather-and-give-jump-loop-cut.md` -- Mining under strict classes.
- `reports/2026-11-22_oracle_census-roads-given-ships-unflown-line.md` -- Intel's unflown census list.
- `reports/2026-11-22_mercury_nexus-melt-sales-and-docked-carapace-crafts.md` -- Trade's first loot sales.
- `reports/2026-11-22_apollo_recruitment-center-raised-receivers-spread-gold-wiring.md` -- the Recruitment Center raised.
- `reports/2026-11-22_apophis_whale-group-proven-hunts-ordered-by-fuel-per-xp.md` -- the first proven group hunt.
- `communications/orders.log` ENT-064; `communications/errors.log` ENT-136; `communications/requests.log` ENT-353, ENT-354; `communications/queue.log` ENT-225.
- `governance/strategy.md` -- phase 1, income.
