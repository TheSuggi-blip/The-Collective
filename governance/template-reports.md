---
name: template-reports
id: 20261114T212228Z
tier: core-template
lock: approval-required
approved_by: Suggi
author: Suggi
links:
  - governance/the-collective-constitution.md
---

# Report Template -- How the Collective Reports

A report is the unit of command information in The Collective. An
Admiral writes one at every session-end about its division; the Fleet
Admiral writes one about the fleet. Reports go up the chain of command
(constitution, section III): the Fleet Admiral reads the Admirals'
reports, Suggi reads the Fleet Admiral's. One file, fixed sections, no
fluff.

## Relationship to the Report Skills

This file is the format specification AND the compliance validator.
The procedure (gather the record, write, check, commit) lives in the
skills `report-admiral` and `report-unity`; both use this file's
Report Checklist as their format gate and do not restate it. Keep the
division: spec + checklist here, procedure there.

## The Report Checklist -- HARD GATE

Pre-commit gate: every item below MUST be confirmed. The report MUST
NOT be committed with any item unconfirmed. Do not include this
checklist in the report.

- [ ] Frontmatter: every Frontmatter Schema field present (name, id, tier, trigger, author, tags, links)  (PASS / HALT)
- [ ] name: lowercase kebab-case, matches the filename slug  (PASS / HALT)
- [ ] id: exact output of `date -u +'%Y%m%dT%H%M%SZ'`, pasted directly; never typed  (PASS / HALT)
- [ ] tier: "report"  (PASS / HALT)
- [ ] trigger: one of {session-end, incident, milestone, order}  (PASS / HALT)
- [ ] author: the writing agent's name, capitalized  (PASS / HALT)
- [ ] tags: lowercase, hyphen-delimited; an Admiral's report carries its division's tag  (PASS / HALT)
- [ ] links: paths relative to the repository root  (PASS / HALT)
- [ ] Title: the division's name (Fleet Admiral: "The Collective"), then the period's main result stated as a fact  (PASS / HALT)
- [ ] Sections: exactly the `##` headings of the report's kind, in order (Body Structure)  (PASS / HALT)
- [ ] Situation names the period covered: from the previous report to this one  (PASS / HALT)
- [ ] Every number is printed from a record the same section names; a number nobody measured is written "not measured"  (PASS / HALT)
- [ ] No section is left out; a section with little to report says what was checked and what the check showed  (PASS / HALT)
- [ ] Division report, minimum words: Situation 250, Activities 250, Problems 150, Plans 250, Suggestions 100, Learnings 200  (PASS / HALT)
- [ ] Fleet report, minimum words: Situation 250, Strategy 300, Divisions 300, Plans 250, Open Questions 150, Learnings 200  (PASS / HALT)
- [ ] `python3 -B scripts/report-words.py reports/<file>` prints `REPORT WORDS: PASS`  (PASS / HALT)
- [ ] The words carry facts: no sentence stands in the report only to reach a minimum, nothing is invented, nothing is said twice  (PASS / HALT)
- [ ] Suggestions (a division report) say what can be changed, each with its reason and its cost  (PASS / HALT)
- [ ] Learnings hold what the period taught the writer about its own role, each lesson with the record that earned it  (PASS / HALT)
- [ ] No secrets: no password, registration code, key or token  (PASS / HALT)
- [ ] File named `YYYY-MM-DD_author_slug.md`, in `reports/`  (PASS / HALT)
- [ ] `bash scripts/check-report-format.sh reports/<file>` prints `REPORT FORMAT: PASS`  (PASS / HALT)
- [ ] ASCII-only: zero non-ASCII characters in the file  (PASS / HALT)

## Frontmatter Schema

```yaml
name: <short-slug>               # lowercase, kebab-case, equals the filename slug
id: <YYYYMMDDTHHMMSSZ>           # ISO 8601 UTC timestamp, permanent, never reused. MUST generate with: date -u +'%Y%m%dT%H%M%SZ' at creation.
tier: report                     # always report
trigger: <what prompted this>    # session-end | incident | milestone | order
author: <name>                   # who wrote this, capitalized
tags: [<topic>, <topic>]         # lowercase, specific; the division first
links: [<path/to/file.md>]       # paths relative to the repository root
```

## Frontmatter Rules

