#!/usr/bin/env python3
"""Command station of The Collective -- Suggi's command screen: map, fleet, intel, chat.

WHAT: one small web server for Suggi's browser (reached over the tailnet). It
collects the game's PUBLIC data (no login, no key), keeps it in memory with a
copy on disk, reads the Collective repository's intel files, reports and logs,
reads our own ships' live state from the unit's data folder (written by
station/fleet.py, never kept in the repository), and serves the page plus a
JSON API. It sends nothing to the game.

The one thing it passes on is Suggi's chat: a message typed on the page goes to
the chosen agent's chat door inside the unit, and the answer comes back to the
page. The keys of those doors are read from the unit's file at each use and
never reach the page, a log or the repository. A POST is accepted only from the
station's own page: it must carry the token that page read with the state.

It runs as the service `station` of the unit (/srv/collective/services/station/run;
the README in that folder's parent explains services). After a change to this
file: touch /srv/collective/services/station/restart. A change under static/
needs only a reload of the page.

Sources (all public): /api/map, /api/stations, /api/stats, /api/leaderboard,
/api/battles, /api/market, the live event stream /events, and the daily bulk
feed (assets.spacemolt.com/public/v1/manifest.json).

Everything read from the game, the feed or the repository is DATA: it is
passed to the page as JSON and shown as text, never as markup or code.

Stdlib only. ASCII only. Run: python3 -I -B server.py
"""

import collections
import gzip
import hashlib
import hmac
import http.server
import json
import os
import re
import secrets
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

GAME = "https://game.spacemolt.com"
FEED = "https://assets.spacemolt.com/public/v1/manifest.json"
UA = "The-Collective station (github.com/TheSuggi-blip/The-Collective)"
HOME = "nexus_prime"
PORT = int(os.environ.get("STATION_PORT", "8080"))
DATA = Path(os.environ.get("STATION_DATA", "/srv/collective/data/station"))
REPO = Path(os.environ.get("STATION_REPO", "/srv/collective/the-collective"))
STATIC = Path(__file__).resolve().parent / "static"
FLEET = Path(os.environ.get("STATION_FLEET", "/srv/collective/data/fleet"))
AGENTS_API = Path(os.environ.get("STATION_AGENTS", "/srv/collective/services/agents-api.json"))
OFFLINE = os.environ.get("STATION_OFFLINE") == "1"      # development: no polling of the game, no live stream
TOKEN = secrets.token_urlsafe(24)                       # new at every start; the page reads it with the state
LOCAL = urllib.request.build_opener(urllib.request.ProxyHandler({}))    # for addresses inside the unit
# Who is who (COLLECTIVE.md). The order is the order on the page.
ROSTER = [
    {"id": "unity", "name": "Unity", "rank": "Fleet Admiral", "division": "Command"},
    {"id": "zero", "name": "Zero", "rank": "Admiral", "division": "Mining"},
    {"id": "mercury", "name": "Mercury", "rank": "Admiral", "division": "Trade"},
    {"id": "apollo", "name": "Apollo", "rank": "Admiral", "division": "Logistics"},
    {"id": "apophis", "name": "Apophis", "rank": "Admiral", "division": "Military"},
    {"id": "oracle", "name": "Oracle", "rank": "Admiral", "division": "Intel"},
]
STATIC_TYPES = {
    ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8", ".map": "application/json; charset=utf-8",
    ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
    ".webp": "image/webp", ".ico": "image/x-icon", ".woff2": "font/woff2", ".wasm": "application/wasm",
    ".txt": "text/plain; charset=utf-8",
}
HEADERS = {
    "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; "
                               "img-src 'self' data:; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
}
PILOT_MAX_AGE = 86400      # a pilot's last jump older than this is dropped
PILOT_CAP = 40000
LOCK = threading.Lock()


