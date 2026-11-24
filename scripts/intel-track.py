#!/usr/bin/env python3
"""intel-track.py -- one pass of the automatic intel: track, index, gate, commit.

WHAT: 1. scripts/intel-planets.py  files the systems our ships have read;
      2. scripts/intel-players.py  files the armed pilots seen in our space;
      3. scripts/intel-factions.py files the player factions that hold a base
                                   or have pilots in our space, and the zones
                                   they hold (game/factions/index.md);
      4. scripts/intel-index.py    rebuilds game/planets/index.md and game/players/index.md;
      5. scripts/validate-intel.py and scripts/validate-ids.sh check the result;
      6. with --commit: one commit of exactly the files this pass wrote.
         Without it the pass is a rehearsal: it prints what it would
         change and takes its files out again.
RULES:
  - Refuses to start when game/planets/, game/players/ or game/factions/ hold a change
    that is not committed: that is another writer's work in progress.
  - A pass that fails a gate takes its own files out again and restores
    the index files, so nothing untracked is left in the clone (an
    untracked file holds every agent's push).
  - Never pushes: the watcher does. Commits by path, as the author given.
WHY:  what ships and public data show reaches the repository without an
      agent retyping it, and never half-written.

USAGE:
  intel-track.py              rehearsal: print what would change; leave nothing behind
  intel-track.py --commit     track, index, gate and commit
  intel-track.py --root <dir> another repository tree (used by tests)
  --author "<name> <mail>"    default: Unity <unity@suggi-workspace.dev>
  --data, --station, --fleet, --kills, --max, --met are handed to the trackers.

Stdlib only. ASCII only.
"""

import argparse
import os
import subprocess
import sys


def run(root, *command):
    done = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def changed(root):
    """Paths under game/planets/, game/players/ and game/factions/ that git sees as new or modified."""
    _code, out = run(root, "git", "status", "--porcelain", "--untracked-files=all", "--", "game/planets", "game/players", "game/factions")
    return [line[3:].strip() for line in out.splitlines() if line.strip()]


def undo(root, paths):
    for path in paths:
        code, _out = run(root, "git", "ls-files", "--error-unmatch", "--", path)
        if code == 0:
            run(root, "git", "checkout", "--", path)          # a tracked file: back to its committed state
        else:
            try:
                os.remove(os.path.join(root, path))           # a file this pass created
            except OSError:
                pass


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="One pass of the automatic intel.")
    parser.add_argument("--root", default=os.path.join(here, ".."))
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--author", default="Unity <unity@suggi-workspace.dev>")
    args, extra = parser.parse_known_args()
    root = os.path.abspath(args.root)
    scripts = os.path.join(root, "scripts")
    before = changed(root)
    if before:
        print("HALT: game/planets/, game/players/ or game/factions/ hold changes that are not committed: %s" % ", ".join(before))
        return 1
    planets_extra = [a for pair in zip(extra, extra[1:]) if pair[0] == "--data" for a in pair]
    players_extra = [a for pair in zip(extra, extra[1:]) if pair[0] in ("--station", "--fleet", "--kills", "--max") for a in pair]
    factions_extra = [a for pair in zip(extra, extra[1:]) if pair[0] in ("--station", "--fleet", "--met", "--min-interval") for a in pair]
    if "--min-interval" not in factions_extra:
        factions_extra += ["--min-interval", "21600"]
    for command in (["python3", "-B", os.path.join(scripts, "intel-planets.py"), "--root", root] + planets_extra,
                    ["python3", "-B", os.path.join(scripts, "intel-players.py"), "--root", root] + players_extra,
                    ["python3", "-B", os.path.join(scripts, "intel-factions.py"), "--root", root] + factions_extra,
                    ["python3", "-B", os.path.join(scripts, "intel-index.py"), "--root", root]):
        code, out = run(root, *command)
        print(out.rstrip())
        if code != 0:
            undo(root, changed(root))
            print("HALT: %s failed; this pass's files were taken out again" % os.path.basename(command[2]))
            return 1
    paths = changed(root)
    if not paths:
        print("Nothing new.")
        return 0
    for command in (["python3", "-B", os.path.join(scripts, "validate-intel.py"), "--root", root],
                    ["bash", os.path.join(scripts, "validate-ids.sh")]):
        code, out = run(root, *command)
        if code != 0:
            print(out.rstrip())
            undo(root, paths)
            print("HALT: a gate failed; this pass's files were taken out again")
            return 1
    if not args.commit:
        undo(root, paths)
        print("Would change (rehearsal; nothing is left in the clone): " + ", ".join(paths))
        return 0
    print("Changed: " + ", ".join(paths))
    name, _sep, mail = args.author.partition(" <")
    run(root, "git", "add", "--", *paths)
    message = "intel: %d file(s) from the automatic tracker" % len(paths)
    code, out = run(root, "git", "-c", "user.name=" + name, "-c", "user.email=" + mail.rstrip(">"), "commit", "-m", message, "--", *paths)
    print(out.rstrip())
    if code != 0:
        run(root, "git", "reset", "-q", "--", *paths)
        undo(root, paths)
        print("HALT: the commit failed; this pass's files were taken out again")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
