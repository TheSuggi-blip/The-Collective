---
name: install-gate-unblocked-treasury-relay-fixed
id: 20261123T110854Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, gates, wallets, treasury, requests]
links:
  - reports/2026-11-23_unity_foundry-deferred-flagship-lent-treasury-at-f7-line.md
  - reports/2026-11-23_oracle_worked-systems-to-region-lists-north-riders-doubled.md
  - reports/2026-11-23_zero_empty-slots-filled-newborn-crossings-gated.md
  - reports/2026-11-23_apollo_prayers-measured-batch-freight-mapped-notice-board-asked.md
  - reports/2026-11-23_apophis_losses-traced-fits-batched-far-herds-gate-closed.md
  - reports/2026-11-23_mercury_solarian-corridor-waiting-traders-into-once-missions.md
---

# The Collective -- The Install Gate Works Again, the Treasury's Relay Keeps What It Owes

## Situation

Period: from my report of 09:12 CET to this turn, 10:30 to about 12:30 CET
on 2026-11-23 (all times CET). Orders in force at the start: orders.log
ENT-081; at the end ENT-082 (this turn).

- **The purse** (tool fleet, view=kpi, computed 12:17): wallets 13,677,655
  cr plus the faction treasury 1,728,042 cr = 15,405,697 cr. Steady money
  (what repeats: sales and rewards that come again, minus fuel and repairs)
  is negative: -93,865 cr an hour over the last hour, -47,795 over 6 hours,
  -72,525 over 24 hours. Money paid once (mission rewards each pilot earns
  one time) ran +619,785 cr in the last hour and +301,794 an hour over 24
  hours, so the wallets still grew: the net of everything read +525,920 cr
  an hour (1 h), +229,269 (24 h).
- **Ships** (500): at 12:05, 367 at work, 6 starting, 125 waiting, 2 held
  by hand (`fill.py check all`).
- **Divisions**, own steady net over 24 hours (view=contribution, 12:17):
  Command -3,534 cr/h; Mining -24,212; Logistics -23,873; Trade +38,422;
  Military -32,507; Intel -26,821.
- **Services and jobs**: all ten services running, each started 11:54
  (`/srv/collective/services/status.json`). My five-minute job printed one
  HALT at 09:26 (four treasury top-ups refused: the leader's wallet held
  861 cr), fixed below. My hourly job printed a test-suite HALT at 11:46
  for the code of before my fixes: 5 of 102 test files failed; two are
  fixed this turn, one passed twice when run again, and three were cut by
  the check's own 180 s limit under load. `inbox.py new` printed nothing.

## Strategy

Suggi's standing goals G1 to G5 and his operational subgoals O1 to O10
stand unchanged, word for word, at the head of ENT-082. Trinity installed
three changes on Suggi's word this morning (queue.log ENT-263, commits
f4b42ec0 and 77d36968): each Admiral may now fund its own division's ships from the
treasury (up to 400,000 cr a ship, 750,000 cr a division a day, the
treasury keeping 500,000) and Logistics may build routine facilities
without asking me; any Admiral can stop one ship's run (`stop_pilot.py`);
and Military now farms pirates, solo or in formations of 3 to 20 or more
ships (rules F9 and F27).

What I decided this turn, in plain words:
- **Yes to the Notice Board** (requests ENT-440): a 50,000 cr board at Node
  Beta where we post paid delivery jobs for the station-core parts we cannot
  make yet; our haulers and neutral factions can fill them. It is one of the
  four trade channels Suggi asked for (O3, O10).
- **No to treasury money for tier-2 mining ships** (ENT-439): a Resonance
  Miner costs 283,809 cr; the ore it would carry most, iron, already stands
  above what we keep, and the ores we lack are short of fields, not of
  cargo space. Zero may fund one himself the day a rare-ore field in reach
  makes cargo the limit.
- **Orders ENT-082**: the same six-part plan; the Admirals are told to send
  waiting ships to the foreign capitals' paid-once missions by a single
  long trip (the "join corridor" Trade proved this turn), to read the
  station core's ores first (uranium, thorium, silicon), and Military to
  keep opening hunting grounds further out.

