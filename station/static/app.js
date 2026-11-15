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

// Ship silhouettes, nose up, in a box of -10..10: a list of parts, each a polygon or a ring. The same
// shapes draw the markers of the map (canvas) and the icons of the roster, the legend and the cards (SVG).
const SHAPES = {
  Flagship: [[[0, -10], [2.6, -5], [2.6, -1], [6.5, 2.5], [6.5, 8], [2.2, 6], [0, 9.5], [-2.2, 6], [-6.5, 8], [-6.5, 2.5], [-2.6, -1], [-2.6, -5]]],
  Guard: [[[0, -9], [7, -6], [7, 1], [0, 9], [-7, 1], [-7, -6]]],
  Mining: [[[-4, -2], [4, -2], [5, 8], [-5, 8]], [[-6.5, -9], [-3.4, -9], [-2.2, -2], [-5.4, -2]], [[6.5, -9], [3.4, -9], [2.2, -2], [5.4, -2]], [[-1.4, -2], [1.4, -2], [0, -6.5]]],
  Trade: [[[0, -9], [5, -5.5], [6.5, 5.5], [3.2, 9], [-3.2, 9], [-6.5, 5.5], [-5, -5.5]]],
  Logistics: [[[-1.4, -9.5], [1.4, -9.5], [1.4, 9.5], [-1.4, 9.5]], [[-6.5, -6.5], [-2.4, -6.5], [-2.4, -2.5], [-6.5, -2.5]], [[6.5, -6.5], [2.4, -6.5], [2.4, -2.5], [6.5, -2.5]],
    [[-6.5, -1], [-2.4, -1], [-2.4, 3], [-6.5, 3]], [[6.5, -1], [2.4, -1], [2.4, 3], [6.5, 3]], [[-6.5, 4.5], [-2.4, 4.5], [-2.4, 8.5], [-6.5, 8.5]], [[6.5, 4.5], [2.4, 4.5], [2.4, 8.5], [6.5, 8.5]]],
  Military: [[[0, -10], [3, 0], [9.5, 7.5], [3, 5.2], [0, 9], [-3, 5.2], [-9.5, 7.5], [-3, 0]]],
  Intel: [[[0, -10], [2, 2.5], [4.6, 8.5], [0, 6.2], [-4.6, 8.5], [-2, 2.5]], { ring: [0, -1.5, 7.6] }],
  Unassigned: [[[0, -8], [6, 7], [-6, 7]]],
};
const KINDS = ['Command', 'Mining', 'Trade', 'Logistics', 'Military', 'Intel', 'Unassigned'];
const kindLabel = (kind) => (kind === 'Command' ? 'the command group' : kind === 'All' ? 'ours' : kind);
function rgba(hex, a) {
  const n = parseInt(hex.slice(1), 16);
  return 'rgba(' + (n >> 16) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')';
}
function shipShape(c, shape, x, y, scale, colour) {     // a silhouette on a canvas
  c.fillStyle = colour; c.strokeStyle = colour;
  for (const part of SHAPES[shape] || SHAPES.Unassigned) {
    c.beginPath();
    if (part.ring) { c.lineWidth = 1.1; c.arc(x + part.ring[0] * scale, y + part.ring[1] * scale, part.ring[2] * scale, 0, 6.2832); c.stroke(); continue; }
    part.forEach((q, i) => (i ? c.lineTo(x + q[0] * scale, y + q[1] * scale) : c.moveTo(x + q[0] * scale, y + q[1] * scale)));
    c.closePath(); c.fill();
  }
}
function shipSvg(shape, colour, size) {                  // the same silhouette as an SVG element
  const NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '-11 -11 22 22'); svg.setAttribute('width', size); svg.setAttribute('height', size);
  svg.setAttribute('class', 'shipicon'); svg.setAttribute('aria-hidden', 'true');
  for (const part of SHAPES[shape] || SHAPES.Unassigned) {
    if (part.ring) {
      const c = document.createElementNS(NS, 'circle');
      c.setAttribute('cx', part.ring[0]); c.setAttribute('cy', part.ring[1]); c.setAttribute('r', part.ring[2]);
      c.setAttribute('fill', 'none'); c.setAttribute('stroke', colour); c.setAttribute('stroke-width', '1.4');
      svg.append(c);
    } else {
      const p = document.createElementNS(NS, 'polygon');
      p.setAttribute('points', part.map((q) => q.join(',')).join(' ')); p.setAttribute('fill', colour);
      svg.append(p);
    }
  }
  return svg;
}
function fleetGroups(list) {                             // our ships at one place, by kind, in the order of KINDS
  const by = new Map();
  list.forEach((r) => { const k = KINDS.includes(r.division) ? r.division : 'Unassigned'; if (!by.has(k)) by.set(k, []); by.get(k).push(r); });
  return KINDS.filter((k) => by.has(k)).map((k) => ({
    kind: k, colour: DIV[k] || DIV.Unassigned, ships: by.get(k),
    shape: k === 'Command' ? (by.get(k).some((r) => r.flagship) ? 'Flagship' : 'Guard') : k,
  }));
}

let S = null;                                  // /api/state
let L = { hour: {}, day: {}, battles: [], stats: {}, stream: {}, groups: [] };
let F = { ships: [], totals: {}, engine: {}, age: -1, birth: null };   // /api/fleet
let fetchedAt = 0;                             // when /api/fleet last answered (ms)
let HIST = { rows: [], at: 0 };                // /api/history, for the Metrics tab
const collapsed = new Set();                   // divisions folded in the roster; remembered by the browser
try { JSON.parse(localStorage.getItem('station.folded') || '[]').forEach((d) => collapsed.add(String(d))); } catch (e) { /* no storage */ }
function saveFolds() { try { localStorage.setItem('station.folded', JSON.stringify([...collapsed])); } catch (e) { /* no storage */ } }
let board = null;
const sys = new Map();
const stationsBy = new Map();
const shipsBy = new Map();                     // system id -> our ships there
const layers = { Lanes: true, Traffic: true, Stations: true, Strongholds: true, Intel: true, Factions: true, Fleet: true, Names: true };
const view = { x: 0, y: 0, k: 0.05 };
let selected = null, hover = null, route = [], tab = 'Selection', pilotCard = null;
let selShip = null, shipCard = null, shipMark = '', docView = null;
const groupsBy = new Map();                    // system id -> the larger groups of one foreign faction seen there
let groupHits = [];                            // their tags as drawn
let pop = null, hoverBadge = null, badgeHits = [];   // the open fleet card {system, kind}; the marker under the pointer; the markers drawn
let cam = null, raf = 0, pulse = 0;                  // an eased move of the view; the frame that is asked for; the timer of the next quiet frame

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

function flyTo(x, y, k, ms) {                       // ease the view to a place; ms 0 jumps
  if (!W || ms === 0) { cam = null; view.x = x; view.y = y; view.k = k; draw(); return; }
  cam = { x0: view.x, y0: view.y, k0: view.k, x1: x, y1: y, k1: k, t0: performance.now(), ms: ms || 520 };
  draw();
}

