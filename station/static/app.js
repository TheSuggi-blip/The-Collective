'use strict';
// Command station page. Everything from the server is data: it is written with textContent only.

const $ = (id) => document.getElementById(id);
function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined && text !== null) e.textContent = String(text);
  return e;
}
async function get(path) {
  const r = await fetch(path, { cache: 'no-store' });
  if (!r.ok) throw new Error(path + ' -> ' + r.status);
  return r.json();
}
const fmt = (n) => Number(n || 0).toLocaleString('en-US');
function ago(s) {
  if (s < 0) return 'never';
  if (s < 90) return s + ' s';
  if (s < 5400) return Math.round(s / 60) + ' min';
  if (s < 129600) return Math.round(s / 3600) + ' h';
  return Math.round(s / 86400) + ' d';
}
const HEX = /^#[0-9a-fA-F]{6}$/;
const LAWLESS = '#59607a';

let S = null;                                  // /api/state
let L = { hour: {}, day: {}, events: [], fills: [], battles: [], stats: {}, stream: {} };
let board = null;
const sys = new Map();
const stationsBy = new Map();
const fleetBy = new Map();
const layers = { Lanes: true, Traffic: true, Stations: true, Strongholds: true, Intel: true, Fleet: true, Names: true };
const view = { x: 0, y: 0, k: 0.05 };
let selected = null, hover = null, route = [], tab = 'System', pilotCard = null;

const canvas = $('map'), ctx = canvas.getContext('2d');
let W = 0, H = 0;

function color(s) {
  const c = s.empire && S.empires[s.empire];
  return c && HEX.test(c) ? c : LAWLESS;
}
const toScreen = (s) => [(s.x - view.x) * view.k + W / 2, (s.y - view.y) * view.k + H / 2];

function resize() {
  const r = canvas.getBoundingClientRect(), d = window.devicePixelRatio || 1;
  W = r.width; H = r.height;
  canvas.width = Math.round(W * d); canvas.height = Math.round(H * d);
  ctx.setTransform(d, 0, 0, d, 0, 0);
  draw();
}

function fit(list, pad) {
  if (!list.length || !W) return;
  const xs = list.map((s) => s.x), ys = list.map((s) => s.y);
  const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
  view.x = (x0 + x1) / 2; view.y = (y0 + y1) / 2;
  view.k = Math.min(W / (x1 - x0 + pad), H / (y1 - y0 + pad));
  draw();
}

function pathFromHome(target) {
  const prev = new Map([[S.home, null]]), queue = [S.home];
  while (queue.length) {
    const here = queue.shift();
    if (here === target) break;
    for (const next of (sys.get(here) || { lanes: [] }).lanes) {
      if (sys.has(next) && !prev.has(next)) { prev.set(next, here); queue.push(next); }
    }
  }
  if (!prev.has(target)) return [];
  const out = [];
  for (let at = target; at !== null; at = prev.get(at)) out.unshift(at);
  return out;
}

