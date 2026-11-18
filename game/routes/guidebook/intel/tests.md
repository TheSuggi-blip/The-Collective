# Intel guidebook -- Tests (tests.md)

### Open Tests
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/intel.md section 7.

- 2026-11-17 23:15 UTC turn (orders ENT-052):
  - The north road (Atria chosen for the outpost, Yildun the station
    candidate): no pirate line on our record within two jumps of Marfik,
    Atria, Regor, Groombridge 34, Chalawan, Rasalhague or Yildun, nor of
    their neighbours (observations kind pirate, 98 lines, 23:20 UTC). Atria
    (5 beyond our border, 7 jumps from home): belt iron 98,472 and copper
    100,000, neon 50,000, argon 49,999, nitrogen ice 49,998; 4 lanes; the
    nearest station with fuel and a market 6 jumps. Regor holds fluorine
    gas 2,314, which the reserve lacks (384). Atria, Regor and Groombridge
    34 were 571 to 630 minutes old: they stood on census-roads.
  - East candidates (lawless systems whose shortest way from our space runs
    through GSC-0044 or Intercrus; tables lanes, fields, stations,
    observations): station Oakridge (5 beyond GSC-0044, 8 out; copper
    299,999, iron 256,837, zinc 15,999, quantum fragments 690, phase crystal
    516; 3 lanes; no pirate line within two jumps; a stronghold 6 jumps;
    fuel and a market 4) or Miaplacidus (5 beyond, 8 out; iron and copper
    100,000 each, nitrogen ice 41,595, water ice 28,046; 3 lanes; no line
    within two; fuel and a market 3); Cervantes (4 beyond, 7 out; iron and
    copper about 200,000 each) has 3 lines within two jumps and an OBKT
    outpost. The outpost beyond: Tidewater (3 beyond Oakridge, 11 out;
    copper 188,894, neon 47,633; 5 lanes; no line within two; fuel and a
    market 1 jump) or Ross 154 (5 beyond Oakridge, 10 out; iron and copper
    199,999 each, nitrogen ice 50,000). East of them lies the Dross group:
    Hollowcrest, Merak (11 Dross at 21:36 UTC), Sheliak, Titawin, Merope,
    Alathfar, 25 lines within two jumps each, the Dross Citadel at Algol.
  - Southeast candidates (toward Biham, by bearing and lanes): the outpost
    GSC-0035 (5 out; copper 199,853, iron 178,055, argon 50,000; 7 lanes;
    34 lines within two jumps, none in the system; a stronghold 4) or
    GSC-0024 (5 out; iron and copper about 100,000 each, nitrogen ice
    50,000; 6 lanes; 34 within two). The station about 4 beyond GSC-0035:
    Fomalhaut (4 beyond, 9 out; copper 100,000, iron 27,832; 3 lanes; no
    line within two) or Yed Posterior (4 beyond, 8 out; copper 87,839,
    water ice 47,425); Alnilam (2 beyond, 7 out; copper 96,893, argon and
    neon 50,000 each, nitrogen ice 50,000; no line within two) is nearer
    than rule F33 asks. Their nearest station with fuel and a market is 6 to
    7 jumps away: a station there has no supply but ours.
  - Uranium ore (2,304 short): six deposits read, all 0 but Markeb Belt 38
    of 5,000 (18:09 UTC); Acubens Belt read 0 at twelve reads from 16:37 to
    22:47 UTC, so no regrowth is seen at home. Thorium ore 72 at GSC-0032
    (132 at 12:33 UTC). Polonium ore: no field. The faint signatures at
    Homam and The Telescope stay the lead: a probe step (use_item, then
    survey_system) is the next build.
  - Pirates filed: 14 lines (file_pirates.py), 11 of them Dross at Merak
    (21:36 UTC, hull 120 to 200, shield 100 to 140), Voss at GSC-0032 and
    Enif, a Dross scout at Sheliak.
  - The game stands at 0.723.2 (changelog, 23:22 UTC), as the rules digest.

