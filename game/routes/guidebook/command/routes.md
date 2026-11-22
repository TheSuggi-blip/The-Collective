# Command guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-22. Evidence: the plan file (tool plan, show); fill.py status command; hive.py standing Unity; workclass.py sales.

Turn of 2026-11-22 21:30 UTC (orders ENT-067). The flagships take
the list First (the missions paid once), then their own routes: a test
the filler adds in front (three ships at most, rule F37), the missions
paid once of their boards, and the far hunts no other division claims
(one ship a herd, `max_ships` 1; the loot goes to a trader by
`gift_to`); then the hand-over routes of their own stores at each
station where they hold goods (to the receivers of Trade and Logistics,
rule F23 shared work), `store-hold` and `park` last. When the near
herds read under their floor, those hand-overs are the work that keeps
a flagship operating (fill gate PASS at 22:00 UTC). The flagships born
in other empires take work of their own region first: the dispatcher
keeps any route over six jumps from them closed unless it says
`far_ok` (rule F35, orders P6). A herd
another division claims is never in this plan (admirals.log; the filler
refuses it since commit 17cb9c29). They hunt for Combat and Piloting and
lead groups when Military flies one (rule F10); Leadership and Tactics
rise only by leading.

The faction's leader, a flagship: the sweep's gifts collect in
its wallet and it deposits between its runs, and a fund from the
treasury (`wallet.py fund`) is withdrawn only while it stands docked.
What would change the plan: a group hunt that kills, a command hull at
the next tier, herds that read below what a route needs (`carries`), or
a claim released.