def fetch(url, cap=40_000_000, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read(cap + 1)
    if len(data) > cap:
        raise ValueError("response over the size cap")
    return data


def text(v, n=120):
    return str(v)[:n] if isinstance(v, (str, int, float)) and not isinstance(v, bool) else ""


def num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0


# ---------------------------------------------------------------- loaders

def load_map():
    d = json.loads(fetch(GAME + "/api/map"))
    systems = []
    for s in d["systems"]:
        systems.append({
            "id": text(s["id"], 80), "name": text(s.get("name") or s["id"], 80),
            "x": round(float(s["x"]), 1), "y": round(float(s["y"]), 1),
            "empire": text(s.get("empire") or "", 20), "home": bool(s.get("is_home")),
            "stronghold": bool(s.get("is_stronghold")),
            "lanes": [text(c, 80) for c in s.get("connections", [])][:40],
        })
    if len(systems) < 100:
        raise ValueError("map has fewer than 100 systems")
    lanes = {s["id"]: s["lanes"] for s in systems}
    dist, queue = {HOME: 0}, collections.deque([HOME])
    while queue:
        here = queue.popleft()
        for there in lanes.get(here, ()):
            if there in lanes and there not in dist:
                dist[there] = dist[here] + 1
                queue.append(there)
    for s in systems:
        s["jumps"] = dist.get(s["id"], -1)
    empires = {text(k, 20): text(v, 9) for k, v in (d.get("empires") or {}).items()}
    return {"systems": systems, "empires": empires}


def load_stations():
    d = json.loads(fetch(GAME + "/api/stations"))
    out = []
    for s in d.get("stations", [])[:2000]:
        out.append({
            "name": text(s.get("name"), 80), "type": text(s.get("type"), 30), "system": text(s.get("system_id"), 80),
            "tag": text(s.get("faction_tag"), 8), "faction": text(s.get("faction_name"), 60),
            "empire": text(s.get("empire"), 20), "condition": text(s.get("condition"), 30),
            "services": [text(x, 30) for x in (s.get("services") or [])][:30], "wrecked": bool(s.get("wrecked")),
            "mobile": bool(s.get("mobile")),
        })
    return out


def load_stats():
    d = json.loads(fetch(GAME + "/api/stats", cap=100_000))
    return {k: (text(v, 40) if isinstance(v, str) else num(v)) for k, v in d.items() if isinstance(k, str)}


def load_leaderboard():
    d = json.loads(fetch(GAME + "/api/leaderboard"))
    out = {"generated_at": text(d.get("generated_at"), 40), "groups": {}}
    for group in ("players", "factions", "exchange", "stations"):
        cats = {}
        for cat, rows in (d.get(group) or {}).items():
            if isinstance(rows, list):
                cats[text(cat, 40)] = [
                    {"rank": num(r.get("rank")), "name": text(r.get("username") or r.get("name"), 60),
                     "tag": text(r.get("tag") or r.get("empire") or r.get("system_name"), 30), "value": num(r.get("value"))}
                    for r in rows[:10] if isinstance(r, dict)]
        out["groups"][group] = cats
    return out


def load_battles():
    d = json.loads(fetch(GAME + "/api/battles"))
    out = []
    for b in d.get("battles", [])[:40]:
        tags = sorted({text(side.get("faction_tag"), 8) for side in b.get("sides", []) if isinstance(side, dict)} - {""})
        out.append({
            "system": text(b.get("system_id"), 80), "system_name": text(b.get("system_name"), 80),
            "category": text(b.get("category"), 20), "status": text(b.get("status"), 20), "tick": num(b.get("start_tick")),
            "destroyed": num(b.get("ships_destroyed")), "lost": [text(x, 40) for x in (b.get("destroyed_names") or [])][:5],
            "pilots": [text(x, 40) for x in (b.get("player_names") or [])][:8], "tags": tags,
            "ended_at": text(b.get("ended_at"), 30),
        })
    return out


def load_market():
    d = json.loads(fetch(GAME + "/api/market"))
    rows = []
    for i in d.get("items", [])[:20000]:
        rows.append([text(i.get("item_id"), 60), text(i.get("item_name"), 60), text(i.get("category"), 20),
                     text(i.get("empire"), 20), num(i.get("best_bid")), num(i.get("best_ask")),
                     num(i.get("bid_quantity")), num(i.get("ask_quantity"))])
    return rows


def feed_file(manifest, name):
    entry = next(f for f in manifest["files"] if f.get("name") == name)
    url = str(entry["url"])
    if not url.startswith("https://assets.spacemolt.com/public/"):
        raise ValueError("feed file outside the public feed")
    raw = fetch(url)
    if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
        raise ValueError(f"feed file {name}: checksum differs from the manifest")
    return [json.loads(line) for line in gzip.decompress(raw).decode("utf-8").splitlines() if line.strip()]


def tag_of(v):
    if isinstance(v, dict):
        return text(v.get("tag") or v.get("name"), 30)
    return text(v, 30)


def load_feed():
    manifest = json.loads(fetch(FEED, cap=1_000_000))
    factions = {}
    for f in feed_file(manifest, "factions")[:5000]:
        factions[text(f.get("tag"), 8)] = {
            "name": text(f.get("name"), 60), "members": num(f.get("member_count")), "leader": text(f.get("leader"), 40),
            "allies": [tag_of(x) for x in (f.get("allies") or [])][:30], "enemies": [tag_of(x) for x in (f.get("enemies") or [])][:30],
            "wars": [tag_of(x) for x in (f.get("wars") or [])][:30],
        }
    players = {}
    keep = ("ships_destroyed", "ships_lost", "pirates_destroyed", "ore_mined", "credits_earned", "trades_completed",
            "systems_explored", "time_played")
    for p in feed_file(manifest, "players")[:100000]:
        name = text(p.get("username"), 40)
        if name:
            st = p.get("stats") or {}
            players[name.lower()] = {"name": name, "empire": text(p.get("empire"), 20), "faction": tag_of(p.get("faction")),
                                     "created": text(p.get("created_at"), 10), "stats": {k: num(st.get(k)) for k in keep}}
    return {"built_at": text(manifest.get("built_at"), 30), "factions": factions, "players": players}


FEEDS = {  # name: (seconds between runs, loader)
    "map": (3600, load_map), "stations": (900, load_stations), "stats": (60, load_stats),
    "leaderboard": (900, load_leaderboard), "battles": (120, load_battles), "market": (900, load_market),
    "feed": (21600, load_feed),
}
VALUE = {}                       # name -> loaded value
STATUS = {name: {"ok_at": 0, "tried_at": 0, "error": ""} for name in FEEDS}


def save(name, value):
    tmp = DATA / (name + ".json.tmp")
    tmp.write_text(json.dumps(value, separators=(",", ":")), encoding="utf-8")
    os.replace(tmp, DATA / (name + ".json"))


def restore():
    for name in list(FEEDS) + ["pilots"]:
        try:
            path = DATA / (name + ".json")
            value = json.loads(path.read_text(encoding="utf-8"))
            if name == "pilots":
                cutoff = time.time() - PILOT_MAX_AGE
                PILOTS.update({k: v for k, v in value.items() if isinstance(v, list) and len(v) == 4 and v[1] >= cutoff})
            else:
                VALUE[name] = value
                STATUS[name]["ok_at"] = path.stat().st_mtime
        except (OSError, ValueError):
            pass


def poller():
    while True:
        for name, (every, loader) in FEEDS.items():
            st = STATUS[name]
            now = time.time()
            wait = every if not st["error"] else min(every, 300)
            if now - max(st["ok_at"], st["tried_at"] if st["error"] else 0) < wait:
                continue
            st["tried_at"] = now
            try:
                value = loader()
                with LOCK:
                    VALUE[name] = value
                st["ok_at"], st["error"] = time.time(), ""
                save(name, value)
            except Exception as e:           # a failed source keeps its last good value
                st["error"] = (type(e).__name__ + ": " + str(e))[:200]
        time.sleep(5)


# ---------------------------------------------------------------- live stream

PILOTS = {}                                   # name -> [system id, seen (epoch), empire, faction tag]
EVENTS = collections.deque(maxlen=120)        # recent jumps
FILLS = collections.deque(maxlen=80)          # recent exchange fills
STREAM = {"connected": False, "last_event": 0, "events": 0, "error": ""}


def on_event(e):
    kind, d = e.get("type"), e.get("data") or {}
    now = time.time()
    STREAM["last_event"] = now
    STREAM["events"] += 1
    if kind == "jump":
        name, to = text(d.get("player"), 40), text(d.get("to_system"), 80)
        if not name or not to:
            return
        info = (e.get("player_info") or {}).get(d.get("player")) or {}
        row = [to, now, text(info.get("empire"), 20), text(info.get("faction_tag"), 8)]
        with LOCK:
            PILOTS[name] = row
            EVENTS.append({"t": now, "pilot": name, "tag": row[3], "from": text(d.get("from_system"), 80), "to": to})
    elif kind == "exchange_fill":
        with LOCK:
            FILLS.append({"t": now, "item": text(d.get("item_name"), 60), "qty": num(d.get("quantity")),
                          "price": num(d.get("price_each")), "station": text(d.get("station_name"), 60),
                          "system": text(d.get("system_id"), 80), "buyer": text(d.get("buyer"), 40),
                          "seller": text(d.get("seller"), 40)})


def stream():
    delay = 5
    while True:
        try:
            req = urllib.request.Request(GAME + "/events", headers={"User-Agent": UA, "Accept": "text/event-stream"})
            with urllib.request.urlopen(req, timeout=90) as r:
                STREAM["connected"], STREAM["error"] = True, ""
                delay = 5
                for raw in r:
                    if raw.startswith(b"data: ") and len(raw) < 100_000:
                        try:
                            on_event(json.loads(raw[6:]))
                        except (ValueError, AttributeError, TypeError):
                            pass
        except Exception as e:
            STREAM["error"] = (type(e).__name__ + ": " + str(e))[:200]
        STREAM["connected"] = False
        time.sleep(delay)
        delay = min(delay * 2, 60)


def housekeeping():
    while True:
        time.sleep(300)
        cutoff = time.time() - PILOT_MAX_AGE
        with LOCK:
            for name in [k for k, v in PILOTS.items() if v[1] < cutoff]:
                del PILOTS[name]
            if len(PILOTS) > PILOT_CAP:
                for name, _ in sorted(PILOTS.items(), key=lambda kv: kv[1][1])[:len(PILOTS) - PILOT_CAP]:
                    del PILOTS[name]
            snapshot = dict(PILOTS)
        try:
            save("pilots", snapshot)
        except OSError:
            pass


# ---------------------------------------------------------------- repository intel

FILE_NAME = re.compile(r"([anh])-([A-Za-z0-9_.\-]{1,80})\.md")
STANDING = {"a": "ally", "n": "neutral", "h": "hostile"}


def repo_text(rel, cap=300_000):
    """A regular file inside the repository clone, as text. Symlinks and big files are refused."""
    path = REPO / rel
    if path.is_symlink() or not path.is_file() or path.stat().st_size > cap:
        raise OSError("not a plain file under the size cap")
    if REPO.resolve() not in path.resolve().parents:
        raise OSError("outside the repository")
    return path.read_text(encoding="utf-8", errors="replace")


def frontmatter(body):
    out, lines = {}, body.splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:60]:
            if line.strip() == "---":
                break
            key, sep, value = line.partition(":")
            if sep and re.fullmatch(r"[a-z_]{1,30}", key.strip()):
                out[key.strip()] = value.strip()[:120]
    return out


