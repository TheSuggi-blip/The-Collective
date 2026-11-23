#!/usr/bin/env python3
"""gitcommit.py -- commit files a script wrote into the clone by path, and never leave them uncommitted there.

WHAT: commit_paths(root, paths, message, who) stages and commits the named paths as `who`, trying again while another
      git holds the clone's index.lock; when the commit still fails, the paths are taken back to the last commit (a
      path new since then is removed), so the clone is clean again, and (False, why) comes back for the caller to print.
RULES:
  - By path only: nothing else in the clone is staged, committed or taken back.
  - A failure is never silent: the caller exits non-zero with the reason, so a scheduled job prints it.
  - Stdlib only, ASCII only; no pilot, no gate, no data folder.
WHY:  2026-11-23: governance/rival-sedcards.md stood written and uncommitted in the clone from 16:29 to 19:38 UTC (the
      hourly refresh swallowed a failed `git add`), and `fleet-build.sh install` refused every member's install while
      the clone was not clean (requests ENT-472, ENT-473). inbox.py met the same lock on 2026-11-21 (requests ENT-288).

USAGE:
  import gitcommit
  ok, text = gitcommit.commit_paths(repo, ["governance/rival-sedcards.md"], "governance: ...", "Unity")
  python3 -I -B game/fleet/gitcommit.py <repo> <message> <who> <path> [<path> ...]

Stdlib only. ASCII only."""
import subprocess
import sys
import time

TRIES, WAIT = 5, 3.0           # a git call that meets another git's index.lock is tried so often, so many seconds apart


def git(root, *args):
    done = subprocess.run(["git", "-C", str(root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def git_locked(root, *args, tries=None, wait=None):
    """git(), tried again while the answer names an index.lock another git holds."""
    tries = TRIES if tries is None else tries
    wait = WAIT if wait is None else wait
    code, out = git(root, *args)
    for _ in range(max(0, tries - 1)):
        if code == 0 or "index.lock" not in out:
            break
        time.sleep(wait)
        code, out = git(root, *args)
    return code, out


def commit_paths(root, paths, message, who, email=None, tries=None, wait=None):
    """(True, 'committed <hash>' or 'unchanged') or (False, why). On a failure every path is taken back to the last
    commit (one not in it is removed), so no script's file is left uncommitted in the clone."""
    paths = [str(p) for p in paths]
    email = email or "%s@suggi-workspace.dev" % str(who).lower().replace(" ", "-")
    code, out = git_locked(root, "status", "--porcelain", "--", *paths, tries=tries, wait=wait)
    if code == 0 and not out.strip():
        return True, "unchanged"
    code, out = git_locked(root, "add", "--", *paths, tries=tries, wait=wait)
    if code == 0:
        code, out = git_locked(root, "-c", "user.name=" + str(who), "-c", "user.email=" + email, "commit", "-q", "-m", message, "--", *paths,
                               tries=tries, wait=wait)
        if code == 0:
            return True, "committed " + git(root, "log", "-1", "--format=%h")[1].strip()
    why = (out or "").strip().splitlines()[-1:] or ["git said nothing"]
    git_locked(root, "reset", "-q", "--", *paths, tries=tries, wait=wait)
    tracked = [p for p in paths if git(root, "cat-file", "-e", "HEAD:" + p)[0] == 0]
    if tracked:
        git_locked(root, "checkout", "--", *tracked, tries=tries, wait=wait)
    for p in paths:
        if p not in tracked:
            subprocess.run(["rm", "-f", "--", "%s/%s" % (root, p)])
    return False, "not committed, taken back to the last commit: " + why[0][:240]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 4:
        print(__doc__.split("USAGE:")[1].strip())
        return 2
    root, message, who, paths = argv[0], argv[1], argv[2], argv[3:]
    ok, text = commit_paths(root, paths, message, who)
    print(text)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
