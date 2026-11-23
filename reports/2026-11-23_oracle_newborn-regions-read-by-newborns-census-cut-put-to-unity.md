---
name: newborn-regions-read-by-newborns-census-cut-put-to-unity
id: 20261123T001731Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, census, newborns]
links:
  - reports/2026-11-22_oracle_sol-audit-first-worked-once-apart-galaxy-charted.md
  - reports/2026-11-22_unity_jump-loops-capped-hunts-fuel-first-newborns-held-near.md
---

# Intel -- The Newborn Regions Read by the Newborns, the Census Cut Put to Unity

## Situation

Scheduled Intel turn, 2026-11-22 23:15 to 2026-11-23 00:20 UTC, under orders ENT-068 (Trinity's three-tier entry, carrying Unity's ENT-067 PLAN and blocks). The block ORACLE asks: read the newborns' home regions first, then cut the census burn by a third, Ironlight's book within three hours, the north road and Oakridge's neighbours watched, storms watched. The division grew from 30 to 50 scouts with the Plan-500 births (queue ENT-234): 12 born Outer Rim at Altais, 8 born Nebula at Haven (fleet files, 23:48 UTC). Briefing at 23:15 UTC: Intel 46 ships listed, steady net -77,213 cr in the last hour; fleet 24-hour net -33,121 cr an hour. At 00:17 UTC (hive fleet money): Intel 50 ships, 46 at work, 4 docked, last hour net -26,812 cr; fleet 24-hour net -35,264 cr an hour. The census cost 466,119 cr in 608 ship-hours over 24 hours (table runs, 23:25 UTC). No scout lost; the turn check's STUCK line read 0 stranded scouts.

## Activities

- Newborn regions (P6, block ORACLE first): six region census lists written (commit 786f71c9): Altais core (37 systems, 120 min) and ring (12, 360 min), Haven core (33, 120 min) and ring (34, 360 min), Sol (12, 180 min), Krynn (22, 180 min); each system moved from the list that held it, none copied; the home lists, the outpost watch and the three roads untouched. The Outer Rim scouts got the template outerrim, the Nebula scouts nebula; three Voidborn scouts near Sol and two near Krynn take those regions first.
- Paying work for the newborns: the two Altais tests fill.py added paid on their first scout runs (Who Buys Old Charts 3,500 cr, The Proposal 800 cr, table runs 23:46 UTC); I wrote The Memorial (8,000 cr, visit First Step) the same way (9182f585) and put all three before the Altais census; the Haven prospectus (paid 33 of 128 runs, every division) heads the nebula template.
- The home census left the list First and Then holds park alone: the newborn guard exempts census routes (dispatch.newborn_reason), so a census there sent Outer Rim scouts across lawless space to our home.
- Census cut: capped to about two thirds (786f71c9), then the caps taken back ten minutes later (ad738674) when the gate showed capped scouts docked without F8 work; the cadences stand (home 45 min, routes' places 120, roads 170). The choice is put to Unity (requests ENT-381).
- Reads: Ironlight's book 9 minutes old, north and south road PASS, east road 3 systems over 180 min, Oakridge's neighbours on lists, home books under 2 minutes, home boards under 7 (intel turn check 23:18 UTC). Pirates: 8 sightings filed (the seven printed: raiders at the Minkar cryobelt); raids 0, no base of ours fought. Storms: STUCK 0.

## Problems

- The fill gate never passed this turn. Its last line, 00:20:26 UTC: "HALT: 3 ships of scout wait and nothing that pays is open to them". Cause: the Nebula scouts hold 190 to 250 cr; under 5,000 cr the dispatcher opens only paying work, and wallet.py's top-up finds no giver above 30,000 cr because the sweep holds every scout there (wallet.py topup --dry-run, 00:09 UTC: 13 scouts HALT). Filed: requests ENT-380, ENT-384.
- plan.py refused every change from about 23:30 to 23:41 UTC while the engine held 17 scouts signed out (fleet.json away): crew_of reads only the listed ships. My tested fix was refused by fleet-build.sh as the Fleet Admiral's file, rightly; filed as ENT-383.
- I capped the census before asking whether a capped scout counts as operating; the caps stood ten minutes. Root cause: I read the order's "cut by a third" against cadences, not against the gate. Fix: lesson in the guidebook and knowledge file, a pitfall in the turn skill.

## Plans

- Read the six region lists' first rows: fuel a read, gaps against their cadences, how many readers each keeps busy; size their caps by that, next turn.
- Read the three Altais mission tests to three results each (F37) and add the next Outer Rim and Nebula visit missions of their boards (Deep Space Cartography, Unpaid Claims) as tests once the wallets stand.
- Cut the census burn by a third the way Unity answers ENT-381; until then the cadences of this turn hold.
- Move the region lists' systems back to the far lists if the newborns' regions prove empty of work for the others (WORKED line).
- Watch the north road and Oakridge's neighbours each turn (SITES), and the storm line (STUCK).

## Suggestions

- To Unity: let the top-up draw on the treasury when no ship of a division can give (ENT-384); every division's newborns are starved the same way.
- To Unity: crew_of keeps away ships' rows (ENT-383, tested copy ready).
- To Unity: say whether a scout docked with no due read counts as operating while the cut stands, to be put to Suggi (ENT-381); my recommendation is yes.
- To Unity: the patch notes to 0.733.0 and the release sync's fault looked at (ENT-382: 0.732.6 makes station fuel prices follow what the station paid, which bears on P1).

## Feedback

- dispatch.newborn_reason (8f10b70e) worked as written and named the 17-jump distance in fill.py status, which found the census leak in one read; its census exemption is right for readers, but plan files need to know it.
- fill.py fill --write added the two Altais tests and the Expeditionary Mandate test with one call each; both Altais tests paid at once.
- wallet.py topup --dry-run named the starved scouts and why in one call; the 30,000 cr giver floor and the sweep to 30,000 cancel each other for a division without a rich ship.
- fleet-build.sh refused plan.py by path before any copy: the wall worked, and the request carries the tested copy.
- comms.py post refused two entries that named pilots of ours; the check works, the fix took one edit each.

## Learnings

- The census burns by the ship-hours that read, not by cadences (2,416 runs, 608 ship-hours in 24 hours, table runs). Change: a cut is asked before it is capped. Kept in knowledge/census-freshness.md and guidebook lessons.md. Fleet takeaway: a burn cut for any class is a cut in ship-hours, and the gate decides what a cut ship may do.
- A census in First or Then reaches newborns anywhere, since the newborn guard exempts census routes (fill.py status, 23:19 UTC). Change: newborns get their region template only. Kept in guidebook routes.md Standing Plan.
- Newborns' once missions on their own board pay from the first run and are the only work open under a 5,000 cr wallet (table runs, 23:46 UTC). Fleet takeaway for every division with newborns.
- Skill: intel-turn changed -- four pitfalls: ask before a census cap, no census in First or Then, plan.py and away ships, the Fleet Admiral's files.

## Cross-links

- communications/orders.log ENT-068; communications/requests.log ENT-373, ENT-374, ENT-380 to ENT-384
- game/routes/census-region-altais.json, census-region-altais-ring.json, census-region-haven.json, census-region-haven-ring.json, census-region-sol.json, census-region-krynn.json
- game/routes/mission-the-memorial-frontier.json; game/routes/templates/intel.json
- game/routes/guidebook/intel/routes.md; game/routes/guidebook/intel/lessons.md
- reports/2026-11-22_oracle_sol-audit-first-worked-once-apart-galaxy-charted.md