function draw() {
  if (!S) return;
  ctx.clearRect(0, 0, W, H);
  const k = view.k, r = Math.max(2, Math.min(7, 2 + k * 28));
  if (layers.Lanes) {
    ctx.strokeStyle = 'rgba(120,128,160,0.22)'; ctx.lineWidth = 1; ctx.beginPath();
    for (const s of S.systems) {
      const [ax, ay] = toScreen(s);
      for (const id of s.lanes) {
        const t = sys.get(id);
        if (t && s.id < id) { const [bx, by] = toScreen(t); ctx.moveTo(ax, ay); ctx.lineTo(bx, by); }
      }
    }
    ctx.stroke();
  }
  if (route.length > 1) {
    ctx.strokeStyle = '#9b59b6'; ctx.lineWidth = 2.5; ctx.beginPath();
    route.forEach((id, i) => { const [x, y] = toScreen(sys.get(id)); if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y); });
    ctx.stroke();
  }
  if (layers.Traffic) {
    for (const s of S.systems) {
      const n = L.hour[s.id] || 0;
      if (!n) continue;
      const [x, y] = toScreen(s);
      ctx.fillStyle = 'rgba(240,180,70,0.16)';
      ctx.beginPath(); ctx.arc(x, y, r + 3 + Math.sqrt(n) * 2.6, 0, 6.2832); ctx.fill();
    }
  }
  for (const s of S.systems) {
    const [x, y] = toScreen(s);
    if (x < -40 || y < -40 || x > W + 40 || y > H + 40) continue;
    ctx.fillStyle = color(s);
    ctx.beginPath(); ctx.arc(x, y, s.home ? r + 2 : r, 0, 6.2832); ctx.fill();
    if (layers.Stations && stationsBy.has(s.id)) {
      const own = stationsBy.get(s.id).some((t) => t.tag);
      ctx.strokeStyle = own ? '#e8c35a' : '#cfd3e6'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(x, y, r + 3, 0, 6.2832); ctx.stroke();
    }
    if (layers.Strongholds && s.stronghold) {
      ctx.strokeStyle = '#e5534b'; ctx.lineWidth = 2; ctx.beginPath();
      ctx.moveTo(x - r - 4, y - r - 4); ctx.lineTo(x + r + 4, y + r + 4);
      ctx.moveTo(x + r + 4, y - r - 4); ctx.lineTo(x - r - 4, y + r + 4); ctx.stroke();
    }
    const intel = layers.Intel && S.intel.systems[s.id];
    if (intel && intel.standing !== 'neutral') {
      ctx.strokeStyle = intel.standing === 'ally' ? '#4cc38a' : '#e5534b'; ctx.lineWidth = 2;
      ctx.strokeRect(x - r - 6, y - r - 6, 2 * r + 12, 2 * r + 12);
    }
    if (layers.Fleet && fleetBy.has(s.id)) {
      ctx.fillStyle = '#c084fc';
      ctx.beginPath(); ctx.moveTo(x, y - r - 9); ctx.lineTo(x + 6, y - r - 3); ctx.lineTo(x, y - r + 3); ctx.lineTo(x - 6, y - r - 3);
      ctx.closePath(); ctx.fill();
      ctx.fillText(String(fleetBy.get(s.id)), x + 9, y - r - 2);
    }
    if (s.id === selected) {
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(x, y, r + 7, 0, 6.2832); ctx.stroke();
    }
    if (layers.Names && (k > 0.16 || s.home || s.id === selected || s.id === hover)) {
      ctx.fillStyle = s.home ? '#ffffff' : '#aab0c8';
      ctx.font = (s.home ? '600 ' : '') + '11px system-ui, sans-serif';
      ctx.fillText(s.name, x + r + 5, y + 4);
    }
  }
}

function nearest(mx, my) {
  let best = null, bd = 14 * 14;
  for (const s of S.systems) {
    const [x, y] = toScreen(s), d = (x - mx) * (x - mx) + (y - my) * (y - my);
    if (d < bd) { bd = d; best = s; }
  }
  return best;
}

// ---------------------------------------------------------------- panels

function facts(rows) {
  const t = el('table');
  for (const [k, v] of rows) { const tr = el('tr'); tr.append(el('th', null, k), el('td', null, v)); t.append(tr); }
  return t;
}
function table(head, rows, numeric) {
  const t = el('table'), hr = el('tr');
  head.forEach((h, i) => hr.append(el('th', numeric && numeric.includes(i) ? 'n' : null, h)));
  t.append(hr);
  for (const row of rows) {
    const tr = el('tr');
    row.forEach((c, i) => {
      const td = el('td', numeric && numeric.includes(i) ? 'n' : null);
      if (c instanceof Node) td.append(c); else td.textContent = c === undefined || c === null ? '' : String(c);
      tr.append(td);
    });
    t.append(tr);
  }
  return t;
}
function sysLink(id) {
  const s = sys.get(id), b = el('button', 'link', s ? s.name : id);
  b.type = 'button';
  b.addEventListener('click', () => select(id, true));
  return b;
}
function pilotLink(name) {
  const b = el('button', 'link', name);
  b.type = 'button';
  b.addEventListener('click', () => showPilot(name));
  return b;
}

