---
name: weekly-search-review-gold-set-repaired
id: 20261115T035544Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, search, scheduled-run]
links:
  - collective-index/gold-queries.yaml
  - communications/queue.log
  - communications/errors.log
---

# The Collective -- Repository Gold Set Repaired: 13 Questions, Every Right File in the First Five

## Situation

Period: this scheduled run only (job `weekly-search-review`, from
2026-11-15 03:46 UTC). No earlier report exists in `reports/`; the
period since my birth is left to my next interactive session-end.

Divisions: no Admiral has reported. `reports/` held no report, and
`apophis.log`, `zero.log`, `apollo.log`, `oracle.log` and
`mercury.log` hold no entry. Mining, Logistics, Trade, Military,
Intel: not reported.

Fleet totals: not measured in this run.

Search indexes, from the output of `gold-drift.py` (plan, apply, eval,
misses) in this run:

| Set | Index | Questions | Rewritten / added / dropped / moved | Right file first | In first five | MRR |
|---|---|---|---|---|---|---|
| collective | OK -- 43 chunks | 11 -> 13 | 8 / 2 / 0 / 0 | 10 of 11 -> 11 of 13 | 11 of 11 -> 13 of 13 | 0.9545 -> 0.9231 |

- Skipped: ws-unity, ws-apophis, ws-zero, ws-apollo, ws-oracle,
  ws-mercury -- empty index, no gold set yet.
- The rewrites follow changed files (`README.md`,
  `communications/protocol.md`, both blueprints,
  `players/n-aetherwraith.md`); the two new questions cover the
  constitution and the report template (c012, c013). Check:
  `CHECK PASS (collective: 10 valid, 0 failures, 0 warnings)`;
  validation: `GOLD SET PASS: 13 valid queries`.
- The scores fell on a changed question set, so the two runs do not
  compare like for like. Misses (file not in the first five): 0.
- Commit `f198285` (the gold file alone) waited in the clone. The
  watcher's pull log, 2026-11-15T03:52:11Z: `push deferred: untracked
  file(s) in the clone: station/fleet.py`, a file the service `fleet`
  runs since 03:38:31Z (`/srv/collective/services/status.json`). A
  session of mine committed it at 03:55:44 (`3af1e66`); at 03:56:21
  this report, written and not yet committed, held the push once more.
  The watcher pushed at 03:57:28, and `git merge-base --is-ancestor`
  answers 0 for `f198285` and for this report's first commit
  `7ea78be`.

## Strategy

No decision in this period. In force, from `DECISIONS.md` in my
workspace: the fleet plays Voidborn (D3); Suggi and I build and run
about the first 100 ships before the Admirals take over their
divisions (D17); play starts with a first wave of miners (D32). This
run changed none of it.

## Divisions

No Admiral report exists, so there is no suggestion to answer. Each
division: not reported.

## Plans

- Divisions: this report gives no new order to any division. What is
  decided stays in force: the Admirals take over ships only after D17.
- Fleet Admiral, proposed fixes for my next interactive session (my
  own skills; not made in this run, whose write scope is the gold
  files and its records):
  1. `weekly-search-review` step 3: hand the writer its brief by path,
     as this run did, or have the tool write its JSON example without
     angle brackets, with a case in `gold-drift-test.py`.
     `delegate_task` refuses a goal containing `<id>` or
     `<your question>` (errors.log ENT-002).
  2. `preflight`: grep the watcher's pull log for `push deferred`, so
     a held push shows at the next session start; and a rule that a
     service's file is committed before the service starts
     (errors.log ENT-003).
- Identity: a scheduled run never edits `IDENTITY.md`. No change
  proposed; the first entry, v1.0, is for an interactive session-end.

## Open Questions

None.

## Cross-links

- `collective-index/gold-queries.yaml` -- the repository's gold set,
  repaired in this run (commit `f198285`).
- `communications/queue.log` -- ENT-017 read in preflight; ENT-018 is
  this run's entry.
- `communications/errors.log` -- ENT-002 (the brief refused by
  `delegate_task`) and ENT-003 (the push held by an untracked file).
- `governance/template-reports.md` -- the format of this report.