- `name` is a short lowercase kebab-case slug, the same as the slug in
  the filename.
- `tier` is always `report`.
- `id` is ISO 8601 UTC (`YYYYMMDDTHHMMSSZ`). Never reuse. Never change
  after publishing. MUST generate with `date -u +'%Y%m%dT%H%M%SZ'` at
  creation. Estimating or rounding = GATE FAILURE.
- `trigger` picks from the list: `session-end` (the regular report),
  `incident` (a loss or failure that cannot wait), `milestone` (a goal
  reached), `order` (a report the Fleet Admiral or Suggi asked for).
  Do not invent new trigger values without updating this file.
- `author` is the agent that wrote the report.
- `tags` use lowercase and hyphens. An Admiral's first tag is its
  division; the Fleet Admiral's first tag is `fleet`.
- `links` are paths relative to the repository root: the reports this
  one builds on (an Admiral: its previous report and the Fleet
  Admiral's report in force; the Fleet Admiral: every Admiral report
  used).

## Naming Convention

Files are named `YYYY-MM-DD_author_slug.md` and live in `reports/`.

- `YYYY-MM-DD` -- UTC date of publication, from `date -u +%Y-%m-%d`.
  MUST NOT change when the file is corrected.
- `author` -- lowercase agent name.
- `slug` -- kebab-case, max 60 chars, unique per author and date.

Example: `<YYYY-MM-DD>_<admiral>_<main-result-in-a-few-words>.md`

## Body Structure

Header hierarchy: `#` = title only, `##` = the section headings below,
`###` = sub-headings inside a section where they help. Sections may
use paragraphs, lists and tables. No section is left out.

### Minimum Length

Every section has a minimum number of words (Suggi, 2026-11-15). The
minimum is a floor: a section is as much longer as its facts need.

| Section | Division report | Fleet report |
|---|---|---|
| Situation | 250 | 250 |
| Activities | 250 | -- |
| Problems | 150 | -- |
| Strategy | -- | 300 |
| Divisions | -- | 300 |
| Plans | 250 | 250 |
| Suggestions | 100 | -- |
| Learnings | 200 | 200 |
| Open Questions | -- | 150 |
| Cross-links | none | none |

- `--` means the section is not part of that report; `none` means the
  section has no minimum.
- A word is a run of characters between spaces that holds a letter or
  a digit. Lists, tables and sub-headings inside a section count;
  code-fence lines and table rule lines do not.
  `python3 -B scripts/report-words.py reports/<file>` counts the words
  of every section and reads the minimums from the table above.
- The words carry facts. A section with little to report reaches its
  minimum by saying what was checked and what the check showed: under
  Problems, the losses and failed orders looked for, the records read
  and the risks watched; under Suggestions and Open Questions, what
  was weighed and why nothing more is proposed or asked; under
  Learnings, what the period confirmed of what the writer already
  knew. Nothing is invented and nothing is said twice to fill a
  section.

### Division report (an Admiral)

Title: `# <Division> -- <main result of the period>`

**`## Situation`** -- *Where does the division stand?*

- The period covered: from the previous report (name it) to now.
- The orders in force, with their source: the Fleet Admiral's report
  or the log entry that gave them.
- The numbers, each from a named record:

```
Ships: <active>/<total>, grounded: <n>, lost: <n>
Credits: start <n>, end <n>, net <n>
Output: <what the division produced, in its own units>
```

**`## Activities`** -- *What did the division do?* Ordered by order or
goal, not by time: what was done and what came of it.

**`## Problems`** -- *What went wrong or stands in the way?* For each:
what happened, where, the cause (or "cause not found"), and what was
done about it. Losses and failed orders are never left out.

**`## Plans`** -- *What does the division do next?* Inside the orders
in force. Say which choices the Admiral made itself.

**`## Suggestions`** -- *What can be changed?* Read by the Fleet
Admiral and by Suggi. Proposals on strategy, orders, resources, rules,
tools or the way the fleet is run, each with its reason and what it
would cost; say whose it is to decide where that is clear. An
objection to an order belongs here.

**`## Learnings`** -- *What did the division learn?* What the period
taught the Admiral about its own role in the game, written from its
learning capture (`learnings-capture`): each lesson, the record that
earned it, what the division does differently because of it, and what
another division or the Fleet Admiral can take from it. It names the
knowledge files created or updated, which stay in the Admiral's
workspace, and what stays an open question. The report carries the
lessons to the fleet.

