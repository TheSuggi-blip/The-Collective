"""game/fleet/fleetfile.py on a disposable repository, data folder and member workspaces: the block it builds, where it goes in
FLEET.md, who may write it, and the commit. No engine, no network."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
MEMBERS = ("Unity", "Zero", "Apollo", "Mercury", "Apophis", "Oracle")
MEASURED = {"date": "2026-11-15", "runs": 3, "minutes": 30, "credits_per_run": 2500, "cph_per_ship": 5000}
ROUTES = {
    "park": {"id": "park", "kind": "circuit", "title": "t", "park": True, "stops": [{"at": "home:core:base"}]},
    "ice": {"id": "ice", "kind": "mine", "title": "t", "belt": "far:belt", "station": "home:core:base", "max_ships": 2, "measured": MEASURED,
            "sell": [{"item": "water_ice", "min_price": 20}]},
}
PLANS = {"miner": ("Zero", ["ice", "gone", "park"]), "command": ("Unity", ["park"]), "sentinel": ("Apophis", ["park"])}
IDLE = {"kind": "idle"}
SHIPS = [   # name, number, status, activity, docked, system
    ("miner-10", 10, "connected", IDLE, "base", "home"),
    ("miner-1", 1, "connected", IDLE, "base", "home"),
    ("miner-2", 2, "connected", IDLE, "base", "far"),
    ("miner-3", 3, "offline", IDLE, "base", "far"),
    ("miner-4", 4, "connected", {"kind": "goal", "since": "2026-11-16T11:20:00Z", "type": "navigate-to-system"}, "", "far"),
    ("Zero Point", 0, "connected", IDLE, "base", "home"),
    ("sentinel-1", 1, "connected", IDLE, "base", "home"),
]
ORDERS = {"miner-1": ("mine ice", "2026-11-16T10:05:00Z"), "miner-10": ("hand Zero", "2026-11-16T12:00:00Z"),
          "Zero Point": ("circuit a|b", "2026-11-16T13:45:00Z"), "sentinel-1": ("circuit park", "2026-11-16T13:50:00Z")}
RUNS = [
    {"route": "ice", "kind": "mine", "pilot": "miner-1", "started": "2026-11-16T09:00:00Z", "minutes": 30, "credits_before": 5000, "credits_after": 6000, "delta": 1000},
    {"route": "park", "kind": "circuit", "pilot": "miner-1", "started": "2026-11-16T08:00:00Z", "minutes": 5, "credits_before": 5000, "credits_after": 5000, "delta": 0},
    {"route": "ice", "kind": "mine", "pilot": "miner-2", "started": "2026-11-16T08:30:00Z", "minutes": 20, "credits_before": 0, "credits_after": 0, "delta": 0},
    {"route": "ice", "kind": "mine", "pilot": "Zero Point", "started": "2026-11-16T07:00:00Z", "minutes": 40, "credits_before": 9000, "credits_after": 7766, "delta": -1234},
]
BEGIN = "<!-- FLEET-ROSTER:BEGIN written by game/fleet/fleetfile.py; do not edit between the two marks -->"
END = "<!-- FLEET-ROSTER:END -->"


def tables(text):
    """[[the lines of one Markdown table]] of a text."""
    out, current = [], None
    for line in text.splitlines():
        if line.startswith("|"):
            if current is None:
                current = []
                out.append(current)
            current.append(line)
        else:
            current = None
    return out


def cells(line):
    return [c.strip() for c in line.strip()[1:-1].split("|")]


def rows_by_first(table):
    return {cells(line)[0]: dict(zip(cells(table[0]), cells(line))) for line in table[2:]}


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-fleetfile-test-")
        self.addCleanup(self.temp.cleanup)
        top = Path(self.temp.name)
        self.root, self.data, self.profiles = top / "repo" / "game", top / "data", top / "profiles"
        for folder in (self.root / "routes" / "plans", self.data / "fleet" / "orders", self.data / "fleet" / "ships", self.data / "routes"):
            folder.mkdir(parents=True)
        for rid, route in ROUTES.items():
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps(route, indent=1) + "\n", encoding="ascii")
        for role, (owner, ids) in PLANS.items():
            (self.root / "routes" / "plans" / (role + ".json")).write_text(json.dumps({"role": role, "owner": owner, "routes": ids}) + "\n", encoding="ascii")
        ships = [{"name": n, "number": num, "status": st, "activity": act, "docked": dock, "system": system, "credits": 9000, "class": "Threshold"}
                 for n, num, st, act, dock, system in SHIPS]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"updated_at": "2026-11-16T14:00:00Z", "ships": ships}))
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({"Zero Point": {"admiral": "Unity", "division": "Command", "role": "command", "of": "Zero"}}))
        for name, (what, since) in ORDERS.items():
            self.order(name, what, since)
        (self.data / "fleet" / "ships" / "miner-1.json").write_text(json.dumps({"skills": {"piloting": {"level": 5, "xp": 10}, "mining": 3},
                                                                               "modules": [{"type": "mining_laser_i"}, {"type": "ice_harvester_i"}]}))
        (self.data / "fleet" / "ships" / "Zero_Point.json").write_text(json.dumps({"skills": {"navigation": {"level": 4}}, "modules": []}))
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in RUNS))
        for member in MEMBERS:
            self.fleet_md(member).parent.mkdir(parents=True)
            self.fleet_md(member).write_text("# FLEET.md -- %s\n\nThe design, written by hand.\n" % member, encoding="ascii")

    def order(self, name, what, since):
        (self.data / "fleet" / "orders" / (name + ".json")).write_text(json.dumps({"pilot": name, "what": what, "since": since}))

    def fleet_md(self, member):
        return self.profiles / member.lower() / ("workspace-" + member.lower()) / "FLEET.md"

    def run_it(self, member, *args, env=None):
        environ = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": self.temp.name}
        if member:
            environ["HERMES_SESSION_PROFILE"] = member
        environ.update(env or {})
        return subprocess.run([sys.executable, "-I", "-B", str(FLEET / "fleetfile.py")] + list(args)
                              + ["--root", str(self.root), "--data", str(self.data), "--profiles", str(self.profiles)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=environ)

    def start_it(self, member, *args):
        """The script started and not waited for: (the process, its environment as run_it builds it)."""
        environ = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": self.temp.name, "HERMES_SESSION_PROFILE": member}
        return subprocess.Popen([sys.executable, "-I", "-B", str(FLEET / "fleetfile.py")] + list(args)
                                + ["--root", str(self.root), "--data", str(self.data), "--profiles", str(self.profiles)],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=environ)

    def git(self, folder, *args):
        return subprocess.run(["git", "-C", str(folder)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                              env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": self.temp.name}).stdout

    def assertTablesWhole(self, text):
        found = tables(text)
        self.assertTrue(found)
        for table in found:
            width = table[0].count("|")
            for line in table:
                self.assertEqual(line.count("|"), width, "a row whose cells differ from its header: " + line)


class BlockTests(Tree):
    def test_one_table_says_each_ships_kind_hull_and_task(self):
        done = self.run_it("zero", "--print")
        self.assertEqual(done.returncode, 0, done.stdout)
        text = done.stdout
        self.assertTrue(text.startswith(BEGIN + "\n| Ship | Kind | Hull | Task now |\n"), text[:200])
        self.assertEqual(text.rstrip("\n").splitlines()[-1], END)
        self.assertRegex(text, r"\nWritten by `game/fleet/fleetfile.py` at \d{4}-\d\d-\d\d \d\d:\d\d UTC from the fleet's live files\.\n")
        self.assertTablesWhole(text)
        found = tables(text)
        self.assertEqual(len(found), 1)                                                            # one table, the whole roster (Suggi, 2026-11-16)
        self.assertEqual(found[0][2:], ["| miner-1 | miner | Threshold | mine ice |", "| miner-2 | miner | Threshold | waits docked |",
                                        "| miner-3 | miner | Threshold | not connected |", "| miner-4 | miner | Threshold | busy by hand (goal) |",
                                        "| miner-10 | miner | Threshold | by hand: Zero |"])              # by number, then name; no level, no place
        self.assertIn("\n5 ships: 1 on a route, 1 waiting, 2 by hand, 1 not connected.\n", text)
        self.assertNotIn("home", text)
        self.assertNotIn("far", text)
        self.assertEqual(self.fleet_md("Zero").read_text(), "# FLEET.md -- Zero\n\nThe design, written by hand.\n")      # printing writes nothing

    def test_the_command_group_is_one_table_and_a_pipe_in_an_order_text_breaks_no_row(self):
        done = self.run_it("unity", "--print")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertTablesWhole(done.stdout)
        found = tables(done.stdout)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0][2:], ["| Zero Point | flagship of Zero | Threshold | circuit a/b |"])       # the sentinels are lent to Military (D226)
        self.assertIn("\n1 ships: 1 on a route, 0 waiting, 0 by hand, 0 not connected.\n", done.stdout)
        self.assertIn("| sentinel-1 | sentinel | Threshold | parked |", self.run_it("apophis", "--print").stdout)
        self.assertIn("No ship of Apollo in the fleet's file.", self.run_it("apollo", "--print").stdout)


class WriteTests(Tree):
    def block_of(self, text):
        start, end = text.index(BEGIN), text.index(END) + len(END)
        return text[start:end]

    def test_a_file_without_marks_gets_the_block_appended_after_one_blank_line(self):
        old = self.fleet_md("Zero").read_bytes()
        self.fleet_md("Zero").chmod(0o664)
        done = self.run_it("zero")
        self.assertEqual(self.fleet_md("Zero").stat().st_mode & 0o777, 0o664)                     # the rename keeps the file's mode
        self.assertEqual((done.returncode, done.stdout), (0, "Zero: written: %s (5 ships, miner)\n" % self.fleet_md("Zero")))
        new = self.fleet_md("Zero").read_bytes()
        self.assertTrue(new.startswith(old))
        self.assertTrue(new[len(old):].startswith(b"\n" + BEGIN.encode()), new[len(old):][:80])
        self.assertTrue(new.endswith(END.encode() + b"\n"))
        self.fleet_md("Apollo").write_bytes(b"# no newline at the end")
        self.assertEqual(self.run_it("apollo").returncode, 0)
        self.assertTrue(self.fleet_md("Apollo").read_bytes().startswith(b"# no newline at the end\n\n" + BEGIN.encode()))
        self.assertIn("No ship of Apollo in the fleet's file.", self.fleet_md("Apollo").read_text())

    def test_the_block_between_the_marks_is_replaced_and_the_text_around_it_kept_byte_for_byte(self):
        before = b"# FLEET.md\r\nA line with two trailing spaces  \n\n"
        after = b"\n\n## After the block\nlast line without a newline"
        self.fleet_md("Zero").write_bytes(before + BEGIN.encode() + b"\nan old table\n| a | b |\n" + END.encode() + after)
        done = self.run_it("zero")
        self.assertEqual(done.returncode, 0, done.stdout)
        new = self.fleet_md("Zero").read_bytes()
        self.assertTrue(new.startswith(before + BEGIN.encode() + b"\n| Ship | Kind | Hull | Task now |\n"))
        self.assertTrue(new.endswith(END.encode() + after))
        self.assertNotIn(b"an old table", new)
        self.assertEqual(new.count(BEGIN.encode()), 1)
        timeless = lambda text: re.sub(r"\d{4}-\d\d-\d\d \d\d:\d\d UTC", "<time>", text)
        self.assertEqual(timeless(new[len(before):len(new) - len(after)].decode()), timeless(self.run_it("zero", "--print").stdout.rstrip("\n")))

    def test_one_mark_alone_halts_and_writes_nothing(self):
        folder = self.fleet_md("Zero").parent
        for text in ("# x\n" + BEGIN + "\nold\n", "# x\nold\n" + END + "\n", "# x\n" + END + "\n" + BEGIN + "\n",
                     "# x\n" + BEGIN + "\n" + BEGIN + "\n" + END + "\n"):
            self.fleet_md("Zero").write_text(text, encoding="ascii")
            done = self.run_it("zero")
            self.assertEqual(done.returncode, 1, done.stdout)
            self.assertTrue(done.stdout.startswith("HALT: Zero: "), done.stdout)
            self.assertEqual(self.fleet_md("Zero").read_text(), text)
            self.assertEqual(sorted(p.name for p in folder.iterdir()), ["FLEET.md"])          # no temporary file left behind

    def test_a_second_run_that_changes_only_the_time_leaves_the_file_alone(self):
        self.assertEqual(self.run_it("zero").returncode, 0)
        path = self.fleet_md("Zero")
        aged = re.sub(r"(Written by `game/fleet/fleetfile.py` at )\d{4}-\d\d-\d\d \d\d:\d\d UTC", r"\g<1>2000-01-01 00:00 UTC", path.read_text())
        self.assertIn("at 2000-01-01 00:00 UTC", aged)
        path.write_text(aged, encoding="ascii")
        before = (path.read_bytes(), path.stat().st_ino, path.stat().st_mtime_ns)
        done = self.run_it("zero")
        self.assertEqual((done.returncode, done.stdout), (0, "Zero: unchanged: %s (5 ships, miner)\n" % path))
        self.assertEqual((path.read_bytes(), path.stat().st_ino, path.stat().st_mtime_ns), before)
        (self.data / "fleet" / "orders" / "miner-1.json").unlink()                                # the ship's run ended: the block changed
        done = self.run_it("zero")
        self.assertIn("Zero: written: ", done.stdout)
        self.assertNotIn("2000-01-01", path.read_text())
        self.assertIn("| miner-1 | miner | Threshold | waits docked |", path.read_text())


class PermissionTests(Tree):
    def test_a_member_writes_its_own_file_only_and_the_fleet_admiral_any(self):
        untouched = {m: self.fleet_md(m).read_bytes() for m in MEMBERS}
        for member, word in (("zero", "Apollo"), ("zero", "all"), ("apollo", "Unity")):
            done = self.run_it(member, word)
            self.assertEqual(done.returncode, 2, done.stdout)
            self.assertTrue(done.stdout.startswith("REFUSED: "), done.stdout)
        for env in ({}, {"FLEET_MEMBER": "dispatch"}):                                            # no member, a service: refused, print free
            for args in ((), ("Zero",)):
                done = self.run_it("", *args, env=env)
                self.assertEqual(done.returncode, 2, done.stdout)
                self.assertTrue(done.stdout.startswith("REFUSED: this shell is no member of The Collective"), done.stdout)     # the refusal names its rule
            done = self.run_it("", "Zero", "--print", env=env)
            self.assertEqual(done.returncode, 0, done.stdout)
            self.assertTrue(done.stdout.startswith(BEGIN))
        done = self.run_it("zero", "Apollo", "--print")
        self.assertEqual(done.returncode, 0)
        self.assertEqual({m: self.fleet_md(m).read_bytes() for m in MEMBERS}, untouched)
        self.assertEqual(self.run_it("zero", "zero").stdout.split(":")[0:2], ["Zero", " written"])
        done = self.run_it("unity", "Mercury")
        self.assertEqual(done.stdout.split(":")[0:2], ["Mercury", " written"])
        done = self.run_it("unity", "all")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual([line.split(":")[0:2] for line in done.stdout.splitlines()],
                         [["Unity", " written"], ["Zero", " unchanged"], ["Apollo", " written"], ["Mercury", " unchanged"], ["Apophis", " written"], ["Oracle", " written"]])
        self.assertIn("Unity: written: %s (1 ships, command)" % self.fleet_md("Unity"), done.stdout)
        self.assertIn("Apophis: written: %s (1 ships, drone, sentinel)" % self.fleet_md("Apophis"), done.stdout)     # lent to Military (D226)


class CommitTests(Tree):
    def test_commit_only_a_clean_file_and_only_in_its_own_repository(self):
        work = self.fleet_md("Zero").parent
        self.git(work, "init", "-q")
        self.git(work, "add", "--", "FLEET.md")
        self.git(work, "-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "start")
        (work / "other.md").write_text("another agent's staged work\n")
        self.git(work, "add", "--", "other.md")
        done = self.run_it("zero", "--commit")
        self.assertEqual(done.returncode, 0, done.stdout)
        head = self.git(work, "log", "-1", "--format=%h").strip()
        self.assertEqual(done.stdout, "Zero: committed %s: %s (5 ships, miner)\n" % (head, self.fleet_md("Zero")))
        self.assertEqual(self.git(work, "log", "-1", "--format=%an <%ae>|%s"), "Zero <zero@suggi-workspace.dev>|FLEET.md: the roster (fleetfile.py)\n")
        self.assertEqual(self.git(work, "show", "--name-only", "--format=", "HEAD").split(), ["FLEET.md"])
        self.assertEqual(self.git(work, "status", "--porcelain"), "A  other.md\n")                # the other file is still staged, not committed
        self.assertEqual(self.run_it("zero", "--commit").stdout.split(":")[0:2], ["Zero", " unchanged"])
        with open(self.fleet_md("Zero"), "a") as handle:                                          # a hand edit not yet committed
            handle.write("\nA note by hand.\n")
        (self.data / "fleet" / "orders" / "miner-1.json").unlink()
        done = self.run_it("zero", "--commit")
        self.assertIn("Zero: written; not committed: FLEET.md carried an uncommitted change before the write", done.stdout)
        self.assertEqual(self.git(work, "log", "-1", "--format=%h").strip(), head)
        self.assertTrue(self.fleet_md("Zero").read_text().endswith("\nA note by hand.\n"))
        self.assertIn("| miner-1 | miner | Threshold | waits docked |", self.fleet_md("Zero").read_text())
        self.git(self.profiles, "init", "-q")                                                     # a parent's repository is not the workspace's
        done = self.run_it("apollo", "--commit")
        self.assertIn("Apollo: written; not committed: no git repository", done.stdout)
        self.assertEqual(self.git(self.profiles, "rev-list", "--all", "--count"), "0\n")             # nothing was committed into the parent

    def test_a_second_run_waits_for_the_first_and_a_print_never_waits(self):
        # the hourly job (Unity, all members) and a member's preflight write and commit the same file
        import fcntl
        with open(self.data / "fleet" / "fleetfile.lock", "w") as held:
            fcntl.flock(held, fcntl.LOCK_EX)                                                      # another run is at work
            done = self.run_it("zero", "--print")
            self.assertEqual((done.returncode, done.stdout.startswith(BEGIN)), (0, True))         # a print writes nothing and asks for no lock
            waiting = self.start_it("zero")
            with self.assertRaises(subprocess.TimeoutExpired):
                waiting.wait(timeout=2.5)
            self.assertNotIn(BEGIN, self.fleet_md("Zero").read_text())                            # nothing written while the other run holds the lock
        out, _err = waiting.communicate(timeout=60)                                               # the lock is free: the run goes through
        self.assertEqual((waiting.returncode, out.split(":")[0:2]), (0, ["Zero", " written"]))
        self.assertIn(BEGIN, self.fleet_md("Zero").read_text())


if __name__ == "__main__":
    unittest.main()