function fit(list, pad, jump) {
  if (!list.length || !W) return;
  const xs = list.map((s) => s.x), ys = list.map((s) => s.y);
  const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
  flyTo((x0 + x1) / 2, (y0 + y1) / 2, Math.min(3, Math.min(W / (x1 - x0 + pad), H / (y1 - y0 + pad))), jump ? 0 : 650);
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

// A fixed field of stars: [x, y] as fractions of the view, brightness, size.
const STARS = Array.from({ length: 460 }, (_, i) => {
  const a = Math.sin(i * 12.9898) * 43758.5453, b = Math.sin(i * 78.233) * 12543.123;
  return [a - Math.floor(a), b - Math.floor(b), 0.18 + ((i * 7) % 10) / 24, i % 11 === 0 ? 1.7 : i % 3 === 0 ? 1.2 : 0.8];
});

function pill(x, y, w, h) {                          // a rounded marker's outline
  const q = h / 2;
  ctx.beginPath(); ctx.moveTo(x + q, y); ctx.lineTo(x + w - q, y); ctx.arc(x + w - q, y + q, q, -1.5708, 1.5708);
  ctx.lineTo(x + q, y + h); ctx.arc(x + q, y + q, q, 1.5708, 4.7124); ctx.closePath();
}

function draw() { if (!raf) raf = requestAnimationFrame(frame); }   // every caller asks for a frame; frames are joined

function frame(now) {
  raf = 0;
  if (cam) {
    const u = Math.min(1, (now - cam.t0) / cam.ms), e = 1 - Math.pow(1 - u, 3);
    view.x = cam.x0 + (cam.x1 - cam.x0) * e; view.y = cam.y0 + (cam.y1 - cam.y0) * e;
    view.k = Math.exp(Math.log(cam.k0) + (Math.log(cam.k1) - Math.log(cam.k0)) * e);
    if (u >= 1) cam = null;
  }
  paint(now / 1000);
  if (cam) draw();
  else if ((selected || route.length > 1) && !pulse) pulse = setTimeout(() => { pulse = 0; draw(); }, 60);   // the selection breathes, the route line moves
}

function paint(t) {
  if (!S) return;
  ctx.clearRect(0, 0, W, H);
  const k = view.k, r = Math.max(2.2, Math.min(7, 2 + k * 28));
  const px = -view.x * k * 0.05, py = -view.y * k * 0.05;           // the stars drift a little with the view
  for (const [u, v, a, size] of STARS) {
    ctx.fillStyle = 'rgba(186,198,232,' + a.toFixed(2) + ')';
    ctx.fillRect((((u * W + px) % W) + W) % W, (((v * H + py) % H) + H) % H, size, size);
  }
  if (layers.Lanes) {
    const strokes = new Map();                                      // one path per colour
    for (const s of S.systems) {
      const [ax, ay] = toScreen(s);
      for (const id of s.lanes) {
        const o = sys.get(id);
        if (!o || s.id >= id) continue;
        const c = s.empire && s.empire === o.empire ? rgba(color(s), 0.3) : 'rgba(125,135,170,0.17)';
        if (!strokes.has(c)) strokes.set(c, []);
        strokes.get(c).push(ax, ay, ...toScreen(o));
      }
    }
    ctx.lineWidth = 1;
    for (const [c, seg] of strokes) {
      ctx.strokeStyle = c; ctx.beginPath();
      for (let i = 0; i < seg.length; i += 4) { ctx.moveTo(seg[i], seg[i + 1]); ctx.lineTo(seg[i + 2], seg[i + 3]); }
      ctx.stroke();
    }
  }
  if (route.length > 1) {                                           // the way from home: a soft band and a moving dash
    const line = () => { ctx.beginPath(); route.forEach((id, i) => { const [x, y] = toScreen(sys.get(id)); if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y); }); ctx.stroke(); };
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.strokeStyle = 'rgba(164,139,224,0.22)'; ctx.lineWidth = 6; line();
    ctx.strokeStyle = '#b9a4ec'; ctx.lineWidth = 1.8; ctx.setLineDash([7, 7]); ctx.lineDashOffset = -t * 16; line();
    ctx.setLineDash([]); ctx.lineCap = 'butt';
  }
  if (layers.Traffic) {
    for (const s of S.systems) {
      const n = L.hour[s.id] || 0;
      if (!n) continue;
      const [x, y] = toScreen(s);
      ctx.fillStyle = 'rgba(220,174,88,0.13)';
      ctx.beginPath(); ctx.arc(x, y, r + 3 + Math.sqrt(n) * 2.6, 0, 6.2832); ctx.fill();
    }
  }
  ctx.font = '11px system-ui, sans-serif';
  for (const s of S.systems) {
    const [x, y] = toScreen(s);
    if (x < -40 || y < -40 || x > W + 40 || y > H + 40) continue;
    const c = color(s), q = s.home ? r + 2 : r, ours = layers.Fleet && shipsBy.has(s.id);
    ctx.fillStyle = rgba(c, 0.16); ctx.beginPath(); ctx.arc(x, y, q * 2.3, 0, 6.2832); ctx.fill();      // glow
    ctx.fillStyle = c; ctx.beginPath(); ctx.arc(x, y, q, 0, 6.2832); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.5)'; ctx.beginPath(); ctx.arc(x - q * 0.28, y - q * 0.28, q * 0.34, 0, 6.2832); ctx.fill();
    if (layers.Stations && stationsBy.has(s.id)) {
      ctx.strokeStyle = stationsBy.get(s.id).some((b) => b.tag) ? 'rgba(232,195,90,0.9)' : 'rgba(207,211,230,0.75)'; ctx.lineWidth = 1.1;
      ctx.beginPath(); ctx.arc(x, y, q + 3.5, 0, 6.2832); ctx.stroke();
    }
    if (layers.Strongholds && s.stronghold) {
      ctx.strokeStyle = '#e06c66'; ctx.lineWidth = 1.8; ctx.lineCap = 'round'; ctx.beginPath();
      ctx.moveTo(x - q - 4, y - q - 4); ctx.lineTo(x + q + 4, y + q + 4);
      ctx.moveTo(x + q + 4, y - q - 4); ctx.lineTo(x - q - 4, y + q + 4); ctx.stroke(); ctx.lineCap = 'butt';
    }
    const intel = layers.Intel && S.intel.systems[s.id];
    if (intel && intel.standing !== 'neutral') {                    // our standing: a dashed ring, green or red
      ctx.strokeStyle = intel.standing === 'ally' ? 'rgba(88,192,140,0.85)' : 'rgba(224,108,102,0.9)'; ctx.lineWidth = 1.4;
      ctx.setLineDash([3, 3]); ctx.beginPath(); ctx.arc(x, y, q + 7, 0, 6.2832); ctx.stroke(); ctx.setLineDash([]);
    }
    if (ours) {                                                     // our ships are here: a quiet ring
      ctx.strokeStyle = shipsBy.get(s.id).some((sh) => sh.name === selShip) ? '#ffffff' : 'rgba(227,230,238,0.5)'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(x, y, q + 10.5, 0, 6.2832); ctx.stroke();
    }
    if (s.id === selected) {
      const beat = (Math.sin(t * 2.6) + 1) / 2;
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1.8;
      ctx.beginPath(); ctx.arc(x, y, q + 13.5, 0, 6.2832); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,' + (0.3 * (1 - beat)).toFixed(2) + ')'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(x, y, q + 14 + beat * 9, 0, 6.2832); ctx.stroke();
    }
    if (layers.Names && (k > 0.16 || s.home || ours || s.id === selected || s.id === hover)) {
      ctx.font = (s.home || ours ? '600 ' : '') + '11px system-ui, sans-serif';
      ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(9,12,18,0.85)'; ctx.lineJoin = 'round';
      ctx.strokeText(s.name, x + q + 6, y + 4);
      ctx.fillStyle = s.home || ours ? '#f1f3f9' : '#a9b0c9';
      ctx.fillText(s.name, x + q + 6, y + 4);
    }
  }
  badgeHits = []; groupHits = [];
  if (layers.Factions) {                                            // the larger groups of one foreign faction: a tag and a count under the system
    ctx.font = '600 10.5px system-ui, sans-serif'; ctx.textBaseline = 'middle';
    for (const [id, list] of groupsBy) {
      const s = sys.get(id);
      if (!s) continue;
      const [x, y] = toScreen(s);
      if (x < -60 || y < -40 || x > W + 60 || y > H + 20) continue;
      const q = s.home ? r + 2 : r, show = list.filter((g) => k >= 0.12 || g.count >= 8).slice(0, 2);
      show.forEach((g, i) => {
        const label = g.tag + ' ' + g.count, w = ctx.measureText(label).width + 14, gx = x - w / 2, gy = y + q + 9 + i * 18;
        const c = g.standing === 'hostile' ? '#e06c66' : g.standing === 'ally' ? '#58c08c' : '#dcae58';
        pill(gx, gy, w, 15);
        ctx.fillStyle = 'rgba(15,20,31,0.9)'; ctx.fill();
        ctx.strokeStyle = rgba(c, 0.7); ctx.lineWidth = 1; ctx.stroke();
        ctx.fillStyle = c; ctx.fillText(label, gx + 7, gy + 8);
        groupHits.push({ x: gx, y: gy, w, h: 15, system: id, group: g });
      });
    }
    ctx.textBaseline = 'alphabetic';
  }
  if (layers.Fleet) {                                               // our ships: one small pie per system, a slice per division, the count beside it
    ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
    ctx.font = '650 10.5px system-ui, sans-serif';
    const rows = [];
    for (const [id, list] of shipsBy) {
      const s = sys.get(id);
      if (!s) continue;
      const [x, y] = toScreen(s);
      if (x < -60 || y < -20 || x > W + 60 || y > H + 80) continue;
      const R = Math.max(4.5, Math.min(7, r));                      // zoomed in it is as large as the system's dot, never larger
      rows.push({ id, x, y, R, list, cy: y - r - 12 - R });
    }
    rows.sort((a, b) => b.y - a.y);                                 // the lowest system first: a pie that would cover another moves up
    const placed = [];
    for (const row of rows) {
      const { id, x, R, list } = row, groups = fleetGroups(list), n = list.length, label = String(n);
      row.w = ctx.measureText(label).width;                         // a pie and its number are one box
      const covers = (b) => Math.abs(b.cy - row.cy) < b.R + R + 5 && x - R - 3 < b.x + b.R + 7 + b.w && b.x - b.R - 3 < x + R + 7 + row.w;
      for (let tries = 0; tries < 12 && placed.some(covers); tries++) row.cy -= 9;
      placed.push(row);
      const cy = row.cy;
      const open = pop && pop.system === id, hot = hoverBadge && hoverBadge.system === id;
      ctx.strokeStyle = 'rgba(213,218,230,0.28)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(x, cy + R + 2); ctx.lineTo(x, row.y - r - 4); ctx.stroke();
      ctx.fillStyle = 'rgba(11,15,24,0.95)';
      ctx.beginPath(); ctx.arc(x, cy, R + 1.5, 0, 6.2832); ctx.fill();
      let from = -1.5708;
      for (const g of groups) {
        const to = from + 6.2832 * g.ships.length / n;
        ctx.fillStyle = g.colour; ctx.beginPath(); ctx.moveTo(x, cy); ctx.arc(x, cy, R, from, to); ctx.closePath(); ctx.fill();
        from = to;
      }
      if (open || hot || list.some((sh) => sh.name === selShip)) {  // open, under the pointer, or the ship in the panel is here
        ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.arc(x, cy, R + 3, 0, 6.2832); ctx.stroke();
      }
      ctx.lineWidth = 3; ctx.lineJoin = 'round'; ctx.strokeStyle = 'rgba(11,15,24,0.92)'; ctx.strokeText(label, x + R + 4, cy + 0.5);
      ctx.fillStyle = '#eef0f6'; ctx.fillText(label, x + R + 4, cy + 0.5);
      badgeHits.push({ x: x - R - 4, y: cy - R - 5, w: 2 * R + 10 + row.w, h: 2 * R + 10, system: id, kind: 'All', count: n,
        parts: groups.map((g) => g.ships.length + ' ' + (g.kind === 'Command' ? 'command group' : g.kind)).join(', ') });
    }
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  }
  placePop();
}

