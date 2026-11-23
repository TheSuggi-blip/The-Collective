# Command guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-23. Evidence: the plan file (tool plan, show); fill.py status command and check all (2026-11-23 11:05 UTC); hive.py standing Unity; workclass.py sales; requests.log ENT-433; trade report 2026-11-23 (join corridor).

Turn of 2026-11-22 21:30 UTC (orders ENT-067). The flagships take
the list First (the missions paid once), then their own routes: a test
the filler adds in front (three ships at most, F37), the missions
paid once of their boards, and the far hunts no other division claims
(one ship a herd, `max_ships` 1; the loot goes to a trader by
`gift_to`); then the hand-over routes of their own stores at each
station where they hold goods (to the receivers of Trade and Logistics,
rule F23 shared work), `store-hold` and `park` last. When the near
herds read under their floor, those hand-overs keep a flagship
operating. The flagships born
in other empires take work of their own region first: the dispatcher
keeps any route over six jumps from them closed unless it says
`far_ok` (rule F35, orders P6); a flagship far from its region heads
its row with the one far_ok stop home (`home-<capital>`), and one
whose home stop rests takes the near hunts no ship flies. A flagship
may be lent to Military for its group hunts by the role in its
flagship entry, as the sentinels are (rule F10). A herd
another division claims is never in this plan (admirals.log; the filler
refuses it since commit 17cb9c29). They hunt for Combat and Piloting and
lead groups when Military flies one (rule F10); Leadership and Tactics
rise only by leading. When the near herds and the home boards are
spent, a flagship heads its row with the paid-once missions of a
foreign capital and the one-stop far trip there (`join-sol-trader`,
Trade's join corridor).

The faction's leader, a flagship: the sweep's gifts collect in
its wallet and it deposits between its runs, and a fund from the
treasury (`wallet.py fund`) is withdrawn only while it stands docked.
What it withdraws for named pilots is owed, never a donor's to give
(`wallet.py owed`, 2a3cfcb6); read its wallet each turn.
What would change the plan: a group hunt that kills, a command hull at
the next tier, herds under what a route needs (`carries`), a claim
released.