- 2026-11-17 19:15 UTC turn:
  - The map is read: 8 never-read systems were left on the explorers'
    lists at 19:18 UTC (147 road reads in 4 hours, 36.8 an hour) and none a
    list can take; 9 strongholds and 3 systems without fuel stay unread.
  - The next sites (orders ENT-042, P4 b; tables fields, herds, lanes,
    stations, observations kind pirate, 19:20 UTC): no pirate line within
    two jumps of any system from our border to Alchiba. A chain with 3 or
    4 systems between sites (rule F33): Acrab (4 out, 6 jumps from home;
    iron and copper ore 199,999 each, null matter 594; 5 lanes; 58
    animals; the nearest station with fuel and a market 5 jumps), GSC-0006
    (4 further; iron and copper about 200,000 each, neon 47,803, lithium
    25,000; 69 animals; 2 from Aldebaran), Oxbow (3 further; iron and
    copper about 200,000 each, water ice 39,328; 6 lanes; 67 animals; 1
    from Hawthorne). Nightveil (3 out; a belt and neon and argon clouds of
    about 50,000 each) is the alternative to Acrab. The south 3 or 4 out (GSC-0021,
    Tanglewood, Felis, Gliese 876) holds 45 to 55 pirate lines within two
    jumps and the Korr stronghold two or three jumps away; GSC-0035 (5 out;
    copper 199,999, iron 181,250, argon 50,000; 7 lanes; 71 animals; no
    pirate line of its own, 34 within two jumps) is the least exposed.
  - Surveys beyond the border (scouting/<system>.json `survey`, 12 systems,
    15:37 to 19:15 UTC): no hidden deposit; Homam and The Telescope answered
    "Survey detected 1 faint signature(s) that your scanner cannot resolve.
    Try a more powerful survey scanner." The scanner scout reached scanning 1.
  - Uranium ore: our books bid 600 cr (was 300 on 2026-11-16), and the only
    field read beyond Acubens is Markeb Belt, 38 of 5,000 (outer rim, 19
    jumps). It is extracted by a Rad Harvester (catalog, base value 990),
    carried by no ship of ours.
  - Glasslight Shoal at Clearwater (requests ENT-221): about 77 silicon ore
    an hour grown back, 08:18 to 18:18 UTC (322 to 15 while Logistics
    gathered 1,081); census-watch-clearwater off, Clearwater on census-worked.
  - A reserve sale (errors.log ENT-095): the Titawin chlorophage hunt sold 6
    caustic sacs at 2,110 cr while the reserve stood 384 short, and the Homam
    frost-moth test 5 superfluid vials the reserve holds back; both store at
    Node Beta now, and the turn check prints RESERVE.
  - Pirates filed: 18 lines, among them ten Dross raiders and raider elites
    at Hollowcrest Frozen Drift (19:06 UTC), where a sentinel hunt works.