INTEL = {"at": 0.0, "value": {"systems": {}, "pilots": {}}}


def scan_intel():
    """The repository's intel files by system id and pilot name; re-read at most every 30 s."""
    if time.time() - INTEL["at"] < 30:
        return INTEL["value"]
    out = {"systems": {}, "pilots": {}}
    for kind, folder, field in (("systems", "planets", "system_id"), ("pilots", "players", "username")):
        try:
            names = sorted(os.listdir(REPO / folder))[:5000]
        except OSError:
            continue
        for fn in names:
            m = FILE_NAME.fullmatch(fn)
            if not m:
                continue
            try:
                fm = frontmatter(repo_text(f"{folder}/{fn}"))
            except OSError:
                continue
            key = fm.get(field) or m.group(2)
            out[kind][key if kind == "systems" else key.lower()] = {
                "file": f"{folder}/{fn}", "name": key[:80], "standing": STANDING[m.group(1)],
                "threat": fm.get("threat", "unknown")[:20], "updated": fm.get("updated", "")[:10]}
    INTEL["at"], INTEL["value"] = time.time(), out
    return out


def read_json(path, cap=5_000_000):
    """A plain JSON file under the size cap; symlinks are refused."""
    if path.is_symlink() or not path.is_file() or path.stat().st_size > cap:
        raise OSError("not a plain file under the size cap")
    return json.loads(path.read_text(encoding="utf-8"))


