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
async function post(path, body) {
  for (let attempt = 0; attempt < 2; attempt++) {
    const r = await fetch(path, {
      method: 'POST', cache: 'no-store',
      headers: { 'Content-Type': 'application/json', 'X-Station-Token': S ? S.token : '' }, body: JSON.stringify(body),
    });
    if (r.status === 403 && attempt === 0) { await loadState(); continue; }   // the station restarted: read the new token
    let d = {};
    try { d = await r.json(); } catch (e) { d = {}; }
    if (!r.ok) throw new Error(d.error || (path + ' -> ' + r.status));
    return d;
  }
  throw new Error('the station refused the message');
}
const fmt = (n) => Number(n || 0).toLocaleString('en-US');
function ago(s) {
  if (s < 0) return 'never';
  if (s < 90) return s + ' s';
  if (s < 5400) return Math.round(s / 60) + ' min';
  if (s < 129600) return Math.round(s / 3600) + ' h';
  return Math.round(s / 86400) + ' d';
}
const pct = (a, b) => (b > 0 ? Math.max(0, Math.min(100, Math.round(100 * a / b))) : 0);
const HEX = /^#[0-9a-fA-F]{6}$/;
const LAWLESS = '#59607a';
const DIV = { Command: '#e3e6ee', Mining: '#d9a857', Trade: '#5fbfad', Logistics: '#6fa8dc', Military: '#d9766f', Intel: '#b18ae0', Unassigned: '#7c869b' };

let S = null;                                  // /api/state
let L = { hour: {}, day: {}, events: [], fills: [], battles: [], stats: {}, stream: {} };
let F = { ships: [], totals: {}, engine: {}, age: -1, birth: null };   // /api/fleet
let fetchedAt = 0;                             // when /api/fleet last answered (ms)
let HIST = { rows: [], at: 0 };                // /api/history, for the Metrics tab
const collapsed = new Set();                   // divisions folded in the roster
let board = null;
const sys = new Map();
const stationsBy = new Map();
const shipsBy = new Map();                     // system id -> our ships there
const layers = { Lanes: true, Traffic: true, Stations: true, Strongholds: true, Intel: true, Fleet: true, Names: true };
const view = { x: 0, y: 0, k: 0.05 };
let selected = null, hover = null, route = [], tab = 'Selection', pilotCard = null;
let selShip = null, shipCard = null, shipMark = '', docView = null;

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
  view.k = Math.min(3, Math.min(W / (x1 - x0 + pad), H / (y1 - y0 + pad)));
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

function diamond(x, y, r) {
  ctx.beginPath(); ctx.moveTo(x, y - r); ctx.lineTo(x + r, y); ctx.lineTo(x, y + r); ctx.lineTo(x - r, y); ctx.closePath(); ctx.fill();
}

