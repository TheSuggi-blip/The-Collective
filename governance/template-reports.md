---
name: template-reports
id: 20261114T212228Z
tier: core-template
lock: approval-required
approved_by: Suggi
author: Suggi
updated: 2026-11-22
links:
  - governance/the-collective-constitution.md
---

# Report Template -- How the Collective Reports

Authoritative format spec and mechanical validator for `/srv/collective/the-collective/reports/`. Procedures live in `report-admiral` and `report-unity` (do not duplicate). One file, fixed sections, dense facts, zero filler.

## The Report Checklist -- HARD GATE

Confirm every item before committing (do not copy this checklist into the report):

- [ ] Frontmatter fields complete: `name`, `id`, `tier`, `trigger`, `author`, `tags`, `links`  (PASS / HALT)
- [ ] `name` is lowercase kebab-case matching filename slug; `tier: report`; `author` capitalized  (PASS / HALT)
- [ ] `id` generated live via `date -u +'%Y%m%dT%H%M%SZ'` (never typed/rounded); `trigger` in `{session-end, incident, milestone, order}`  (PASS / HALT)
- [ ] `tags` lowercase hyphenated (division tag first; `fleet` for Unity); `links` repo-relative  (PASS / HALT)
- [ ] Title (`# <Division or The Collective> -- <main result>`) + exact `##` headings in order  (PASS / HALT)
- [ ] `Situation` names period since previous report; every number cites its source (or `"not measured"`); zero pilot names  (PASS / HALT)
- [ ] Division report, minimum words: Situation 100, Activities 120, Problems 60, Plans 100, Suggestions 40, Feedback 60, Learnings 80  (PASS / HALT)
- [ ] Fleet report, minimum words: Situation 100, Strategy 120, Divisions 150, Plans 100, Advice and Suggestions 80, Learnings 80  (PASS / HALT)
- [ ] `bash scripts/check-report-format.sh reports/<file>` prints `REPORT FORMAT: PASS`  (PASS / HALT)
- [ ] `python3 -B scripts/report-words.py reports/<file>` prints `REPORT WORDS: PASS` with zero padding/repetition  (PASS / HALT)
- [ ] Pure 7-bit ASCII; zero secrets, tokens, keys, or passwords  (PASS / HALT)

## Frontmatter & Naming

Filename: `reports/YYYY-MM-DD_<author>_<slug>.md` (`YYYY-MM-DD` from `date -u +%Y-%m-%d`, permanent; `<author>` lowercase; `<slug>` kebab-case `<= 60` chars, matches `name:`).

```yaml
name: <short-slug>
id: <YYYYMMDDTHHMMSSZ>           # exact output of date -u +'%Y%m%dT%H%M%SZ'
tier: report
trigger: session-end             # session-end | incident | milestone | order
author: <Name>                   # capitalized
tags: [<division-or-fleet>, <topic>]
links:
  - reports/<prior-or-source-report>.md
```

## Body Structure

Exactly one `#` title, required `##` sections in exact order (`###`, lists, tables allowed inside).

### Minimum Length

Floors read live by `scripts/report-words.py` (`--` = omitted, `none` = no floor). Reach floors with concrete facts, checks, and measurements -- never filler. If a section is quiet, state what was checked and what the check showed.

| Section | Division report | Fleet report |
|---|---|---|
| Situation | 100 | 100 |
| Activities | 120 | -- |
| Problems | 60 | -- |
| Strategy | -- | 120 |
| Divisions | -- | 150 |
| Plans | 100 | 100 |
| Suggestions | 40 | -- |
| Feedback | 60 | -- |
| Learnings | 80 | 80 |
| Advice and Suggestions | -- | 80 |
| Cross-links | none | none |

### Division Report Sections (Admirals)
- **`## Situation`**: period since previous report, active `orders.log ENT-NNN`, sourced `Ships`, `Credits`, `Output` summary.
- **`## Activities`**: ordered by goal/order -- action taken and measured result.
- **`## Problems`**: losses, failed orders, blockers -- what, where, root cause (or `"cause not found"`), action taken.
- **`## Plans`**: next actions inside orders; note autonomous choices made.
- **`## Suggestions`**: proposed improvements/objections with reason, cost, and decision owner.
- **`## Feedback`**: empirical review of Unity's recent tools/scripts/rules/orders (call + output, friction, improvements, self-built items).
- **`## Learnings`**: from `learnings-capture` -- lesson, record, behavioral change, fleet takeaway, knowledge path, `Skill:` line.
- **`## Cross-links`**: cited repo paths with 1-line descriptions.

### Fleet Report Sections (Unity)
- **`## Situation`**: period covered, fleet purse totals, one cited line per division.
- **`## Strategy`**: active standing goals, decided changes vs proposals.
- **`## Divisions`**: per-division synthesis, judgment on every suggestion (`accepted`/`declined`/`open` + reason), and cross-turn consistency check.
- **`## Plans`**: next fleet/division steps, upcoming builds/bases/orders, unresolved decisions.
- **`## Advice and Suggestions`**: informs without nagging (Suggi 2026-11-17) -- key decisions/reasons in plain ELI5 words, advised focus, and constitution-reserved items with recommendation + default fleet action.
- **`## Learnings`**: from `learnings-capture` on fleet leadership/systems.
- **`## Cross-links`**: every Admiral report and strategy doc cited.

## Anti-Patterns
- **Diary order:** organize by goal/result, never chronological narration.
- **Unsourced numbers:** cite the exact command/table or write `"not measured"`.
- **Padding / thin brush-offs:** never write `"None."` and never pad with repetition; state what was checked and observed.
- **Copy-paste fleet report:** Unity cites, judges, and decides rather than copying division reports.

## Minimal Skeleton

```markdown
---
name: <slug>
id: <YYYYMMDDTHHMMSSZ>
tier: report
trigger: session-end
author: <Name>
tags: [<division>, <topic>]
links:
  - reports/<fleet-report>.md
---

# <Division> -- <Main Result>

## Situation
Period: since `reports/<prev>.md`. Orders: `orders.log ENT-NNN`.
Ships: <active>/<total>, grounded: <n>, lost: <n> | Credits: <start> -> <end> (<net>) | Output: <units> | Source: <record>.

## Activities
## Problems
## Plans
## Suggestions
## Feedback
## Learnings
## Cross-links
```
