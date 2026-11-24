#!/usr/bin/env python3
"""runhost.py -- one program that flies the runs the dispatcher starts, each run as a thread instead of a process.

WHAT: a runner (mine.py, route_run.py, hunt.py, census.py, guard.py) waits most of its time: for a
      goal, for a mining loop, for a herd. As a process of its own each waiting run holds about
      13 MB; as a thread of this program under 1 MB (measured in the unit's sandbox). The
      dispatcher hands a run over as a job file; this program flies it with the runner's own
      script, read from disk for every run, and nothing in a runner is changed for it.
        data/fleet/host/inbox/<pilot>.json     a run that waits to be taken (written by dispatch.py)
        data/fleet/host/running/<pilot>.json   a run in flight: pilot, what, script, arguments, since when
        data/fleet/host/state.json             alive, accepting, how many runs; rewritten every few seconds
        data/fleet/host/stop/<pilot>           touch it to end that pilot's run (it leaves as a run leaves)
        data/fleet/host/drain                  touch it to let the runs in flight end, take no new one, and
                                               start fresh; meanwhile the dispatcher starts processes
      Which kinds of run are hosted is the dispatcher's: data/fleet/hosting.json (see dispatch.py).
RULES:
  - A run sees what a process of its own would see: its arguments, its log (data/routes/logs/<pilot>.log),
    its own exit list (atexit), its own sys.excepthook, its own environment and a number of its own for
    os.getpid(). os._exit and a signal handler of a run end and catch nothing of the host.
  - A job is flown only when its script is a script of the fleet folder and the pilot's order file names
    that work: the dispatcher writes the order first. A job for a pilot whose last run has not ended is
    not flown, and that old run is told to stop. Two programs never drive one pilot.
  - A run is told to stop at its next sleep: it ends as a runner ends on a signal (guard.py writes its
    row), then its exit list runs.
  - When this program starts it frees the pilots of the runs a dead host left (their order files, when
    they still name that work): the dispatcher gives them work again, and stops an engine loop left behind.
  - A module of the fleet folder that this program has loaded (division.py) and this file itself are
    watched: when one changes on disk the host drains and ends, and the shelf starts it with the new text.
    A runner's script needs none of that: the next run reads it.
  - Above its cap of runs it takes no more; above its cap of memory it drains and starts fresh.
  - Only a service is the host, and only one: a second one ends at once.
  - It sends no command to the game itself: the runs do, through the engine's gate, as before.
WHY:  247 waiting runner processes filled the services' container (4 GB, killed whole on 2026-11-16
      20:50 UTC, every run in flight lost) while together they used a tenth of one core.

USAGE:
  runhost.py              run forever (the service `runhost`)
  --fleet <dir>   the folder of the runners (default: this file's folder)
  --data <dir>    the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import argparse
import atexit                                     # noqa: F401  a run's `import atexit` gets its own face of it
import builtins
import fcntl
import itertools
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path

EVERY = 1                    # seconds between two looks
ALIVE = 30                   # a state file older than this: the host is away
TAKE_BACK = 60               # a job that waited this long in the inbox is the dispatcher's again
MAX_RUNS = 600               # runs in flight at most
MAX_RSS_MB = 2048            # above this the host drains and starts fresh
MAX_RETIRING = 3             # retiring worker generations allowed in flight during drain-free handover
TOTAL_RSS_MB = 2600          # cap total RSS across active + retiring workers before pausing new handovers
DEBOUNCE = 5.0               # seconds watched files stay quiet before requesting a single handover
SCRIPT = re.compile(r"^[a-z][a-z0-9_]*\.py$")
NUMBERS = itertools.count(1000001)   # what a run reads as its process id: its own, and above every real one (files named by os.getpid())
STOPPED = "stopped by the host's stop file"
ENDING = "stopped: the host is ending"


def folder(data):
    """The host's folder in the unit's data folder."""
    return Path(data) / "fleet" / "host"


def job_file(pilot):
    """The file name of a pilot's job, by the fleet collector's rule for a ship's file."""
    return (re.sub(r"[^A-Za-z0-9_.-]", "_", pilot)[:60] or "pilot") + ".json"


def stamp(now=None):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() if now is None else now))


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path, value):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(value), encoding="utf-8")
    os.replace(tmp, path)


# ---- the dispatcher's side ----