function groupAt(mx, my) {
  for (let i = groupHits.length - 1; i >= 0; i--) {
    const b = groupHits[i];
    if (mx >= b.x && mx <= b.x + b.w && my >= b.y && my <= b.y + b.h) return b;
  }
  return null;
}

function badgeAt(mx, my) {
  for (let i = badgeHits.length - 1; i >= 0; i--) {
    const b = badgeHits[i];
    if (mx >= b.x && mx <= b.x + b.w && my >= b.y && my <= b.y + b.h) return b;
  }
  return null;
}

// ---------------------------------------------------------------- the fleet card over the map

function openPop(system, kind) { pop = { system, kind }; renderPop(); draw(); }
function closePop() { pop = null; $('fleetpop').hidden = true; draw(); }

function placePop() {                                // the card stays beside its system while the view moves
  const box = $('fleetpop');
  if (!pop || box.hidden || !sys.has(pop.system)) return;
  const [x, y] = toScreen(sys.get(pop.system)), w = box.offsetWidth, h = box.offsetHeight;
  const left = x + 30 + w <= W - 8 ? x + 30 : Math.max(8, x - 30 - w);
  box.style.left = Math.round(left) + 'px';
  box.style.top = Math.round(Math.max(8, Math.min(H - h - 8, y - h / 3))) + 'px';
}

function renderPop() {
  const box = $('fleetpop');
  if (!pop) { box.hidden = true; return; }
  const s = sys.get(pop.system), all = fleetGroups(shipsBy.get(pop.system) || []);
  const groups = pop.kind === 'All' ? all : all.filter((g) => g.kind === pop.kind);
  if (!s || !groups.length) { closePop(); return; }                // the ships have left
  const ships = groups.flatMap((g) => g.ships), body = box.querySelector('.popbody'), keep = body ? body.scrollTop : 0;
  const head = el('div', 'pophead'), title = el('div', 'poptitle'), close = el('button', 'popclose', '\u00d7');
  const one = groups.length === 1 ? groups[0] : null;
  head.append(shipSvg(one ? one.shape : all[0].shape, one ? one.colour : '#e3e6ee', 26));
  title.append(el('b', null, one ? (one.kind === 'Command' ? 'Command group' : one.kind) : 'Our ships'),
    el('span', null, 'at ' + s.name + (one && one.ships[0].admiral ? ' | Adm. ' + one.ships[0].admiral : '')));
  close.type = 'button'; close.title = 'Close (Esc)'; close.addEventListener('click', closePop);
  head.append(title, close);
  const low = (a, b) => ships.reduce((m, r) => Math.min(m, r[b] > 0 ? Math.round(100 * r[a] / r[b]) : 100), 100);
  const stats = el('div', 'popstats'), n = {};
  for (const [label, value, bad] of [['Ships', ships.length], ['Credits', fmt(ships.reduce((a, r) => a + r.credits, 0))],
    ['Lowest hull', low('hull', 'max_hull') + '%', low('hull', 'max_hull') < 50], ['Lowest fuel', low('fuel', 'max_fuel') + '%', low('fuel', 'max_fuel') < 25]]) {
    const cell = el('div', bad ? 'bad' : null);
    cell.append(el('div', 'k', label), el('div', 'v', String(value)));
    stats.append(cell);
  }
  ships.forEach((r) => { const w = shipState(r)[1]; n[w] = (n[w] || 0) + 1; });
  const doing = el('div', 'popdoing', Object.entries(n).sort((a, b) => b[1] - a[1]).slice(0, 4).map(([w, c]) => c + ' ' + w).join(', '));
  const list = el('div', 'popbody');
  const row = (r) => {
    const b = el('button', 'poprow'), who = el('div', 'who'), nm = el('div', 'nm', r.name), bars = el('div', 'bars');
    b.type = 'button';
    if (r.flagship) { const f = el('span', 'flag', '\u2605' + (r.flagship_of ? ' ' + r.flagship_of : '')); nm.append(f); }
    who.append(nm, el('div', 'at', shipState(r)[1]));
    bars.append(bar('hull', r.hull, r.max_hull, 0.5), bar('fuel', r.fuel, r.max_fuel, 0.25), bar('cargo', r.cargo_used, r.cargo_capacity));
    b.append(who, bars, el('div', 'cr', fmt(r.credits)));
    b.title = 'Open ' + r.name;
    b.addEventListener('click', () => { closePop(); selectShip(r.name, false); });
    return b;
  };
  for (const g of groups) {
    const parts = g.kind === 'Command'
      ? [['Flagships', g.ships.filter((r) => r.flagship), 'Flagship'], ['Guard', g.ships.filter((r) => !r.flagship), 'Guard']]
      : [[g.kind, g.ships, g.shape]];
    for (const [label, rows, shape] of parts) {
      if (!rows.length) continue;
      const sec = el('div', 'popsec');
      sec.append(shipSvg(shape, g.colour, 13), label + ' ', el('b', null, String(rows.length)));
      list.append(sec);
      rows.forEach((r) => list.append(row(r)));
    }
  }
  const foot = el('div', 'popfoot'), go = el('button', 'poplink', 'Open ' + s.name);
  go.type = 'button'; go.addEventListener('click', () => { closePop(); select(s.id, false); });
  foot.append(go, el('span', null, 'fleet data ' + fleetAgeText()));
  box.replaceChildren(head, stats, doing, list, foot);
  box.hidden = false;
  list.scrollTop = keep;
  placePop();
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
  if (a.kind === 'order') return ['work', a.type];
  if (a.kind === 'goal' || a.kind === 'job') return ['work', r.order ? r.order + ': ' + a.type : a.type];
  return r.docked ? ['dock', 'parked'] : ['idle', 'idle in space'];
}

function signed(n) { return (n > 0 ? '+' : '') + fmt(n); }
function tint(n) { return el('span', n < 0 ? 'neg' : n > 0 ? 'pos' : null, signed(n)); }   // a signed number: green above zero, red below
function shade(n, cls) { return el('span', n > 0 ? cls : null, fmt(n)); }                  // an amount without a sign: income green, a cost red
function liveAge() { return F.age < 0 ? -1 : F.age + Math.round((Date.now() - fetchedAt) / 1000); }

function isWorking(r) { return ['work', 'move', 'wait'].includes(shipState(r)[0]); }

function renderMembers() {                       // the top bar: the six members, each with its symbol and its ships; then the fleet
  const box = $('members'), by = new Map();
  box.replaceChildren();
  F.ships.forEach((r) => { if (!by.has(r.division)) by.set(r.division, []); by.get(r.division).push(r); });
  for (const a of (S ? S.roster : [])) {
    const list = by.get(a.division) || [], c = DIV[a.division] || DIV.Unassigned, b = el('button', 'member');
    const working = list.filter(isWorking).length, who = el('div', 'who');
    b.type = 'button';
    who.append(el('div', 'n', a.name), el('div', 'd', a.division));
    b.append(shipSvg(a.division === 'Command' ? 'Flagship' : a.division, c, 20), who, el('div', 'c', String(list.length)));
    b.style.setProperty('--c', c);
    b.title = a.name + ', ' + a.rank + ' | ' + a.division + ': ' + list.length + ' ships, ' + working + ' working, '
      + (list.length - working) + ' without work | click to write to ' + a.name;
    b.addEventListener('click', () => address(a.id));
    box.append(b);
  }
  const t = F.totals || {}, all = el('div', 'member total'), who = el('div', 'who');
  who.append(el('div', 'n', 'Fleet'), el('div', 'd', t.ships ? (t.working || 0) + ' working' : 'no data'));
  all.append(who, el('div', 'c', fmt(t.ships)));
  all.title = 'All ships: ' + fmt(t.working) + ' working, ' + fmt(t.parked) + ' parked at a station without work, ' + fmt(t.adrift) + ' in space without work';
  box.append(all);
}

