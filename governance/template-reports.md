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
- [ ] An empty section says "None." -- it is never left out  (PASS / HALT)
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
use paragraphs, lists and tables. There is no minimum length: a
section is as long as its facts. A section with nothing to say holds
the single word "None."

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

**`## Suggestions`** -- *What should the Fleet Admiral change?*
Proposals on strategy, resources, rules or tools, each with its
reason and what it would cost. An objection to an order belongs here.

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
with the reason.

**`## Plans`** -- *What happens next?* What each division does next,
and what the Fleet Admiral does herself: systems to build, diplomacy,
questions to settle.

**`## Open Questions`** -- *What must Suggi decide?* Each question
with the Fleet Admiral's recommendation.

**`## Cross-links`** -- every Admiral report used, and the files the
strategy rests on, by repository path with a short description.

## Anti-patterns

| Anti-pattern | Why It Fails | The Fix |
|---|---|---|
| Report as diary | "First X, then Y, then Z." The reader has to find the result alone. | Order by goal. State the result first. |
| Numbers from memory | A typed number looks like a measured one. | Print it from the record and name the record, or write "not measured". |
| Success-only report | "Problems: None." beside lost ships. The Fleet Admiral plans on a false picture. | Every loss and failed order goes under Problems with its cause. |
| Suggestion without a reason | It cannot be accepted or declined, only ignored. | Say what should change, why, and what it costs. |
| Fleet report that copies | Repeating five division reports adds nothing. | Cite them, judge them, decide. |
| Padding | Length hides the two lines that matter. | A section is as long as its facts. |

## Example -- Minimal Structure

Shows the layout only. Every `<...>` is a placeholder, not data.

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

<What should change>, because <reason>; it would cost <cost>.

## Cross-links

- `reports/<the-fleet-admirals-report-in-force>.md` -- the plan this
  period ran under.
```

---

*Last updated: 2026-11-14 by Morpheus, on Suggi's instruction. Suggi refines the contents with the Fleet Admiral.*
