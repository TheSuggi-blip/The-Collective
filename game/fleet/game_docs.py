#!/usr/bin/env python3
"""game_docs.py -- zero-bloat, pull-on-demand live SpaceMolt API & guide discovery for all Collective agents.

WHAT: gives every Admiral and Unity 100% live, version-synced awareness of every SpaceMolt v2 command (320+ actions
      across 20 tool groups), exact API parameter contracts (`help`), and all official career/mechanic guides
      (`guide`) WITHOUT stuffing manuals into agent prompts and WITHOUT holding or interrupting any ship.
      - `overview`: compact summary of all live tool groups (with action counts) and all official guide slugs.
      - `commands [--group <tool>] [--search <kw>] [--limit N]`: search/filter every live SpaceMolt v2 action.
      - `help <tool> [topic]`: fetch exact live official API help (`https://game.spacemolt.com/api/v2/<tool>/help`),
        cached per game version.
      - `guide <slug>`: read any official SpaceMolt guide (`drones`, `base-builder`, `boarding`, `passenger-lines`,
        `crafting`, `packages`, `factions`, `nomad`, `miner`, `trader`, `arbitrage`, `mission-runner`,
        `pirate-hunter`, `explorer`, `taxes`, `fuel`, `client-dev`), cached per game version.
      - `refresh [--force]`: refresh cached command & guide index (auto-triggered on game version bump).

USAGE:
  game_docs.py overview [--data <dir>]
  game_docs.py commands [--group <tool>] [--search <keyword>] [--limit N] [--data <dir>]
  game_docs.py help <tool> [topic] [--data <dir>]
  game_docs.py guide <slug> [--data <dir>]
  game_docs.py refresh [--force] [--data <dir>]

Stdlib only. ASCII only. Read-only against game state (zero ship hold, zero game ticks).
"""

import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division  # noqa: E402

DATA_DEFAULT = division.DATA
API_HELP_BASE = "https://game.spacemolt.com/api/v2"
MAX_HELP_CHARS = 9000
MAX_GUIDE_CHARS = 14000


def _ascii(text):
    return str(text or "").encode("ascii", "replace").decode("ascii")


def _read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = "%s.%d.tmp" % (p, os.getpid())
    with open(tmp, "w", encoding="ascii") as h:
        json.dump(obj, h, indent=1, ensure_ascii=True)
        h.write("\n")
    os.replace(tmp, p)


def live_version(data_dir):
    st = _read_json(Path(data_dir) / "station" / "stats.json", {})
    return str(st.get("version") or "").strip() if isinstance(st, dict) else ""


def cache_dir(data_dir):
    return Path(data_dir) / "catalog" / "game_docs"


def _any_pilot(data_dir):
    fl = _read_json(Path(data_dir) / "fleet" / "fleet.json", {})
    ships = fl.get("ships") if isinstance(fl, dict) else []
    for s in ships or []:
        if isinstance(s, dict) and s.get("name") and s.get("status", "connected") == "connected":
            if s["name"] == "Prime Directive":
                return s["name"]
    for s in ships or []:
        if isinstance(s, dict) and s.get("name") and s.get("status", "connected") == "connected":
            return str(s["name"])
    return "Prime Directive"


def _gate_read(pilot, action, params=None):
    """Read-only spacemolt query through engine gate (get_commands / get_guide: free, zero tick, zero hold)."""
    import gate
    st, ans = gate.call(
        "post",
        "/accounts/%s/raw" % gate.q(pilot),
        {"toolGroup": "spacemolt", "action": action, "params": params or {}},
        timeout=30,
    )
    if st != 200:
        return None, "gate returned HTTP %s: %s" % (st, _ascii(ans)[:160])
    try:
        body = json.loads(ans)
    except ValueError:
        return None, "unreadable JSON from gate"
    if isinstance(body, dict) and body.get("error"):
        return None, _ascii(body.get("error"))[:200]
    return body, ""