def api_fleet():
    """Our ships, from the fleet collector's files in the data folder (station/fleet.py)."""
    path = FLEET / "fleet.json"
    try:
        d = read_json(path)
        age = int(time.time() - path.stat().st_mtime)
    except (OSError, ValueError):
        return {"ships": [], "totals": {}, "engine": {"ok": False, "error": "no fleet data yet"}, "updated_at": "", "age": -1,
                "history": []}
    try:
        history = read_json(FLEET / "history.json")[-288:]
    except (OSError, ValueError, TypeError):
        history = []
    return {"ships": d.get("ships") or [], "totals": d.get("totals") or {}, "engine": d.get("engine") or {},
            "updated_at": text(d.get("updated_at"), 30), "age": age, "history": history}


def api_ship(name):
    fn = re.sub(r"[^A-Za-z0-9_.-]", "_", name)[:60]
    try:
        return read_json(FLEET / "ships" / (fn + ".json"))
    except (OSError, ValueError):
        return {"error": "no such ship"}


DOC_PATH = re.compile(r"(reports|communications|planets|players)/[A-Za-z0-9_.\-]{1,120}\.(md|log)|MAP\.md")
ENTRY = re.compile(r"^## \[(ENT-\d+)\] \| ([^|\n]+) \| ([^|\n]+) \|", re.M)