def accepting(data, now=None):
    """True while a host is alive and takes runs: its state file is younger than ALIVE seconds and says so."""
    state = read_json(folder(data) / "state.json", {})
    at = state.get("at") if isinstance(state, dict) else None
    now = time.time() if now is None else now
    return bool(isinstance(at, (int, float)) and -ALIVE <= now - at <= ALIVE and state.get("accepting"))


def _pid_alive(pid):
    if not isinstance(pid, int) or pid <= 1:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False


def _proc_rss_mb(pid):
    try:
        with open("/proc/%d/statm" % int(pid), encoding="ascii") as handle:
            return int(handle.read().split()[1]) * os.sysconf("SC_PAGE_SIZE") // (1024 * 1024)
    except (OSError, ValueError, IndexError):
        return 0


def retiring_runs(data):
    """Runs still flying in retiring worker generations during a drain-free handover."""
    home, total = folder(data), 0
    if not home.is_dir():
        return 0
    for path in sorted(home.glob("retiring.*.json")):
        info = read_json(path, {})
        if not isinstance(info, dict):
            continue
        pid = info.get("pid")
        if _pid_alive(pid):
            total += int(info.get("runs") or 0)
    return total


def load(data):
    """Runs the host flies or is about to: active + retiring workers and those waiting in inbox."""
    state = read_json(folder(data) / "state.json", {})
    return int((state.get("runs") if isinstance(state, dict) else 0) or 0) + retiring_runs(data) + waiting(data)


def waiting(data):
    """How many runs wait in the host's inbox."""
    inbox = folder(data) / "inbox"
    return len(list(inbox.glob("*.json"))) if inbox.is_dir() else 0


def submit(data, pilot, what, script, argv, env=None, now=None):
    """Hand one run to the host: a job file in its inbox, written whole (the host never reads half a file). The
    pilot's order file, naming `what`, is written first by the caller."""
    home = folder(data)
    (home / "inbox").mkdir(parents=True, exist_ok=True)
    job = {"pilot": pilot, "what": what, "script": script, "argv": [str(a) for a in argv], "env": dict(env or {}), "at": stamp(now)}
    tmp = home / (job_file(pilot) + ".tmp")
    tmp.write_text(json.dumps(job), encoding="utf-8")
    os.replace(tmp, home / "inbox" / job_file(pilot))


def take_back(data, now=None, after=TAKE_BACK):
    """[job] the host did not take within `after` seconds, each taken out of its inbox: the caller starts them itself.
    A job is taken by a rename, as the host takes it: whoever is first has it, never both."""
    home, out = folder(data), []
    now = time.time() if now is None else now
    for path in sorted((home / "inbox").glob("*.json")) if (home / "inbox").is_dir() else []:
        mine = home / ("back." + path.name)
        try:
            if now - path.stat().st_mtime < after:
                continue
            os.rename(path, mine)
        except OSError:
            continue
        job = read_json(mine, None)
        try:
            mine.unlink()
        except OSError:
            pass
        if isinstance(job, dict) and job.get("pilot") and job.get("script"):
            out.append(job)
    return out


# ---- the host ----

class Facade:
    """A module as one run sees it: its own value where a process of its own would have one, the real module for the rest."""

    def __init__(self, real, **own):
        object.__setattr__(self, "_real", real)
        for name, value in own.items():
            object.__setattr__(self, name, value)

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, "_real"), name)


def guarded(stream, call, *args, **options):
    """Call something of a run's on its way out; what it raises is reported in the run's log and ends nothing else."""
    try:
        call(*args, **options)
    except SystemExit:
        pass
    except BaseException:
        traceback.print_exc(file=stream)


