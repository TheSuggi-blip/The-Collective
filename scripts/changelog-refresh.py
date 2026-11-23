#!/usr/bin/env python3
"""changelog-refresh.py -- keep SpaceMolt patch notes in data/catalog/releases.json (and 15-patch-notes.md) current.

WHAT: SpaceMolt publishes an official RSS 2.0 release feed at
      https://spacemolt.com/changelog/rss.xml alongside its running version at
      https://game.spacemolt.com/api/stats (also cached every 60s by station in
      <data>/station/stats.json). This script keeps <data>/catalog/releases.json
      current so store.py mirrors every release into read.db (table
      game_releases) and craftbook.py / collective_mcp.py answer `releases`
      automatically within minutes of any game update.

USAGE:
  changelog-refresh.py check                    compare our newest release vs live game version
  changelog-refresh.py refresh [--commit]       fetch RSS when new (or missing), write releases.json, optionally update 15-patch-notes.md
  changelog-refresh.py show [--top N]           print the newest N releases on disk (default 5)
  --data <dir>     the unit's data folder (default /srv/collective/data)
  --root <dir>     repository root (default: parent of scripts/)
  --rss-url <url>  RSS feed URL (default https://spacemolt.com/changelog/rss.xml)

Stdlib only. Pure 7-bit ASCII. All external feed text is stripped of HTML and treated strictly as untrusted DATA.
"""

import argparse
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

RSS_URL = "https://spacemolt.com/changelog/rss.xml"
STATS_URL = "https://game.spacemolt.com/api/stats"
DATA = "/srv/collective/data"
AGENT = "the-collective-catalog-refresh"
VER_RE = re.compile(r"(\d+(?:\.\d+)+)")
LI_RE = re.compile(r"<li[^>]*>(.*?)</li>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")


def clean_ascii(text):
    """Strip HTML tags, unescape entities, and normalize to single-line 7-bit ASCII."""
    raw = html.unescape(TAG_RE.sub(" ", str(text or "")))
    repl = (raw.replace("\u2014", "--").replace("\u2013", "-").replace("\u2018", "'")
               .replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
               .replace("\u2192", "->").replace("\u00a0", " "))
    collapsed = " ".join(repl.split())
    return collapsed.encode("ascii", "replace").decode("ascii")


def sort_key(ver):
    """Zero-padded version key so SQL ORDER BY sort_key DESC sorts 0.732.10 > 0.732.3."""
    parts = [int(x) for x in ver.split(".") if x.isdigit()]
    return ".".join("%05d" % p for p in parts)


def parse_rss(xml_bytes):
    """Parse RSS 2.0 XML bytes into a list of clean release dicts, newest version first."""
    root = ET.fromstring(xml_bytes)
    items = []
    seen = set()
    for item in root.findall("./channel/item"):
        title = clean_ascii(item.findtext("title") or "")
        guid = clean_ascii(item.findtext("guid") or "")
        m = VER_RE.search(title) or VER_RE.search(guid)
        if not m:
            continue
        ver = m.group(1)
        if ver in seen:
            continue
        seen.add(ver)
        pub = clean_ascii(item.findtext("pubDate") or "")
        desc_raw = item.findtext("description") or ""
        desc_unescaped = html.unescape(desc_raw)
        bullets = [clean_ascii(b) for b in LI_RE.findall(desc_unescaped)]
        bullets = [b for b in bullets if b]
        if not bullets:
            fallback = clean_ascii(desc_unescaped)
            if fallback:
                bullets = [fallback]
        summary = "; ".join(bullets)
        items.append({
            "version": ver,
            "sort_key": sort_key(ver),
            "pub_date": pub,
            "bullets": bullets,
            "summary": summary[:2000],
        })
    items.sort(key=lambda r: tuple(int(x) for x in r["version"].split(".")), reverse=True)
    return items


def live_version(data, stats_url=STATS_URL):
    """Read live version cheaply from <data>/station/stats.json if fresh (<5m), else /api/stats."""
    st_file = Path(data) / "station" / "stats.json"
    try:
        if st_file.is_file() and (time.time() - st_file.stat().st_mtime) < 300:
            d = json.loads(st_file.read_text(encoding="utf-8"))
            v = str(d.get("version") or "").strip()
            if VER_RE.fullmatch(v):
                return v
    except (OSError, ValueError, TypeError):
        pass
    req = urllib.request.Request(stats_url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read().decode("utf-8", "replace"))
        return str(d.get("version") or "").strip()


def load_releases(data):
    path = Path(data) / "catalog" / "releases.json"
    if not path.is_file():
        return []
    try:
        obj = json.loads(path.read_text(encoding="ascii"))
        return obj.get("releases", []) if isinstance(obj, dict) else []
    except (OSError, ValueError, TypeError):
        return []