- 2026-11-17 15:15 UTC turn:
  - The far explorers (census-far-1 to 5, from 11:25 UTC): 97 first reads
    by 15:16 UTC (17, 17, 19, 18 and 26 by direction) and 22 more on
    census-roads; the farthest systems read, by direction: Dustfall 27
    jumps, Glenhaven 26, Alcyone 29 (with Altair, Castula, Ashmark and
    Mekbuda, all 29), Quartzfield 29, Praecipua 24. `chain` 3 read up to
    three more systems within minutes of the first; no ship ran short of
    fuel (lowest tank 46 of 95 at 15:19 UTC, table ships). The map: 506
    systems, 367 read, 139 never read (15:17 UTC): 127 on the explorers'
    lists, 9 pirate strongholds, 3 whose stations sell no fuel (Blackthorn,
    GSC-0013, Winterhold). Nothing is left to widen; the lists run dry
    about 18:45 UTC at 37.8 first reads an hour.
  - Exploration XP is the pilot's own: every scout's XP at 15:19 UTC against
    its runs to 15:45 UTC (data/fleet/ships/, data/routes/runs.jsonl). A
    scout on a mining mission at Rotanev, no census flown, gained 10; scouts
    reading systems the fleet had read for hours but they had not gained 5
    to 30 (Sualocin 10, Acrux 5, Sirius 15, GSC-0016 20, Mirach 30); every
    gain is a multiple of 5. So a pilot's first visit to a system, a system
    flown through included, pays about 5 XP whoever read it first, and the
    class's skill does not stop when the map is read: a scout keeps training
    it on census lists it has not flown. 23 of 30 scouts stand at level 3
    (2 at 11:29 UTC).
  - Leads from the new reads (table fields, herds, 15:31 UTC): silicon ore
    at GSC-0007 Dark Beacon Cluster 18,639 of 20,000 (27 jumps), Emberglow
    4,935, Edasich 4,545, Muphrid 4,325, Hadar 3,518, Netherwick 3,052;
    pirates stood at Muphrid's Worklight Outcrop and Netherwick's Glass Reef
    at 13:11 and 12:59 UTC. Thorium ore 132 at GSC-0032 (26 jumps); uranium
    ore nowhere (1 unit at Acubens). Herds new to our record: magnet
    barnacles (anchor plate) at Alphecca and Ashmark, mirror skates (foil
    scale) at Sadachbia and Redmarsh, cobalt squids (cobalt ink) at Tabit
    and Edgewater; silica borers (silica lens, 10,436 short) graze at Nexus
    Prime's Material Harvesters (2) and in nine systems more. Of the 28 raw
    inputs the reserve is short of, 24 have a field, an ask or a herd; none
    for graphene thread, irradiated marrow, salvage metal and uranium ore.
  - Pirates filed: 29 lines (file_pirates.py): groups of four to six Crix
    raiders at Redmarsh and Netherwick, six Nyx raider elites at Violethall,
    two Kael raider elites at Dustfall, Sable scouts at Muphrid, Larchfield
    and Zubenelgenubi, the two Korr raider elites again at Felis Belt B
    (14:53 UTC).
  - GSC-0044 watch: reads came 70 to 75 minutes apart (11:50, 13:03, 14:17
    UTC at GSC-0044) and Intercrus was read once in four hours; the route
    now holds all seven systems at 45 minutes with `chain` 3. No pirate on
    record in any of them.
  - The survey step (census.py 7540393): the scanner scout flies census-far-1
    and surveys every system it reads; its first rows say whether a survey
    beyond the border reveals a place get_poi does not show.
  - A figure fault: the store's run figure of mine-nightveil-dark-residue
    read -200,720 for a command ship's run whose row reads -720: the
    treasury deposit of 13:41 UTC was counted, the gifts that funded it
    were not (requests.log, this turn's request to Unity).

- 2026-11-17 11:15 UTC turn:
  - The survey test (one scout by hand, Survey Scanner I, survey power
    30): survey_system docked at Central Nexus, between 11:34:04 and
    11:34:33 UTC, answered "Survey complete. No hidden deposits detected in
    this system. Ore readings for 4 charted POI(s) are in deposits." One
    action gave every field's units and maximum (the Material Harvesters
    belt depleted: iron 0 of 100,000, silicon 0 of 20,000, copper 0 of
    100,000, energy crystal 0 of 200), the system's wildlife by species
    with an estimate (drift-ray 24, pilot-whale 10, belt-grazer 5 and five
    more) and the bloom status, and 5 scanning XP; the first scanning XP
    of any scout. A survey where hidden places are likely (the frontier,
    0.722.0) is the next test; a survey step in census.py for a ship with a
    scanner would train scanning on every read and save a leg per field.
  - The missions of Intel's class (rule F34): Local Sector Survey (visit
    Sirius, Node Alpha, Horizon; 2,500 cr, 380 piloting XP) and Deep Space
    Cartography (visit The Crucible and Horizon; 4,000 cr) accepted by the
    survey scout at 11:34 UTC. The game's answer: "Your ship's sensors will
    automatically log the data as you jump between systems", so a census
    jump counts; whether a pass through a system counts is read at the next
    turn from its objectives (0 of 1 each at 11:35 UTC). Horizon stands on
    census-far-1, The Crucible on census-far-5. Listening Orders (survey
    Sarin, Greymist, Emberglow, all on census-far-1; 7,000 cr and a ship
    scanner) needs a survey step.
  - The chain test: census-roads-chain never flew because its list was
    census-roads' list and dispatch.py counts each census order against
    every route that lists its system (9 of 1 at the briefing). Off; the
    chain flies on census-far-1 to census-far-5, whose lists are disjoint.
  - GSC-0044, the first outpost's site (orders ENT-036, P4 a), read at
    10:06 UTC: GSC-0044 Belt iron 99,998 and copper 99,999 of 100,000,
    Forgotten Tailings iron and copper 100,000 each and sol alloy ore 1,527
    of 1,527. Pilots of others met in the six hours to 11:36 UTC: none at
    GSC-0044, Botein or HD 40307; one at Acrux (IRLC) and one at Atlas;
    three at Cedarhold (PRME), six at Intercrus (ENDL, HIVE, BUSY) and five
    at Achernar on the road (PAYN, PEPE, IRLC, BUSY). No pirate on record in
    any of them. Read every hour from 11:25 UTC (census-watch-gsc-0044).
  - Pirates filed this turn (file_pirates.py, 9 lines, observations kind
    pirate): two raider elites of the Korr pirates, Ironhold (125 hull) and
    Blockade (250 hull), at the GSC-0016 Emission Nebula (08:30 UTC), where
    a gas route of Trade's works, and again at Felis Frost Ring (09:36 UTC),
    where a hollow-pilgrim hunt of Military's works; scouts at Felis Belt B,
    Felis Frost Ring and Gliese 876; a raider elite of 450 hull and a scout
    at Sheliak and a scout at Merope, both 12 jumps out on the roads.
  - Caustic sac: a command hunt at Alathfar sold 4 sacs at 2,110 cr each
    at Hex Star in Dheneb (run row of 10:42 UTC); our Amberfall hunt stores
    its sacs for the reserve (rule F24).

