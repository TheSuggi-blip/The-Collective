#!/usr/bin/env python3
"""data-keeper.py -- keeps the append-only records of the unit's data folder from growing forever.

WHAT: the service `keeper` runs it. Every ten minutes it looks at each record of RECORDS. A
      record above its limit is cut at a line boundary: the older lines go, compressed, to
      <data>/archive/<record>.<UTC time>.<hash>.jsonl.gz, the newer lines stay where every
      reader expects them. Of each record the five newest archives are kept and older ones
      are deleted.
RULES:
  - No line is lost and none is written twice while other programs append: the record is
    replaced in one step, and lines appended to the old file around that step are carried
    over into the new one.
  - A record belongs in RECORDS only when no program needs its old lines in place. Before a
    record is listed, name every reader of it and what each needs.
  - It reads and writes files of the data folder only: no ship, no web, no repository.
WHY:  every file in the data folder is replaced or capped (services README). Records that
      only grow make every reader slower each day and fill the disk in the end.

Not listed yet, and why:
  routes/runs.jsonl      game/fleet/dispatch.py reads from it which pilot flew a route once
                         (done_once, max_pilots): cut lines would send pilots out again.
  comms/messages.jsonl   game/fleet/inbox.py rebuilds the contact logs from it: cut lines
                         would vanish from communications/contacts/.

USAGE:
  data-keeper.py                 run forever (the service `keeper`)
  data-keeper.py --once          one pass, then stop
  data-keeper.py --list          the records: limit, size, archives
  --data <dir>                   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import fcntl
import gzip
import hashlib
import os
import stat
import sys
import time
from pathlib import Path

MB = 1_000_000
RECORDS = {                    # record: (cut when above this many MB, lines of this many MB stay)
    "market/history.jsonl": (8, 4),
    "wildlife/history.jsonl": (8, 4),
}
KEEP = 5                       # archives kept per record
EVERY = 600                    # seconds between two passes
SETTLE = 2.0                   # seconds a record's old file is watched for late lines after the swap


def stem_of(name):
    stem = name.replace("/", "-")
    return stem[:-6] if stem.endswith(".jsonl") else stem


def archives(data, name):
    """The archives of one record, oldest first."""
    return sorted((Path(data) / "archive").glob(stem_of(name) + ".[0-9]*Z.*.jsonl.gz"))


def store(data, name, head):
    """Write the cut lines as one archive; None when an archive of exactly these lines exists
    (a pass that ended between the archive and the swap is taken up again without a twin)."""
    folder = Path(data) / "archive"
    folder.mkdir(exist_ok=True)
    digest = hashlib.sha256(head).hexdigest()[:12]
    if list(folder.glob("%s.*.%s.jsonl.gz" % (stem_of(name), digest))):
        return None
    target = folder / ("%s.%s.%s.jsonl.gz" % (stem_of(name), time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()), digest))
    tmp = folder / ("." + target.name + ".tmp")
    with open(tmp, "wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as packed:
            packed.write(head)
        raw.flush()
        os.fsync(raw.fileno())
    os.replace(tmp, target)
    return target


def rest(handle, position):
    """What the old file holds from `position` on."""
    handle.seek(position)
    return handle.read()


def trim(data, name, limit, stay, keep=KEEP, settle=SETTLE):
    """Cut one record when it is above `limit` bytes so that about `stay` bytes of whole lines
    stay. Returns a line that says what was done, or None when nothing was."""
    path = Path(data) / name
    try:
        size = path.stat().st_size
    except OSError:
        return None
    if size <= limit:
        return None
    with open(path, "rb") as old:                 # stays open: lines appended to this file later are read from here
        whole = old.read(size)
        end = whole.rfind(b"\n") + 1               # the end of the last whole line
        start = end - stay                         # where the lines that stay begin, at the earliest
        if start <= 0:
            return None
        cut = whole.find(b"\n", start - 1) + 1     # the first line start at or after `start`
        if cut <= 0 or cut >= end:
            return None
        head, tail = whole[:cut], whole[cut:end]
        target = store(data, name, head)
        fresh = path.with_name("." + path.name + ".keeper")
        position = end
        with open(fresh, "wb") as new:
            new.write(tail)
            more = rest(old, position)             # appended since the read: whole lines only
            more = more[:more.rfind(b"\n") + 1]
            new.write(more)
            position += len(more)
            new.flush()
            os.fsync(new.fileno())
        os.chmod(fresh, stat.S_IMODE(os.fstat(old.fileno()).st_mode))
        os.replace(fresh, path)                    # the swap: a reader sees the old record or the new one, whole
        late = 0
        for _ in range(2):                         # a writer that had opened the old file before the swap
            time.sleep(settle / 2)
            more = rest(old, position)
            if more:
                out = os.open(path, os.O_WRONLY | os.O_APPEND)
                try:
                    os.write(out, more)
                finally:
                    os.close(out)
                position += len(more)
                late += len(more)
    gone = archives(data, name)[:-keep] if keep else []
    for old_archive in gone:
        old_archive.unlink()
    return "%s: %.1f MB cut to %.1f MB; %d lines %s; %d late bytes carried over; %d archive(s) kept, %d deleted" % (
        name, size / MB, (len(tail) + position - end) / MB, head.count(b"\n"),
        "to archive/" + target.name if target else "were archived before", late, len(archives(data, name)), len(gone))


def one_pass(data):
    """Trim every record that is above its limit; the lines to print."""
    folder = Path(data) / "archive"
    folder.mkdir(exist_ok=True)
    with open(folder / ".keeper.lock", "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return ["another keeper is at work: nothing done"]
        lines = []
        for name, (limit, stay) in sorted(RECORDS.items()):
            try:
                line = trim(data, name, int(limit * MB), int(stay * MB), settle=SETTLE)
            except OSError as error:
                line = "%s: not trimmed (%s: %s)" % (name, type(error).__name__, error)
            if line:
                lines.append(line)
        return lines


def listing(data):
    lines = []
    for name, (limit, stay) in sorted(RECORDS.items()):
        path = Path(data) / name
        size = path.stat().st_size if path.is_file() else 0
        kept = archives(data, name)
        lines.append("%-26s cut above %d MB to %d MB | now %.2f MB | archives %d (%.2f MB)%s" % (
            name, limit, stay, size / MB, len(kept), sum(p.stat().st_size for p in kept) / MB,
            " %s .. %s" % (kept[0].name.split(".")[1], kept[-1].name.split(".")[1]) if kept else ""))
    return lines


def main(argv):
    data = "/srv/collective/data"
    if "--data" in argv:
        data = argv[argv.index("--data") + 1]
    if "--list" in argv:
        print("\n".join(listing(data)))
        return 0
    if "--once" in argv:
        lines = one_pass(data)
        print("\n".join(lines) if lines else "keeper: no record is above its limit")
        return 0
    print("keeper: %d record(s), a look every %d s, %d archives kept of each" % (len(RECORDS), EVERY, KEEP), flush=True)
    while True:
        for line in one_pass(data):
            print(time.strftime("%Y-%m-%dT%H:%M:%SZ ", time.gmtime()) + line, flush=True)
        time.sleep(EVERY)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