async function renderSystem(panel) {
  if (pilotCard) { renderPilot(panel, pilotCard); return; }
  if (!selected) { panel.append(el('p', 'empty', 'Click a system on the map.')); return; }
  const s = sys.get(selected);
  panel.append(el('h2', null, s.name), el('p', 'sub', s.id));
  const intel = S.intel.systems[s.id];
  if (intel) {
    const chips = el('div', 'chips');
    chips.append(el('span', 'tag ' + intel.standing, intel.standing), el('span', 'tag ' + intel.threat, 'threat ' + intel.threat));
    panel.append(chips);
  }
  panel.append(facts([
    ['Empire', s.empire || 'lawless'], ['Position', 'x ' + s.x + ', y ' + s.y],
    ['Jumps from home', s.jumps < 0 ? 'no lane route' : s.jumps],
    ['Pilots seen (1 h / 24 h)', (L.hour[s.id] || 0) + ' / ' + (L.day[s.id] || 0)],
    ['Flags', [s.home ? 'empire home' : '', s.stronghold ? 'pirate stronghold' : ''].filter(Boolean).join(', ') || 'none'],
  ]));
  panel.append(el('h3', null, 'Lanes'));
  const lanes = el('div', 'chips');
  s.lanes.forEach((id) => lanes.append(sysLink(id)));
  panel.append(lanes);
  if (route.length > 1) {
    panel.append(el('h3', null, 'Route from home'));
    const way = el('div', 'chips');
    route.forEach((id) => way.append(sysLink(id)));
    panel.append(way);
  }
  const st = stationsBy.get(s.id) || [];
  panel.append(el('h3', null, 'Stations'));
  if (st.length) {
    panel.append(table(['Station', 'Owner', 'State', 'Services'],
      st.map((t) => [t.name, t.tag || t.empire || '', t.wrecked ? 'wrecked' : t.condition, t.services.join(', ')])));
  } else panel.append(el('p', 'empty', 'None on the public list.'));
  const fleet = S.fleet.filter((f) => f.system === s.id);
  if (fleet.length) {
    panel.append(el('h3', null, 'Our ships (MAP.md)'));
    panel.append(table(['Division', 'POI', 'Ships', 'Doing', 'As of'], fleet.map((f) => [f.division, f.poi, f.ships, f.doing, f.as_of]), [2]));
  }
  const id = s.id;
  const box = el('div');
  panel.append(box);
  try {
    const d = await get('/api/system?id=' + encodeURIComponent(id));
    if (selected !== id || tab !== 'System' || pilotCard) return;
    box.append(el('h3', null, 'Pilots last seen here (' + d.pilot_count + ')'));
    if (d.pilots.length) {
      box.append(table(['Pilot', 'Faction', 'Empire', 'Seen'], d.pilots.map((p) => [pilotLink(p.name), p.tag, p.empire, ago(p.age) + ' ago'])));
    } else box.append(el('p', 'empty', 'Nobody jumped here in the last 24 h.'));
    if (d.battles.length) {
      box.append(el('h3', null, 'Recent battles'));
      box.append(table(['Kind', 'Pilots', 'Lost'], d.battles.map((b) => [b.category, b.pilots.join(', '), b.lost.join(', ')])));
    }
    if (d.intel) {
      box.append(el('h3', null, 'Intel file: ' + d.intel.file));
      box.append(el('pre', null, d.intel_text));
    }
  } catch (e) { box.append(el('p', 'empty', 'Detail not available: ' + e.message)); }
}