**`## Cross-links`** -- the reports and files this one builds on, by
repository path with a short description.

### Fleet report (the Fleet Admiral)

Title: `# The Collective -- <main result of the period>`

**`## Situation`** -- *Where does the fleet stand?* The period
covered; one line per division taken from its Admiral's newest report
(cite it); fleet totals where they were measured.

**`## Strategy`** -- *What are we playing for, and how?* The strategy
in force; what Suggi and the Fleet Admiral decided in the period, and
why; what changed.

**`## Divisions`** -- *What did the Admirals report?* For each
division: what its Admiral reported, the Fleet Admiral's judgment of
it, and an answer to every suggestion: accepted, declined or open,
with the reason. A suggestion that is Suggi's to decide is carried
into Open Questions with the Fleet Admiral's recommendation.

**`## Plans`** -- *What happens next?* What each division does next,
and what the Fleet Admiral does herself: systems to build, diplomacy,
questions to settle.

**`## Open Questions`** -- *What must Suggi decide?* Each question
with the Fleet Admiral's recommendation.

**`## Learnings`** -- *What did the Fleet Admiral learn?* What the
period taught her about leading the fleet (its strategy, its orders
and its systems), written from her learning capture
(`learnings-capture`): each lesson, the record that earned it, what
she does differently because of it, and what the Admirals or Suggi can
take from it. It names the knowledge files created or updated, which
stay in her workspace, and what stays an open question.

**`## Cross-links`** -- every Admiral report used, and the files the
strategy rests on, by repository path with a short description.

## Anti-patterns

| Anti-pattern | Why It Fails | The Fix |
|---|---|---|
| Report as diary | "First X, then Y, then Z." The reader has to find the result alone. | Order by goal. State the result first. |
| Numbers from memory | A typed number looks like a measured one. | Print it from the record and name the record, or write "not measured". |
| Success-only report | "Problems: None." beside lost ships. The Fleet Admiral plans on a false picture. | Every loss and failed order goes under Problems with its cause. |
| Suggestion without a reason | It cannot be accepted or declined, only ignored. | Say what can be changed, why, and what it costs. |
| Fleet report that copies | Repeating five division reports adds nothing. | Cite them, judge them, decide. |
| Padding | Words without facts hide the lines that matter, and a minimum met with filler is a false account of the work. | Reach the minimum with what was done, measured, checked or weighed; never repeat, never invent. |
| Thin section | "Problems: None." tells the reader nothing about what was looked at. | Say what was checked and what the check showed; every section has a minimum (Minimum Length). |

## Example -- Minimal Structure

Shows the layout only, not the length: every `<...>` is a placeholder,
not data, and a real section holds at least its minimum of words.

```markdown
---
name: <main-result-in-a-few-words>
id: <YYYYMMDDTHHMMSSZ>
tier: report
trigger: session-end
author: <Admiral>
tags: [<division>, <topic>]
links:
  - reports/<the-fleet-admirals-report-in-force>.md
---

# <Division> -- <Main Result of the Period>

## Situation

Period: since `reports/<my-previous-report>.md`. Orders in force:
<order>, from `reports/<the-fleet-admirals-report-in-force>.md`.

Ships: <active>/<total>, grounded: <n>, lost: <n>
Credits: start <n>, end <n>, net <n>
Output: <amount and unit>
Source: <the record these numbers were printed from>

## Activities

<Goal>: <what was done>; <what came of it>.

## Problems

<What happened, where>. Cause: <cause>. Done: <action>.

## Plans

<What the division does next, inside its orders>.

## Suggestions

<What can be changed>, because <reason>; it would cost <cost>.

## Learnings

<Lesson>, shown by <record>; the division now <what it does
differently>. For the fleet: <what another division can take from
it>. Kept in: <knowledge file, or "unpromoted">.

## Cross-links

- `reports/<the-fleet-admirals-report-in-force>.md` -- the plan this
  period ran under.
```

---

*Last updated: 2026-11-15 by Morpheus, on Suggi's instruction: a fleet report carries Learnings too, at least 200 words. Suggi refines the contents with the Fleet Admiral.*
