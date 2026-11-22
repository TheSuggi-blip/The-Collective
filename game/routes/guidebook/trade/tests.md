# Trade guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-22. Evidence: runs.jsonl; data/missions/*.json (rewards.skill_xp, 03:4x UTC); table books 03:3x UTC; requests.log ENT-335.

What the division tests, with the readings it rests on; a reading is
the state of its hour, not a verdict (rule F22).

How a trade test gets its three results (rule F37): a gap or a far bid
is one buyer, so one ship flies it three times; a mission paid once per
pilot shares no buyer, so three ships fly it at once (`max_ships` 3); a
buy of goods starts with one ship and one load (F12), two more follow.

- Once per pilot: mission-federation-market-analysis-market and
  mission-federation-trade-route-prospectus-grand (6,000 and 4,000 cr,
  Federation space), three ships each; voidborn-network-commerce
  (1,500 cr, rule F35), one ship first.
- Trade Runs pay XP only (the board's rewards: 20 to 40 trading, 80 to
  580 piloting). The runner reads no Trade Run id yet (ENT-335):
  trade-run-cinderspice-nova-terra was accepted, flown and handed in by
  hand: 21 minutes, about -241 cr on the goods before fuel, 637 trading
  and 211 piloting XP (runs.jsonl, xpsnap.py, 2026-11-22 04:25 UTC).
- Far buy-and-sell: trade-chemical-liner-beta-to-first-step bought 32
  for 19,618 cr and sold 26 for 19,734 at First Step (runs.jsonl 00:30
  UTC), 6 stored there; carry-liner-first-step-to-ramens waits for Ramen's
  Rest's bid.
- Far carries of stored surplus: carry-hydrogen-beta-to-nova-terra
  (`hive.py route`), carry-lead-*, carry-curd-*.