function renderPilot(panel, d) {
  const back = el('button', 'link', 'Back to the system');
  back.type = 'button';
  back.addEventListener('click', () => { pilotCard = null; render(); });
  panel.append(back, el('h2', null, d.name));
  if (d.intel) {
    const chips = el('div', 'chips');
    chips.append(el('span', 'tag ' + d.intel.standing, d.intel.standing), el('span', 'tag ' + d.intel.threat, 'threat ' + d.intel.threat));
    panel.append(chips, el('p', 'sub', d.intel.file));
  }
  const rows = [];
  if (d.seen) rows.push(['Last jump', sysLink(d.seen.system)], ['Seen', ago(d.seen.age) + ' ago'], ['Faction', d.seen.tag || 'none'], ['Empire', d.seen.empire]);
  else rows.push(['Last jump', 'not seen on the live stream in the last 24 h']);
  if (d.profile) {
    rows.push(['Registered', d.profile.created], ['Faction (daily feed)', d.profile.faction || 'none'], ['Empire (daily feed)', d.profile.empire]);
    for (const [k, v] of Object.entries(d.profile.stats)) rows.push([k.replace(/_/g, ' '), fmt(v)]);
  }
  const t = el('table');
  for (const [k, v] of rows) {
    const tr = el('tr'), td = el('td');
    if (v instanceof Node) td.append(v); else td.textContent = String(v);
    tr.append(el('th', null, k), td); t.append(tr);
  }
  panel.append(t);
}

function renderFeed(panel) {
  panel.append(el('h3', null, 'Jumps (' + fmt(L.pilots_tracked) + ' pilots tracked)'));
  panel.append(table(['Ago', 'Pilot', 'From', 'To'],
    L.events.slice(0, 40).map((e) => [ago(e.t), pilotLink(e.pilot), sysLink(e.from), sysLink(e.to)])));
  panel.append(el('h3', null, 'Exchange fills'));
  panel.append(table(['Ago', 'Item', 'Qty', 'Each', 'Where'],
    L.fills.slice(0, 25).map((f) => [ago(f.t), f.item, fmt(f.qty), fmt(f.price), sysLink(f.system)]), [2, 3]));
  panel.append(el('h3', null, 'Battles'));
  panel.append(table(['Where', 'Kind', 'Pilots', 'Lost'],
    L.battles.slice(0, 20).map((b) => [sysLink(b.system), b.category, b.pilots.join(', '), b.lost.join(', ')])));
}

async function renderBoard(panel) {
  if (!board) board = await get('/api/leaderboard');
  const groups = Object.keys(board.groups || {});
  if (!groups.length) { panel.append(el('p', 'empty', 'No leaderboard yet.')); return; }
  const g = el('select'), c = el('select'), out = el('div'), row = el('div', 'row');
  groups.forEach((n) => g.append(new Option(n, n)));
  const fill = () => { c.replaceChildren(); Object.keys(board.groups[g.value]).forEach((n) => c.append(new Option(n.replace(/_/g, ' '), n))); show(); };
  const show = () => out.replaceChildren(table(['#', 'Name', '', 'Value'],
    (board.groups[g.value][c.value] || []).map((r) => [r.rank, r.name, r.tag, fmt(r.value)]), [0, 3]));
  g.addEventListener('change', fill); c.addEventListener('change', show);
  row.append(g, c); panel.append(row, out, el('p', 'sub', 'Generated ' + board.generated_at));
  fill();
}

function renderMarket(panel) {
  const input = el('input'), out = el('div');
  input.type = 'search'; input.placeholder = 'Item name, e.g. iron';
  let timer = 0;
  input.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(async () => {
      const d = await get('/api/market?q=' + encodeURIComponent(input.value));
      out.replaceChildren(d.rows.length
        ? table(['Item', 'Market', 'Best bid', 'Best ask', 'Bid qty', 'Ask qty'], d.rows.map((r) => [r[1], r[3], fmt(r[4]), fmt(r[5]), fmt(r[6]), fmt(r[7])]), [2, 3, 4, 5])
        : el('p', 'empty', input.value.length < 2 ? fmt(d.items) + ' items on the public market summary.' : 'No item matches.'));
    }, 250);
  });
  const row = el('div', 'row'); row.append(input);
  panel.append(row, out, el('p', 'sub', 'Best prices per empire market, from the public summary. Station order books need a docked ship.'));
  input.dispatchEvent(new Event('input'));
}