def api_docs():
    """Reports and logs of the repository: what exists, newest first."""
    reports, logs = [], []
    try:
        names = sorted(os.listdir(REPO / "reports"), reverse=True)[:300]
    except OSError:
        names = []
    for fn in names:
        if not DOC_PATH.fullmatch("reports/" + fn):
            continue
        try:
            fm = frontmatter(repo_text("reports/" + fn))
        except OSError:
            continue
        reports.append({"path": "reports/" + fn, "name": fm.get("name", fn)[:80], "author": fm.get("author", "")[:40],
                        "id": fm.get("id", "")[:20]})
    try:
        names = sorted(os.listdir(REPO / "communications"))[:100]
    except OSError:
        names = []
    for fn in names:
        if not fn.endswith(".log") or not DOC_PATH.fullmatch("communications/" + fn):
            continue
        try:
            entries = ENTRY.findall(repo_text("communications/" + fn, cap=3_000_000))
        except OSError:
            continue
        last = entries[-1] if entries else None
        logs.append({"path": "communications/" + fn, "name": fn, "entries": len(entries),
                     "last": {"ent": last[0], "at": last[1].strip()[:20], "by": last[2].strip()[:30]} if last else None})
    return {"reports": reports, "logs": logs}


def api_doc(rel):
    """One report, log or intel file of the repository, as text. A long log shows its newest part."""
    if not DOC_PATH.fullmatch(rel):
        return {"error": "not a document the station shows"}
    try:
        body = repo_text(rel, cap=3_000_000)
    except OSError:
        return {"error": "not found"}
    part = body[-80_000:] if rel.endswith(".log") else body[:80_000]
    return {"path": rel, "text": part, "cut": len(body) > len(part)}


# ---------------------------------------------------------------- chat with the agents

CHATS = {a["id"]: {"turn": 0, "running": False, "events": [], "started": 0.0} for a in ROSTER}
CHAT_LOCK = threading.Lock()
SESSION_ID = re.compile(r"[A-Za-z0-9_.\-]{1,80}")


def hermes(agent, method, path, body=None, stream=False, timeout=60):
    """A request to one agent's chat door. The key is read here and goes nowhere else."""
    cfg = json.loads(AGENTS_API.read_text(encoding="utf-8"))
    door = cfg["agents"][agent]
    headers = {"Authorization": "Bearer " + str(door["key"])}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if stream:
        headers["Accept"] = "text/event-stream"
    url = str(cfg["base_url"]).rstrip("/") + str(door["prefix"]) + path
    return LOCAL.open(urllib.request.Request(url, data=data, method=method, headers=headers), timeout=timeout)