- 2026-11-17 07:15 UTC turn, from the fleet's database (tables fields,
  herds, met, observations; reads of 2026-11-17 03:05 to 07:20 UTC):
  - The first outpost near the iron belts (orders ENT-029, task 3): every
    system within one jump of Garnet, Keid and Amberfall is read and on a
    census list. Intel names Garnet, as Mining does (admirals.log
    ENT-018): Garnet Belt and Garnet Dim Lattice hold iron and copper at
    100,000 of 100,000 each (gold ore 31 of 25,000), no station; five iron
    fields lie one jump away (Achernar, Ruchbah, Cedarhold, Atlas); The
    Experiment's station, with fuel and a market, is two jumps away; no
    pirate is on record within two jumps (observations, kind pirate);
    HEXC miners and a BUSY combat drone were met at Garnet Belt. Keid holds
    more kinds in one system (a full belt, a full nebula, and an ice shelf
    with deuterium 5,000 of 5,000; Okab, GSC-0012 and GSC-0031 one jump
    away), but its nearest station is four jumps away, the pirate
    stronghold Gliese 581 four, and pirates are on record one jump away
    (Coldwater) and two (GSC-0021, Thornhaven, Stormwatch, Tanglewood).
    Amberfall is third: a full belt and the chlorophage nebula, four jumps
    from a station, Thornhaven's pirates one jump away. Judged first on
    resources alone, Keid was named in admirals.log ENT-020 and corrected
    by the entry after it.
  - Hubs (task 2), for Intel: 565 scout census runs in 24 hours, each
    counted out from and back to Central Nexus (a census ends at the last
    station it read, else at Central Nexus, so the figures are an upper
    bound); had each started and ended at the nearest of the four
    candidate places, they would have flown 2,036 fewer jumps a day:
    Pherkad 956 (235 runs nearer), The Experiment 788 (217), Hamal 696
    (152), GSC-0027 610 (216), each alone (lanes table, BFS; runs table,
    2026-11-17 07:25 UTC). The census refuels at every station it docks
    and starts where it ends, so a hub saves Intel jumps only where a
    scout can dock and refuel: The Experiment today; beyond Pherkad,
    Hamal and GSC-0027 an outpost with a fuel bunker.
  - Reserve inputs with a known source: 18 of the 28 raw inputs the
    reserve is short of have a field with units, a herd of the species
    that drops them, or an ask in a book; no source for anchor plate,
    cobalt ink, foil scale, graphene thread, hoarfrost heartcore,
    irradiated marrow, salvage metal, silica lens, thorium ore and
    uranium ore (`surplus.py reserve` 07:23 UTC). New leads: the
    cauldronback (alloy scale, 56,520 short) grazes at home, one each at
    Node Beta's Eltanin Prime Belt and Node Alpha's extraction zone
    (06:40 and 06:55 UTC); slag tortoises (ferrous nodule, 28,260 short)
    stand in most belts; pressblisters (nitrogen bladder) in six ice
    fields of the north road.
  - Uranium, thorium, seam glass (requests.log ENT-194): no field of the
    116 systems read holds a unit; the only deposits read (Acubens Belt
    uranium, Nova Terra and Bellatrix Major thorium) stand at 0 of 5,000.
    Both ores are extracted by `rad` (catalog items); seam glass by mining,
    "found in the debris shells of dead stars". The search: 97 never-read
    systems on census-roads from 07:21 UTC, and the survey test.