function renderFleet(panel) {
  panel.append(el('h2', null, 'Fleet'));
  if (!S.fleet.length) {
    panel.append(el('p', 'empty', 'No ships deployed yet. This tab shows the positions in MAP.md; live ship status comes with the fleet program.'));
  } else {
    panel.append(table(['Division', 'System', 'POI', 'Ships', 'Doing', 'As of'],
      S.fleet.map((f) => [f.division, sysLink(f.system), f.poi, f.ships, f.doing, f.as_of]), [3]));
  }
  panel.append(el('h3', null, 'Intel files in the repository'));
  const a = Object.values(S.intel.systems), p = Object.values(S.intel.pilots);
  panel.append(table(['File', 'Standing', 'Threat', 'Updated'],
    a.concat(p).map((i) => [i.file, i.standing, i.threat, i.updated])));
  panel.append(el('h3', null, 'Data sources'));
  panel.append(table(['Source', 'Last good', 'Problem'],
    Object.entries(S.sources).map(([n, s]) => [n, ago(s.age) + (s.age < 0 ? '' : ' ago'), s.error])));
}

const TABS = { System: renderSystem, Feed: renderFeed, Leaderboard: renderBoard, Market: renderMarket, Fleet: renderFleet };
let renderSeq = 0;
function render() {
  const panel = $('panel'), mine = ++renderSeq;
  panel.replaceChildren();
  document.querySelectorAll('nav button').forEach((b) => b.classList.toggle('on', b.textContent === tab));
  Promise.resolve(TABS[tab](panel)).catch((e) => { if (mine === renderSeq) panel.append(el('p', 'empty', e.message)); });
}

function select(id, center) {
  if (!sys.has(id)) return;
  selected = id; pilotCard = null; route = pathFromHome(id); tab = 'System';
  if (center) { const s = sys.get(id); view.x = s.x; view.y = s.y; if (view.k < 0.12) view.k = 0.2; }
  draw(); render();
}
async function showPilot(name) {
  pilotCard = await get('/api/pilot?name=' + encodeURIComponent(name));
  tab = 'System';
  if (pilotCard.seen && sys.has(pilotCard.seen.system)) {
    selected = pilotCard.seen.system; route = pathFromHome(selected);
    const s = sys.get(selected); view.x = s.x; view.y = s.y; if (view.k < 0.12) view.k = 0.2;
    draw();
  }
  render();
}

function status() {
  const box = $('status'), st = L.stats || {};
  box.replaceChildren();
  const item = (label, value, cls) => { const s = el('span'); if (cls) s.append(el('i', 'dot ' + cls)); s.append(label + ' '); s.append(el('b', null, value)); box.append(s); };
  item('Tick', fmt(st.tick)); item('Game', st.version || '?'); item('Online', fmt(st.online_players));
  const live = L.stream || {};
  item('Live stream', live.connected ? ago(live.age) + ' ago' : 'down', live.connected && live.age < 60 ? 'good' : 'bad');
  if (S) {
    const bad = Object.entries(S.sources).filter(([, s]) => s.error || s.age < 0).map(([n]) => n);
    item('Sources', bad.length ? 'problem: ' + bad.join(', ') : 'all good', bad.length ? 'warn' : 'good');
  }
}

async function loadState() {
  S = await get('/api/state');
  sys.clear(); stationsBy.clear(); fleetBy.clear();
  S.systems.forEach((s) => sys.set(s.id, s));
  S.stations.forEach((t) => { if (!stationsBy.has(t.system)) stationsBy.set(t.system, []); stationsBy.get(t.system).push(t); });
  S.fleet.forEach((f) => fleetBy.set(f.system, (fleetBy.get(f.system) || 0) + f.ships));
  const legend = $('legend');
  legend.replaceChildren();
  for (const [name, c] of Object.entries(S.empires).concat([['lawless', LAWLESS]])) {
    const span = el('span'), dot = el('i');
    dot.style.background = HEX.test(c) ? c : LAWLESS;
    span.append(dot, name); legend.append(span);
  }
  legend.append(el('span', null, 'ring: station (gold: player faction)'), el('span', null, 'red cross: pirate stronghold'),
    el('span', null, 'glow: pilots seen in the last hour'));
}
async function loadLive() {
  try { L = await get('/api/live'); } catch (e) { L.stream = { connected: false, age: -1 }; }
  status(); draw();
  if (tab === 'Feed') render();
}