def chat_sessions():
    try:
        value = json.loads((DATA / "chat.json").read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def chat_session(agent, create=False):
    """The station's conversation with this agent; made on the first message."""
    sessions = chat_sessions()
    sid = sessions.get(agent)
    if isinstance(sid, str) and SESSION_ID.fullmatch(sid):
        return sid
    if not create:
        return None
    with hermes(agent, "POST", "/api/sessions", {"title": "Command station"}) as r:
        sid = text((json.loads(r.read(200_000)).get("session") or {}).get("id"), 80)
    if not SESSION_ID.fullmatch(sid):
        raise ValueError("the agent's door gave no session")
    sessions[agent] = sid
    save("chat", sessions)
    return sid


def chat_turn(agent, sid, message, turn):
    """One turn: send the message, follow the answer stream, keep its events for the page."""
    chat = CHATS[agent]

    def add(kind, **more):
        with CHAT_LOCK:
            if chat["turn"] == turn:
                chat["events"].append(dict(more, n=len(chat["events"]) + 1, kind=kind))

    def on(event, payload):
        try:
            d = json.loads(payload)
        except ValueError:
            return
        if not isinstance(d, dict):
            return
        if event == "assistant.delta":
            add("delta", text=text(d.get("delta"), 20000))
        elif event == "assistant.completed":
            add("final", text=text(d.get("content"), 200000))
        elif event == "assistant.commentary" and not d.get("already_streamed"):
            add("note", text=text(d.get("text"), 4000))
        elif event == "tool.started":
            add("tool", tool=text(d.get("tool") or d.get("tool_name") or d.get("name"), 60), text=text(d.get("preview"), 300))
        elif event in ("tool.completed", "tool.failed"):
            add("tool_done", tool=text(d.get("tool") or d.get("tool_name") or d.get("name"), 60), failed=event == "tool.failed" or bool(d.get("error")))
        elif event in ("run.failed", "run.cancelled"):
            add("error", text=event.split(".")[1] + ": " + text(d.get("error") or d.get("message") or "", 300))

    try:
        with hermes(agent, "POST", f"/api/sessions/{sid}/chat/stream", {"input": message}, stream=True, timeout=1800) as r:
            event, data = "", []
            for raw in r:
                line = raw.decode("utf-8", "replace").rstrip("\r\n")
                if line.startswith("event:"):
                    event = line[6:].strip()
                elif line.startswith("data:"):
                    data.append(line[5:].lstrip())
                elif not line:
                    if data:
                        on(event, "\n".join(data))
                    event, data = "", []
    except Exception as e:
        add("error", text=(type(e).__name__ + ": " + str(e))[:300])
    finally:
        with CHAT_LOCK:
            if chat["turn"] == turn:
                chat["running"] = False
                chat["events"].append({"n": len(chat["events"]) + 1, "kind": "end"})


def chat_send(body):
    agent, message = body.get("agent"), body.get("text")
    if agent not in CHATS or not isinstance(message, str) or not message.strip():
        return 400, {"error": "agent and text are needed"}
    message = message.strip()[:12000]
    chat = CHATS[agent]
    with CHAT_LOCK:
        if chat["running"]:
            return 409, {"error": "still answering the last message"}
        chat["turn"] += 1
        chat["running"], chat["events"], chat["started"] = True, [], time.time()
        turn = chat["turn"]
    try:
        sid = chat_session(agent, create=True)
    except Exception as e:
        with CHAT_LOCK:
            chat["running"] = False
        return 502, {"error": "the agent's chat door did not answer: " + type(e).__name__}
    threading.Thread(target=chat_turn, args=(agent, sid, message, turn), daemon=True).start()
    return 200, {"ok": True, "turn": turn}


def chat_new(body):
    """Forget the conversation with one agent; the next message starts a new one."""
    agent = body.get("agent")
    if agent not in CHATS:
        return 400, {"error": "agent is needed"}
    with CHAT_LOCK:
        if CHATS[agent]["running"]:
            return 409, {"error": "still answering the last message"}
        CHATS[agent]["events"] = []
    sessions = chat_sessions()
    sessions.pop(agent, None)
    save("chat", sessions)
    return 200, {"ok": True}


def api_chat(agent, after):
    """The running or last turn with one agent: its events after number `after`."""
    if agent not in CHATS:
        return {"error": "no such agent"}
    chat = CHATS[agent]
    with CHAT_LOCK:
        events = [e for e in chat["events"] if e["n"] > after]
        return {"agent": agent, "turn": chat["turn"], "running": chat["running"], "events": events,
                "seconds": int(time.time() - chat["started"]) if chat["running"] else 0}


def api_chat_history(agent):
    """What was said so far in the station's conversation with one agent."""
    if agent not in CHATS:
        return {"error": "no such agent"}
    try:
        sid = chat_session(agent)
        if not sid:
            return {"agent": agent, "messages": []}
        with hermes(agent, "GET", f"/api/sessions/{sid}/messages") as r:
            rows = json.loads(r.read(20_000_000)).get("data") or []
    except Exception as e:
        return {"agent": agent, "messages": [], "error": "history not available: " + type(e).__name__}
    out = []
    for m in rows:
        if isinstance(m, dict) and m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str) and m["content"].strip():
            out.append({"role": m["role"], "text": m["content"][:200000], "at": num(m.get("timestamp"))})
    out.sort(key=lambda m: m["at"])
    return {"agent": agent, "messages": out[-200:]}