def world(script, job, stream, stop):
    """(the globals the runner's script is run in, its modules, its exit list). A runner is written as a program of
    its own: it reads `sys.argv`, prints, registers with `atexit`, sets `sys.excepthook`, names files by `os.getpid()`,
    puts its folder into `sys.path`. In a thread each of these would be every run's at once, so the script's
    `import sys` (os, time, atexit, signal) gets a module of this run's own. `time.sleep` is where a run is told to
    stop: once, with the SystemExit a runner's own signal handler raises; its sleeps after that are plain sleeps."""
    leaving, told = [], []

    def report(kind, error, trace):
        traceback.print_exception(kind, error, trace, file=stream)

    def register(call, *args, **options):
        leaving.append((call, args, options))
        return call

    def unregister(call):
        leaving[:] = [entry for entry in leaving if entry[0] != call]

    def leave(code=0):
        raise SystemExit(code)

    def nap(seconds):
        if told:
            time.sleep(seconds)
        elif stop.wait(max(float(seconds), 0)):
            told.append(True)
            raise SystemExit(stop.why)

    env = dict(os.environ)
    env.update({str(key): str(value) for key, value in (job.get("env") or {}).items() if str(key).startswith("FLEET_")})
    number = next(NUMBERS)
    mods = {"sys": Facade(sys, argv=[str(script)] + [str(a) for a in job.get("argv") or []], stdout=stream, stderr=stream, excepthook=report,
                          __excepthook__=report, path=list(sys.path)),
            "atexit": Facade(sys.modules["atexit"], register=register, unregister=unregister),
            "signal": Facade(signal, signal=lambda number, handler: signal.SIG_DFL),
            "time": Facade(time, sleep=nap),
            "os": Facade(os, _exit=leave, environ=env, getenv=lambda key, default=None: env.get(key, default), getpid=lambda: number)}

    def importer(module, globals=None, locals=None, fromlist=(), level=0):
        found = builtins.__import__(module, globals, locals, fromlist, level)
        top = module.partition(".")[0]
        return mods[top] if level == 0 and top in mods and (module == top or not fromlist) else found

    def say(*values, **options):
        options.setdefault("file", stream)
        print(*values, **options)

    scope = {"__name__": "__main__", "__file__": str(script), "__builtins__": dict(vars(builtins), __import__=importer, print=say)}
    return scope, mods, leaving


class Stop(threading.Event):
    why = STOPPED


def rss_mb():
    """Megabytes this program holds in memory now; 0 when it cannot be read."""
    try:
        with open("/proc/self/statm", encoding="ascii") as handle:
            return int(handle.read().split()[1]) * os.sysconf("SC_PAGE_SIZE") // (1024 * 1024)
    except (OSError, ValueError, IndexError):
        try:
            import resource
            return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024
        except (ImportError, OSError, ValueError):
            return 0