function fleetAgeText() {
  const age = liveAge();
  return age < 0 ? 'no data' : ago(age) + ' ago';
}
function fleetLive() { const age = liveAge(); return Boolean(F.engine && F.engine.ok && age >= 0 && age < 60); }

function tickAges() {                          // every second: the one age label counts up between polls
  const b = $('fleet-age');
  if (!b) return;
  b.textContent = fleetAgeText();
  const dot = b.parentElement.querySelector('.dot');
  if (dot) dot.className = 'dot ' + (fleetLive() ? 'good' : 'bad');
}

function shipRow(r) {
  const [cls, what] = shipState(r), b = el('button', 'ship' + (r.name === selShip ? ' on' : ''));
  b.type = 'button';
  const who = el('div', 'who'), bars = el('div', 'bars'), cr = el('div', 'cr', fmt(r.credits));
  const nm = el('div', 'nm', r.name);
  if (r.flagship) {                               // a star after the name: a word would be cut off behind a long name
    const of = r.flagship_of || r.admiral || '';
    const flag = el('span', 'flag', '\u2605' + (of && of !== r.admiral ? ' ' + of : ''));
    flag.title = 'Flagship' + (of ? ' of ' + of : '');
    nm.append(flag);
  }
  who.append(nm, el('div', 'at', (r.system_name || r.system || 'position unknown') + ' | ' + what));
  bars.append(bar('hull', r.hull, r.max_hull, 0.5), bar('fuel', r.fuel, r.max_fuel, 0.25), bar('cargo', r.cargo_used, r.cargo_capacity));
  const best = r.top_skill || ['', 0];
  cr.append(el('small', null, best[1] ? best[0].replace(/_/g, ' ') + ' ' + best[1] : (r.class || '')));
  b.append(el('i', 'glyph ' + cls), who, bars, cr);
  b.title = r.name + ': hull ' + r.hull + '/' + r.max_hull + ', fuel ' + r.fuel + '/' + r.max_fuel + ', cargo ' + r.cargo_used + '/' + r.cargo_capacity;
  b.addEventListener('click', () => selectShip(r.name, true));
  return b;
}

function renderRoster() {
  const box = $('roster'), keep = box.scrollTop, by = new Map();
  box.replaceChildren();
  F.ships.forEach((r) => { if (!by.has(r.division)) by.set(r.division, []); by.get(r.division).push(r); });
  const divisions = (S ? S.roster : []).filter((a) => a.division !== 'Command' || by.has('Command')).map((a) => [a.division, a]);
  if (by.has('Unassigned')) divisions.push(['Unassigned', null]);
  for (const [division, admiral] of divisions) {
    const list = by.get(division) || [], block = el('div', 'div'), head = el('div', 'divhead'), c = DIV[division] || DIV.Unassigned;
    const folded = collapsed.has(division), sum = el('span', 'sum');
    const name = el('button', 'name', division), fold = el('span', 'fold', folded ? '+' : '-');
    name.type = 'button';
    name.prepend(fold);
    fold.after(shipSvg(division === 'Command' ? 'Flagship' : division, c, 13));
    name.append(el('b', 'count', String(list.length)));
    head.style.borderLeftColor = c; name.style.color = c;
    name.title = (folded ? 'Unfold' : 'Fold') + ' the ' + list.length + ' ships of ' + division;
    name.setAttribute('aria-expanded', folded ? 'false' : 'true');
    name.addEventListener('click', () => { if (collapsed.has(division)) collapsed.delete(division); else collapsed.add(division); saveFolds(); renderRoster(); });
    head.append(name);
    if (admiral) {
      const b = linkButton('Adm. ' + admiral.name, () => address(admiral.id), 'adm');
      b.title = 'Write to ' + admiral.name + ' in comms';
      head.append(b);
    }
    if (list.length) {
      const dr = ((F.totals.rates || {}).divisions || {})[division];
      sum.append(el('b', null, fmt(list.reduce((a, r) => a + r.credits, 0))), ' cr');
      if (dr) sum.append('  ', el('b', dr.cph < 0 ? 'neg' : dr.cph > 0 ? 'pos' : null, signed(dr.cph)), ' /h');
    }
    head.append(sum); block.append(head);
    if (!list.length) block.append(el('div', 'noships', 'No ships yet'));
    if (!folded) list.forEach((r) => block.append(shipRow(r)));
    else if (list.length) {                     // folded: the division in one line
      const n = { work: 0, move: 0, dock: 0, idle: 0, wait: 0, bad: 0, off: 0 };
      list.forEach((r) => { n[shipState(r)[0]] += 1; });
      const parts = [[n.work + n.move, 'working'], [n.wait, 'waiting'], [n.dock, 'parked'], [n.idle, 'idle in space'], [n.bad, 'failing'], [n.off, 'offline']];
      const line = el('button', 'divline', parts.filter((p) => p[0]).map((p) => p[0] + ' ' + p[1]).join(', '));
      line.type = 'button';
      line.title = 'Unfold ' + division;
      line.addEventListener('click', () => { collapsed.delete(division); saveFolds(); renderRoster(); });
      block.append(line);
    }
    box.append(block);
  }
  box.scrollTop = keep;
  const all = $('fold-all'), names = divisions.map((d) => d[0]), everyFolded = names.length > 0 && names.every((d) => collapsed.has(d));
  all.textContent = everyFolded ? 'Unfold all' : 'Fold all';
  all.onclick = () => { names.forEach((d) => (everyFolded ? collapsed.delete(d) : collapsed.add(d))); saveFolds(); renderRoster(); };
  const fresh = $('fleet-fresh'), ok = fleetLive();
  fresh.textContent = ok ? F.ships.length + ' ships' : (F.age < 0 ? 'no data' : 'stale');
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
  const skills = Object.entries(d.skills || {}).sort((x, y) => (y[1].level - x[1].level) || (y[1].xp - x[1].xp));
  panel.append(el('h3', null, 'Levels'));
  if (!skills.length) panel.append(el('p', 'empty', 'No skill trained yet.'));
  else {
    const lv = el('div', 'levels');
    for (const [k, v] of skills) {
      const row = el('div', 'lv'), b = el('div', 'bar xp'), i = el('i');
      i.style.width = pct(v.xp, v.next) + '%'; b.append(i);
      row.title = k.replace(/_/g, ' ') + ': level ' + v.level + ', ' + fmt(v.xp) + ' of ' + fmt(v.next) + ' XP to the next level';
      row.append(el('span', 'n', k.replace(/_/g, ' ')), el('b', null, String(v.level)), b);
      lv.append(row);
    }
    panel.append(lv);
  }
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
  panel.append(el('h3', null, 'Service record'));
  panel.append(facts(Object.entries(d.stats || {}).map(([k, v]) => [k.replace(/_/g, ' '), fmt(v)])));
}