function draw() {
  if (!S) return;
  ctx.clearRect(0, 0, W, H);
  const k = view.k, r = Math.max(2, Math.min(7, 2 + k * 28));
  if (layers.Lanes) {
    ctx.strokeStyle = 'rgba(120,130,165,0.22)'; ctx.lineWidth = 1; ctx.beginPath();
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
    ctx.strokeStyle = '#a48be0'; ctx.lineWidth = 2.5; ctx.beginPath();
    route.forEach((id, i) => { const [x, y] = toScreen(sys.get(id)); if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y); });
    ctx.stroke();
  }
  if (layers.Traffic) {
    for (const s of S.systems) {
      const n = L.hour[s.id] || 0;
      if (!n) continue;
      const [x, y] = toScreen(s);
      ctx.fillStyle = 'rgba(220,174,88,0.15)';
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
      ctx.strokeStyle = '#e06c66'; ctx.lineWidth = 2; ctx.beginPath();
      ctx.moveTo(x - r - 4, y - r - 4); ctx.lineTo(x + r + 4, y + r + 4);
      ctx.moveTo(x + r + 4, y - r - 4); ctx.lineTo(x - r - 4, y + r + 4); ctx.stroke();
    }
    const intel = layers.Intel && S.intel.systems[s.id];
    if (intel && intel.standing !== 'neutral') {
      ctx.strokeStyle = intel.standing === 'ally' ? '#58c08c' : '#e06c66'; ctx.lineWidth = 1.5;
      ctx.strokeRect(x - r - 6, y - r - 6, 2 * r + 12, 2 * r + 12);
    }
    if (s.id === selected) {
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(x, y, r + 7, 0, 6.2832); ctx.stroke();
    }
    const ours = layers.Fleet && shipsBy.has(s.id);
    if (layers.Names && (k > 0.16 || s.home || ours || s.id === selected || s.id === hover)) {
      ctx.fillStyle = s.home || ours ? '#ffffff' : '#aab0c8';
      ctx.font = (s.home || ours ? '600 ' : '') + '11px system-ui, sans-serif';
      ctx.fillText(s.name, x + r + 5, y + 4);
    }
  }
  if (layers.Fleet) {
    for (const [id, list] of shipsBy) {            // our ships: one diamond per division, with its count
      const s = sys.get(id);
      if (!s) continue;
      const [x, y] = toScreen(s), q = r + 10, groups = new Map();
      list.forEach((sh) => groups.set(sh.division, (groups.get(sh.division) || 0) + 1));
      ctx.strokeStyle = list.some((sh) => sh.name === selShip) ? '#ffffff' : 'rgba(213,218,230,0.75)'; ctx.lineWidth = 1.5; ctx.beginPath();
      for (const [dx, dy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) {     // corner brackets around the system
        ctx.moveTo(x + dx * q, y + dy * (q - 5)); ctx.lineTo(x + dx * q, y + dy * q); ctx.lineTo(x + dx * (q - 5), y + dy * q);
      }
      ctx.stroke();
      let i = 0;
      ctx.font = '600 11px system-ui, sans-serif';
      for (const [division, n] of groups) {
        const cx = x - q + 5 + i * 26, cy = y - q - 9;
        ctx.fillStyle = DIV[division] || DIV.Unassigned;
        diamond(cx, cy, 5);
        ctx.fillStyle = '#d5dae6';
        ctx.fillText(String(n), cx + 8, cy + 4);
        i++;
      }
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

// ---------------------------------------------------------------- small builders

function facts(rows) {
  const t = el('table');
  for (const [k, v] of rows) {
    const tr = el('tr'), td = el('td');
    if (v instanceof Node) td.append(v); else td.textContent = v === undefined || v === null ? '' : String(v);
    tr.append(el('th', null, k), td); t.append(tr);
  }
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
function linkButton(label, go, cls) {
  const b = el('button', cls || 'link', label);
  b.type = 'button';
  b.addEventListener('click', go);
  return b;
}
const sysLink = (id) => linkButton(sys.has(id) ? sys.get(id).name : id, () => select(id, true));
const pilotLink = (name) => linkButton(name, () => showPilot(name));
const shipLink = (name) => linkButton(name, () => selectShip(name, false));
function bar(kind, a, b, lowBelow) {
  const o = el('div', 'bar ' + kind + (lowBelow && b > 0 && a / b < lowBelow ? ' low' : '')), i = el('i');
  i.style.width = pct(a, b) + '%';
  o.append(i); o.title = kind + ' ' + fmt(a) + ' / ' + fmt(b);
  return o;
}
function divTag(division) {
  const t = el('span', 'tag', division), c = DIV[division] || DIV.Unassigned;
  t.style.color = c; t.style.borderColor = c;
  return t;
}

// ---------------------------------------------------------------- fleet: resources, roster, ship card

function shipState(r) {
  if (r.status !== 'connected') return ['off', 'offline'];
  const waiting = r.loop_failures > 0 && /depleted/i.test(r.loop_last_failure || '');   // a patient loop at an empty belt
  if (r.loop_failures >= 3 && !waiting) return ['bad', 'loop failing'];
  if (r.jumping) return ['move', 'jumping'];
  if (r.in_transit) return ['move', 'to ' + (r.dest_poi || 'another place')];
  const a = r.activity || {};
  if (a.kind === 'loop') return waiting ? ['wait', 'waiting for ore'] : ['work', a.type + ' loop'];
  if (a.kind === 'goal' || a.kind === 'job') return ['work', a.type];
  return r.docked ? ['dock', 'docked'] : ['idle', 'idle in space'];
}

function signed(n) { return (n > 0 ? '+' : '') + fmt(n); }
function liveAge() { return F.age < 0 ? -1 : F.age + Math.round((Date.now() - fetchedAt) / 1000); }

function renderResources() {
  const box = $('resources'), t = F.totals || {}, r = t.rates;
  box.replaceChildren();
  const cell = (k, v, small, smallCls, bad, tip) => {
    const c = el('div', 'res' + (bad ? ' bad' : '')), val = el('div', 'v', v);
    if (small) val.append(el('small', smallCls || null, small));
    c.append(el('div', 'k', k), val);
    if (tip) c.title = tip;
    box.append(c);
    return c;
  };
  const head = cell('CPH', r ? fmt(r.cph) : '--', r ? fmt(r.cph_per_ship) + ' / ship' : 'measuring', r && r.cph > 0 ? 'up' : null, false,
    'Credits per hour: recurring income over the last ' + (r ? r.window_minutes : 60) + ' minutes, one-time starter rewards excluded');
  head.classList.add('head');
  cell('Credits', fmt(t.credits), r ? signed(r.net_per_hour) + ' / h' : '', r && r.net_per_hour < 0 ? 'down' : 'up', false,
    'All wallets; the small number is the net change per hour, spending and seed money included');
  cell('Per ship', fmt(t.credits_per_ship), '', null, false, 'Credits divided by ships');
  cell('Ships', fmt(t.ships), t.ships ? (t.idle ? t.idle + ' idle' : 'all busy') : '', t.idle ? 'warn' : 'up');
  cell('Ore / h', r ? fmt(r.ore_per_hour) : '--', r ? r.missions_per_hour + ' missions / h' : '');
  const age = liveAge(), ok = Boolean(F.engine && F.engine.ok && age >= 0 && age < 60);
  const eng = cell('Engine', ok ? 'live' : 'no data', age >= 0 ? age + ' s ago' : '', null, !ok);
  eng.id = 'engine-cell';
}

function tickAges() {                          // every second: the age labels count up between polls
  const age = liveAge(), cell = $('engine-cell');
  if (cell) { const s = cell.querySelector('small'); if (s) s.textContent = age >= 0 ? age + ' s ago' : ''; }
  const fresh = $('fleet-fresh');
  if (fresh && age >= 0) fresh.textContent = (F.engine && F.engine.ok && age < 60 ? 'live | ' : 'stale | ') + age + ' s ago';
}

function shipRow(r) {
  const [cls, what] = shipState(r), b = el('button', 'ship' + (r.name === selShip ? ' on' : ''));
  b.type = 'button';
  const who = el('div', 'who'), bars = el('div', 'bars'), cr = el('div', 'cr', fmt(r.credits));
  who.append(el('div', 'nm', r.name), el('div', 'at', (r.system_name || r.system || 'position unknown') + ' | ' + what));
  bars.append(bar('hull', r.hull, r.max_hull, 0.5), bar('fuel', r.fuel, r.max_fuel, 0.25), bar('cargo', r.cargo_used, r.cargo_capacity));
  cr.append(el('small', null, r.class || ''));
  b.append(el('i', 'glyph ' + cls), who, bars, cr);
  b.title = r.name + ': hull ' + r.hull + '/' + r.max_hull + ', fuel ' + r.fuel + '/' + r.max_fuel + ', cargo ' + r.cargo_used + '/' + r.cargo_capacity;
  b.addEventListener('click', () => selectShip(r.name, true));
  return b;
}

function renderRoster() {
  const box = $('roster'), keep = box.scrollTop, by = new Map();
  box.replaceChildren();
  F.ships.forEach((r) => { if (!by.has(r.division)) by.set(r.division, []); by.get(r.division).push(r); });
  const divisions = (S ? S.roster : []).filter((a) => a.division !== 'Command').map((a) => [a.division, a]);
  if (by.has('Unassigned')) divisions.push(['Unassigned', null]);
  for (const [division, admiral] of divisions) {
    const list = by.get(division) || [], block = el('div', 'div'), head = el('div', 'divhead'), c = DIV[division] || DIV.Unassigned;
    const name = el('span', 'name', (collapsed.has(division) ? '+ ' : '') + division), sum = el('span', 'sum');
    head.style.borderLeftColor = c; name.style.color = c;
    name.title = 'Fold or unfold this division';
    name.addEventListener('click', () => { if (collapsed.has(division)) collapsed.delete(division); else collapsed.add(division); renderRoster(); });
    head.append(name);
    if (admiral) {
      const b = linkButton('Adm. ' + admiral.name, () => openChat(admiral.id), 'adm');
      b.title = 'Open the chat with ' + admiral.name;
      head.append(b);
    }
    if (list.length) {
      const dr = ((F.totals.rates || {}).divisions || {})[division];
      sum.append(el('b', null, String(list.length)), list.length === 1 ? ' ship  ' : ' ships  ', el('b', null, fmt(list.reduce((a, r) => a + r.credits, 0))), ' cr');
      if (dr) sum.append('  ', el('b', null, fmt(dr.cph)), ' /h');
    }
    head.append(sum); block.append(head);
    if (!list.length) block.append(el('div', 'noships', 'No ships yet'));
    if (!collapsed.has(division)) list.forEach((r) => block.append(shipRow(r)));
    box.append(block);
  }
  box.scrollTop = keep;
  const fresh = $('fleet-fresh'), ok = F.age >= 0 && F.age < 60 && F.engine && F.engine.ok;
  fresh.textContent = F.age < 0 ? 'no data' : (ok ? 'live | ' : 'stale | ') + liveAge() + ' s ago';
  fresh.className = 'fresh' + (ok ? '' : ' bad');
}

function renderShip(panel) {
  const d = shipCard;
  panel.append(linkButton('Back to the system', () => { selShip = null; shipCard = null; shipMark = ''; renderRoster(); draw(); render(); }));
  if (!d) { panel.append(el('p', 'empty', 'Loading the ship...')); return; }
  if (d.error) { panel.append(el('p', 'empty', 'The fleet data has no file for this ship.')); return; }
  const chips = el('div', 'chips'), [cls, what] = shipState(d);
  panel.append(el('h2', null, d.name), el('p', 'sub', [d.class, d.empire].filter(Boolean).join(' | ')));
  chips.append(divTag(d.division));
  if (d.admiral) chips.append(el('span', 'tag', 'Adm. ' + d.admiral));
  chips.append(el('span', 'tag ' + (cls === 'bad' ? 'bad' : cls === 'idle' || cls === 'wait' ? 'warn' : cls === 'work' ? 'good' : ''), what));
  panel.append(chips);
  const g = el('div', 'gauges');
  for (const [k, kind, a, b, low] of [['Hull', 'hull', d.hull, d.max_hull, 0.5], ['Shield', 'shield', d.shield, d.max_shield, 0],
    ['Fuel', 'fuel', d.fuel, d.max_fuel, 0.25], ['Cargo', 'cargo', d.cargo_used, d.cargo_capacity, 0]]) {
    g.append(el('span', 'k', k), bar(kind, a, b, low), el('span', 'v', fmt(a) + ' / ' + fmt(b)));
  }
  panel.append(g);
  const loc = d.system && sys.has(d.system) ? sysLink(d.system) : (d.system_name || 'unknown');
  panel.append(facts([
    ['System', loc], ['Place', d.jumping ? 'jumping to the next system' : d.in_transit ? 'in transit to ' + (d.dest_poi || '?') : (d.poi_name || '-')],
    ['Docked at', d.docked || 'not docked'], ['Credits', fmt(d.credits)], ['Home base', d.home_base || '-'],
    ['Security here', d.security || '-'], ['State as of', (d.state_at || '') + ' UTC'],
  ]));
  if (d.loop && d.loop.type) {
    panel.append(el('h3', null, 'Loop'));
    panel.append(facts([['Type', d.loop.type + (d.loop.running ? ' (running)' : ' (stopped)')], ['Last step', d.loop.last_step || '-'],
      ['Failures in a row', d.loop_failures], ['Last failure', d.loop_last_failure || 'none']]));
  }
  panel.append(el('h3', null, 'Missions (' + (d.mission_list || []).length + ' of 5)'));
  if (!(d.mission_list || []).length) panel.append(el('p', 'empty', 'None accepted.'));
  for (const m of d.mission_list || []) {
    const box = el('div', 'mission'), top = el('div', 't'), b = el('div', 'bar'), i = el('i');
    top.append(el('b', null, m.title), el('span', null, fmt(m.credits) + ' cr'));
    i.style.width = Math.round(m.percent) + '%'; b.append(i);
    box.append(top, b);
    m.objectives.forEach((o) => box.append(el('div', 'o' + (o.done ? ' done' : ''), (o.done ? '[done] ' : '[' + o.current + '/' + o.required + '] ') + o.text)));
    panel.append(box);
  }
  panel.append(el('h3', null, 'Cargo'));
  if (d.cargo.length) panel.append(table(['Item', 'Units'], d.cargo.map((c) => [c.name || c.item, fmt(c.quantity)]), [1]));
  else panel.append(el('p', 'empty', 'Empty hold.'));
  panel.append(el('h3', null, 'Modules'));
  panel.append(table(['Module', 'Kind', 'Slot'], d.modules.map((m) => [m.name, m.kind, m.slot])));
  const skills = Object.entries(d.skills || {});
  if (skills.length) {
    panel.append(el('h3', null, 'Skills'));
    panel.append(table(['Skill', 'Level', 'XP'], skills.map(([k, v]) => [k.replace(/_/g, ' '), v.level, fmt(v.xp) + ' / ' + fmt(v.next)]), [1, 2]));
  }
  panel.append(el('h3', null, 'Service record'));
  panel.append(facts(Object.entries(d.stats || {}).map(([k, v]) => [k.replace(/_/g, ' '), fmt(v)])));
}

async function selectShip(name, center) {
  selShip = name; shipCard = null; shipMark = ''; pilotCard = null; docView = null; tab = 'Selection';
  const row = F.ships.find((r) => r.name === name);
  if (row && sys.has(row.system)) {
    selected = row.system; route = pathFromHome(selected);
    if (center) { const s = sys.get(selected); view.x = s.x; view.y = s.y; if (view.k < 0.12) view.k = 0.35; }
  }
  renderRoster(); draw(); render();
  try { shipCard = await get('/api/ship?name=' + encodeURIComponent(name)); } catch (e) { shipCard = { error: e.message }; }
  shipMark = JSON.stringify(shipCard);
  if (selShip === name) render();
}

// ---------------------------------------------------------------- right panel

async function renderSelection(panel, live) {
  if (selShip) { renderShip(panel); return; }
  if (pilotCard) { renderPilot(panel, pilotCard); return; }
  if (!selected) { panel.append(el('p', 'empty', 'Click a system on the map or a ship in the roster.')); return; }
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
  const ours = shipsBy.get(s.id) || [];
  if (ours.length) {
    panel.append(el('h3', null, 'Our ships here (' + ours.length + ')'));
    panel.append(table(['Ship', 'Doing', 'Cargo'], ours.map((r) => [shipLink(r.name), shipState(r)[1], r.cargo_used + ' / ' + r.cargo_capacity])));
  }
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
  const id = s.id, box = el('div');
  panel.append(box);
  try {
    const d = await get('/api/system?id=' + encodeURIComponent(id));
    if (!live()) return;
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
  } catch (e) { if (live()) box.append(el('p', 'empty', 'Detail not available: ' + e.message)); }
}

function renderPilot(panel, d) {
  panel.append(linkButton('Back to the system', () => { pilotCard = null; render(); }), el('h2', null, d.name));
  if (d.intel) {
    const chips = el('div', 'chips');
    chips.append(el('span', 'tag ' + d.intel.standing, d.intel.standing), el('span', 'tag ' + d.intel.threat, 'threat ' + d.intel.threat));
    panel.append(chips, linkButton('Intel file: ' + d.intel.file, () => openDoc(d.intel.file)));
  }
  const rows = [];
  if (d.seen) rows.push(['Last jump', sysLink(d.seen.system)], ['Seen', ago(d.seen.age) + ' ago'], ['Faction', d.seen.tag || 'none'], ['Empire', d.seen.empire]);
  else rows.push(['Last jump', 'not seen on the live stream in the last 24 h']);
  if (d.profile) {
    rows.push(['Registered', d.profile.created], ['Faction (daily feed)', d.profile.faction || 'none'], ['Empire (daily feed)', d.profile.empire]);
    for (const [k, v] of Object.entries(d.profile.stats)) rows.push([k.replace(/_/g, ' '), fmt(v)]);
  }
  panel.append(facts(rows));
}

function renderTraffic(panel) {
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

async function renderRanks(panel, live) {
  if (!board) board = await get('/api/leaderboard');
  if (!live()) return;
  const groups = Object.keys(board.groups || {});
  if (!groups.length) { panel.append(el('p', 'empty', 'No leaderboard yet.')); return; }
  const g = el('select'), c = el('select'), out = el('div'), row = el('div', 'row');
  groups.forEach((n) => g.append(new Option(n, n)));
  const show = () => out.replaceChildren(table(['#', 'Name', '', 'Value'],
    (board.groups[g.value][c.value] || []).map((r) => [r.rank, r.name, r.tag, fmt(r.value)]), [0, 3]));
  const fill = () => { c.replaceChildren(); Object.keys(board.groups[g.value]).forEach((n) => c.append(new Option(n.replace(/_/g, ' '), n))); show(); };
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

async function openDoc(path) {
  tab = 'Docs'; selShip = null; shipCard = null; docView = { path, text: 'Loading...' };
  renderRoster(); render();
  try { docView = await get('/api/doc?path=' + encodeURIComponent(path)); } catch (e) { docView = { path, error: e.message }; }
  if (tab === 'Docs') render();
}

async function renderDocs(panel, live) {
  if (docView) {
    panel.append(linkButton('Back to the list', () => { docView = null; render(); }), el('h2', null, docView.path));
    if (docView.error) panel.append(el('p', 'empty', docView.error));
    else {
      if (docView.cut) panel.append(el('p', 'sub', docView.path.endsWith('.log') ? 'Long log: the newest part is shown.' : 'Long file: the first part is shown.'));
      panel.append(el('pre', null, docView.text));
    }
    return;
  }
  const d = await get('/api/docs');
  if (!live()) return;
  const row = (label, small, path) => { const b = linkButton(label, () => openDoc(path), 'rowlink'); if (small) b.append(el('small', null, small)); return b; };
  panel.append(el('h3', null, 'Reports'));
  if (d.reports.length) d.reports.forEach((r) => panel.append(row(r.name, r.author, r.path)));
  else panel.append(el('p', 'empty', 'No report yet. One is written at every session end.'));
  panel.append(el('h3', null, 'Logs'));
  d.logs.forEach((g) => panel.append(row(g.name, g.entries ? g.entries + ' entries, last ' + g.last.ent + ' by ' + g.last.by + ', ' + g.last.at : 'no entries', g.path)));
  panel.append(el('h3', null, 'Intel files'));
  const intel = Object.values(S.intel.systems).concat(Object.values(S.intel.pilots));
  if (intel.length) intel.forEach((i) => panel.append(row(i.file, i.standing + ', threat ' + i.threat + (i.updated ? ', ' + i.updated : ''), i.file)));
  else panel.append(el('p', 'empty', 'None yet.'));
  panel.append(el('h3', null, 'Station data sources'));
  panel.append(table(['Source', 'Last good', 'Problem'],
    Object.entries(S.sources).map(([n, s]) => [n, ago(s.age) + (s.age < 0 ? '' : ' ago'), s.error])));
}

function chart(rows, pick, label, unit) {
  const c = el('canvas', 'chart'), wrap = el('div', 'chartbox');
  wrap.append(el('div', 'chartlabel', label), c);
  requestAnimationFrame(() => {
    const w = c.clientWidth || 340, h = 90, d = window.devicePixelRatio || 1, g = c.getContext('2d');
    c.width = w * d; c.height = h * d; g.scale(d, d);
    const pts = rows.map((r) => [r[0], pick(r)]).filter((p) => p[1] !== null && isFinite(p[1]));
    if (pts.length < 2) { g.fillStyle = '#5c6780'; g.font = '12px system-ui'; g.fillText('Not enough samples yet', 8, 48); return; }
    const t0 = pts[0][0], t1 = pts[pts.length - 1][0];
    let lo = Math.min(...pts.map((p) => p[1])), hi = Math.max(...pts.map((p) => p[1]));
    if (lo > 0) lo = 0;
    if (hi === lo) hi = lo + 1;
    const X = (t) => 4 + (w - 8) * (t - t0) / Math.max(1, t1 - t0), Y = (v) => h - 14 - (h - 26) * (v - lo) / (hi - lo);
    g.strokeStyle = 'rgba(135,145,168,0.25)'; g.lineWidth = 1; g.beginPath(); g.moveTo(4, Y(0)); g.lineTo(w - 4, Y(0)); g.stroke();
    g.strokeStyle = '#a48be0'; g.lineWidth = 1.6; g.beginPath();
    pts.forEach((p, i) => (i ? g.lineTo(X(p[0]), Y(p[1])) : g.moveTo(X(p[0]), Y(p[1]))));
    g.stroke();
    g.fillStyle = '#8791a8'; g.font = '10.5px system-ui';
    g.fillText(fmt(hi) + unit, 6, 10);
    g.fillText(new Date(t0 * 1000).toISOString().slice(11, 16) + ' UTC', 6, h - 2);
    g.fillText(new Date(t1 * 1000).toISOString().slice(11, 16), w - 34, h - 2);
  });
  return wrap;
}

function rolling(rows, minutes) {               // CPH over a trailing window, from the minute samples
  const out = [];
  for (let i = 0; i < rows.length; i++) {
    let j = i;
    while (j > 0 && rows[i][0] - rows[j - 1][0] <= minutes * 60) j--;
    const dt = rows[i][0] - rows[j][0];
    out.push([rows[i][0], dt >= 300 ? (rows[i][3] - rows[j][3]) * 3600 / dt : null]);
  }
  return out;
}

async function renderMetrics(panel, live) {
  const t = F.totals || {}, r = t.rates;
  panel.append(el('h2', null, 'Fleet performance'));
  panel.append(el('p', 'sub', r ? 'Rates over the last ' + r.window_minutes + ' minutes.' : 'Rates appear after five minutes of samples.'));
  const grid = el('div', 'kpis');
  const kpi = (k, v, sub, cls) => { const b = el('div', 'kpi' + (cls ? ' ' + cls : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sub) b.append(el('div', 's', sub)); grid.append(b); };
  kpi('CPH', r ? fmt(r.cph) : '--', 'recurring credits per hour', 'main');
  kpi('CPH per ship', r ? fmt(r.cph_per_ship) : '--', 'production capacity of one ship', 'main');
  kpi('Credits per ship', fmt(t.credits_per_ship), fmt(t.credits) + ' in all');
  kpi('Net per hour', r ? signed(r.net_per_hour) : '--', 'wallet change, all included');
  kpi('Ore per hour', r ? fmt(r.ore_per_hour) : '--', 'units mined');
  kpi('Missions per hour', r ? String(r.missions_per_hour) : '--', 'completed');
  panel.append(grid);
  const b = F.birth;
  if (b && b.planned && !b.finished_at) {
    panel.append(el('h3', null, 'Birth in progress'));
    panel.append(facts([['Registered', b.registered + ' of ' + b.planned + (b.failed ? ', ' + b.failed + ' refused' : '')],
      ['Starter missions done', b.starter_done], ['Standing orders given', b.ordered], ['Stopped', b.stopped || 'no']]));
  }
  panel.append(el('h3', null, 'By division'));
  const div = t.divisions || {}, dr = (r || {}).divisions || {};
  const order = (S ? S.roster : []).filter((a) => a.division !== 'Command').map((a) => [a.division, a.name]);
  if (div.Unassigned) order.push(['Unassigned', '']);
  panel.append(table(['Division', 'Ships', 'Credits', 'Per ship', 'CPH', 'CPH / ship', 'Ore / h'],
    order.map(([d, adm]) => {
      const x = div[d] || {}, y = dr[d] || {}, name = el('span', null, d);
      name.style.color = DIV[d] || DIV.Unassigned; name.title = adm ? 'Admiral ' + adm : '';
      return [name, fmt(x.ships), fmt(x.credits), fmt(x.credits_per_ship), r ? fmt(y.cph) : '--', r ? fmt(y.cph_per_ship) : '--', r ? fmt(y.ore_per_hour) : '--'];
    }), [1, 2, 3, 4, 5, 6]));
  panel.append(el('h3', null, 'Last six hours'));
  const box = el('div');
  panel.append(box);
  if (Date.now() - HIST.at > 30000) {
    try { HIST = Object.assign(await get('/api/history?q=6'), { at: Date.now() }); } catch (e) { HIST = { rows: [], at: Date.now() }; }
    if (!live()) return;
  }
  box.append(chart(rolling(HIST.rows, 30), (p) => p[1], 'CPH, trailing 30 minutes', ''),
    chart(HIST.rows, (p) => p[1], 'Credits, all wallets', ''),
    chart(HIST.rows, (p) => (p[2] ? p[1] / p[2] : null), 'Credits per ship', ''));
  panel.append(el('p', 'sub', 'CPH counts what the pilots earn (missions, sales) minus one-time starter rewards. Seed money and spending show in the net change, not in CPH.'));
}

const TABS = { Selection: renderSelection, Metrics: renderMetrics, Traffic: renderTraffic, Market: renderMarket, Ranks: renderRanks, Docs: renderDocs };
let renderSeq = 0, viewKey = '';
function render() {
  const panel = $('panel'), mine = ++renderSeq, live = () => mine === renderSeq;
  const key = [tab, selShip, selShip ? '' : selected, pilotCard ? pilotCard.name : '', docView ? docView.path : ''].join('|');
  const keep = key === viewKey ? panel.scrollTop : 0;
  viewKey = key;
  panel.replaceChildren();
  document.querySelectorAll('nav button').forEach((b) => b.classList.toggle('on', b.textContent === tab));
  Promise.resolve(TABS[tab](panel, live)).catch((e) => { if (live()) panel.append(el('p', 'empty', e.message)); });
  panel.scrollTop = keep;
}

function select(id, center) {
  if (!sys.has(id)) return;
  selected = id; pilotCard = null; selShip = null; shipCard = null; docView = null; route = pathFromHome(id); tab = 'Selection';
  if (center) { const s = sys.get(id); view.x = s.x; view.y = s.y; if (view.k < 0.12) view.k = 0.2; }
  renderRoster(); draw(); render();
}
async function showPilot(name) {
  pilotCard = await get('/api/pilot?name=' + encodeURIComponent(name));
  tab = 'Selection'; selShip = null; shipCard = null; docView = null;
  if (pilotCard.seen && sys.has(pilotCard.seen.system)) {
    selected = pilotCard.seen.system; route = pathFromHome(selected);
    const s = sys.get(selected); view.x = s.x; view.y = s.y; if (view.k < 0.12) view.k = 0.2;
    draw();
  }
  renderRoster(); render();
}

function status() {
  const box = $('status'), st = L.stats || {};
  box.replaceChildren();
  const item = (label, value, cls, wide) => { const s = el('span', wide ? 'wide' : null); if (cls) s.append(el('i', 'dot ' + cls)); s.append(label + ' '); s.append(el('b', null, value)); box.append(s); };
  item('Tick', fmt(st.tick)); item('Game', st.version || '?', null, true); item('Online', fmt(st.online_players));
  const liveStream = L.stream || {};
  item('Stream', liveStream.connected ? ago(liveStream.age) + ' ago' : 'down', liveStream.connected && liveStream.age < 60 ? 'good' : 'bad');
  if (S) {
    const bad = Object.entries(S.sources).filter(([, s]) => s.error || s.age < 0).map(([n]) => n);
    item('Sources', bad.length ? 'problem: ' + bad.join(', ') : 'good', bad.length ? 'warn' : 'good');
  }
}

// ---------------------------------------------------------------- chat with the six agents

const chat = { agent: 'unity', after: 0, timer: 0, draft: null, lastText: '', running: false, seq: 0 };
const agentOf = (id) => ((S && S.roster) || []).find((a) => a.id === id) || { id, name: id, division: 'Command' };

function chatLine(cls, text) {
  const log = $('chat-log'), hint = log.querySelector('.chathint'), m = el('div', cls, text);
  if (hint) hint.remove();
  log.append(m); log.scrollTop = log.scrollHeight;
  return m;
}
function bubble(role, text) {
  const m = chatLine('msg ' + (role === 'user' ? 'user' : 'agent'), text);
  if (role !== 'user') m.style.borderLeftColor = DIV[agentOf(chat.agent).division] || DIV.Command;
  return m;
}
function setRunning(on) { chat.running = on; $('chat-send').disabled = on; }

function applyChatEvent(e) {
  const log = $('chat-log');
  if (e.kind === 'delta') {
    if (!chat.draft) chat.draft = bubble('agent', '');
    chat.draft.textContent += e.text;
  } else if (e.kind === 'final') {
    if (chat.draft) chat.draft.textContent = e.text;
    else if (e.text && e.text !== chat.lastText) bubble('agent', e.text);
    chat.lastText = e.text; chat.draft = null;
  } else if (e.kind === 'tool') {
    if (chat.draft) { chat.lastText = chat.draft.textContent; chat.draft = null; }
    chatLine('toolline', '> ' + (e.tool || 'tool') + (e.text ? '  ' + e.text : ''));
  } else if (e.kind === 'tool_done') {
    if (e.failed) chatLine('toolline failed', 'x ' + (e.tool || 'tool') + ' failed');
  } else if (e.kind === 'note') chatLine('toolline', e.text);
  else if (e.kind === 'error') chatLine('msg err', e.text);
  else if (e.kind === 'end') chat.draft = null;
  log.scrollTop = log.scrollHeight;
}

async function pollChat(mine, first) {
  let d = null;
  try { d = await get('/api/chat?agent=' + encodeURIComponent(chat.agent) + '&after=' + chat.after); } catch (e) { d = null; }
  if (mine !== chat.seq) return;
  if (d && !d.error) {
    if (first && !d.running) return;                 // nothing in flight: the history is complete
    for (const e of d.events) { applyChatEvent(e); chat.after = e.n; }
    setRunning(d.running);
    $('chat-state').textContent = d.running ? agentOf(chat.agent).name + ' is working | ' + d.seconds + ' s' : '';
    if (!d.running) return;
  }
  chat.timer = setTimeout(() => pollChat(mine, false), 1000);
}

async function openChat(id) {
  const mine = ++chat.seq, a = agentOf(id), c = DIV[a.division] || DIV.Command, log = $('chat-log');
  clearTimeout(chat.timer);
  chat.agent = id; chat.after = 0; chat.draft = null; chat.lastText = '';
  setRunning(false); $('chat-state').textContent = '';
  document.querySelectorAll('#chat-tabs button').forEach((b) => {
    const on = b.dataset.id === id;
    b.classList.toggle('on', on); b.style.borderBottomColor = on ? c : 'transparent';
  });
  $('chat-input').placeholder = 'Message to ' + a.name + ' (Enter sends, Shift+Enter: new line)';
  log.replaceChildren(el('div', 'chathint', 'Loading the conversation with ' + a.name + '...'));
  let h;
  try { h = await get('/api/chat/history?agent=' + encodeURIComponent(id)); } catch (e) { h = { messages: [], error: e.message }; }
  if (mine !== chat.seq) return;
  log.replaceChildren();
  if (!h.messages || !h.messages.length) {
    log.append(el('div', 'chathint', h.error || 'No conversation with ' + a.name + ' here yet. Your first message starts one. It is separate from your chats in the desktop app.'));
  } else h.messages.forEach((m) => bubble(m.role, m.text));
  log.scrollTop = log.scrollHeight;
  pollChat(mine, true);
}

async function sendChat() {
  const input = $('chat-input'), message = input.value.trim(), mine = chat.seq;
  if (!message || chat.running) return;
  setRunning(true);
  try { await post('/api/chat/send', { agent: chat.agent, text: message }); } catch (e) {
    setRunning(false); chatLine('msg err', 'Not sent: ' + e.message); return;
  }
  if (mine !== chat.seq) return;
  input.value = '';
  bubble('user', message);
  chat.after = 0; chat.draft = null; chat.lastText = '';
  $('chat-state').textContent = agentOf(chat.agent).name + ' is working';
  clearTimeout(chat.timer);
  pollChat(mine, false);
}

async function newChat() {
  if (chat.running) return;
  try { await post('/api/chat/new', { agent: chat.agent }); } catch (e) { chatLine('msg err', e.message); return; }
  openChat(chat.agent);
}

function initChat() {
  const tabs = $('chat-tabs');
  tabs.replaceChildren();
  for (const a of S.roster) {
    const b = el('button', null, a.name);
    b.type = 'button'; b.dataset.id = a.id;
    b.append(el('small', null, a.division));
    b.addEventListener('click', () => openChat(a.id));
    tabs.append(b);
  }
  $('chat-send').addEventListener('click', sendChat);
  $('chat-input').addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); } });
  $('chat-new').addEventListener('click', newChat);
  openChat('unity');
}

// ---------------------------------------------------------------- loading

async function loadState() {
  S = await get('/api/state');
  sys.clear(); stationsBy.clear();
  S.systems.forEach((s) => sys.set(s.id, s));
  S.stations.forEach((t) => { if (!stationsBy.has(t.system)) stationsBy.set(t.system, []); stationsBy.get(t.system).push(t); });
  const legend = $('legend');
  legend.replaceChildren();
  for (const [name, c] of Object.entries(S.empires).concat([['lawless', LAWLESS]])) {
    const span = el('span'), dot = el('i');
    dot.style.background = HEX.test(c) ? c : LAWLESS;
    span.append(dot, name); legend.append(span);
  }
  const ours = el('span'), mark = el('i', 'sq');
  mark.style.background = DIV.Mining;
  ours.append(mark, 'diamond: our ships, by division');
  legend.append(ours, el('span', null, 'ring: station (gold: player faction)'), el('span', null, 'red cross: pirate stronghold'),
    el('span', null, 'glow: pilots seen in the last hour'));
}
async function loadLive() {
  try { L = await get('/api/live'); } catch (e) { L.stream = { connected: false, age: -1 }; }
  status(); draw();
  if (tab === 'Traffic') render();
}
async function loadFleet() {
  try { F = await get('/api/fleet'); fetchedAt = Date.now(); } catch (e) { F = Object.assign({}, F, { age: -1 }); }
  shipsBy.clear();
  F.ships.forEach((r) => { if (r.system) { if (!shipsBy.has(r.system)) shipsBy.set(r.system, []); shipsBy.get(r.system).push(r); } });
  renderResources(); renderRoster(); draw();
  if (tab === 'Metrics') render();
  if (selShip) {
    const name = selShip;
    try {
      const d = await get('/api/ship?name=' + encodeURIComponent(name)), mark = JSON.stringify(d);
      if (selShip === name && mark !== shipMark) { shipMark = mark; shipCard = d; if (tab === 'Selection') render(); }
    } catch (e) { /* keep the last card */ }
  }
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
    b.addEventListener('click', () => { tab = name; if (name !== 'Selection') pilotCard = null; if (name !== 'Docs') docView = null; render(); });
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
      const ours = (shipsBy.get(s.id) || []).length;
      tip.textContent = s.name + (s.empire ? ' (' + s.empire + ')' : '') + ' | ' + (L.hour[s.id] || 0) + ' pilots in the last hour' + (ours ? ' | ' + ours + ' of ours' : '');
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
  $('btn-fleet').addEventListener('click', fitFleet);
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
      F.ships.filter((r) => r.name.toLowerCase().includes(input.value.trim().toLowerCase())).slice(0, 8)
        .forEach((r) => add(r.name, 'our ship', () => selectShip(r.name, true)));
      d.systems.forEach((s) => add(s.name, 'system', () => select(s.id, true)));
      d.pilots.forEach((n) => add(n, 'pilot', () => showPilot(n)));
      if (!results.children.length) results.append(el('button', null, 'Nothing found'));
      results.hidden = false;
    }, 250);
  });
  document.addEventListener('click', (e) => { if (!e.target.closest('.search')) results.hidden = true; });
  window.addEventListener('resize', resize);
}

function fitFleet() {
  const list = [...shipsBy.keys()].map((id) => sys.get(id)).filter(Boolean);
  if (!list.length) { fit(S.systems.filter((s) => s.jumps >= 0 && s.jumps <= 4), 500); return; }
  fit(list.concat(list.flatMap((s) => s.lanes.map((id) => sys.get(id)).filter(Boolean))), 300);
}

(async function main() {
  init();
  await loadState();
  resize();
  await loadFleet();
  fitFleet();
  await loadLive();
  render();
  initChat();
  setInterval(loadLive, 5000);
  setInterval(loadFleet, 5000);
  setInterval(tickAges, 1000);
  setInterval(async () => { await loadState(); draw(); if (tab === 'Docs' && !docView) render(); }, 120000);
})().catch((e) => { $('panel').replaceChildren(el('p', 'empty', 'The station could not load its data: ' + e.message)); });