def _http_help(tool, topic=""):
    """Public SpaceMolt v2 API help endpoint (no account, no tick, no ship hold)."""
    t = re.sub(r"[^a-zA-Z0-9_]", "", str(tool or "").strip())
    if not t:
        return None, "invalid tool name"
    url = "%s/%s/help" % (API_HELP_BASE, t)
    if topic:
        url += "?topic=" + urllib.parse.quote(str(topic).strip(), safe="")
    req = urllib.request.Request(url, headers={"User-Agent": "the-collective-game-docs/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError) as err:
        return None, "HTTP fetch failed (%s): %s" % (url, _ascii(err)[:160])
    try:
        body = json.loads(raw)
        txt = body.get("result") if isinstance(body, dict) else raw
    except ValueError:
        txt = raw
    return _ascii(txt), ""


def _parse_guides_index(text):
    """Extract [(slug, title, summary)] from get_guide() overview text."""
    out = []
    lines = _ascii(text).splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r"^\s*-\s+([a-z0-9-]+)\s+[^a-zA-Z0-9]+\s*(.+)$", lines[i])
        if m:
            slug, title = m.group(1).strip(), m.group(2).strip()
            summary = ""
            if i + 1 < len(lines) and lines[i + 1].startswith("      "):
                summary = lines[i + 1].strip()
                i += 1
            out.append({"slug": slug, "title": title, "summary": summary[:220]})
        i += 1
    return out


def load_index(data_dir, force=False, gate_fn=None):
    """Load (or refresh when missing/version-changed) the live commands + guides index."""
    cdir = cache_dir(data_dir)
    idx_path = cdir / "index.json"
    ver = live_version(data_dir)
    cached = _read_json(idx_path, {})
    if (not force and isinstance(cached, dict) and cached.get("actions")
            and (not ver or cached.get("version") == ver)):
        return cached, ""

    reader = gate_fn or _gate_read
    pilot = _any_pilot(data_dir)
    body_c, err_c = reader(pilot, "get_commands", {})
    if not body_c:
        if cached and cached.get("actions"):
            return cached, ""
        return {}, "failed to read get_commands: " + err_c
    sc = body_c.get("structuredContent") if isinstance(body_c, dict) else {}
    raw_actions = (sc.get("actions") if isinstance(sc, dict) else None) or []
    actions = []
    for a in raw_actions:
        if isinstance(a, dict) and a.get("tool") and a.get("action"):
            actions.append({
                "tool": _ascii(a["tool"]).strip(),
                "action": _ascii(a["action"]).strip(),
                "description": _ascii(a.get("description") or "").strip()[:220],
            })
    actions.sort(key=lambda x: (x["tool"], x["action"]))

    guides = cached.get("guides") or []
    body_g, _err_g = reader(pilot, "get_guide", {})
    if isinstance(body_g, dict) and body_g.get("result"):
        parsed = _parse_guides_index(body_g["result"])
        if parsed:
            guides = parsed
        m_v = re.search(r"Server version:\s*([0-9.]+)", _ascii(body_g["result"]))
        if m_v and not ver:
            ver = m_v.group(1)

    doc = {
        "version": ver or cached.get("version") or "unknown",
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "action_count": len(actions),
        "actions": actions,
        "guides": guides,
    }
    _write_json(idx_path, doc)
    return doc, ""


def render_overview(data_dir, gate_fn=None):
    idx, err = load_index(data_dir, gate_fn=gate_fn)
    if err:
        return "HALT: " + err
    by_tool = defaultdict(list)
    for a in idx.get("actions") or []:
        by_tool[a["tool"]].append(a["action"])
    lines = [
        "SPACEMOLT LIVE CAPABILITIES | server %s | %d actions across %d tool groups | %d official guides"
        % (idx.get("version") or "?", len(idx.get("actions") or []), len(by_tool), len(idx.get("guides") or [])),
        "",
        "Tool Groups (use view=commands group=<tool> or search=<keyword>, or view=help tool=<tool> topic=<action>):",
    ]
    for t in sorted(by_tool):
        acts = by_tool[t]
        sample = ", ".join(acts[:8]) + (" ..." if len(acts) > 8 else "")
        lines.append("  %-26s (%2d): %s" % (t, len(acts), sample))
    guides = idx.get("guides") or []
    if guides:
        lines.append("")
        lines.append("Official Guides (use view=guide guide=<slug>):")
        for g in guides:
            lines.append("  %-16s -- %s" % (g["slug"], g["title"]))
    return "\n".join(lines)


def render_commands(data_dir, group="", search="", limit=60, gate_fn=None):
    idx, err = load_index(data_dir, gate_fn=gate_fn)
    if err:
        return "HALT: " + err
    g_lo = str(group or "").strip().lower()
    q_lo = str(search or "").strip().lower()
    hits = []
    for a in idx.get("actions") or []:
        if g_lo and g_lo not in a["tool"].lower():
            continue
        if q_lo and q_lo not in (a["tool"] + " " + a["action"] + " " + a["description"]).lower():
            continue
        hits.append(a)
    cap = max(1, min(int(limit or 60), 200))
    lines = [
        "SPACEMOLT COMMANDS | server %s | matches: %d (showing %d)%s%s"
        % (idx.get("version") or "?", len(hits), min(len(hits), cap),
           (" | group=" + g_lo) if g_lo else "", (" | search=" + q_lo) if q_lo else "")
    ]
    for a in hits[:cap]:
        lines.append("  %s.%s -- %s" % (a["tool"], a["action"], a["description"]))
    if len(hits) > cap:
        lines.append("  ... %d more (narrow with group= or search=)" % (len(hits) - cap))
    lines.append("Tip: call game_docs view=help tool=<tool> topic=<action> for exact parameter schema and rules.")
    return "\n".join(lines)


def render_help(data_dir, tool, topic="", http_fn=None):
    t = re.sub(r"[^a-zA-Z0-9_]", "", str(tool or "").strip())
    tp = re.sub(r"[^a-zA-Z0-9_:-]", "", str(topic or "").strip())
    if not t:
        return "REFUSED: tool is required (e.g. tool=spacemolt_facility topic=faction_dismantle)"
    ver = live_version(data_dir) or "unknown"
    hdir = cache_dir(data_dir) / "help"
    key = "%s__%s__%s.txt" % (re.sub(r"[^0-9A-Za-z._-]", "_", ver), t, tp or "_all")
    cpath = hdir / key
    if cpath.is_file():
        txt = cpath.read_text(encoding="ascii", errors="replace")
    else:
        fetcher = http_fn or _http_help
        txt, err = fetcher(t, tp)
        if err or txt is None:
            return "HALT: " + (err or "empty help response")
        hdir.mkdir(parents=True, exist_ok=True)
        cpath.write_text(_ascii(txt), encoding="ascii", errors="replace")
    if len(txt) > MAX_HELP_CHARS:
        txt = txt[:MAX_HELP_CHARS] + "\n... [truncated; pass topic=<action> for one command]"
    return "LIVE API HELP | %s%s (server %s)\n%s" % (t, (" topic=" + tp) if tp else "", ver, txt)


def render_guide(data_dir, slug, gate_fn=None):
    s = re.sub(r"[^a-z0-9-]", "", str(slug or "").strip().lower())
    if not s:
        return "REFUSED: guide slug is required (call view=overview to list all 17 guides)"
    ver = live_version(data_dir) or "unknown"
    gdir = cache_dir(data_dir) / "guides"
    key = "%s__%s.txt" % (re.sub(r"[^0-9A-Za-z._-]", "_", ver), s)
    cpath = gdir / key
    if cpath.is_file():
        txt = cpath.read_text(encoding="ascii", errors="replace")
    else:
        reader = gate_fn or _gate_read
        body, err = reader(_any_pilot(data_dir), "get_guide", {"guide": s})
        if err or not isinstance(body, dict):
            return "HALT: failed to read guide %s: %s" % (s, err)
        txt = _ascii(body.get("result") or json.dumps(body))
        gdir.mkdir(parents=True, exist_ok=True)
        cpath.write_text(txt, encoding="ascii", errors="replace")
    if len(txt) > MAX_GUIDE_CHARS:
        txt = txt[:MAX_GUIDE_CHARS] + "\n... [truncated at %d chars]" % MAX_GUIDE_CHARS
    return "OFFICIAL SPACEMOLT GUIDE | %s (server %s)\n%s" % (s, ver, txt)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Live SpaceMolt API command, help, and guide lookup (zero bloat).")
    sub = ap.add_subparsers(dest="cmd")

    p_ov = sub.add_parser("overview")
    p_ov.add_argument("--data", default=DATA_DEFAULT)

    p_cm = sub.add_parser("commands")
    p_cm.add_argument("--group", default="")
    p_cm.add_argument("--search", default="")
    p_cm.add_argument("--limit", type=int, default=60)
    p_cm.add_argument("--data", default=DATA_DEFAULT)

    p_hp = sub.add_parser("help")
    p_hp.add_argument("tool")
    p_hp.add_argument("topic", nargs="?", default="")
    p_hp.add_argument("--data", default=DATA_DEFAULT)

    p_gd = sub.add_parser("guide")
    p_gd.add_argument("slug")
    p_gd.add_argument("--data", default=DATA_DEFAULT)

    p_rf = sub.add_parser("refresh")
    p_rf.add_argument("--force", action="store_true")
    p_rf.add_argument("--data", default=DATA_DEFAULT)

    args = ap.parse_args(argv)
    cmd = args.cmd or "overview"
    data = getattr(args, "data", DATA_DEFAULT)
    if cmd == "overview":
        print(render_overview(data))
        return 0
    if cmd == "commands":
        print(render_commands(data, group=args.group, search=args.search, limit=args.limit))
        return 0
    if cmd == "help":
        out = render_help(data, args.tool, args.topic)
        print(out)
        return 1 if out.startswith(("HALT:", "REFUSED:")) else 0
    if cmd == "guide":
        out = render_guide(data, args.slug)
        print(out)
        return 1 if out.startswith(("HALT:", "REFUSED:")) else 0
    if cmd == "refresh":
        idx, err = load_index(data, force=args.force)
        if err:
            print("HALT: " + err)
            return 1
        print("game_docs refreshed: server %s | %d actions | %d guides"
              % (idx.get("version"), idx.get("action_count", 0), len(idx.get("guides") or [])))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