# ---------------------------------------------------------------- API

def api_state():
    with LOCK:
        m = VALUE.get("map") or {"systems": [], "empires": {}}
        out = {
            "home": HOME, "systems": m["systems"], "empires": m["empires"], "stations": VALUE.get("stations") or [],
            "stats": VALUE.get("stats") or {}, "feed_built_at": (VALUE.get("feed") or {}).get("built_at", ""),
        }
    out["intel"] = scan_intel()
    out["roster"] = ROSTER
    out["token"] = TOKEN
    now = time.time()
    out["sources"] = {n: {"age": int(now - s["ok_at"]) if s["ok_at"] else -1, "error": s["error"]} for n, s in STATUS.items()}
    return out


def api_live():
    now = time.time()
    hour, day = collections.Counter(), collections.Counter()
    with LOCK:
        for system, seen, _, _ in PILOTS.values():
            day[system] += 1
            if now - seen <= 3600:
                hour[system] += 1
        events = [dict(e, t=int(now - e["t"])) for e in list(EVENTS)[-60:]]
        fills = [dict(f, t=int(now - f["t"])) for f in list(FILLS)[-40:]]
        battles = VALUE.get("battles") or []
        stats = VALUE.get("stats") or {}
        pilots = len(PILOTS)
    return {"hour": hour, "day": day, "events": events[::-1], "fills": fills[::-1], "battles": battles, "stats": stats,
            "pilots_tracked": pilots,
            "stream": {"connected": STREAM["connected"], "age": int(now - STREAM["last_event"]) if STREAM["last_event"] else -1,
                       "error": STREAM["error"]}}


def api_system(sid):
    now = time.time()
    with LOCK:
        here = sorted(((n, v) for n, v in PILOTS.items() if v[0] == sid), key=lambda kv: -kv[1][1])
        pilots = [{"name": n, "empire": v[2], "tag": v[3], "age": int(now - v[1])} for n, v in here[:80]]
        battles = [b for b in (VALUE.get("battles") or []) if b["system"] == sid]
        factions = (VALUE.get("feed") or {}).get("factions") or {}
        tags = {s["tag"] for s in (VALUE.get("stations") or []) if s["system"] == sid and s["tag"]}
    intel = scan_intel()["systems"].get(sid)
    body = ""
    if intel:
        try:
            body = repo_text(intel["file"])[:30000]
        except OSError:
            body = ""
    return {"id": sid, "pilots": pilots, "pilot_count": len(here), "battles": battles, "intel": intel, "intel_text": body,
            "factions": {t: factions[t] for t in tags if t in factions}}


def api_pilot(name):
    key = name.lower()
    now = time.time()
    with LOCK:
        hit = next(((n, v) for n, v in PILOTS.items() if n.lower() == key), None)
        profile = ((VALUE.get("feed") or {}).get("players") or {}).get(key)
    intel = scan_intel()["pilots"].get(key)
    return {"name": hit[0] if hit else (profile or {}).get("name", name[:40]),
            "seen": {"system": hit[1][0], "age": int(now - hit[1][1]), "empire": hit[1][2], "tag": hit[1][3]} if hit else None,
            "profile": profile, "intel": intel}


def api_search(q):
    q = q.strip().lower()[:40]
    if len(q) < 2:
        return {"systems": [], "pilots": []}
    with LOCK:
        systems = [{"id": s["id"], "name": s["name"]} for s in (VALUE.get("map") or {}).get("systems", [])
                   if q in s["id"] or q in s["name"].lower()][:12]
        names = {n for n in PILOTS if q in n.lower()}
        names |= {p["name"] for k, p in ((VALUE.get("feed") or {}).get("players") or {}).items() if q in k}
    ranked = sorted(names, key=lambda n: (not n.lower().startswith(q), len(n), n))[:12]
    return {"systems": systems, "pilots": ranked}


def api_market(q):
    q = q.strip().lower()[:40]
    with LOCK:
        rows = VALUE.get("market") or []
    if len(q) < 2:
        return {"rows": [], "items": len({r[0] for r in rows})}
    hits = [r for r in rows if q in r[0] or q in r[1].lower()]
    hits.sort(key=lambda r: (r[1], r[3]))
    return {"rows": hits[:90], "items": len({r[0] for r in rows})}


