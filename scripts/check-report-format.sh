#!/bin/bash
# check-report-format.sh -- mechanical format gate for reports/
# (governance/template-reports.md, Report Checklist).
# Usage: bash scripts/check-report-format.sh <reports/YYYY-MM-DD_author_slug.md>
# PASS: prints "REPORT FORMAT: PASS", exit 0.
# HALT: prints one line per violation, then "REPORT FORMAT: HALT", exit 1.
# It checks form only: file name, frontmatter, section headings, ASCII.
# Whether the numbers are true is the writer's gate, not this one.
set -u
F="${1:-}"
if [ ! -f "$F" ]; then
  echo "FAIL: file not found: $F"
  exit 1
fi
fail=0
miss() { echo "$1"; fail=1; }

base=$(basename "$F")
if ! printf '%s\n' "$base" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}_[a-z0-9-]+_[a-z0-9-]+\.md$'; then
  miss "FILE NAME is not YYYY-MM-DD_author_slug.md (lower case)"
fi
stem=${base%.md}
file_author=$(printf '%s' "$stem" | cut -d_ -f2)
file_slug=$(printf '%s' "$stem" | cut -d_ -f3-)

# Frontmatter: the lines between the first two '---' lines.
[ "$(head -n 1 "$F")" = "---" ] || miss "MISSING frontmatter (the first line is not ---)"
front=$(awk '/^---$/ {c++; next} c==1 {print} c>=2 {exit}' "$F")
field() { printf '%s\n' "$front" | sed -n "s/^$1: *//p" | head -n 1; }
for key in name id tier trigger author tags links; do
  printf '%s\n' "$front" | grep -qE "^$key:" || miss "MISSING frontmatter $key:"
done
[ "$(field name)" = "$file_slug" ] || miss "name: does not match the file name's slug ($file_slug)"
field id | grep -qE '^[0-9]{8}T[0-9]{6}Z$' || miss "id: is not YYYYMMDDTHHMMSSZ"
[ "$(field tier)" = "report" ] || miss "tier: is not report"
field trigger | grep -qE '^(session-end|incident|milestone|order)$' || miss "trigger: is not one of session-end, incident, milestone, order"
author=$(field author)
[ "$(printf '%s' "$author" | tr 'A-Z' 'a-z')" = "$file_author" ] || miss "author: does not match the file name's author ($file_author)"
printf '%s\n' "$author" | grep -qE '^[A-Z]' || miss "author: is not capitalized"
printf '%s\n' "$front" | grep -qE '^tags: \[.+\]' || miss "tags: is not a filled YAML array (tags: [a, b])"

# Body: everything after the frontmatter.
body=$(awk '/^---$/ {c++; if (c<=2) next} c>=2 {print}' "$F")
[ "$(printf '%s\n' "$body" | grep -c '^# ')" = 1 ] || miss "the body needs exactly one '# ' title line"
if printf '%s\n' "$body" | grep -q '^## Strategy$'; then
  kind=fleet
  want='Situation|Strategy|Divisions|Plans|Open Questions|Cross-links'
else
  kind=division
  want='Situation|Activities|Problems|Plans|Suggestions|Learnings|Cross-links'
fi
have=$(printf '%s\n' "$body" | sed -n 's/^## //p' | paste -sd'|' -)
[ "$have" = "$want" ] || miss "SECTIONS of a $kind report must be exactly, in order: $want (found: $have)"
if LC_ALL=C grep -qP '[^\x00-\x7F]' "$F"; then
  miss "NON-ASCII bytes present"
fi

if [ "$fail" -eq 0 ]; then
  echo "REPORT FORMAT: PASS ($kind report)"
else
  echo "REPORT FORMAT: HALT -- fix the violations and re-run"
fi
exit $fail