class Host:
    def __init__(self, fleet, data, say=print, max_runs=MAX_RUNS, max_rss_mb=MAX_RSS_MB, managed=False, debounce=None):
        self.fleet, self.data, self.say = Path(os.path.realpath(fleet)), data, say
        self.max_runs, self.max_rss_mb = max_runs, max_rss_mb
        self.managed = bool(managed)
        if debounce is None:
            self.debounce = float(os.environ.get("FLEET_HOST_DEBOUNCE") or DEBOUNCE) if self.managed else 0.0
        else:
            self.debounce = max(0.0, float(debounce))
        self.folder = folder(data)
        for part in ("inbox", "running", "stop"):
            (self.folder / part).mkdir(parents=True, exist_ok=True)
        (Path(data) / "routes" / "logs").mkdir(parents=True, exist_ok=True)
        if str(self.fleet) not in sys.path:
            sys.path.insert(0, str(self.fleet))          # a runner's `import division` finds it; a run's own sys.path is a copy
        self.runs = {}                   # job file name -> (thread, its stop event, the job)
        self.codes = {}                  # script -> (what its file looked like, its compiled text)
        self.seen = {}                   # watched file -> what it looked like when first seen
        self.pending_change = ("", 0.0)  # (filename, last_changed_epoch) waiting for debounce quiet window
        self.draining = ""               # why the host takes no new run and ends when the last one has ended
        self.retired = False             # managed worker handed over inbox/state to replacement; finishes in-flight runs only
        self.retire_requested = ""       # external retire request from parent (SIGUSR2 after replacement confirmed)
        self.handover_requested = ""     # handover queued with parent; worker keeps accepting until SIGUSR2 arrives
        self.wrote = (None, None, 0.0)   # the state last written: accepting, runs, when
        self.retire_wrote = (None, 0.0)  # retiring marker last written: runs, when
        self.flown = 0

    def request_retire(self, reason="parent handover"):
        if not self.retire_requested:
            self.retire_requested = reason

    def _running_elsewhere(self, run_path):
        info = read_json(run_path, None)
        if not isinstance(info, dict):
            return False
        pid = info.get("pid")
        return bool(isinstance(pid, int) and pid != os.getpid() and _pid_alive(pid))

    # -- what the host looks at --

    def order_names(self, job):
        """True when the pilot's order file names the job's work."""
        order = read_json(Path(self.data) / "fleet" / "orders" / (str(job.get("pilot")) + ".json"), {})
        return isinstance(order, dict) and bool(job.get("what")) and order.get("what") == job.get("what")

    def changed(self, now=None):
        """The name of a watched file that changed on disk once quiet for `self.debounce` seconds, or ''."""
        ts = time.time() if now is None else float(now)
        watched = {os.path.realpath(__file__)}
        prefix = str(self.fleet) + os.sep
        for module in list(sys.modules.values()):
            path = getattr(module, "__file__", None)
            if isinstance(path, str) and path.startswith(prefix) and os.sep not in path[len(prefix):]:
                watched.add(path)
        changed_name = ""
        for path in sorted(watched):
            try:
                found = os.stat(path)
                sig = (found.st_mtime_ns, found.st_size)
            except OSError:
                sig = None
            prev = self.seen.setdefault(path, sig)
            if prev != sig:
                self.seen[path] = sig
                if not changed_name:
                    changed_name = os.path.basename(path)
        if changed_name:
            if self.debounce <= 0.0:
                self.pending_change = ("", 0.0)
                return changed_name
            self.pending_change = (changed_name, ts)
            return ""
        if self.pending_change[0] and (ts - self.pending_change[1]) >= self.debounce:
            ready = self.pending_change[0]
            self.pending_change = ("", 0.0)
            return ready
        return ""

    def code(self, script):
        """The runner's script compiled, read again when its file changed."""
        path = self.fleet / script
        found = path.stat()
        looked = (found.st_mtime_ns, found.st_size)
        if self.codes.get(script, (None, None))[0] != looked:
            self.codes[script] = (looked, compile(path.read_text(encoding="utf-8"), str(path), "exec"))
        return self.codes[script][1]

    # -- one look --

    def recover(self, skip_live=False):
        """Free the pilots of the runs a dead host left in `running/`; returns one line per run."""
        lines = []
        for path in sorted((self.folder / "running").glob("*.json")):
            job = read_json(path, {})
            if skip_live and isinstance(job, dict):
                pid = job.get("pid")
                if isinstance(pid, int) and pid != os.getpid() and _pid_alive(pid):
                    continue
            pilot = str(job.get("pilot") or path.stem) if isinstance(job, dict) else path.stem
            freed = False
            if isinstance(job, dict) and self.order_names(job):
                try:
                    (Path(self.data) / "fleet" / "orders" / (pilot + ".json")).unlink()
                    freed = True
                except OSError:
                    pass
            lines.append("%s: its run `%s` died with the host before this one%s" % (
                pilot, job.get("what") if isinstance(job, dict) else "?", ": the pilot is free again" if freed else "; its order file is another's or gone"))
            try:
                path.unlink()
            except OSError:
                pass
        return lines

    def refuse(self, job, path, why):
        self.say("%s: `%s` not flown: %s" % (job.get("pilot") if isinstance(job, dict) else path.stem, job.get("what") if isinstance(job, dict) else "?", why))
        try:
            path.unlink()
        except OSError:
            pass

    def take(self, path):
        """One job of the inbox: flown, or refused and removed."""
        job = read_json(path, None)
        if not isinstance(job, dict):
            return self.refuse({}, path, "the job file is no JSON object")
        pilot, script = str(job.get("pilot") or ""), str(job.get("script") or "")
        if not pilot or "/" in pilot or pilot in (".", "..") or job_file(pilot) != path.name:
            return self.refuse(job, path, "the job names no pilot of its file")
        if not SCRIPT.match(script) or not (self.fleet / script).is_file():
            return self.refuse(job, path, "`%s` is no script of the fleet folder" % script)
        run_marker = self.folder / "running" / path.name
        if path.name in self.runs:
            self.runs[path.name][1].set()                # that run kept its order file stale for the dispatcher to give new work: it is stuck
            return self.refuse(job, path, "the pilot's last run has not ended; it is told to stop")
        if run_marker.exists() and self._running_elsewhere(run_marker):
            try:
                (self.folder / "stop" / pilot).write_text("", encoding="ascii")
            except OSError:
                pass
            return self.refuse(job, path, "the pilot's last run has not ended in a retiring host; it is told to stop")
        if not self.order_names(job):
            return self.refuse(job, path, "the pilot's order file does not name this work")
        try:
            code = self.code(script)
        except (OSError, SyntaxError, ValueError) as error:
            return self.refuse(job, path, "%s does not compile: %s" % (script, " ".join(str(error).split())[:120]))
        job["since"] = stamp()
        job["pid"] = os.getpid()
        try:
            write_json(self.folder / "running" / path.name, job)
            path.unlink()
        except OSError as error:
            return self.refuse(job, path, "the job could not be moved: %s" % error)
        stop = Stop()
        thread = threading.Thread(target=self.fly, args=(job, path.name, code, stop), name="run " + pilot, daemon=True)
        self.runs[path.name] = (thread, stop, job)
        self.flown += 1
        thread.start()

    def _retire_path(self):
        return self.folder / ("retiring.%d.json" % os.getpid())

    def _write_retiring(self, now):
        if len(self.runs) == self.retire_wrote[0] and 0 <= now - self.retire_wrote[1] < 5:
            return
        try:
            write_json(self._retire_path(), {"pid": os.getpid(), "runs": len(self.runs), "memory_mb": rss_mb(),
                                             "reason": self.draining, "at": now, "updated_at": stamp(now)})
            self.retire_wrote = (len(self.runs), now)
        except OSError:
            pass

    def step(self, now=None):
        """One look. False when the host has drained and must end, so that the shelf starts it fresh."""
        now = time.time() if now is None else now
        for name in [n for n, run in self.runs.items() if not run[0].is_alive()]:
            del self.runs[name]
        for path in sorted((self.folder / "stop").iterdir()):
            jname = job_file(path.name)
            run = self.runs.get(jname)
            if run:
                run[1].set()
                self.say("%s: its run `%s` is told to stop (stop file)" % (path.name, run[2].get("what")))
                try:
                    path.unlink()
                except OSError:
                    pass
            elif not self.retired:
                # Leave stop files belonging to a live retiring worker untouched so that worker handles them.
                rm = self.folder / "running" / jname
                owned_elsewhere = rm.exists() and self._running_elsewhere(rm)
                try:
                    stale_stop = (now - path.stat().st_mtime) > 15
                except OSError:
                    stale_stop = False
                if not owned_elsewhere or stale_stop:
                    try:
                        path.unlink()
                    except OSError:
                        pass
        if not self.draining:
            if self.retire_requested:
                self.draining = self.handover_requested or self.retire_requested
                self.handover_requested = ""
                if self.managed:
                    self.retired = True
                    self.say("retiring for drain-free handover (%s): %d run(s) finish cleanly while replacement accepts" % (self.draining, len(self.runs)))
                else:
                    self.say("draining (%s): %d run(s) in flight end first, no new run is taken" % (self.draining, len(self.runs)))
            else:
                want = ""
                found = self.changed(now)
                if found:
                    want = "%s changed on disk" % found
                elif (self.folder / "drain").exists():
                    want = "the drain file"
                elif self.max_rss_mb and rss_mb() > self.max_rss_mb:
                    want = "memory above %d MB" % self.max_rss_mb
                if want:
                    if self.managed:
                        if not self.handover_requested or not (self.folder / "handover.json").exists():
                            self.handover_requested = want
                            try:
                                write_json(self.folder / "handover.json", {"pid": os.getpid(), "reason": want, "at": now})
                            except OSError:
                                pass
                            self.say("requesting drain-free handover (%s): continuing to accept until replacement is confirmed" % want)
                    else:
                        self.draining = want
                        self.say("draining (%s): %d run(s) in flight end first, no new run is taken" % (self.draining, len(self.runs)))
        if self.draining and not self.runs:
            if self.retired:
                try:
                    self._retire_path().unlink()
                except OSError:
                    pass
                self.say("retired worker ended cleanly: %s" % self.draining)
                return False
            try:
                (self.folder / "drain").unlink()
            except OSError:
                pass
            self.write_state(now, False)
            self.say("ending for a fresh start: %s" % self.draining)
            return False
        if self.retired:
            self._write_retiring(now)
            return True
        if not self.draining:
            used_other = retiring_runs(self.data) if self.managed else 0
            for path in sorted((self.folder / "inbox").glob("*.json")):
                if len(self.runs) + used_other >= self.max_runs:
                    break
                self.take(path)
        used_other = retiring_runs(self.data) if self.managed else 0
        self.write_state(now, not self.draining and (len(self.runs) + used_other) < self.max_runs)
        return True

    def write_state(self, now, accepting_now):
        if (accepting_now, len(self.runs)) == self.wrote[:2] and 0 <= now - self.wrote[2] < 5:
            return
        try:
            write_json(self.folder / "state.json", {"updated_at": stamp(now), "at": now, "accepting": accepting_now, "runs": len(self.runs),
                                                    "flown": self.flown, "draining": self.draining, "memory_mb": rss_mb(), "pid": os.getpid()})
            self.wrote = (accepting_now, len(self.runs), now)
        except OSError:
            pass

    def close(self, grace=8.0):
        """The host is ending now: every run is told to stop and given `grace` seconds to leave as a run leaves."""
        for _thread, stop, _job in self.runs.values():
            stop.why = ENDING
            stop.set()
        limit = time.time() + grace
        while time.time() < limit and any(run[0].is_alive() for run in self.runs.values()):
            time.sleep(0.05)
        left = sorted(str(run[2].get("pilot")) for run in self.runs.values() if run[0].is_alive())
        if self.retired:
            try:
                self._retire_path().unlink()
            except OSError:
                pass
        else:
            self.write_state(time.time() + 6, False)
        return left

    # -- one run --

    def fly(self, job, name, code, stop):
        """One run, start to end, in its own thread: the runner's script with this run's arguments and log, ended the
        way Python ends a process: an exception goes to the run's `sys.excepthook`, a `sys.exit` with a text prints
        it, then what the run gave `atexit` is called, the last registered first."""
        try:
            with open(Path(self.data) / "routes" / "logs" / (str(job["pilot"]) + ".log"), "w", encoding="utf-8", buffering=1) as stream:
                scope, mods, leaving = world(self.fleet / job["script"], job, stream, stop)
                try:
                    exec(code, scope)
                except SystemExit as leave:
                    if leave.code is not None and not isinstance(leave.code, int):
                        print(leave.code, file=stream)
                except BaseException as error:
                    guarded(stream, mods["sys"].excepthook, type(error), error, error.__traceback__)
                for call, args, options in reversed(leaving):
                    guarded(stream, call, *args, **options)
                del leaving[:]
                scope.clear()                            # the run's functions hold its globals and they hold the functions: let go now
        except BaseException as error:                   # the host's own fault must not leave the run listed as flying
            self.say("%s: its run ended on the host's fault: %s: %s" % (job.get("pilot"), type(error).__name__, " ".join(str(error).split())[:160]))
        finally:
            try:
                rm = self.folder / "running" / name
                info = read_json(rm, {})
                if not isinstance(info, dict) or info.get("pid") in (None, os.getpid()):
                    rm.unlink()
            except OSError:
                pass