def static_file(url_path):
    """The file of static/ behind a request path, or None. `/` is index.html; nothing outside static/."""
    rel = "index.html" if url_path == "/" else url_path.lstrip("/")
    path = (STATIC / rel).resolve()
    if STATIC.resolve() not in path.parents or not path.is_file() or path.suffix not in STATIC_TYPES:
        return None
    return path


class Handler(http.server.BaseHTTPRequestHandler):
    server_version, sys_version = "station", ""

    def log_message(self, format, *args):
        pass

    def reply(self, code, body, ctype, head_only=False):
        if len(body) > 2000 and "gzip" in self.headers.get("Accept-Encoding", ""):
            body, encoded = gzip.compress(body, 5), True
        else:
            encoded = False
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if encoded:
            self.send_header("Content-Encoding", "gzip")
        for key, value in HEADERS.items():
            self.send_header(key, value)
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def route(self, head_only):
        url = urllib.parse.urlsplit(self.path)
        query = urllib.parse.parse_qs(url.query, max_num_fields=5)
        arg = (query.get("q") or query.get("id") or query.get("name") or query.get("agent") or [""])[0][:80]
        after = (query.get("after") or ["0"])[0]
        after = int(after) if after.isdigit() and len(after) < 9 else 0
        doc = (query.get("path") or [""])[0][:200]
        try:
            page = None if url.path.startswith("/api/") else static_file(urllib.parse.unquote(url.path))
            if page is not None:
                return self.reply(200, page.read_bytes(), STATIC_TYPES[page.suffix], head_only)
            handlers = {
                "/api/state": api_state, "/api/live": api_live, "/api/system": lambda: api_system(arg),
                "/api/pilot": lambda: api_pilot(arg), "/api/search": lambda: api_search(arg),
                "/api/market": lambda: api_market(arg),
                "/api/leaderboard": lambda: VALUE.get("leaderboard") or {"groups": {}},
                "/api/fleet": api_fleet, "/api/ship": lambda: api_ship(arg),
                "/api/docs": api_docs, "/api/doc": lambda: api_doc(doc),
                "/api/chat": lambda: api_chat(arg, after), "/api/chat/history": lambda: api_chat_history(arg),
                "/healthz": lambda: {"ok": True, "sources": sum(1 for s in STATUS.values() if s["ok_at"])},
            }
            if url.path not in handlers:
                return self.reply(404, b'{"error":"not found"}', "application/json", head_only)
            body = json.dumps(handlers[url.path](), separators=(",", ":")).encode("utf-8")
            return self.reply(200, body, "application/json; charset=utf-8", head_only)
        except Exception as e:
            body = json.dumps({"error": type(e).__name__}).encode("utf-8")
            return self.reply(500, body, "application/json", head_only)

    def own_page(self):
        """True when a POST carries the page's token. Only a page loaded from the station can read
        the token (/api/state), and the extra header keeps other sites' forms and scripts out."""
        if self.headers.get("Sec-Fetch-Site") in ("cross-site", "same-site"):
            return False
        return hmac.compare_digest(self.headers.get("X-Station-Token", ""), TOKEN)

    def do_POST(self):
        handlers = {"/api/chat/send": chat_send, "/api/chat/new": chat_new}
        url = urllib.parse.urlsplit(self.path)
        try:
            length = int(self.headers.get("Content-Length") or "0")
            if url.path not in handlers:
                return self.reply(404, b'{"error":"not found"}', "application/json")
            if not self.own_page() or not self.headers.get("Content-Type", "").startswith("application/json"):
                return self.reply(403, b'{"error":"only the station page may send"}', "application/json")
            if not 0 < length <= 65536:
                return self.reply(413, b'{"error":"message too long"}', "application/json")
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError("not an object")
            code, out = handlers[url.path](body)
            return self.reply(code, json.dumps(out, separators=(",", ":")).encode("utf-8"), "application/json; charset=utf-8")
        except ValueError:
            return self.reply(400, b'{"error":"bad request"}', "application/json")
        except Exception as e:
            return self.reply(500, json.dumps({"error": type(e).__name__}).encode("utf-8"), "application/json")

    def do_GET(self):
        self.route(False)

    def do_HEAD(self):
        self.route(True)


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    restore()
    for target in (() if OFFLINE else (poller, stream, housekeeping)):
        threading.Thread(target=target, daemon=True).start()
    server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.daemon_threads = True
    print(f"station: listening on {PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
