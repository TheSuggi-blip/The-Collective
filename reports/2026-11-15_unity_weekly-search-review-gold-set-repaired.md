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

# The Collective -- Repository Gold Set Repaired; the Clone's Push Is Held by an Untracked File

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
- Commit `f198285` (the gold file alone) is in the clone and not on
  `origin/main`. The watcher's pull log, 2026-11-15T03:52:11Z: `push
  deferred: untracked file(s) in the clone: station/fleet.py`. The
  service `fleet` runs that file since 03:38:31Z
  (`/srv/collective/services/status.json`).

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
- Fleet Admiral: once `station/fleet.py` is committed, the watcher
  pushes `f198285` and this run's records; I check
  `git merge-base --is-ancestor f198285 origin/main` at my next
  session.
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

1. `station/fleet.py` is untracked in the clone and run by the
   service `fleet`; while it stays untracked, no agent's commit
   reaches GitHub. Recommendation: the session that built it reviews
   and commits it now; if that session is gone, I commit it at my next
   interactive session after reading it, on your word.

## Cross-links

- `collective-index/gold-queries.yaml` -- the repository's gold set,
  repaired in this run (commit `f198285`).
- `communications/queue.log` -- ENT-017 read in preflight; ENT-018 is
  this run's entry.
- `communications/errors.log` -- ENT-002 (the brief refused by
  `delegate_task`) and ENT-003 (the push held by an untracked file).
- `governance/template-reports.md` -- the format of this report.