- Species tests from 2026-11-16 03:11 UTC, one scout each: what each
  kill dropped is in its run row (`data/routes/runs.jsonl`); a drop
  without a bid of 50 cr is stored, so the row shows it. Military tests
  other species (`guidebook/military.md`).
- Caustic sac (428 short in the reserve, `surplus.py reserve` 2026-11-17
  03:23 UTC): answered. hunt-test-amberfall-chlorophage flew 8 runs from
  2026-11-16 23:45 to 2026-11-17 03:08 UTC: 15 kills, 6 sacs dropped (0.4
  a kill), 7 sold at 420 cr into the Node Beta bid (`data/routes/runs.jsonl`).
  From 03:24 UTC hunt-amberfall-chlorophage-sac stores every drop at Node
  Beta and sells nothing (rule F24). The herd read 2 or 3 chlorophages
  in every census since 2026-11-16 02:06 UTC: one hunter, about two sacs
  an hour if the herd holds. Another herd of chlorophages: not read.
- The regions of the base sites (orders P4), read by the census
  (`data/scouting/`, 2026-11-16 23:50 to 2026-11-17 01:56 UTC); none holds a
  station, so a place in any of them can take an outpost:
  - North: Hawthorne holds one belt with iron and copper ore at 100,000
    of 100,000 each, 9 belt-grazers, 4 patina grazers, 4 slag tortoises;
    Aldebaran one ice field (nitrogen ice 50,000) and no belt; Alchiba an
    ice field (water ice 27,529, nitrogen 50,000); Yildun two belts mined
    down (copper 29,501 of 30,000, iron 27,712 of 35,000, carbon 66 of
    30,000, aluminum 102 of 20,000) and one pilot not ours. Hawthorne is
    the north's richest read.
  - South: Felis holds three belts at 100,000 iron and 100,000 copper each,
    an ice field, a nebula with deuterium ice 4,355 and null matter 361,
    and the largest herds we read (45 belt-grazers, 21 patina grazers, 20
    slag tortoises); one pirate at its frost ring (Flinch, 85 hull and 30
    shield in Military's test). Biham and the nine systems around it are
    on census-roads since 03:24 UTC.
  - East: Intercrus holds three belts at 100,000 iron and copper each, an
    ice field, sol alloy ore 1,401 and null matter 427; 50 belt-grazers
    and 3 crusher mantises (predators); four pilots not ours at its read.
    Diadem and seven systems around it are on census-roads since 03:24 UTC.
- The census chain (census.py 9ceae23): census-roads-chain tests it with
  one explorer from 03:30 UTC; its rows (one per system) are compared
  with census-roads per system read.
- Game 0.722.0 (changelog, read 2026-11-17 03:39 UTC): "calibration defects
  in recently sold survey scanners" were fixed and "frontier explorers
  should recheck their survey data". Our census reads `get_poi` and fits
  no survey scanner (survey_scanner_i, base value 4,400): whether a survey
  shows resources `get_poi` does not (silicon ore among them) is not
  tested.
- Silicon ore (53,222 short in the reserve; 34 held): no field of the 63
  systems read holds it (data/scouting/, 2026-11-16 23:20 UTC). Asked at
  Central Nexus at 420 cr (424 at the best price, 16,189 over all
  levels), at Ironlight Crossroads (LHS 1140) at 561 cr for 200, at
  Synchrony at 376 cr for 4. The explorers' 28 road systems are the
  search for a field.
- Leads no field we read holds (`data/scouting/`, read 2026-11-16 between 03:02 and 03:16 UTC):
  tritium ice (bid 400 cr for 2,000 at each of five stations of ours and
  973 at Ironlight Crossroads), caustic sac (420 cr, 50 at seven), void-
  charged ichor (1,142 cr, 517), control nodes and quantum silk. Uranium,
  thorium and tungsten ore stand at 0 in the home belts that held them.
- Solarian law (get_empire_info, read 2026-11-16 by one scout): foreigners
  pay 3% sales tax and a fuel surcharge of 6 cr a unit; eight goods are
  contraband (fine 2x their value); an attack in policed space carries a
  500 cr bounty. Nova Terra Central was read by one scout with an empty
  hold at 03:22 UTC (requests.log ENT-073): 517 items, 16 price gaps with
  our books, the deepest 73 units; 304 cr for the round trip of about 25
  minutes (`game/planets/n-nova_terra.md`).
- Base sites beside the best ice (queue.log ENT-067): Achernar, Alnair,
  Wolf 1061 in that order; Ruchbah and Intercrus not advised. The same
  three as station sites for S6 (queue.log ENT-090, 2026-11-16 08:30
  UTC): Achernar first as the only one with belt, gas and ice (iron and
  copper ore 99,997 of 100,000 each); each system's file in
  `game/planets/` holds its line "Station site (S6)".
- Crimson law (get_empire_info, read 2026-11-16 08:18 UTC, queue.log
  ENT-089): a Voidborn visitor pays 4% sales tax on what it buys and a
  fuel surcharge of 4 cr a unit; income and property tax fall on
  citizens; the contraband list is the Solarian one. The Rampart
  Checkpoint lies 17 jumps out and Blood Forge 20, behind 13 lawless
  systems of which 9 are unread.
- Ores bid everywhere and sold nowhere at the bid (station/market.json and
  our books, 2026-11-16 12:16 UTC): uranium ore 300 cr (5,871 units at
  the best price over our eight books; asked only by Nebula at 500 and
  the Outer Rim), thorium ore 240 cr (6,246), seam glass 1,200 cr (333 at
  each of our seven books, base value 600, made into annealed seam
  glass), palladium ore 358 cr (43,450 at four). Every uranium and
  thorium deposit we read stands at 0 of 5,000 (Acubens Belt, Bellatrix
  Major Belt at Node Gamma, Nova Terra Industrial Belt); no field we read
  holds seam glass. The capacity tool names the tool for uranium and
  thorium as `rad`, carried by none of ours. A deposit of either beyond
  the frontier is the largest lead of the picture.
- The game stood at 0.723.1 at 2026-11-17 03:39 UTC (https://spacemolt.com/changelog,
  1,886 releases); `game/rules/15-patch-notes.md` names 0.719.3.
- Pirates in the fourth ring: one at Gliese 876 (Stillwork Belt) and one
  at Felis (Felis Dim Lattice), census of 04:40 UTC (`data/wildlife/`).

- The frontier (orders F13): 51 systems on the list since 2026-11-16
  04:31 UTC: rings 1 to 3 of our border, Atlas, Intercrus, LHS 1140,
  Goldcrest, Bluerift, and the next ring (Marfik, Acrab, Acrux, Botein,
  Deepwell, Felis, Gliese 876, HD 147513, Rastaban), 6 or 7 jumps from
  home; all lawless, none a pirate stronghold (Gliese 581 stays off).
  All nine new systems were taken by ships of three plans within two
  minutes of the commit. The base-site
  line of each read system is in its file in `game/planets/`.
- Order books beyond the border: Ironlight Crossroads (LHS 1140) read,
  no trade with depth to ours (queue.log ENT-046); Hive Antares has no
  market; the Ironlight bases at Goldcrest and Bluerift are outposts
  without services (queue.log ENT-049). The next markets: Korr
  Fortress Station in the pirate stronghold Gliese 581, the Solarian
  stations that F3 keeps us out of (requests.log ENT-067), then The
  Crescent Moon (MOON) eight jumps past the border
  (`data/station/stations.json`).
- Predators beyond the border: rainbow leviathans at Atlas, crusher
  mantises at Intercrus (census of 2026-11-15); what they do to a
  starter is Military's to test.
- BUSY pilots hunt herds in our space and beyond and fight pirates: one
  destroyed a pirate at Thornhaven at 23:07 UTC (`data/station/battles.json`);
  none has fired on a ship of ours (`game/factions/n-busy.md`).
- The game stood at 0.717.0 at 23:33 UTC; the lines of `game/rules/`
  it makes wrong are in `requests.log` ENT-038. At 0.719.0 on
  2026-11-16 08:17 UTC: starter ships pay no property tax (0.717.1),
  five prestige hulls (0.718.0), a faction board of pirates destroyed
  (0.719.0); the lines they make wrong are in `requests.log` ENT-119.