function init() {
  const lay = $('layers');
  for (const name of Object.keys(layers)) {
    const label = el('label'), box = el('input');
    box.type = 'checkbox'; box.checked = layers[name];
    box.addEventListener('change', () => { layers[name] = box.checked; draw(); });
    label.append(box, ' ' + name); lay.append(label);
  }
  const nav = $('tabs');
  for (const name of Object.keys(TABS)) {
    const b = el('button', null, name);
    b.type = 'button';
    b.addEventListener('click', () => { tab = name; if (name !== 'System') pilotCard = null; render(); });
    nav.append(b);
  }
  let drag = null, moved = false;
  canvas.addEventListener('mousedown', (e) => { drag = [e.clientX, e.clientY, view.x, view.y]; moved = false; canvas.classList.add('drag'); });
  window.addEventListener('mouseup', () => { drag = null; canvas.classList.remove('drag'); });
  canvas.addEventListener('mousemove', (e) => {
    const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
    if (drag) {
      if (Math.abs(e.clientX - drag[0]) + Math.abs(e.clientY - drag[1]) > 3) moved = true;
      view.x = drag[2] - (e.clientX - drag[0]) / view.k; view.y = drag[3] - (e.clientY - drag[1]) / view.k;
      draw(); return;
    }
    const s = S && nearest(mx, my), tip = $('tip');
    hover = s ? s.id : null;
    if (s) {
      tip.textContent = s.name + (s.empire ? ' (' + s.empire + ')' : '') + ' | ' + (L.hour[s.id] || 0) + ' pilots in the last hour';
      tip.style.left = mx + 14 + 'px'; tip.style.top = my + 12 + 'px'; tip.hidden = false;
    } else tip.hidden = true;
    draw();
  });
  canvas.addEventListener('mouseleave', () => { $('tip').hidden = true; hover = null; draw(); });
  canvas.addEventListener('click', (e) => {
    if (moved || !S) return;
    const r = canvas.getBoundingClientRect(), s = nearest(e.clientX - r.left, e.clientY - r.top);
    if (s) select(s.id, false);
  });
  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left - W / 2, my = e.clientY - r.top - H / 2;
    const k = Math.max(0.01, Math.min(3, view.k * (e.deltaY < 0 ? 1.2 : 1 / 1.2)));
    view.x += mx / view.k - mx / k; view.y += my / view.k - my / k; view.k = k;
    draw();
  }, { passive: false });
  $('btn-all').addEventListener('click', () => fit(S.systems, 1200));
  $('btn-home').addEventListener('click', () => fit(S.systems.filter((s) => s.jumps >= 0 && s.jumps <= 4), 500));
  const input = $('search'), results = $('results');
  let timer = 0;
  input.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(async () => {
      if (input.value.trim().length < 2) { results.hidden = true; return; }
      const d = await get('/api/search?q=' + encodeURIComponent(input.value));
      results.replaceChildren();
      const add = (label, kind, go) => {
        const b = el('button', null, label);
        b.type = 'button'; b.append(el('small', null, kind));
        b.addEventListener('click', () => { results.hidden = true; input.value = ''; go(); });
        results.append(b);
      };
      d.systems.forEach((s) => add(s.name, 'system', () => select(s.id, true)));
      d.pilots.forEach((n) => add(n, 'pilot', () => showPilot(n)));
      if (!results.children.length) results.append(el('button', null, 'Nothing found'));
      results.hidden = false;
    }, 250);
  });
  document.addEventListener('click', (e) => { if (!e.target.closest('.search')) results.hidden = true; });
  window.addEventListener('resize', resize);
}

(async function main() {
  init();
  await loadState();
  resize();
  fit(S.systems, 1200);
  await loadLive();
  render();
  setInterval(loadLive, 5000);
  setInterval(async () => { await loadState(); draw(); if (tab === 'Fleet') render(); }, 120000);
})().catch((e) => { $('panel').replaceChildren(el('p', 'empty', 'The station could not load its data: ' + e.message)); });