def _run_worker(args, say):
    host = Host(args.fleet, args.data, say=say, max_runs=int(os.environ.get("FLEET_HOST_MAX_RUNS") or MAX_RUNS),
                max_rss_mb=int(os.environ.get("FLEET_HOST_MAX_MB") or MAX_RSS_MB), managed=True)
    for line in host.recover(skip_live=True):
        say(line)
    leaving = []
    signal.signal(signal.SIGTERM, lambda number, frame: leaving.append(number))
    if hasattr(signal, "SIGUSR2"):
        signal.signal(signal.SIGUSR2, lambda number, frame: host.request_retire("parent handover"))
    try:
        import faulthandler
        faulthandler.register(signal.SIGUSR1, file=sys.stderr, all_threads=True)
    except (ImportError, AttributeError, ValueError, OSError):
        pass
    say("worker %d started: at most %d runs, %d MB" % (os.getpid(), host.max_runs, host.max_rss_mb))
    while host.step():
        if leaving:
            left = host.close()
            say("worker %d stopped by a signal: %d run(s) were told to stop%s" % (
                os.getpid(), len(host.runs), ("; not out in time: " + ", ".join(left)) if left else ""))
            return 0
        time.sleep(float(os.environ.get("FLEET_HOST_EVERY") or EVERY))
    return 0


