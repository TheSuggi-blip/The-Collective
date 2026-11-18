# Command guidebook -- Lessons (lessons.md)

### About DESIGN.md
Status: proven. Updated: 2026-11-18. Evidence: migrated from DESIGN.md, the text above its first section.

How the fleet is built and why: the layers of command, accounts,
divisions, sizes, growth, the engine and the work cycle. It holds the
design in force and its reasons, and nothing another file owns: ranks
and the chain of command are the constitution's; goals and phases
`governance/strategy.md`; the rules `governance/rulebook.md`; roles
and missions `ROSTER.md` and each `MISSION.md`; the systems as built `BOX.md`; the plan
of now the newest entry of `communications/orders.log`.

The file is kept short (Suggi, 2026-11-17): at most 20,000
characters, and the pre-commit hook blocks a commit beyond that. The
research behind it (2026-11-14 and 15: the game's facts with their
sources, other operators, agent teams, four ways to fly a fleet, what
was checked of the engine, the records of the first two waves, what
the Admirals needed at birth, 36 sources) stands word for word in
`memory/2026-11-17-design-full.md`, found by `query-workspace-unity`.
A figure of sections 1 and 2 has its source there (its sections 1 to
3, 7 and 11); an older record that cites `FLEET.md s.<n>` or
`DESIGN.md s.<n>` means that text.

### Game Facts That Shape the Fleet
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 1.

| Fact | Consequence for us |
|---|---|
| One account flies one ship and takes one action per tick of 10 s | A division of n ships is n accounts; work scales with accounts, not with hulls owned |
| Many accounts under one website account are allowed; one game-client API key acts as all of them | One secret controls the fleet: the engine alone holds it (section 5) |
| One program may drive an account; a name and an empire are permanent | One driver per ship; a name states its division for good |
| Skills belong to the pilot, rise only by doing the activity and are never lost; a hull has fixed slots: "there is no fit that does everything" | Specialists, not allrounders (section 3.4); levelling is part of every plan (rule F23) |
| Hull tiers 2 to 5 need Piloting 10, 20, 30 and 50 | A ship's next hull is earned by flying |

### Game Facts That Shape the Fleet, continued
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 1.

| Fact | Consequence for us |
|---|---|
| Every new pilot starts with 100 cr in a free tier-0 mining ship | A role's hull and fit are bought from what the fleet earns |
| A faction holds 20 members without a recruitment office (the game refused the 21st join on 2026-11-17) and 50, 100, 200, 400 or 1,000 with one; joining is by invitation | The faction grows by offices (`BOX.md` 9.5; goal G2) |
| An outpost stands in lawless space only, eight per faction; a Faction Lockbox needs a station | Where we build: rule F33 |
| Faction rosters and each pilot's page are public | Names state a role and nothing else; positions and plans stay in the data folder |
| Voidborn: shields and cloaking; +12 percent shield, +3 percent cargo, +2 percent speed | It suits a fleet that scouts and is not seen |
| Fuel is the only running cost; the weekly tax is 6 percent of income and 0.75 percent of ship value | A ship that flies without a buyer for its cargo loses money; a docked ship costs nothing |
| Sign-ins: 30 a minute per address; 100 connections per address before batching | Pilots are born in waves, never in a tight loop |

### What Others' Fleets Taught
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 2.

- One model and good code run 154 ships (Wexler's Void Safari): the
  ships are code, the model supervises and fixes the stuck ship.
- About 200 scripted ships, 160 miners to 40 haulers and one hub
  pilot (Brocktree): "Scripts are cheaper than tokens"; planning for
  200 agents by a model "almost always overwhelmed them"; a quarter of
  the swarm was lost in two hours because every miner converged on an
  attacker. A reflex others can predict is farmed.
- An agent self-destructed a new hauler against warnings (hiver):
  what must never happen is refused in code, not remembered.
- The largest fleet (Busy Being Dead, 1,249 pilots, second by wealth)
  names its pilots by five roles: 54 percent fighters, 24 percent
  miners, 8 percent haulers, 8 percent market, 2 percent scouts,
  registered in waves over seven months. It books 95 percent of its
  credits on 58 pilots outside those roles: the goods are sold by a
  few.

### What Others' Fleets Taught, continued
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 2.

- Of 6,590 pilots with 50 hours or more, those who only mine earned a
  median of 81 cr an hour, those who trade and do not mine 1,687.
- The server is run by volunteers: one operator used half a month's
  bandwidth, and a runaway loop is seen by the developers and the
  galaxy. Push over polling, no loops that die and restart.
- Command research: one commander leads three to seven; independent
  agents amplify errors 17 times, a central orchestrator 4 times;
  beyond about 20 coordinating agents success drops; many agents cost
  3 to 15 times the tokens of one.
