#!/usr/bin/env python3
"""docs_export.py -- copies an allowlist of each member's own files into the data folder, where the store mirrors them into its tables docs and doc_versions: every member's soul, mission, learnings and knowledge, readable by every member from the database.

WHAT: the members' own files lie in their profiles (/opt/data/profiles/<member>/), which the store's container does
      not mount. Unity's five-minute job runs this script in the agents' container; it copies, for each member m of
      unity, zero, oracle, mercury, apollo and apophis, exactly these files and no other:
        /opt/data/profiles/<m>/SOUL.md
        /opt/data/profiles/<m>/workspace-<m>/MISSION.md, LEARNINGS.md, IDENTITY.md, knowledge/*.md, and COLLECTIVE.md
        while it still stands (2026-11-18 it is split into ROSTER.md and MISSION.md)
        and for unity also DESIGN.md, DECISIONS.md, BOX.md
      to data/docs/members/<m>/ (SOUL.md, MISSION.md, knowledge/<name>.md ...), and once the roster every member's
        workspace holds the same: /opt/data/profiles/unity/workspace-unity/ROSTER.md -> data/docs/members/fleet/ROSTER.md
      docs.py loads them at the store's next pass as kind `member`, owned by the member's division (the roster: Fleet;
      an old COLLECTIVE.md: its part below the MISSION mark as the section `mission`, the shared part above it from
      Unity's copy only).
RULES:
  - The allowlist above is the whole of it: never another file (no .env, no memory/, no scripts/, no settings, no
    AGENTS.md). A knowledge file is a regular file `knowledge/<name>.md` directly in the folder, its name of letters,
    digits, dots, dashes and underscores, not starting with a dot.
  - A link is never followed: a source that is a symbolic link, or a knowledge folder that is one, is skipped.
  - A file larger than MAX_BYTES, or one that holds what looks like a credential (SECRET: a GitHub, OpenAI, Slack or
    AWS key, a private key block), is held back: not copied, its old copy removed, and named in the output.
  - A copy is written only when its source changed: same size and mtime as the copy is unchanged without a read;
    else the source is read and its sha1 compared with the copy's, and only a new text is written (to a dot file
    beside it, then renamed: the store never reads half a file). The copy takes the source's mtime.
  - A copy whose source left (or was held back) is removed, and so is any other file in data/docs/members/. A
    member whose profile folder is missing or unreadable keeps its copies (a run in the wrong container removes
    nothing) and is named.
  - It reads the members' folders and writes data/docs/members/ only; it calls nothing.
WHY:  Suggi, 2026-11-18: "Everything must be in the database, so the other agents know what the other admirals are
      doing ... They edit it, but then the script fetches it and stores it in the database. NEVER BY HAND." The store
      runs where the profiles are not mounted; this copy is its way in.

USAGE:
  docs_export.py [--dry-run] [--quiet]   copy what changed, remove what left; one line of counts (--quiet: only when
                                         something was copied, removed or held back); --dry-run says what it would do
  --profiles <dir>   the members' profiles (default /opt/data/profiles)
  --data <dir>       the unit's data folder (default: the fleet's)

Stdlib only. ASCII only.
"""

import hashlib
import os
import re
import stat
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  the members, the data folder

PROFILES = "/opt/data/profiles"
TARGET = Path("docs") / "members"                 # under the data folder
WORKSPACE_FILES = ("MISSION.md", "LEARNINGS.md", "IDENTITY.md", "COLLECTIVE.md")    # COLLECTIVE.md: until the split into ROSTER.md and MISSION.md is in
UNITY_FILES = ("DESIGN.md", "DECISIONS.md", "BOX.md")
SHARED = (("fleet", "unity", "ROSTER.md"),)       # (copy's folder, whose workspace, file): the same in every workspace, copied once
KNOWLEDGE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.md")
MAX_BYTES = 1000000            # a member's file above this is held back: a knowledge file is a few ten thousand bytes
SECRET = re.compile(rb"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|gh[ousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}"
                    rb"|xox[abprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")


def members():
    """The copies' folders: each member's, then each shared file's (fleet)."""
    return [name.lower() for name in division.MEMBERS] + list(dict.fromkeys(folder for folder, _member, _name in SHARED))


def home_of(profiles, folder):
    """The profile folder a copies' folder is read from: the member's own; a shared file's, its member's."""
    return Path(profiles) / next((member for shared, member, _name in SHARED if shared == folder), folder)


def allowlist(profiles, member):
    """[(name of the copy, source path)] of one copies' folder: the allowlist, whether the files exist or not, knowledge
    files as they stand in a knowledge folder that is no link; a shared folder (fleet) holds its shared files only."""
    shared = [(name, Path(profiles) / owner / ("workspace-" + owner) / name) for folder, owner, name in SHARED if folder == member]
    if shared:
        return shared
    home = Path(profiles) / member
    work = home / ("workspace-" + member)
    out = [("SOUL.md", home / "SOUL.md")]
    out += [(name, work / name) for name in WORKSPACE_FILES + (UNITY_FILES if member == "unity" else ())]
    folder = work / "knowledge"
    if folder.is_dir() and not folder.is_symlink():
        out += [("knowledge/" + path.name, path) for path in sorted(folder.iterdir()) if KNOWLEDGE.fullmatch(path.name)]
    return out