def _file_sig(path):
    try:
        st = os.stat(path)
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return None


def _run_parent(args, say):
    home = folder(args.data)
    for part in ("inbox", "running", "stop"):
        (home / part).mkdir(parents=True, exist_ok=True)
    lock = open(home / "lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        sys.exit("another host flies the runs: this one ends")
    for stale in list(home.glob("retiring.*.json")) + [home / "handover.json"]:
        try:
            stale.unlink()
        except OSError:
            pass
    for line in Host(args.fleet, args.data, say=say).recover(skip_live=True):
        say(line)
    leaving = []
    signal.signal(signal.SIGTERM, lambda number, frame: leaving.append(number))
    script = os.path.realpath(__file__)
    script_sig = _file_sig(script)
    script_changed_at = 0.0
    debounce = max(0.0, float(os.environ.get("FLEET_HOST_DEBOUNCE") or DEBOUNCE))
    max_retiring = int(os.environ.get("FLEET_HOST_MAX_RETIRING") or MAX_RETIRING)
    total_rss_cap = int(os.environ.get("FLEET_HOST_TOTAL_MB") or TOTAL_RSS_MB)
    cmd = [sys.executable, "-I", "-B", script, "--worker", "--fleet", args.fleet, "--data", args.data]

    def spawn_worker():
        return subprocess.Popen(cmd, env=dict(os.environ))

    active = spawn_worker()
    retiring = []
    say("host supervisor started (drain-free handover enabled, active worker pid %d)" % active.pid)
    try:
        while not leaving:
            still = []
            for proc in retiring:
                if proc.poll() is not None:
                    try:
                        (home / ("retiring.%d.json" % proc.pid)).unlink()
                    except OSError:
                        pass
                else:
                    still.append(proc)
            retiring = still

            if active.poll() is not None:
                rc = active.returncode
                try:
                    (home / "handover.json").unlink()
                except OSError:
                    pass
                for line in Host(args.fleet, args.data, say=say).recover(skip_live=True):
                    say(line)
                if leaving:
                    break
                time.sleep(0.5 if rc == 0 else 1.5)
                active = spawn_worker()
                say("active worker restarted (previous exit %s -> pid %d)" % (rc, active.pid))
                continue

            reason = ""
            ho_path = home / "handover.json"
            ho = read_json(ho_path, None) if ho_path.exists() else None
            if isinstance(ho, dict) and ho.get("pid") == active.pid:
                reason = str(ho.get("reason") or "module changed")
            elif (home / "drain").exists():
                reason = "the drain file"
            else:
                now_sig = _file_sig(script)
                if now_sig != script_sig:
                    script_sig = now_sig
                    script_changed_at = time.time()
                if script_changed_at and (time.time() - script_changed_at) >= debounce:
                    script_changed_at = 0.0
                    reason = "runhost.py changed on disk"

            if reason:
                total_rss = sum(_proc_rss_mb(p.pid) for p in [active] + retiring)
                if len(retiring) < max_retiring and (not total_rss_cap or total_rss < total_rss_cap):
                    for f in (ho_path, home / "drain"):
                        try:
                            f.unlink()
                        except OSError:
                            pass
                    if hasattr(signal, "SIGUSR2"):
                        try:
                            active.send_signal(signal.SIGUSR2)
                        except OSError:
                            pass
                    old_pid = active.pid
                    retiring.append(active)
                    active = spawn_worker()
                    say("drain-free handover (%s): worker %d retiring (%d retiring total), new worker %d accepting immediately" % (
                        reason, old_pid, len(retiring), active.pid))
            time.sleep(min(0.5, float(os.environ.get("FLEET_HOST_EVERY") or EVERY)))
    finally:
        procs = [p for p in [active] + retiring if p is not None and p.poll() is None]
        for p in procs:
            try:
                p.terminate()
            except OSError:
                pass
        limit = time.time() + 12.0
        while time.time() < limit and any(p.poll() is None for p in procs):
            time.sleep(0.1)
        for p in procs:
            if p.poll() is None:
                try:
                    p.kill()
                except OSError:
                    pass
                p.wait()
        for stale in list(home.glob("retiring.*.json")) + [home / "handover.json"]:
            try:
                stale.unlink()
            except OSError:
                pass
        say("host supervisor stopped cleanly")
    return 0


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Fly the runs the dispatcher hands over, each as a thread.")
    parser.add_argument("--fleet", default=str(here))
    parser.add_argument("--data", default="/srv/collective/data")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    sys.path.insert(0, str(here))
    import division                               # who is asking
    kind, _name = division.member()
    if kind != "service":
        sys.exit("REFUSED: the host is a service (the shelf's `runhost`), never a member's shell: a second host would free the pilots of the first one's runs.")

    def say(text):
        print(stamp(), text, flush=True)

    if args.worker:
        return _run_worker(args, say)
    return _run_parent(args, say)


if __name__ == "__main__":
    sys.exit(main())
