# Command guidebook -- Topic: systems (topic-systems.md)

### What Limits Scale
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 4.

| Limit | Value |
|---|---|
| Agents | The Fleet Admiral and five Admirals |
| Credits | A new account brings 100 cr and a tier-0 hull; hulls and fits come from income |
| Faction members | 20 today; 50 with a Hiring Board, 100 with a Recruitment Desk, then 200, 400, 1,000 |
| What we may build | Eight outposts per faction; a station of our own takes 5,000,000 cr and a station core |
| The unit | The agents share one container of 4 CPUs and 6 GB, and the services share Suggi's server: one whole test suite per install, no polling, nothing left running |
| The server | Sign-ins 30 a minute; push over polling; no runaway loop |
| Visibility | Rosters and pilot pages are public |

### The Engine and the Door
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 5.

- Four ways to fly were compared on 2026-11-14: the game's own MCP
  (one ship per session, a tool list of 24,000 to 82,000 tokens), a
  proxy with a model turn per ship every 90 s, the daemon setpoint
  built on the official library, and an engine of our own on that
  library.
- In force: setpoint is the engine, run by the box in a container
  that alone holds the key, pinned to one commit (`BOX.md` 7). In
  front of it stands a door of our own: the fleet's scripts with the
  lock of the divisions, and the collective MCP server through which
  every member reads and commands (`BOX.md` 9.3, 9.11).
- Why both: setpoint's goals and loops cover what we would otherwise
  learn by losing ships, and its API has no sign-in, knows no
  divisions and passes any raw command, none of which may reach an
  agent unfiltered.
- It is the reversible choice: if setpoint is abandoned or falls
  behind the game, the engine is replaced by our own code on the same
  library and the same key, and the members' tools do not change. The
  game changes often; an engine nobody updates stops flying.
- The risks seen (one author, no CI, no sign-in on its port) and what
  was and was not tested: the archived text, sections 9.3 and 9.7.

### The Work Cycle
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 6.

- Each Admiral takes a turn every four hours, 15 minutes after the
  one before: Zero, Oracle, Mercury, Apollo, Apophis; Unity an hour
  and a half after the last. A
  turn is a session of its own: preflight, the division's work, the
  fill gate, session-end with a report (`BOX.md` 3.6). That is 36
  sessions a day.
- A turn sets work up; it does not fly ships by hand (rule F29).
  Between two turns code flies: the dispatcher and the runners, the
  five-minute and the hourly pass, the guards (wallet, loss stop,
  claim watch). Nobody waits for a hand (rule F32).
- The orders are the newest entry of `orders.log` and stay lean: only
  Suggi's standing orders and goals are permanent; a task leaves when
  it is done, and what lasts becomes a rule.