def regular(path):
    """os.stat_result of a regular file that is no link, else None."""
    try:
        found = os.lstat(path)
    except OSError:
        return None
    return found if stat.S_ISREG(found.st_mode) else None


def digest(data):
    return hashlib.sha1(data).hexdigest()


def plan(profiles, data):
    """What one run does: {copy: [(member, name, source, target, reason)], keep: n, held: [(member, name, why)],
    remove: [target], missing: [member]}."""
    root = Path(data) / TARGET
    out = {"copy": [], "keep": 0, "held": [], "remove": [], "missing": []}
    wanted = set()
    for member in members():
        home = home_of(profiles, member)
        if not home.is_dir() or not os.access(str(home), os.R_OK | os.X_OK):
            out["missing"].append(member)
            if (root / member).is_dir():
                wanted |= {p for p in (root / member).rglob("*") if p.is_file() and not p.name.startswith(".")}
            continue
        for name, source in allowlist(profiles, member):
            found = regular(source)
            if found is None:
                continue
            target = root / member / name
            if found.st_size > MAX_BYTES:
                out["held"].append((member, name, "larger than %d bytes" % MAX_BYTES))
                continue
            copy = regular(target)
            if copy is not None and copy.st_size == found.st_size and int(copy.st_mtime) == int(found.st_mtime):
                wanted.add(target)
                out["keep"] += 1
                continue
            try:
                body = Path(source).read_bytes()
            except OSError as error:
                out["held"].append((member, name, "not readable: %s" % error.strerror))
                if copy is not None:
                    wanted.add(target)                    # a passing read fault: the old copy stays
                continue
            if SECRET.search(body):
                out["held"].append((member, name, "it holds what looks like a credential"))
                continue
            wanted.add(target)
            if copy is not None and digest(target.read_bytes()) == digest(body):
                out["copy"].append((member, name, body, target, found.st_mtime, "mtime"))
            else:
                out["copy"].append((member, name, body, target, found.st_mtime, "new" if copy is None else "changed"))
    if root.is_dir():
        for path in sorted(root.rglob("*")):
            if (path.is_file() or path.is_symlink()) and path not in wanted:
                out["remove"].append(path)
    return out


def write(target, body, mtime):
    """The new text beside the copy under a dot name, then renamed over it; the copy takes the source's mtime."""
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(".%s.%d.tmp" % (target.name, os.getpid()))
    try:
        with open(temp, "wb") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp, 0o644)
        os.utime(temp, (mtime, mtime))
        os.replace(temp, target)
    finally:
        if temp.exists():
            temp.unlink()


def run(profiles, data, dry_run=False):
    """Carry out (or, dry, only say) one run: (lines to print, {copied, touched, kept, removed, held, missing})."""
    work = plan(profiles, data)
    lines, root = [], Path(data) / TARGET
    counts = {"copied": 0, "touched": 0, "kept": work["keep"], "removed": 0, "held": len(work["held"]), "missing": len(work["missing"])}
    for member, name, body, target, mtime, reason in work["copy"]:
        if reason == "mtime":
            counts["touched"] += 1
            if not dry_run:
                os.utime(target, (mtime, mtime))
            continue
        counts["copied"] += 1
        lines.append("  %s %s/%s (%s, %d bytes)" % ("would copy" if dry_run else "copied", member, name, reason, len(body)))
        if not dry_run:
            write(target, body, mtime)
    for path in work["remove"]:
        counts["removed"] += 1
        lines.append("  %s %s (its source left or is no part of the allowlist)" % ("would remove" if dry_run else "removed", path.relative_to(root).as_posix()))
        if not dry_run:
            path.unlink()
    if not dry_run and root.is_dir():
        for folder in sorted((p for p in root.rglob("*") if p.is_dir()), key=lambda p: -len(p.parts)):
            if not any(folder.iterdir()):
                folder.rmdir()
    for member, name, why in work["held"]:
        lines.append("  held back %s/%s: %s" % (member, name, why))
    for member in work["missing"]:
        lines.append("  not read: %s is missing or not readable; the copies in %s/ stay" % (home_of(profiles, member), member))
    return lines, counts


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    if any(a in ("-h", "--help") for a in args) or [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--profiles", "--data"))]:
        sys.exit(__doc__)
    profiles, data, dry = value("--profiles", PROFILES), value("--data", division.DATA), "--dry-run" in args
    lines, counts = run(profiles, data, dry)
    if "--quiet" in args and not (counts["copied"] or counts["removed"] or counts["held"] or counts["missing"]):
        return 0
    print("EXPORT%s | the members' own files into %s: %d copied, %d with only their time set, %d unchanged, %d removed, %d held back, "
          "%d members not read" % (" (dry run: nothing written)" if dry else "", Path(data) / TARGET, counts["copied"], counts["touched"], counts["kept"],
                                   counts["removed"], counts["held"], counts["missing"]))
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