def update_patch_notes_md(repo_root, releases):
    """Insert any newer release rows at the top of game/rules/15-patch-notes.md table when clean."""
    md_path = Path(repo_root) / "game" / "rules" / "15-patch-notes.md"
    if not md_path.is_file() or not releases:
        return []
    text = md_path.read_text(encoding="ascii")
    existing = set(re.findall(r"^\|\s*(\d+(?:\.\d+)+)\s*\|", text, flags=re.M))
    if not existing:
        return []
    max_existing = max(existing, key=lambda v: tuple(int(x) for x in v.split(".")))
    max_tuple = tuple(int(x) for x in max_existing.split("."))
    missing = [r for r in releases if tuple(int(x) for x in r["version"].split(".")) > max_tuple and r["version"] not in existing]
    if not missing:
        return []
    marker = "| Version | Change |\n|---|---|\n"
    if marker not in text:
        return []
    new_rows = []
    for r in missing:
        cell = clean_ascii(" ".join(r["bullets"])).replace("|", "/")
        new_rows.append("| %s | %s |" % (r["version"], cell))
    updated = text.replace(marker, marker + "\n".join(new_rows) + "\n", 1)
    today = time.strftime("%Y-%m-%d", time.gmtime())
    updated = re.sub(r"# Rules 15 -- Patch Notes \(read [0-9-]+\)", "# Rules 15 -- Patch Notes (read %s)" % today, updated, count=1)
    md_path.write_text(updated, encoding="ascii")
    return [r["version"] for r in missing]


def sync_md(args, releases):
    """game/rules/15-patch-notes.md brought to the releases given and committed by path as Unity, when the file stands
    clean in the clone; the list of versions added (none when current or when another hand's change is in it)."""
    dirty = subprocess.run(["git", "-C", args.root, "status", "--porcelain", "--", "game/rules/15-patch-notes.md"], capture_output=True, text=True)
    if dirty.returncode != 0 or dirty.stdout.strip() or not releases:
        return []
    patched = update_patch_notes_md(args.root, releases)
    if patched:
        subprocess.run(["git", "-C", args.root, "add", "--", "game/rules/15-patch-notes.md"], check=False)
        subprocess.run([
            "git", "-C", args.root, "-c", "user.name=Unity", "-c", "user.email=unity@suggi-workspace.dev",
            "commit", "-q", "-m", "rules: auto-sync patch notes %s from changelog RSS" % (", ".join(patched)),
            "--", "game/rules/15-patch-notes.md"
        ], check=False)
    return patched


def cmd_refresh(args):
    folder = Path(args.data) / "catalog"
    folder.mkdir(parents=True, exist_ok=True)
    state_path = folder / "releases-state.json"
    rel_path = folder / "releases.json"
    state = {}
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="ascii"))
        except (OSError, ValueError):
            state = {}
    headers = {"User-Agent": AGENT}
    if state.get("etag") and rel_path.is_file():
        headers["If-None-Match"] = state["etag"]
    req = urllib.request.Request(args.rss_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            xml_bytes = resp.read(4_000_000)
            etag = resp.headers.get("ETag") or ""
    except urllib.error.HTTPError as e:
        if e.code == 304:                       # the feed did not change: the notes may still lag the releases on disk
            if args.commit:                     # (an hour whose commit failed was never tried again: requests ENT-382)
                sync_md(args, load_releases(args.data))
            return 0
        print("changelog-refresh: HTTP %s from %s" % (e.code, args.rss_url))
        return 1
    except OSError as e:
        print("changelog-refresh: fetch failed: %s" % e)
        return 1
    try:
        releases = parse_rss(xml_bytes)
    except ET.ParseError as e:
        print("changelog-refresh: bad XML: %s" % e)
        return 1
    if not releases:
        print("changelog-refresh: RSS contained zero releases")
        return 1
    before = {r["version"] for r in load_releases(args.data)}
    payload = {
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "latest": releases[0]["version"],
        "count": len(releases),
        "releases": releases,
    }
    tmp = folder / ".releases.json.tmp"
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="ascii")
    os.replace(tmp, rel_path)
    state_tmp = folder / ".releases-state.json.tmp"
    state_tmp.write_text(json.dumps({"etag": etag, "latest": releases[0]["version"], "checked_at": payload["updated_at"]}, ensure_ascii=True) + "\n", encoding="ascii")
    os.replace(state_tmp, state_path)
    added = [r["version"] for r in releases if r["version"] not in before]
    if args.commit:
        sync_md(args, releases)
    if added:
        print("changelog-refresh: synced %d release(s), newest %s (added: %s)" % (len(releases), releases[0]["version"], ", ".join(added[:8])))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sync SpaceMolt RSS patch notes into data/catalog/releases.json")
    ap.add_argument("verb", choices=("check", "refresh", "show"))
    ap.add_argument("--data", default=DATA)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--rss-url", default=RSS_URL)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args(argv)
    if args.verb == "check":
        rels = load_releases(args.data)
        ours = rels[0]["version"] if rels else "none"
        try:
            live = live_version(args.data)
        except OSError:
            live = "unreachable"
        print("ours: %s | live: %s | %s" % (ours, live, "same" if ours == live else "differ"))
        return 0
    if args.verb == "show":
        rels = load_releases(args.data)[:max(1, args.top)]
        if not rels:
            print("no releases in %s/catalog/releases.json" % args.data)
            return 0
        for r in rels:
            print("v%s (%s)" % (r["version"], r.get("pub_date") or ""))
            for b in r.get("bullets") or []:
                print("  - %s" % b)
        return 0
    return cmd_refresh(args)


if __name__ == "__main__":
    sys.exit(main())