Proposal, not decided: a lean pass over the rulebook next turn (DECISIONS
Q75), because only 50 characters of room are left under its cap.

## Divisions

**Intel (Oracle, reports.log ENT-147).** Four systems where other divisions
work moved to the census lists of the capital nearest them; six explorers
now read the north road; the census ends at each pilot's own capital
(2156e121, my yes of queue ENT-259 landed). Freshness stays under target:
54.9% of places read within three hours (ALARM). Suggestions: a check that
names files left uncommitted in the shared clone -- **open**, my build next
turn (Q75 (3)); the same fault blocked four installs today. SPACEMOLT.md at
86% of its cap -- **closed** by Trinity's 90% warning line (ENT-263); no
trim needed.

**Mining (Zero, ENT-148).** Empty laser slots filled by empire (10 fit runs,
12,026 cr of modules); ships with off-role starter modules 129 -> 121. Twelve
Nebula-born miners flew about 20 jumps to store small holds (errors.log
ENT-154); Zero closed it the same turn with a reach limit on the home store.
Suggestions: a reach rule for store-only routes in the dispatcher --
**open**, put to Trinity (Q75 (2)): Suggi's corridor unlock of today sends
standing work without a reach on purpose, so where work ends and a mere
store trip begins is the designer's line to draw; a per-ship stop --
**done** by Trinity (`stop_pilot.py`, ENT-263).

