# Command guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-24. Evidence: the plan file (tool plan, show); fill.py check command (2026-11-24 08:10 and 08:47 UTC); admirals.log ENT-119; hive.py standing Unity; requests.log ENT-433, ENT-500, ENT-517.

The flagships take the list First (the missions paid once; at its
head the `finish-` routes of missions held half done, open only to
their holders by `requires.mission`, ENT-514), then their own routes: a test the filler adds in front (three ships at
most, F37), the missions paid once of their boards, the far hunts no
other division claims (one ship a herd, `max_ships` 1; the loot to a
trader by `gift_to`), and last the nearest open herds Military claims,
told in admirals.log and taken out on its word (ENT-119: on
2026-11-24 every own herd read under its floor and two flagships
waited); then the hand-overs of their stores at each station (to the
receivers of Trade and Logistics, rule F23), `store-hold` and `park`
last. The flagships born in other empires take work of their own
region first: the dispatcher keeps a route over six jumps closed
unless it says `far_ok` (rule F35, orders P6); a flagship far from
home heads its row with the one far_ok stop home (`home-<capital>`).
A flagship may be lent to Military for its group hunts, as the
sentinels are (rule F10). They hunt for Combat and Piloting and lead
groups when Military flies one; Leadership and Tactics rise only by
leading. When the near herds and the home boards are spent, a flagship
heads its row with a foreign capital's paid-once missions and the
one-stop trip there (Trade's join corridor).

The faction's leader, a flagship: the sweep's gifts collect in its
wallet and it deposits between its runs. Treasury withdrawals (funds,
top-ups) are served by any docked Officer (wallet.py auto-officer
staffing), so the leader need not dock for them; its errands (roles,
promotions, Notice Board posts) still hold it docked (leader errands).
What would change the plan: a group hunt that kills, a command hull at
the next tier, herds under what a route needs (`carries`), a claim
released or asked back.