async function selectShip(name, center) {
  selShip = name; shipCard = null; shipMark = ''; pilotCard = null; docView = null; tab = 'Selection';
  const row = F.ships.find((r) => r.name === name);
  if (row && sys.has(row.system)) {
    selected = row.system; route = pathFromHome(selected);
    if (center) { const s = sys.get(selected); flyTo(s.x, s.y, view.k < 0.12 ? 0.35 : view.k); }
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
    panel.append(table(['Ship', 'Doing', 'Cargo'], ours.slice(0, 12).map((r) => [shipLink(r.name), shipState(r)[1], r.cargo_used + ' / ' + r.cargo_capacity])));
    if (ours.length > 12) panel.append(linkButton('All ' + ours.length + ' ships: open the card', () => openPop(s.id, 'All')));
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
    box.append(el('h3', null, 'Foreign factions here, last hour'));
    if (d.groups.length) {
      box.append(table(['Tag', 'Faction', 'Pilots', 'Standing'], d.groups.map((g) => [g.tag, g.name || '', g.count, g.standing]), [2]));
    } else box.append(el('p', 'empty', 'No faction had two or more pilots jump here in the last hour.'));
    box.append(el('p', 'sub', fmt(d.pilot_count) + ' pilots of any kind made their last jump here in the last 24 h.'));
    if (d.battles.length) {
      box.append(el('h3', null, 'Recent battles'));
      box.append(table(['Kind', 'Pilots', 'Lost'], d.battles.map((b) => [b.category, b.pilots.join(', '), b.lost.join(', ')])));
    }
    if (d.intel) {
      box.append(el('h3', null, 'Intel'));
      box.append(markdown(d.intel_text, d.intel.file, false));
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

function setWide(on) {                          // a document gets a wide panel; the map is resized to what is left
  const right = $('main-right');
  if (right.classList.contains('wide') === on) return;
  right.classList.toggle('wide', on);
  resize();
}

async function openDoc(path) {
  tab = 'Docs'; selShip = null; shipCard = null; docView = { path, text: '', loading: true };
  renderRoster(); render();
  try { docView = await get('/api/doc?path=' + encodeURIComponent(path)); } catch (e) { docView = { path, error: e.message }; }
  if (tab === 'Docs') render();
}

// ---- Markdown and logs as formatted text. Everything is built from DOM nodes with textContent; no HTML is parsed.
const DOC_RE = /^(reports|communications|governance|game\/(planets|players|factions|rules|routes\/guidebook|routes|fleet))\/[A-Za-z0-9_.\-]{1,120}\.(md|log)$/;
function docTarget(target, base) {              // a link or a quoted path that names a document the station shows
  let t = String(target).split('#')[0];
  if (!t || t.includes('://') || t.startsWith('/')) return null;
  if (!t.includes('/') && base && base.includes('/')) t = base.slice(0, base.lastIndexOf('/') + 1) + t;
  return DOC_RE.test(t) ? t : null;
}
function inline(parent, text, base) {           // `code`, **bold**, [label](target)
  const re = /(`[^`\n]+`|\*\*[^*\n]+\*\*|\[[^\]\n]+\]\([^)\s]+\))/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) parent.append(text.slice(last, m.index));
    const t = m[0];
    if (t[0] === '`') {
      const body = t.slice(1, -1), path = docTarget(body, '');
      if (path) parent.append(linkButton(body, () => openDoc(path), 'doclink code')); else parent.append(el('code', null, body));
    } else if (t[0] === '*') parent.append(el('b', null, t.slice(2, -2)));
    else {
      const k = t.indexOf(']('), label = t.slice(1, k), path = docTarget(t.slice(k + 2, -1), base);
      if (path) parent.append(linkButton(label, () => openDoc(path), 'doclink')); else parent.append(label);
    }
    last = m.index + t.length;
  }
  if (last < text.length) parent.append(text.slice(last));
  return parent;
}
function mdTable(rows, base) {
  const wrap = el('div', 'mdtable'), t = el('table');
  const cells = (line) => line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());
  rows.forEach((line, n) => {
    if (n === 1) return;                         // the |---|---| line
    const tr = el('tr');
    cells(line).forEach((c) => tr.append(inline(el(n === 0 ? 'th' : 'td'), c, base)));
    t.append(tr);
  });
  wrap.append(t);
  return wrap;
}
function markdown(text, base, hard) {            // hard: every line is its own paragraph (log entries)
  const out = el('div', 'md'), lines = String(text).replace(/\r/g, '').split('\n');
  let i = 0;
  if (lines[0] && lines[0].trim() === '---') {   // frontmatter: one quiet line
    const meta = [];
    for (i = 1; i < lines.length && lines[i].trim() !== '---'; i++) {
      const m = /^(name|author|tier|id|status|updated|standing|threat):\s*(.+)$/.exec(lines[i]);
      if (m) meta.push(m[1] + ' ' + m[2]);
    }
    i++;
    if (meta.length) out.append(el('div', 'mdmeta', meta.join('  |  ')));
  }
  const isBullet = (l) => /^\s*([-*]|\d+\.)\s+/.test(l), isBlock = (l) => /^(#{1,5}\s|```|>|\|)/.test(l) || /^-{3,}\s*$/.test(l) || isBullet(l);
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    if (line.startsWith('```')) {
      const code = [];
      for (i++; i < lines.length && !lines[i].startsWith('```'); i++) code.push(lines[i]);
      i++; out.append(el('pre', null, code.join('\n'))); continue;
    }
    const h = /^(#{1,5})\s+(.*)$/.exec(line);
    if (h) { out.append(inline(el('div', 'mdh mdh' + h[1].length), h[2], base)); i++; continue; }
    if (/^-{3,}\s*$/.test(line)) { out.append(el('hr')); i++; continue; }
    if (line.startsWith('|') && /^\|?[\s:|-]+\|?\s*$/.test(lines[i + 1] || '')) {
      const rows = [];
      for (; i < lines.length && lines[i].startsWith('|'); i++) rows.push(lines[i]);
      out.append(mdTable(rows, base)); continue;
    }
    if (isBullet(line)) {
      const ul = el('ul');
      while (i < lines.length && (isBullet(lines[i]) || (/^\s{2,}\S/.test(lines[i]) && ul.lastChild))) {
        if (isBullet(lines[i])) {
          const m = /^(\s*)([-*]|\d+\.)\s+(.*)$/.exec(lines[i]), li = el('li', m[1].length >= 2 ? 'sub' : null);
          if (/\d/.test(m[2])) li.dataset.n = m[2];
          li.dataset.text = m[3]; ul.append(li);
        } else ul.lastChild.dataset.text += ' ' + lines[i].trim();
        i++;
      }
      for (const li of ul.children) { if (li.dataset.n) li.append(el('span', 'num', li.dataset.n + ' ')); inline(li, li.dataset.text, base); delete li.dataset.text; }
      out.append(ul); continue;
    }
    if (line.startsWith('>')) {
      const q = [];
      for (; i < lines.length && lines[i].startsWith('>'); i++) q.push(lines[i].replace(/^>\s?/, ''));
      out.append(inline(el('blockquote'), q.join(' '), base)); continue;
    }
    const para = [line.trim()];
    for (i++; !hard && i < lines.length && lines[i].trim() && !isBlock(lines[i]); i++) para.push(lines[i].trim());
    const p = inline(el('p'), para.join(' '), base);
    if (/^@[A-Za-z]+:/.test(para[0])) p.className = 'ask';
    out.append(p);
  }
  return out;
}
function logView(text, cut, base) {              // an append-only log as entry cards, newest first
  const out = el('div', 'entries'), parts = String(text).split(/^(?=## \[ENT-\d+\])/m);
  const entries = parts.filter((p) => p.startsWith('## [ENT-'));
  if (!entries.length) { out.append(markdown(text, base, true)); return out; }
  for (const raw of entries.reverse()) {
    const nl = raw.indexOf('\n'), head = (nl < 0 ? raw : raw.slice(0, nl)).replace(/^## /, '').split('|').map((s) => s.trim());
    const card = el('div', 'entry'), top = el('div', 'entryhead'), who = head[2] || '';
    const member = ((S && S.roster) || []).find((a) => a.name === who);
    const name = el('b', null, who || 'unknown');
    name.style.color = member ? (DIV[member.division] || DIV.Command) : 'var(--dim)';
    card.style.borderLeftColor = member ? (DIV[member.division] || DIV.Command) : 'var(--line2)';
    top.append(name, el('span', 'tag', head[0].replace(/[[\]]/g, '')), el('span', 'tag' + (head[3] === 'error' ? ' bad' : ''), head[3] || ''), el('span', 'when', head[1] || ''));
    const refs = head.slice(4).filter(Boolean);
    card.append(top);
    if (refs.length) card.append(inline(el('div', 'entryrefs'), refs.map((r) => r.replace(/^(ref|see):\s*(\S+)/, (m, k, v) => k + ': `' + v + '`')).join('   '), ''));
    card.append(markdown(nl < 0 ? '' : raw.slice(nl + 1), base, true));
    out.append(card);
  }
  return out;
}

function docTitle(path) {                         // a file's short name: governance/map.md -> Map
  const stem = String(path).split('/').pop().replace(/\.(md|log)$/, '').replace(/[-_]/g, ' ');
  return stem.charAt(0).toUpperCase() + stem.slice(1);
}

async function renderDocs(panel, live) {
  setWide(Boolean(docView));
  if (docView) {
    panel.append(linkButton('Back to the list', () => { docView = null; render(); }), el('h2', null, docView.title || docTitle(docView.path)));
    if (docView.loading) panel.append(el('p', 'empty', 'Loading...'));
    else if (docView.error) panel.append(el('p', 'empty', docView.error));
    else {
      const isLog = docView.path.endsWith('.log');
      if (docView.cut) panel.append(el('p', 'sub', isLog ? 'Long log: the newest part is shown.' : 'Long file: the first part is shown.'));
      panel.append(isLog ? logView(docView.text, docView.cut, docView.path) : markdown(docView.text, docView.path, false));
    }
    return;
  }
  const d = await get('/api/docs');
  if (!live()) return;
  const row = (label, small, path) => { const b = linkButton(label, () => openDoc(path), 'rowlink'); if (small) b.append(el('small', null, small)); return b; };
  panel.append(el('h3', null, 'Governance'));
  (d.governance || []).forEach((g) => panel.append(row(g.title, '', g.path)));
  panel.append(el('h3', null, 'Reports'));
  if ((d.reports || []).length) d.reports.forEach((r) => panel.append(row(r.title, [r.author, r.date].filter(Boolean).join(', '), r.path)));
  else panel.append(el('p', 'empty', 'No report yet. One is written at every session end.'));
  panel.append(el('h3', null, 'Logs'));
  (d.logs || []).forEach((g) => panel.append(row(g.title, g.entries ? g.entries + ' entries, last by ' + g.last.by + ', ' + g.last.at : 'no entries', g.path)));
  panel.append(el('h3', null, 'Fleet knowledge'));
  (d.knowledge || []).forEach((g) => panel.append(row(g.title, '', g.path)));
  panel.append(el('h3', null, 'Station data sources'));
  panel.append(table(['Source', 'Last good', 'Problem'],
    Object.entries(S.sources).map(([n, s]) => [n, ago(s.age) + (s.age < 0 ? '' : ' ago'), s.error])));
}

function chart(label, series) {                  // series: [{ pts: [[t, value], ...], colour, name }] on one scale
  const c = el('canvas', 'chart'), wrap = el('div', 'chartbox'), head = el('div', 'chartlabel', label);
  series.filter((s) => s.name).forEach((s) => { const key = el('span', 'key', s.name); key.style.color = s.colour; head.append(key); });
  wrap.append(head, c);
  requestAnimationFrame(() => {
    const w = c.clientWidth || 340, h = 90, d = window.devicePixelRatio || 1, g = c.getContext('2d');
    c.width = w * d; c.height = h * d; g.scale(d, d);
    const lines = series.map((s) => s.pts.filter((p) => p[1] !== null && p[1] !== undefined && isFinite(p[1]))), flat = lines.flat();
    if (flat.length < 2) { g.fillStyle = '#5c6780'; g.font = '12px system-ui'; g.fillText('Not enough samples yet', 8, 48); return; }
    const t0 = Math.min(...flat.map((p) => p[0])), t1 = Math.max(...flat.map((p) => p[0]));
    let lo = Math.min(0, ...flat.map((p) => p[1])), hi = Math.max(0, ...flat.map((p) => p[1]));
    if (hi === lo) hi = lo + 1;
    const X = (t) => 4 + (w - 8) * (t - t0) / Math.max(1, t1 - t0), Y = (v) => h - 14 - (h - 28) * (v - lo) / (hi - lo);
    g.strokeStyle = 'rgba(135,145,168,0.3)'; g.lineWidth = 1; g.beginPath(); g.moveTo(4, Y(0)); g.lineTo(w - 4, Y(0)); g.stroke();
    lines.forEach((pts, n) => {
      g.strokeStyle = series[n].colour || '#a48be0'; g.lineWidth = 1.6; g.beginPath();
      pts.forEach((p, i) => (i ? g.lineTo(X(p[0]), Y(p[1])) : g.moveTo(X(p[0]), Y(p[1]))));
      g.stroke();
    });
    g.fillStyle = '#8791a8'; g.font = '10.5px system-ui';
    g.fillText(fmt(Math.round(hi)), 6, 10);
    if (lo < 0) g.fillText(fmt(Math.round(lo)), 6, h - 16);
    g.fillText(new Date(t0 * 1000).toISOString().slice(11, 16) + ' UTC', 6, h - 2);
    g.fillText(new Date(t1 * 1000).toISOString().slice(11, 16), w - 34, h - 2);
  });
  return wrap;
}

function trailing(rows, minutes, col) {          // the change of a running sum per hour, over the minutes before each sample
  const out = [];
  let j = 0;
  for (let i = 0; i < rows.length; i++) {
    while (rows[i][0] - rows[j][0] > minutes * 60) j++;
    const dt = rows[i][0] - rows[j][0];
    out.push([rows[i][0], dt >= 300 && rows[i][col] !== null && rows[j][col] !== null ? (rows[i][col] - rows[j][col]) * 3600 / dt : null]);
  }
  return out;
}

const WINDOWS = { '1h': ['Last hour', 6, 60, 4], '6h': ['6 hours', 24, 60, 6], '24h': ['24 hours', 48, 180, 24] };   // label, hours of graph, minutes behind each point, hours of the routes table
let metricWin = '1h';
let INCOME = { routes: [], at: 0, key: '' };

async function renderMetrics(panel, live) {
  const t = F.totals || {}, r = t.rates, w = r && r.windows ? r.windows[metricWin] : null, [, graphHours, behind, routeHours] = WINDOWS[metricWin];
  panel.append(el('h2', null, 'Fleet economy'));
  const pickRow = el('div', 'winsel');
  for (const [key, def] of Object.entries(WINDOWS)) {
    const b = el('button', key === metricWin ? 'on' : null, def[0]);
    b.type = 'button';
    b.addEventListener('click', () => { metricWin = key; HIST.at = 0; INCOME.at = 0; render(); });
    pickRow.append(b);
  }
  panel.append(pickRow);
  const span = w ? (w.minutes >= 120 ? Math.round(w.minutes / 60) + ' hours' : w.minutes + ' minutes') : '';
  panel.append(el('p', 'sub', w
    ? 'Steady money over the last ' + span + ': what the fleet makes again and again. Rewards the game pays once per pilot are left out.'
      + (w.ships_changed ? ' The fleet grew in this stretch: a new pilot\'s first credits count as income here.' : '')
    : 'No figures for this stretch yet: the collector needs five minutes of samples.'));
  const grid = el('div', 'kpis');
  const kpi = (k, v, sub, cls) => { const b = el('div', 'kpi' + (cls ? ' ' + cls : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sub) b.append(el('div', 's', sub)); grid.append(b); return b; };
  const tone = (n) => (n < 0 ? ' neg' : n > 0 ? ' pos' : '');
  kpi('Steady net / h', w ? signed(w.cph) : '--', 'income minus costs', 'main' + (w ? tone(w.cph) : ''));
  kpi('Net per ship / h', w ? signed(w.cph_per_ship) : '--', 'what one ship makes', 'main' + (w ? tone(w.cph_per_ship) : ''));
  kpi('Steady income / h', w ? fmt(w.income_per_hour) : '--', 'sales and repeatable rewards', w && w.income_per_hour > 0 ? 'pos' : '');
  kpi('Running costs / h', w ? fmt(w.costs_per_hour) : '--', 'fuel, repairs, goods, modules', w && w.costs_per_hour > 0 ? 'neg' : '');
  const metered = w && w.fuel_cr_per_hour !== undefined;
  kpi('Fuel / h', metered ? fmt(w.fuel_cr_per_hour) : '--', metered ? fmt(w.fuel_units_per_hour) + ' units bought' : 'not measured in this stretch yet', metered && w.fuel_cr_per_hour > 0 ? 'neg' : '');
  kpi('Repairs / h', metered ? fmt(w.repair_cr_per_hour) : '--', metered ? fmt(w.hull_points_per_hour) + ' hull points' : 'not measured in this stretch yet', metered && w.repair_cr_per_hour > 0 ? 'neg' : '');
  kpi('Ships working', t.ships ? fmt(t.working) + ' of ' + fmt(t.ships) : '--',
    fmt(t.parked) + ' parked at a station' + (t.adrift ? ', ' + fmt(t.adrift) + ' in space without work' : ''));
  kpi('Credits', fmt(t.credits), fmt(t.credits_per_ship) + ' per ship');
  panel.append(grid);
  if (w) { const once = el('p', 'sub', 'Paid once in this stretch (not counted above): '); once.append(tint(Math.round(w.one_time_per_hour * w.minutes / 60)), ' cr.'); panel.append(once); }
  const b = F.birth;
  if (b && b.planned && !b.finished_at) {
    panel.append(el('h3', null, 'Birth in progress'));
    panel.append(facts([['Registered', b.registered + ' of ' + b.planned + (b.failed ? ', ' + b.failed + ' refused' : '')],
      ['Starter missions done', b.starter_done], ['Standing orders given', b.ordered], ['Stopped', b.stopped || 'no']]));
  }
  panel.append(el('h3', null, 'By division'));
  const div = t.divisions || {}, dw = (w || {}).divisions || {};
  const order = (S ? S.roster : []).filter((a) => a.division !== 'Command' || div.Command).map((a) => [a.division, a.name]);
  if (div.Unassigned) order.push(['Unassigned', '']);
  panel.append(table(['Division', 'Working', 'Income / h', 'Costs / h', 'Net / h', 'Net / ship'],
    order.map(([d, adm]) => {
      const x = div[d] || {}, y = dw[d] || {}, name = el('span', null, d);
      name.style.color = DIV[d] || DIV.Unassigned; name.title = adm ? 'Admiral ' + adm : '';
      return [name, fmt(x.working) + ' / ' + fmt(x.ships), w ? shade(y.income_per_hour, 'pos') : '--', w ? shade(y.costs_per_hour, 'neg') : '--', w ? tint(y.cph) : '--', w ? tint(y.cph_per_ship) : '--'];
    }), [1, 2, 3, 4, 5]));
  const routesBox = el('div'), graphs = el('div');
  panel.append(el('h3', null, 'Where the money comes from, last ' + routeHours + ' hours'), routesBox, el('h3', null, 'Last ' + graphHours + ' hours'), graphs);
  panel.append(el('p', 'sub', 'How it is counted. Income: the game\'s counter of credits earned, less the rewards paid once per pilot. Costs: everything spent, '
    + 'less what was bought for such a reward. Net: income minus costs. Fuel and repairs: counted when a docked ship\'s tank or hull rises and its wallet falls. '
    + 'A route\'s figure counts only runs that read a wallet.'));
  if (Date.now() - HIST.at > 30000 || HIST.key !== metricWin) {
    try { HIST = Object.assign(await get('/api/history?q=' + graphHours), { at: Date.now(), key: metricWin }); } catch (e) { HIST = { rows: [], at: Date.now(), key: metricWin }; }
    if (!live()) return;
  }
  if (Date.now() - INCOME.at > 30000 || INCOME.key !== metricWin) {
    try { INCOME = Object.assign(await get('/api/income?q=' + routeHours), { at: Date.now(), key: metricWin }); } catch (e) { INCOME = { routes: [], at: Date.now(), key: metricWin }; }
    if (!live()) return;
  }
  const steady = INCOME.routes.filter((x) => !x.once && (x.runs || x.flying)).sort((a, b2) => b2.credits - a.credits), once = INCOME.routes.filter((x) => x.once && (x.runs || x.flying));
  if (steady.length) {
    routesBox.append(table(['Route', 'Ships now', 'Runs', 'Ship-hours', 'Credits', 'Per ship-hour'], steady.map((x) => {
      const name = el('span', null, x.route);
      name.title = x.title || '';
      return [name, x.flying || '', x.runs, x.ship_hours, tint(x.credits), x.per_ship_hour === null ? 'no reading' : tint(x.per_ship_hour)];
    }), [1, 2, 3, 4, 5]));
  } else routesBox.append(el('p', 'empty', 'No run of a repeating route in this stretch.'));
  if (once.length) {
    routesBox.append(el('p', 'sub', 'Paid once per pilot:'));
    routesBox.append(table(['Route', 'Ships now', 'Runs', 'One-time credits'], once.map((x) => {
      const name = el('span', null, x.route);
      name.title = x.title || '';
      return [name, x.flying || '', x.runs, tint(x.one_time)];
    }), [1, 2, 3]));
  }
  const rows = HIST.rows || [];
  graphs.append(
    chart('Steady net per hour, over the ' + behind + ' minutes before', [{ pts: trailing(rows, behind, 5), colour: '#a48be0' }]),
    chart('Per hour:', [{ pts: trailing(rows, behind, 3), colour: '#58c08c', name: 'income' }, { pts: trailing(rows, behind, 4), colour: '#e06c66', name: 'costs' }]),
    chart('Ships working', [{ pts: rows.map((p) => [p[0], p[6]]), colour: '#6fa8dc' }]),
    chart('Credits, all wallets', [{ pts: rows.map((p) => [p[0], p[1]]), colour: '#dcae58' }]));
}

const TABS = { Selection: renderSelection, Metrics: renderMetrics, Market: renderMarket, Docs: renderDocs };
let renderSeq = 0, viewKey = '';
function render() {
  const panel = $('panel'), mine = ++renderSeq, live = () => mine === renderSeq;
  const key = [tab, selShip, selShip ? '' : selected, pilotCard ? pilotCard.name : '', docView ? docView.path : ''].join('|');
  const keep = key === viewKey ? panel.scrollTop : 0;
  viewKey = key;
  panel.replaceChildren();
  document.querySelectorAll('nav button').forEach((b) => b.classList.toggle('on', b.textContent === tab));
  if (tab !== 'Docs') setWide(false);
  Promise.resolve(TABS[tab](panel, live)).catch((e) => { if (live()) panel.append(el('p', 'empty', e.message)); });
  panel.scrollTop = keep;
}

function select(id, center) {
  if (!sys.has(id)) return;
  selected = id; pilotCard = null; selShip = null; shipCard = null; docView = null; route = pathFromHome(id); tab = 'Selection';
  if (center) { const s = sys.get(id); flyTo(s.x, s.y, view.k < 0.12 ? 0.2 : view.k); }
  renderRoster(); draw(); render();
}
async function showPilot(name) {
  pilotCard = await get('/api/pilot?name=' + encodeURIComponent(name));
  tab = 'Selection'; selShip = null; shipCard = null; docView = null;
  if (pilotCard.seen && sys.has(pilotCard.seen.system)) {
    selected = pilotCard.seen.system; route = pathFromHome(selected);
    const s = sys.get(selected); flyTo(s.x, s.y, view.k < 0.12 ? 0.2 : view.k);
  }
  renderRoster(); render();
}

function status() {
  const box = $('status'), st = L.stats || {};
  box.replaceChildren();
  const item = (label, value, cls, wide) => { const s = el('span', wide ? 'wide' : null); if (cls) s.append(el('i', 'dot ' + cls)); s.append(label + ' '); s.append(el('b', null, value)); box.append(s); };
  item('Fleet data', fleetAgeText(), fleetLive() ? 'good' : 'bad');
  box.lastChild.querySelector('b').id = 'fleet-age';
  box.lastChild.title = 'How old the picture of our ships is. The collector reads the engine every 10 seconds, about once a game tick';
  item('Tick', fmt(st.tick), null, true); item('Game', st.version || '?', null, true); item('Online', fmt(st.online_players));
  const liveStream = L.stream || {};
  item('Stream', liveStream.connected && liveStream.age < 60 ? 'live' : 'down', liveStream.connected && liveStream.age < 60 ? 'good' : 'bad');
  if (S) {
    const bad = Object.entries(S.sources).filter(([, s]) => s.error || s.age < 0).map(([n]) => n);
    item('Sources', bad.length ? 'problem: ' + bad.join(', ') : 'good', bad.length ? 'warn' : 'good');
  }
}

// ---------------------------------------------------------------- comms: one conversation with all six members

const chat = { after: 0, timer: 0, busy: false, first: true };
const agentOf = (id) => ((S && S.roster) || []).find((a) => a.id === id) || { id, name: id, division: 'Command', rank: '' };

function address(id) {                           // put @Name at the head of the message, or take it out again
  const input = $('chat-input'), tag = '@' + (id === 'all' ? 'all' : agentOf(id).name);
  const has = new RegExp('(^|\\s)' + tag + '(?![A-Za-z0-9_])\\s*', 'i');
  input.value = has.test(input.value) ? input.value.replace(has, '$1') : tag + ' ' + input.value;
  input.focus();
  markWho();
}

function markWho() {                             // light the portraits the message is for; nobody named: the Fleet Admiral
  const names = ($('chat-input').value.match(/@[A-Za-z]+/g) || []).map((s) => s.slice(1).toLowerCase());
  const all = names.some((n) => ['all', 'everyone', 'fleet'].includes(n)), admirals = names.includes('admirals');
  const to = [];
  document.querySelectorAll('#chat-who button').forEach((b) => {
    const a = agentOf(b.dataset.id);
    const on = b.dataset.id === 'all' ? all : (all || names.includes(a.name.toLowerCase()) || (admirals && a.rank === 'Admiral'));
    b.classList.toggle('on', on);
    if (on && b.dataset.id !== 'all') to.push(a.name);
  });
  if (!to.length) {
    const unity = document.querySelector('#chat-who button[data-id="unity"]');
    if (unity) unity.classList.add('on');
    to.push('Unity');
  }
  $('chat-input').placeholder = 'To ' + (all ? 'everyone' : to.join(', ')) + '. Click a symbol or type @Name to choose. Enter sends.';
}

function chatNote(text) {
  const log = $('chat-log'), hint = log.querySelector('.chathint');
  if (hint) hint.remove();
  log.append(el('div', 'msg err', text));
  log.scrollTop = log.scrollHeight;
}

function groupMessage(m) {
  const log = $('chat-log'), hint = log.querySelector('.chathint');
  if (hint) hint.remove();
  const mine = m.who === 'suggi', a = mine ? null : agentOf(m.who);
  const box = el('div', 'msg ' + (mine ? 'user' : m.kind === 'error' ? 'err' : 'agent')), head = el('div', 'msghead');
  if (mine) head.append(el('b', null, 'Suggi'), el('span', 'to', ' to ' + ((m.to || []).length >= 6 ? 'everyone' : (m.to || []).map((i) => agentOf(i).name).join(', ') || 'the group')));
  else {
    const name = el('b', null, a.name), c = DIV[a.division] || DIV.Command;
    name.style.color = c; box.style.borderLeftColor = c;
    head.append(shipSvg(a.division === 'Command' ? 'Flagship' : a.division, c, 12), name, el('span', null, ' ' + a.division));
  }
  head.append(el('span', 'when', new Date((m.t || 0) * 1000).toISOString().slice(11, 16)));
  box.append(head);
  if (mine || m.kind === 'error') box.append(el('div', 'msgtext', m.text)); else box.append(markdown(m.text, '', false));
  log.append(box);
}

async function pollGroup() {
  clearTimeout(chat.timer);
  let d = null;
  try { d = await get('/api/group?after=' + chat.after); } catch (e) { d = null; }
  if (d && d.messages) {
    const log = $('chat-log'), stick = chat.first || log.scrollHeight - log.scrollTop - log.clientHeight < 80;
    d.messages.forEach((m) => { groupMessage(m); chat.after = Math.max(chat.after, m.n); });
    if (chat.first && !log.children.length) {
      log.append(el('div', 'chathint', 'One conversation with Unity and the five Admirals. A message goes to Unity unless it names someone: click a symbol above or type @Name; @all reaches everyone.'));
    }
    if (d.messages.length && stick) log.scrollTop = log.scrollHeight;
    chat.first = false;
    chat.busy = d.running.length > 0;
    $('chat-state').textContent = d.running.map((r) => agentOf(r.agent).name + ' is working, ' + r.seconds + ' s' + (r.tool ? ' (' + r.tool + ')' : '')).join('  |  ');
    document.querySelectorAll('#chat-who button').forEach((b) => b.classList.toggle('busy', d.running.some((r) => r.agent === b.dataset.id)));
  }
  chat.timer = setTimeout(pollGroup, chat.busy ? 1500 : 5000);
}

async function sendGroup() {
  const input = $('chat-input'), message = input.value.trim(), send = $('chat-send');
  if (!message || send.disabled) return;
  send.disabled = true;
  try {
    const d = await post('/api/group/send', { text: message });
    input.value = '';
    markWho();
    if (d.busy && d.busy.length) chatNote('Not sent to ' + d.busy.map((i) => agentOf(i).name).join(', ') + ': still answering the last message.');
  } catch (e) { chatNote('Not sent: ' + e.message); }
  send.disabled = false;
  pollGroup();
}

function initChat() {
  const who = $('chat-who');
  who.replaceChildren();
  for (const a of S.roster) {
    const b = el('button', null), c = DIV[a.division] || DIV.Command;
    b.type = 'button'; b.dataset.id = a.id;
    b.style.setProperty('--c', c);
    b.append(shipSvg(a.division === 'Command' ? 'Flagship' : a.division, c, 18), el('span', null, a.name));
    b.title = a.name + ', ' + a.rank + (a.division === 'Command' ? '' : ' of ' + a.division) + ': write to ' + a.name;
    b.addEventListener('click', () => address(a.id));
    who.append(b);
  }
  const all = el('button', 'all', 'All');
  all.type = 'button'; all.dataset.id = 'all';
  all.title = 'Write to all six';
  all.addEventListener('click', () => address('all'));
  who.append(all);
  $('chat-send').addEventListener('click', sendGroup);
  $('chat-input').addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendGroup(); } });
  $('chat-input').addEventListener('input', markWho);
  markWho();
  pollGroup();
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
  for (const kind of KINDS.slice(0, 6)) {            // our ships: the silhouette of each kind
    const span = el('span', 'kind');
    span.append(shipSvg(kind === 'Command' ? 'Flagship' : kind, DIV[kind], 13), kind === 'Command' ? 'command group' : kind.toLowerCase());
    legend.append(span);
  }
  legend.append(el('span', null, 'ring: station (gold: player faction)'), el('span', null, 'red cross: pirate stronghold'),
    el('span', null, 'glow: pilots seen in the last hour'), el('span', null, 'pie and number: our ships by division'),
    el('span', null, 'tag and number: a foreign faction, last hour'));
}
async function loadLive() {
  try { L = await get('/api/live'); } catch (e) { L.stream = { connected: false, age: -1 }; }
  groupsBy.clear();
  (L.groups || []).forEach((g) => { if (!groupsBy.has(g.system)) groupsBy.set(g.system, []); groupsBy.get(g.system).push(g); });
  status(); draw();
}
async function loadFleet() {
  try { F = await get('/api/fleet'); fetchedAt = Date.now(); } catch (e) { F = Object.assign({}, F, { age: -1 }); }
  shipsBy.clear();
  F.ships.forEach((r) => { if (r.system) { if (!shipsBy.has(r.system)) shipsBy.set(r.system, []); shipsBy.get(r.system).push(r); } });
  renderMembers(); renderRoster(); tickAges(); renderPop(); draw();
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
  canvas.addEventListener('mousedown', (e) => { cam = null; drag = [e.clientX, e.clientY, view.x, view.y]; moved = false; canvas.classList.add('drag'); });
  window.addEventListener('mouseup', () => { drag = null; canvas.classList.remove('drag'); });
  canvas.addEventListener('mousemove', (e) => {
    const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
    if (drag) {
      if (Math.abs(e.clientX - drag[0]) + Math.abs(e.clientY - drag[1]) > 3) moved = true;
      view.x = drag[2] - (e.clientX - drag[0]) / view.k; view.y = drag[3] - (e.clientY - drag[1]) / view.k;
      draw(); return;
    }
    const tip = $('tip'), badge = S && badgeAt(mx, my), grp = !badge && S && groupAt(mx, my), s = !badge && !grp && S && nearest(mx, my);
    hover = s ? s.id : null; hoverBadge = badge || null;
    canvas.style.cursor = badge ? 'pointer' : '';
    const placeName = (b) => { const o = sys.get(b.system); return o ? o.name : b.system; };
    if (badge) {
      tip.textContent = badge.count + (badge.count === 1 ? ' ship' : ' ships') + ' of ours at ' + placeName(badge) + ': ' + badge.parts + ' | click for the card';
      tip.style.left = mx + 14 + 'px'; tip.style.top = my + 12 + 'px'; tip.hidden = false;
    } else if (grp) {
      const g = grp.group;
      tip.textContent = '[' + g.tag + '] ' + (g.name || 'a faction') + ': ' + g.count + ' pilots jumped into ' + placeName(grp) + ' in the last hour | our standing: ' + g.standing;
      tip.style.left = mx + 14 + 'px'; tip.style.top = my + 12 + 'px'; tip.hidden = false;
    } else if (s) {
      const ours = (shipsBy.get(s.id) || []).length;
      tip.textContent = s.name + (s.empire ? ' (' + s.empire + ')' : '') + ' | ' + (L.hour[s.id] || 0) + ' pilots in the last hour' + (ours ? ' | ' + ours + ' of ours' : '');
      tip.style.left = mx + 14 + 'px'; tip.style.top = my + 12 + 'px'; tip.hidden = false;
    } else tip.hidden = true;
    draw();
  });
  canvas.addEventListener('mouseleave', () => { $('tip').hidden = true; hover = null; hoverBadge = null; draw(); });
  canvas.addEventListener('click', (e) => {
    if (moved || !S) return;
    const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top, badge = badgeAt(mx, my);
    if (badge) { $('tip').hidden = true; openPop(badge.system, badge.kind); return; }
    const s = nearest(mx, my);
    if (pop) closePop();
    if (s) select(s.id, false);
  });
  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left - W / 2, my = e.clientY - r.top - H / 2;
    const k = Math.max(0.01, Math.min(3, view.k * (e.deltaY < 0 ? 1.2 : 1 / 1.2)));
    cam = null;
    view.x += mx / view.k - mx / k; view.y += my / view.k - my / k; view.k = k;
    draw();
  }, { passive: false });
  $('btn-all').addEventListener('click', () => fit(S.systems, 1200));
  $('btn-home').addEventListener('click', () => fit(S.systems.filter((s) => s.jumps >= 0 && s.jumps <= 4), 500));
  $('btn-fleet').addEventListener('click', () => fitFleet(false));
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
  window.addEventListener('keydown', (e) => { if (e.key === 'Escape' && pop) closePop(); });
}

function fitFleet(jump) {
  const list = [...shipsBy.keys()].map((id) => sys.get(id)).filter(Boolean);
  if (!list.length) { fit(S.systems.filter((s) => s.jumps >= 0 && s.jumps <= 4), 500, jump); return; }
  fit(list.concat(list.flatMap((s) => s.lanes.map((id) => sys.get(id)).filter(Boolean))), 300, jump);
}

(async function main() {
  init();
  await loadState();
  resize();
  await loadFleet();
  fitFleet(true);
  await loadLive();
  render();
  initChat();
  setInterval(loadLive, 5000);
  setInterval(loadFleet, 5000);
  setInterval(tickAges, 1000);
  setInterval(async () => { await loadState(); draw(); if (tab === 'Docs' && !docView) render(); }, 120000);
})().catch((e) => { $('panel').replaceChildren(el('p', 'empty', 'The station could not load its data: ' + e.message)); });