**Logistics (Apollo, ENT-149).** Three Prayer freighters bought or
commissioned (19,556 cr, booked once); the shipping board mapped: 13 of 165
contracts run through our space, the best pays 361 cr. 80 haulers still
wait at 12:05 (73 at his turn's start): no class work in reach. Suggestions:
a freight step in the circuit runner -- **accepted**, his build; the Notice
Board now -- **accepted** (ENT-440); the outpost's 100,000 faction iron for
steel -- **declined for now**: 12,170 iron already lies at Factory Belt and
Grand Exchange in miners' storage for his two new steel routes, waiting on
Zero's give routes (ENT-437).

**Military (Apophis, ENT-150).** Four ships lost in 24 hours, all traced
(errors.log ENT-155): two newborns on a chain of short hunts while still in
a fight, two fitted hunters at whale herds. Two whale hunts off for danger;
11 Laser III and 11 Shield Booster II fitted (232,661 cr from the ships'
own wallets); 8 far hunts; drones waiting 5 -> 0 at 11:13. Suggestions: the
install gate -- **accepted and done** (418871ed), and his runner fix
installed for him (ENT-441); the briefing's loss line naming hour and ship
-- **open** (Q75 (5)); Trade watching our own yard's bids -- Mercury's call
(ENT-438).

**Trade (Mercury, ENT-151).** A one-stop far trip to Sol opened the Solarian
paid-once missions to waiting traders: at work 14 -> 54 within the hour,
352,480 cr paid once against 14,418 cr of fuel; 39 still wait at 12:05.
Suggestions: the route maker sizes a new once route's cap to the pilots its
board serves, not 3 -- **open**, my build (Q75 (6)); the join pattern for
every division -- **accepted**, now in Apollo's block.

Thread check: ENT-081 said no trader or hauler waits docked. Traders
improved (71 -> 39 waiting), haulers did not (73 -> 80). Mercury's paid-once
figure fits the store's: 619,785 cr paid once in the hour to 12:17.

## Plans

What I did for the Admirals' next turns (from 13:00 CET):

- **The install gate works again.** Three faults failed every member's
  install this morning: the rulebook stood 1,467 characters over its cap
  after the pirate-farming rules (fixed by rewording four rows and leaving
  F16's list of who does what to ROSTER.md, its one home: 88e94009); a test
  that pruned its own rows by the clock after seven days (fixed in
  2a3cfcb6); and the gate crashed on a slow test file and could not put
  files back while another member committed (fixed in 418871ed).
- **The treasury's relay** (2a3cfcb6): money the leader withdraws for named
  pilots is no longer given away to others first; old top-up rows whose
  pilots were served another way end: 17 had ended by 12:07, and at
  12:25 none stood withdrawn (34 ended, 32 given; funds.json).
- **Military's runner fix** (ships still in a fight flee first; under 60%
  hull they go to repair): installed for Apophis (b8b901ae, requests
  ENT-442).
- **Flagships**: three waited at the turn's start (FLEET.md, briefing).
  The last two waiting got the flagships' own one-stop trip to Sol's
  paid-once missions (`join-sol-command`, adfe6bba), standing so that the
  loss stop does not rest a trip that earns nothing itself; at 12:22 every
  command ship flies (`fill.py check command` PASS).
- **The hourly test check** stops a file at 180 s; one store test alone
  ran 190 s in my copy. Its author is Trinity: the limit is put to him
  (queue.log ENT-268), with the gate's 600 s as the measure.

Next turn (14:30 CET): the open builds of DECISIONS Q75 -- the rulebook lean
pass, the uncommitted-files check, top-up withdrawals by any docked
officer, the loss line, the route maker's cap; post the first Notice Board
job once Apollo reports it standing; read the leader's wallet back above
rule F7's floor.

## Advice and Suggestions

Nothing in this turn needs your word. In plain words: the fleet earns most
of its money right now from missions each pilot can do only once (about
300,000 cr an hour), while its repeating work loses about 50,000 to 100,000
cr an hour, mostly fuel for travel. The once-money will run out as pilots
finish their lists, so the turns ahead push the repeating work up: selling
what we hold, crafting at stations without flying, and the delivery jobs
the new Notice Board will carry.

Advised focus for you to watch: the rulebook is full. Each new rule you
give through Trinity now needs an old line merged, or every member's tools
stop installing, as happened today from 11:37 to 11:47. I will shrink
it next turn. The question of a second faction (DECISIONS Q74)
remains yours; I read it again before the endgame, and nothing is done
meanwhile.

## Learnings

- **Credits held for someone are no one else's to give.** The leader held
  226,852 cr withdrawn for named pilots; the top-up pass treated it as free
  money and gave it away, the named gifts then failed and the leader fell
  under the 3,000 cr floor. Record: funds.json (withdrawals of 07:32 and
  09:48 for 44 and 19 pilots); the routes-index HALT of 09:26. Change: owed credits are subtracted from
  every donor (2a3cfcb6). Kept in: knowledge/money-figures.md. Takeaway: a
  relay wallet is two purses in one; the code must name both.
- **A shared gate runs under everyone's load.** A 300 s test limit and a
  put-back without retry turned normal concurrency into failed installs and
  files left in the clone. Record: errors.log ENT-155, requests ENT-441, my
  two failed installs. Change: 600 s and retries (418871ed). Kept in:
  knowledge/faults-that-leave-no-record.md.
- Skill: fleet-build no change -- its commands held; the gate itself was
  fixed.

## Cross-links

- `reports/2026-11-23_oracle_worked-systems-to-region-lists-north-riders-doubled.md` -- Intel.
- `reports/2026-11-23_zero_empty-slots-filled-newborn-crossings-gated.md` -- Mining.
- `reports/2026-11-23_apollo_prayers-measured-batch-freight-mapped-notice-board-asked.md` -- Logistics.
- `reports/2026-11-23_apophis_losses-traced-fits-batched-far-herds-gate-closed.md` -- Military.
- `reports/2026-11-23_mercury_solarian-corridor-waiting-traders-into-once-missions.md` -- Trade.
- `communications/orders.log` ENT-082 -- the orders now in force.
- `communications/requests.log` ENT-439, ENT-440, ENT-442 -- my answers (ENT-441 Military's ask).
- `communications/queue.log` ENT-263 (Trinity), ENT-266 (the gate faults), ENT-267 (wallet, store test, hunt fix), ENT-268 (the hourly test check, to Trinity).
- `governance/rulebook.md` -- rows F9, F16, F27, F39 and section 14 reworded.
- `governance/strategy.md` -- phase 1, income, unchanged.
