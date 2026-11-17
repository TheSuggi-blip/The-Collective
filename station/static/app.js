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

// Times on the page are Suggi's (the zone below; CET in winter, CEST in summer). The logs and the data stay UTC.
const ZONE = 'Europe/Berlin';
const zoneFmt = new Intl.DateTimeFormat('en-GB', { timeZone: ZONE, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZoneName: 'short' });
function zoned(ms) {                               // the parts of a moment in his zone
  const p = {};
  zoneFmt.formatToParts(new Date(ms)).forEach((x) => { p[x.type] = x.value; });
  if (/^(GMT|UTC)/.test(p.timeZoneName || '')) p.timeZoneName = p.timeZoneName === 'GMT+2' ? 'CEST' : 'CET';
  return p;
}
function clock(ms) { const p = zoned(ms); return p.hour + ':' + p.minute; }                                    // 06:28
function clockZ(ms) { const p = zoned(ms); return p.hour + ':' + p.minute + ' ' + p.timeZoneName; }             // 06:28 CET
function stampOf(ms) { const p = zoned(ms); return p.year + '-' + p.month + '-' + p.day + ' ' + p.hour + ':' + p.minute + ' ' + p.timeZoneName; }
function stampCet(text) {                          // a UTC stamp as the files write it (2026-11-17 04:36 UTC, 2026-11-17T04:36:00Z) in his time; other text as it is
  const m = /^(\d{4})-(\d\d)-(\d\d)[ T](\d\d):(\d\d)(?::(\d\d))?/.exec(String(text || ''));
  return m ? stampOf(Date.UTC(+m[1], m[2] - 1, +m[3], +m[4], +m[5], +(m[6] || 0))) : String(text || '');
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

// Face portraits of the six members: robots drawn to fit each one's role. A list of SVG primitives in a box of
// 40 x 40; 'C' is the member's colour, 'K' the dark of the page. The same portrait stands in the top bar and in comms.
const LINE = { fill: 'none', stroke: 'C', 'stroke-linecap': 'round' };
const HEAD = { fill: 'C', 'fill-opacity': 0.2, stroke: 'C', 'stroke-width': 1.6, 'stroke-linejoin': 'round' };
const FACES = {
  unity: [                                          // the Fleet Admiral: one calm head under a halo, six lights in its visor: many agents, one purpose
    ['path', { ...LINE, d: 'M9 9.5 Q20 3 31 9.5', 'stroke-width': 1.6 }],
    ['rect', { ...HEAD, x: 9, y: 12, width: 22, height: 23, rx: 9 }],
    ['rect', { x: 11.5, y: 19, width: 17, height: 6.4, rx: 3.2, fill: 'K', stroke: 'C', 'stroke-width': 0.8 }],
    ...[13.6, 16.16, 18.72, 21.28, 23.84, 26.4].map((x) => ['circle', { cx: x, cy: 22.2, r: 0.95, fill: 'C' }]),
    ['path', { ...LINE, d: 'M16 30.5 H24', 'stroke-width': 1.4 }],
  ],
  zero: [                                           // Mining, the prospector: a hard hat with its lamp, goggles, a grille
    ['path', { d: 'M10 17 Q10 8 20 8 Q30 8 30 17 Z', fill: 'C' }],
    ['path', { ...LINE, d: 'M6.5 17.5 H33.5', 'stroke-width': 2.2 }],
    ['circle', { cx: 20, cy: 12.6, r: 2.6, fill: 'K' }], ['circle', { cx: 20, cy: 12.6, r: 1.2, fill: 'C' }],
    ['path', { ...HEAD, d: 'M10.5 19 V30 Q10.5 35 15.5 35 H24.5 Q29.5 35 29.5 30 V19 Z' }],
    ['circle', { cx: 15.6, cy: 24, r: 3.1, fill: 'K', stroke: 'C', 'stroke-width': 1.2 }], ['circle', { cx: 24.4, cy: 24, r: 3.1, fill: 'K', stroke: 'C', 'stroke-width': 1.2 }],
    ['path', { ...LINE, d: 'M18.7 24 H21.3', 'stroke-width': 1.2 }],
    ['path', { ...LINE, d: 'M16.5 30.5 V33 M20 30.5 V33 M23.5 30.5 V33', 'stroke-width': 1.2 }],
  ],
  mercury: [                                        // Trade, the merchant: the winged helm, a coin on the brow, a smile
    ['path', { d: 'M11 15 L3.5 8.5 L6.5 14 L2.5 13.5 L7 18 L5 19 L10.5 21 Z', fill: 'C' }],
    ['path', { d: 'M29 15 L36.5 8.5 L33.5 14 L37.5 13.5 L33 18 L35 19 L29.5 21 Z', fill: 'C' }],
    ['ellipse', { ...HEAD, cx: 20, cy: 22, rx: 9.6, ry: 12.5 }],
    ['circle', { cx: 20, cy: 14.6, r: 2.5, fill: 'K', stroke: 'C', 'stroke-width': 1.1 }], ['path', { ...LINE, d: 'M20 13.3 V15.9', 'stroke-width': 1.1 }],
    ['path', { ...LINE, d: 'M13.5 21.8 Q15.8 19.6 18 21.8 M22 21.8 Q24.2 19.6 26.5 21.8', 'stroke-width': 1.5 }],
    ['path', { ...LINE, d: 'M15 27.5 Q20 31.6 25 27.5', 'stroke-width': 1.5 }],
  ],
  apollo: [                                         // Logistics, the builder: the sun's rays over a square head, a brow plate, a level mouth, two bolts
    ['path', { ...LINE, d: 'M20 3.5 V8 M11.5 5.6 L13.8 9.4 M28.5 5.6 L26.2 9.4', 'stroke-width': 1.7 }],
    ['rect', { ...HEAD, x: 8.5, y: 11.5, width: 23, height: 23.5, rx: 3.5 }],
    ['rect', { x: 8.5, y: 11.5, width: 23, height: 5, rx: 2.5, fill: 'C' }],
    ['rect', { x: 12, y: 20, width: 6.2, height: 4.2, rx: 0.8, fill: 'K', stroke: 'C', 'stroke-width': 1 }], ['rect', { x: 21.8, y: 20, width: 6.2, height: 4.2, rx: 0.8, fill: 'K', stroke: 'C', 'stroke-width': 1 }],
    ['rect', { x: 14, y: 28.3, width: 12, height: 2.6, rx: 0.6, fill: 'C' }],
    ['circle', { cx: 11.4, cy: 32.2, r: 0.9, fill: 'C' }], ['circle', { cx: 28.6, cy: 32.2, r: 0.9, fill: 'C' }],
  ],
  apophis: [                                        // Military, the warrior: a horned helm with a crest, the visor one narrow V
    ['path', { d: 'M10.5 13 L4 4.5 L8.5 17 Z', fill: 'C' }], ['path', { d: 'M29.5 13 L36 4.5 L31.5 17 Z', fill: 'C' }],
    ['path', { ...HEAD, d: 'M20 6.5 L30 12 L32 24 L26 35 H14 L8 24 L10 12 Z' }],
    ['path', { d: 'M11.5 18.5 L20 23 L28.5 18.5 L27.5 22.5 L20 26.5 L12.5 22.5 Z', fill: 'C' }],
    ['path', { ...LINE, d: 'M20 6.5 V15', 'stroke-width': 1.6 }],
    ['path', { ...LINE, d: 'M17 30.5 H23', 'stroke-width': 1.3 }],
  ],
  oracle: [                                         // Intel, the seer: one great eye, an antenna, and it listens to both sides
    ['path', { ...LINE, d: 'M20 10.5 V6', 'stroke-width': 1.4 }], ['circle', { cx: 20, cy: 4.7, r: 1.7, fill: 'C' }],
    ['path', { ...LINE, d: 'M5.2 16.5 Q2.6 22 5.2 27.5 M34.8 16.5 Q37.4 22 34.8 27.5', 'stroke-width': 1.3 }],
    ['circle', { ...HEAD, cx: 20, cy: 22.5, r: 12 }],
    ['circle', { cx: 20, cy: 21.5, r: 6, fill: 'K', stroke: 'C', 'stroke-width': 1.1 }],
    ['circle', { cx: 20, cy: 21.5, r: 3.1, fill: 'none', stroke: 'C', 'stroke-width': 1.1 }], ['circle', { cx: 20, cy: 21.5, r: 1.3, fill: 'C' }],
    ['path', { ...LINE, d: 'M16.5 31 H23.5', 'stroke-width': 1.2 }],
  ],
};
function faceSvg(id, division, colour, size) {      // a member's portrait; a member without one gets its division's ship
  const parts = FACES[id];
  if (!parts) return shipSvg(division === 'Command' ? 'Flagship' : division, colour, Math.round(size * 0.7));
  const NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 40 40'); svg.setAttribute('width', size); svg.setAttribute('height', size);
  svg.setAttribute('class', 'face'); svg.setAttribute('aria-hidden', 'true');
  for (const [tag, attrs] of parts) {
    const e = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v === 'C' ? colour : v === 'K' ? '#0b0e15' : v));
    svg.append(e);
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
let F = { ships: [], totals: {}, engine: {}, age: -1, birth: null, wave: null, waves: [] };   // /api/fleet
let fetchedAt = 0;                             // when /api/fleet last answered (ms)
let HIST = { rows: [], at: 0 };                // /api/history, for the Metrics tab
const collapsed = new Set();                   // divisions folded in the roster; remembered by the browser
try { JSON.parse(localStorage.getItem('station.folded') || '[]').forEach((d) => collapsed.add(String(d))); } catch (e) { /* no storage */ }
function saveFolds() { try { localStorage.setItem('station.folded', JSON.stringify([...collapsed])); } catch (e) { /* no storage */ } }
const shut = new Set();                        // what Suggi has hidden: the side panels, the messages of comms, the legend, the layers; remembered
try { JSON.parse(localStorage.getItem('station.hidden') || '[]').forEach((d) => shut.add(String(d))); } catch (e) { /* no storage */ }
function saveShut() { try { localStorage.setItem('station.hidden', JSON.stringify([...shut])); } catch (e) { /* no storage */ } }
let board = null;
const sys = new Map();
const stationsBy = new Map();
const shipsBy = new Map();                     // system id -> our ships there
const layers = { Regions: true, 'Our space': true, Lanes: true, Traffic: true, Stations: true, 'Our bases': true, Strongholds: true, Intel: true, Factions: true, Fleet: true, Names: true };
const sitesBy = new Map();                     // system id -> a site named for a base of ours (game/map/sites.tsv)
const holdBy = new Map();                      // system id -> the buildings of ours there (what the faction owns, read from the game)
const sphere = new Map();                      // system id -> when a ship of ours was last seen there (ms): our own space on the map
const SPHERE_MS = 3600000;                     // a system stays in our space for an hour after the last ship of ours was seen there
try { for (const [id, at] of JSON.parse(localStorage.getItem('station.sphere') || '[]')) { if (typeof id === 'string' && Date.now() - at < SPHERE_MS) sphere.set(id, Number(at)); } } catch (e) { /* no storage */ }
let sphereSaved = 0;
let bounds = null, terrR = 250, homeEmpire = '';   // the galaxy's extent; the radius of the ground under one system; our empire
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

function minZoom() {                                 // the whole galaxy with a margin: the map never gets smaller than this
  if (!bounds || !W) return 0.01;
  return 0.86 * Math.min(W / (bounds.x1 - bounds.x0 + 1200), H / (bounds.y1 - bounds.y0 + 1200));
}
function clampView() {                               // the view stays on the galaxy: a limit to zooming out and to dragging away
  if (!bounds || !W) return;
  view.k = Math.max(minZoom(), Math.min(3, view.k));
  const hx = Math.max(0, (bounds.x1 - bounds.x0 + 1200) / 2 - W / (2 * view.k)) + 0.2 * W / view.k;
  const hy = Math.max(0, (bounds.y1 - bounds.y0 + 1200) / 2 - H / (2 * view.k)) + 0.2 * H / view.k;
  const mx = (bounds.x0 + bounds.x1) / 2, my = (bounds.y0 + bounds.y1) / 2;
  view.x = Math.max(mx - hx, Math.min(mx + hx, view.x)); view.y = Math.max(my - hy, Math.min(my + hy, view.y));
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
  clampView();
  paint(now / 1000);
  if (cam) draw();
  else if ((selected || route.length > 1) && !pulse) pulse = setTimeout(() => { pulse = 0; draw(); }, 60);   // the selection breathes, the route line moves
}

// ---------------------------------------------------------------- the marks of the map

const OURS = '#d9d0f5';                              // our own space and the sites chosen for a base
const BUILT = '#ffffff', RAISING = '#dcae58';        // a building of ours the game lists as active; one it does not (being built, or down)
// One drawing per mark in a box of 12 by 12: the map paints it on the canvas, the legend shows the same path as an SVG.
const GLYPHS = {
  storage: { d: 'M2 4.1 6 2.1 10 4.1V8.5L6 10.5 2 8.5Z M2 4.1 6 6.1 10 4.1 M6 6.1V10.5' },
  recruit: { d: 'M6 1.9a2 2 0 1 0 0 4a2 2 0 1 0 0-4Z M2.3 10.4c0-2.3 1.6-3.6 3.7-3.6s3.7 1.3 3.7 3.6Z', fill: true },
  office: { d: 'M2.4 10.2V4.6L6 2 9.6 4.6V10.2Z M4.9 10.2V7.4H7.1V10.2' },
  outpost: { d: 'M6 1.6 9.8 3.8V8.2L6 10.4 2.2 8.2V3.8Z M6 4.9a1.1 1.1 0 1 0 0 2.2a1.1 1.1 0 1 0 0-2.2Z' },
  station: { d: 'M6 1.4 10 3.7V8.3L6 10.6 2 8.3V3.7Z', fill: true },
  flag: { d: 'M3 10.8V1.7 M3 1.9 9.8 3.9 3 5.9Z', fill: true },
  pip: { d: 'M6 2.4 9.6 6 6 9.6 2.4 6Z', fill: true },
  cross: { d: 'M3 3 9 9 M9 3 3 9' },
  threat: { d: 'M6 2.2 10.2 9.6H1.8Z', fill: true },
};
function glyph(c, name, x, y, size, colour, hollow) {    // a mark centred on x, y, with a dark edge so that it reads on any ground
  const g = GLYPHS[name] || GLYPHS.office, f = size / 12;
  if (!g.path) g.path = new Path2D(g.d);
  c.save(); c.translate(x - size / 2, y - size / 2); c.scale(f, f);
  c.lineJoin = 'round'; c.lineCap = 'round';
  c.strokeStyle = 'rgba(9,12,18,0.9)'; c.lineWidth = 3.4 / f; c.stroke(g.path);
  if (g.fill && !hollow) { c.fillStyle = colour; c.fill(g.path); }
  c.strokeStyle = colour; c.lineWidth = 1.2 / f; c.stroke(g.path);
  c.restore();
}
function glyphSvg(name, colour, size, hollow) {          // the same mark as an SVG element
  const NS = 'http://www.w3.org/2000/svg', g = GLYPHS[name] || GLYPHS.office, svg = document.createElementNS(NS, 'svg'), path = document.createElementNS(NS, 'path');
  svg.setAttribute('viewBox', '0 0 12 12'); svg.setAttribute('width', size); svg.setAttribute('height', size); svg.setAttribute('aria-hidden', 'true');
  path.setAttribute('d', g.d); path.setAttribute('fill', g.fill && !hollow ? colour : 'none'); path.setAttribute('stroke', colour);
  path.setAttribute('stroke-width', '1.2'); path.setAttribute('stroke-linejoin', 'round'); path.setAttribute('stroke-linecap', 'round');
  svg.append(path);
  return svg;
}
function tokenSvg() {                                    // a small picture of the marker of our ships, for the legend
  const NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg'), round = 2 * Math.PI * 8.3;
  const add = (tag, attrs, words) => { const n = document.createElementNS(NS, tag); Object.entries(attrs).forEach(([a, v]) => n.setAttribute(a, v)); if (words) n.textContent = words; svg.append(n); };
  const home = S && S.empires[homeEmpire];
  svg.setAttribute('viewBox', '0 0 26 26'); svg.setAttribute('width', 24); svg.setAttribute('height', 24); svg.setAttribute('aria-hidden', 'true');
  add('circle', { cx: 13, cy: 13, r: 12, fill: '#0b0f18', stroke: home && HEX.test(home) ? home : LAWLESS, 'stroke-width': 1.6 });
  let from = 0;
  for (const [colour, share] of [[DIV.Mining, 0.45], [DIV.Logistics, 0.3], [DIV.Military, 0.25]]) {
    add('circle', { cx: 13, cy: 13, r: 8.3, fill: 'none', stroke: colour, 'stroke-width': 2.6, transform: 'rotate(-90 13 13)',
      'stroke-dasharray': (share * round).toFixed(2) + ' ' + round.toFixed(2), 'stroke-dashoffset': (-from * round).toFixed(2) });
    from += share;
  }
  add('text', { x: 13, y: 16, 'text-anchor': 'middle', 'font-size': 8.5, 'font-weight': 700, fill: '#eef0f6' }, '12');
  return svg;
}
const stands = (b) => !b.status || /^(active|built|online|operational)$/i.test(b.status);   // else the tooltip and the panel show the game's own word

// The ground under the map, as on a strategy game's galaxy map: each empire's space is one region with a soft fill and
// a thin border in its colour. Our own space lies over it as a region of its own: the systems where a ship of ours
// was seen in the last hour, and the systems where we own a building. All regions of one view are painted once on
// a canvas of their own and laid under the map until the view or the data changes.
const ground = document.createElement('canvas'), gctx = ground.getContext('2d');
const realm = document.createElement('canvas'), rctx = realm.getContext('2d');
let realmKey = '', realmVer = 0, realmNames = [];
const regionRadius = (k) => Math.max(9, terrR * k * 1.3);     // how far a region reaches around each of its systems, on the screen
function ourSpace() {
  const ids = new Set(holdBy.keys());
  for (const id of sphere.keys()) ids.add(id);
  return [...ids].map((id) => sys.get(id)).filter(Boolean);
}
function paintTerritory(k) {
  const d = window.devicePixelRatio || 1, R = regionRadius(k);
  const key = [view.x.toFixed(1), view.y.toFixed(1), k.toFixed(5), canvas.width, canvas.height, layers.Regions, layers['Our space'], realmVer].join('|');
  if (key !== realmKey) {
    realmKey = key;
    for (const c of [ground, realm]) { if (c.width !== canvas.width || c.height !== canvas.height) { c.width = canvas.width; c.height = canvas.height; } }
    rctx.setTransform(1, 0, 0, 1, 0, 0); rctx.clearRect(0, 0, realm.width, realm.height);
    const area = (list, colour, fill, edge, radius) => {
      if (!list.length) return;
      const half = radius * 0.75, line = 1.4, inside = new Set(list.map((s) => s.id)), at = new Map(list.map((s) => [s.id, toScreen(s)]));
      // only the part of the view the region covers is painted and laid down: a region off the view costs nothing
      let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
      for (const [x, y] of at.values()) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
      x0 = Math.max(0, Math.floor(x0 - radius - 2)); x1 = Math.min(W, Math.ceil(x1 + radius + 2)); y0 = Math.max(0, Math.floor(y0 - radius - 2)); y1 = Math.min(H, Math.ceil(y1 + radius + 2));
      if (x1 <= x0 || y1 <= y0) return;
      // The shape: a disc per system, a band along each lane between two systems of the region, and the triangles and
      // squares its lanes close, so that a region has no hole. All of it is one path, filled once.
      const spans = [], faces = [];
      for (const s of list) {
        const p = at.get(s.id), near = s.lanes.filter((id) => id > s.id && inside.has(id));
        for (const id of near) spans.push([p, at.get(id)]);
        for (let i = 0; i < near.length; i++) {
          for (let j = i + 1; j < near.length; j++) {
            const a = sys.get(near[i]), b = sys.get(near[j]);
            if (a.lanes.includes(b.id)) faces.push([p, at.get(a.id), at.get(b.id)]);
            const far = a.lanes.find((id) => id > s.id && id !== b.id && inside.has(id) && b.lanes.includes(id));
            if (far) faces.push([p, at.get(a.id), at.get(far), at.get(b.id)]);
          }
        }
      }
      const outline = (rad, wide) => {
        const path = new Path2D();
        const face = (pts) => {                                   // every part runs the same way round as a disc: parts that overlap add up and never cancel
          let turn = 0;
          for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; turn += p[0] * q[1] - q[0] * p[1]; }
          if (turn < 0) pts = pts.slice().reverse();
          path.moveTo(pts[0][0], pts[0][1]);
          for (let i = 1; i < pts.length; i++) path.lineTo(pts[i][0], pts[i][1]);
          path.closePath();
        };
        for (const [x, y] of at.values()) { path.moveTo(x + rad, y); path.arc(x, y, rad, 0, 6.2832); }
        for (const [p, q] of spans) {                             // the band along a lane: its ends lie inside the two discs
          const len = Math.hypot(q[0] - p[0], q[1] - p[1]) || 1, nx = -(q[1] - p[1]) / len * wide, ny = (q[0] - p[0]) / len * wide;
          face([[p[0] + nx, p[1] + ny], [q[0] + nx, q[1] + ny], [q[0] - nx, q[1] - ny], [p[0] - nx, p[1] - ny]]);
        }
        faces.forEach(face);
        return path;
      };
      const box = [Math.floor(x0 * d), Math.floor(y0 * d), Math.ceil((x1 - x0) * d), Math.ceil((y1 - y0) * d)];
      gctx.setTransform(d, 0, 0, d, 0, 0); gctx.globalCompositeOperation = 'source-over'; gctx.globalAlpha = 1;
      gctx.clearRect(x0 - 1, y0 - 1, x1 - x0 + 2, y1 - y0 + 2);
      gctx.fillStyle = colour;
      gctx.fill(outline(radius, half));
      gctx.globalCompositeOperation = 'destination-out'; gctx.globalAlpha = 1 - fill / edge;   // the inside is thinned to the fill; what stays whole is the border
      gctx.fill(outline(radius - line, half - line));
      gctx.globalCompositeOperation = 'source-over'; gctx.globalAlpha = 1;
      rctx.globalAlpha = edge; rctx.drawImage(ground, box[0], box[1], box[2], box[3], box[0], box[1], box[2], box[3]);
    };
    if (layers.Regions) {
      const realms = new Map();
      for (const s of S.systems) { if (s.empire) { if (!realms.has(s.empire)) realms.set(s.empire, []); realms.get(s.empire).push(s); } }
      for (const list of realms.values()) area(list, color(list[0]), 0.1, 0.5, R);
    }
    if (layers['Our space']) area(ourSpace(), OURS, 0.085, 0.7, R * 0.62);
    rctx.globalAlpha = 1;
  }
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(realm, 0, 0); ctx.restore();
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
  if (layers.Regions || layers['Our space']) paintTerritory(k);
  if (layers.Regions && k < 0.24) {                                 // each empire's name across its space, large and faint; it fades as the view comes close
    const size = Math.max(11, Math.min(22, 250 * k)), fade = Math.min(1, (0.24 - k) / 0.08), gap = size * 0.42, reach = regionRadius(k) + size * 0.9;
    const dots = S.systems.map(toScreen);
    ctx.font = '600 ' + size.toFixed(1) + 'px system-ui, sans-serif'; ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
    for (const n of realmNames) {
      const x = (n.x - view.x) * k + W / 2, letters = [...n.word], widths = letters.map((ch) => ctx.measureText(ch).width);
      const total = widths.reduce((a, b) => a + b, 0) + gap * (letters.length - 1);
      const under = (n.y1 - view.y) * k + H / 2 + reach, over = (n.y0 - view.y) * k + H / 2 - reach;   // just outside the region, below or above it: where fewer systems stand
      const crowd = (yy) => dots.reduce((m, q) => m + (Math.abs(q[0] - x) < total / 2 + 8 && Math.abs(q[1] - yy) < size * 0.8 + 5 ? 1 : 0), 0);
      const y = crowd(under) <= crowd(over) ? under : over;
      if (x < -total || x > W + total || y < -30 || y > H + 30) continue;
      ctx.fillStyle = rgba(n.colour, (0.55 * fade).toFixed(2));
      let at = x - total / 2;
      letters.forEach((ch, i) => { ctx.fillText(ch, at, y); at += widths[i] + gap; });
    }
    ctx.textBaseline = 'alphabetic';
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
      ctx.fillStyle = 'rgba(220,174,88,0.07)';
      ctx.beginPath(); ctx.arc(x, y, r + 2 + Math.min(11, Math.sqrt(n) * 1.5), 0, 6.2832); ctx.fill();
    }
  }
  // Our ships: one marker per system, in the system's own place. Inside: a ring with a slice per division around the
  // number of ships; the outer ring keeps the colour of whose space it is. Where two markers would touch, the smaller
  // group is drawn small and without its number (the tooltip and the card still tell it).
  const tokens = new Map();
  if (layers.Fleet) {
    const rows = [];
    for (const [id, list] of shipsBy) {
      const s = sys.get(id);
      if (!s) continue;
      const [x, y] = toScreen(s);
      if (x < -60 || y < -60 || x > W + 60 || y > H + 60) continue;
      const n = list.length, core = n > 99 ? 9.6 : n > 9 ? 7.2 : 5.2;
      rows.push({ id, x, y, n, list, core, R: core + 6.3, full: true });
    }
    rows.sort((a, b) => b.n - a.n || (a.id < b.id ? -1 : 1));
    const full = [];
    for (const row of rows) {
      if (full.some((o) => Math.hypot(o.x - row.x, o.y - row.y) < o.R + row.R + 1)) { row.full = false; row.core = 0; row.R = 7; } else full.push(row);
      tokens.set(row.id, row);
    }
  }
  for (const s of S.systems) {                                      // the systems without ships of ours: a small star in the colour of whose space it is
    const [x, y] = toScreen(s);
    if (x < -40 || y < -40 || x > W + 40 || y > H + 40 || tokens.has(s.id)) continue;
    const c = color(s), q = s.home ? r + 2 : r;
    ctx.fillStyle = rgba(c, 0.09); ctx.beginPath(); ctx.arc(x, y, q * 1.5, 0, 6.2832); ctx.fill();      // glow
    ctx.fillStyle = c; ctx.beginPath(); ctx.arc(x, y, q, 0, 6.2832); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.3)'; ctx.beginPath(); ctx.arc(x - q * 0.28, y - q * 0.28, q * 0.34, 0, 6.2832); ctx.fill();
  }
  badgeHits = []; groupHits = [];
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '700 9.5px system-ui, sans-serif';
  for (const tok of [...tokens.values()].sort((a, b) => Number(b.full) - Number(a.full))) {   // the markers with a number first, the small ones over them
    const { id, x, y, R, core, n, list } = tok, groups = fleetGroups(list), c = color(sys.get(id)), rim = core ? 1.9 : 1.5, ro = R - rim - (core ? 1.3 : 1.1);
    ctx.fillStyle = 'rgba(11,15,24,0.96)'; ctx.beginPath(); ctx.arc(x, y, R, 0, 6.2832); ctx.fill();
    ctx.strokeStyle = c; ctx.lineWidth = rim; ctx.beginPath(); ctx.arc(x, y, R - rim / 2, 0, 6.2832); ctx.stroke();   // the outer ring: whose space it is
    let from = -1.5708;
    for (const g of groups) {
      const to = from + 6.2832 * g.ships.length / n;
      ctx.fillStyle = g.colour; ctx.beginPath();
      if (core) { ctx.arc(x, y, ro, from, to); ctx.arc(x, y, core, to, from, true); } else { ctx.moveTo(x, y); ctx.arc(x, y, ro, from, to); }
      ctx.closePath(); ctx.fill();
      from = to;
    }
    if (core) { ctx.fillStyle = '#eef0f6'; ctx.fillText(String(n), x, y + 0.5); }
    if ((pop && pop.system === id) || (hoverBadge && hoverBadge.system === id) || list.some((sh) => sh.name === selShip)) {   // open, under the pointer, or the ship in the panel is here
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.arc(x, y, R + 2.2, 0, 6.2832); ctx.stroke();
    }
    badgeHits.push({ x: x - R - 1, y: y - R - 1, w: 2 * R + 2, h: 2 * R + 2, system: id, kind: 'All', count: n,
      parts: groups.map((g) => g.ships.length + ' ' + (g.kind === 'Command' ? 'command group' : g.kind)).join(', ') });
  }
  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  const labels = [], size = (id, home) => (tokens.has(id) ? tokens.get(id).R : home ? r + 2 : r);   // how far a system's own mark reaches
  const near = k >= 0.09;                                          // from far away the map keeps to regions, ships, our own marks and what is dangerous
  ctx.font = '11px system-ui, sans-serif';
  for (const s of S.systems) {                                      // the small marks beside each system, and its name
    const [x, y] = toScreen(s);
    if (x < -40 || y < -40 || x > W + 40 || y > H + 40) continue;
    const q = size(s.id, s.home), ours = tokens.has(s.id), d = q * 0.71 + 3.4;   // d: a mark on the system's diagonal, just outside it
    const bases = layers.Stations ? (stationsBy.get(s.id) || []).filter((b) => !(b.tag && b.tag === S.our_tag)) : [];
    const theirs = bases.some((b) => b.tag);                       // a station of others: gold when a player faction owns it; the empires' own only from near
    if (bases.length && (theirs || near)) glyph(ctx, 'pip', x + d, y + d, near ? 7.5 : 6.5, theirs ? '#e8c35a' : '#aeb5cc');
    if (layers.Strongholds && s.stronghold) glyph(ctx, 'cross', x - d, y - d, 8.5, '#e06c66');
    const intel = layers.Intel && S.intel.systems[s.id];
    if (intel) {                                                    // what our intel files say of the danger there: a red triangle always, an amber one from near
      const high = intel.standing === 'hostile' || /high|severe|extreme|deadly/.test(intel.threat || '');
      if (high || (near && intel.threat === 'medium')) glyph(ctx, 'threat', x + d, y - d, 8, high ? '#e06c66' : '#dcae58');
    }
    const own = layers['Our bases'] ? holdBy.get(s.id) || [] : [], site = layers['Our bases'] ? sitesBy.get(s.id) : null;
    const planned = site && site.status !== 'dropped' && site.status !== 'built' && !own.some((b) => b.kind === 'outpost' || b.kind === 'station');
    if (own.length || planned) {                                    // ours, above the system: one mark per kind of building, amber while one is not active; a flag for a planned base
      const kinds = new Map(), row = [];
      for (const b of own) { if (!kinds.has(b.kind)) kinds.set(b.kind, true); if (!stands(b)) kinds.set(b.kind, false); }
      for (const [kind, done] of kinds) row.push([kind, done ? BUILT : RAISING, false]);
      if (planned) row.push(['flag', site.status === 'candidate' ? rgba(OURS, 0.7) : OURS, site.status === 'candidate']);
      row.forEach(([name, colour, hollow], i) => glyph(ctx, name, x - (row.length - 1) * 7 + i * 14, y - q - 10.5, 12, colour, hollow));
    }
    if (s.id === selected) {
      const beat = (Math.sin(t * 2.6) + 1) / 2, ring = ours ? q + 4.5 : q + 8.5;
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1.8;
      ctx.beginPath(); ctx.arc(x, y, ring, 0, 6.2832); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,' + (0.3 * (1 - beat)).toFixed(2) + ')'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(x, y, ring + 0.5 + beat * 6, 0, 6.2832); ctx.stroke();
    }
    if (layers.Names) {                                             // names are drawn after the systems: the important ones first, none over another
      const picked = s.id === selected || s.id === hover;
      const rank = picked ? 2000 : s.home ? 1500 : own.length || planned ? 800 : ours && k > 0.085 ? 500 + shipsBy.get(s.id).length : k > 0.16 ? 100 : 0;
      if (rank) labels.push({ name: s.name, x, y, q, bold: Boolean(s.home || ours), rank });
    }
  }
  if (layers.Factions) {                                            // the larger groups of one foreign faction: a tag and a count under the system
    ctx.font = '600 10.5px system-ui, sans-serif'; ctx.textBaseline = 'middle';
    for (const [id, list] of groupsBy) {
      const s = sys.get(id);
      if (!s) continue;
      const [x, y] = toScreen(s);
      if (x < -60 || y < -40 || x > W + 60 || y > H + 20) continue;
      const q = size(id, s.home), show = list.filter((g) => k >= 0.12 || g.count >= 8).slice(0, 2);
      show.forEach((g, i) => {
        const label = g.tag + ' ' + g.count, w = ctx.measureText(label).width + 14, gx = x - w / 2, gy = y + q + 9 + i * 18;
        const c = g.standing === 'hostile' ? '#e06c66' : g.standing === 'ally' ? '#58c08c' : '#dcae58';
        pill(gx, gy, w, 15);
        ctx.fillStyle = 'rgba(15,20,31,0.9)'; ctx.fill();
        ctx.strokeStyle = rgba(c, 0.7); ctx.lineWidth = 1; ctx.stroke();
        ctx.fillStyle = c; ctx.fillText(label, gx + 7, gy + 8);
        groupHits.push({ x: gx, y: gy, w, h: 15, system: id, group: g });
        if (k >= 0.2) {                                             // zoomed in: one small hull per pilot, twelve at most
          ctx.fillStyle = rgba(c, 0.8);
          for (let j = 0; j < Math.min(12, g.count); j++) {
            const hx = gx + w + 5 + j * 8, hy = gy + 7.5;
            ctx.beginPath(); ctx.moveTo(hx + 6, hy); ctx.lineTo(hx, hy - 3.6); ctx.lineTo(hx + 1.7, hy); ctx.lineTo(hx, hy + 3.6); ctx.closePath(); ctx.fill();
          }
        }
      });
    }
    ctx.textBaseline = 'alphabetic';
  }
  labels.sort((a, b) => b.rank - a.rank);                           // names last: beside their system, right or left, where no marker and no other name stands
  const taken = badgeHits.concat(groupHits).map((b) => [b.x, b.y, b.x + b.w, b.y + b.h]);
  ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(9,12,18,0.85)'; ctx.lineJoin = 'round';
  for (const l of labels) {
    ctx.font = (l.bold ? '600 ' : '') + '11px system-ui, sans-serif';
    const w = ctx.measureText(l.name).width, spots = [l.x + l.q + 6, l.x - l.q - 6 - w];
    let at = spots.find((px) => !taken.some((b) => px - 3 < b[2] && px + w + 3 > b[0] && l.y - 7 < b[3] && l.y + 8 > b[1]));
    if (at === undefined) { if (l.rank < 1000) continue; at = spots[0]; }   // the home system and the one picked are always named
    taken.push([at - 3, l.y - 7, at + w + 3, l.y + 8]);
    ctx.strokeText(l.name, at, l.y + 4);
    ctx.fillStyle = l.bold ? '#f1f3f9' : '#a9b0c9';
    ctx.fillText(l.name, at, l.y + 4);
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

let groupCard = null;                                // the open card of a foreign faction's group: {group, data}
async function openGroup(system, g) {
  pop = { system, kind: 'Group', tag: g.tag }; groupCard = { group: g, data: null, failed: false };
  renderPop(); draw();
  try {
    const d = await get('/api/faction?q=' + encodeURIComponent(system + '|' + g.tag));
    if (pop && pop.kind === 'Group' && pop.system === system && pop.tag === g.tag) { groupCard.data = d; renderPop(); }
  } catch (e) {
    if (pop && pop.kind === 'Group' && pop.system === system && pop.tag === g.tag) { groupCard.failed = true; renderPop(); }
  }
}

function renderGroupPop(box) {                       // who of one foreign faction jumped in here, with the hulls our ships saw
  const s = sys.get(pop.system), g = groupCard && groupCard.group, d = groupCard && groupCard.data;
  if (!s || !g) { closePop(); return; }
  const body = box.querySelector('.popbody'), keep = body ? body.scrollTop : 0;
  const c = g.standing === 'hostile' ? '#e06c66' : g.standing === 'ally' ? '#58c08c' : '#dcae58';
  const head = el('div', 'pophead'), title = el('div', 'poptitle'), close = el('button', 'popclose', '\u00d7'), tag = el('span', 'grouptag', g.tag);
  tag.style.color = c;
  title.append(el('b', null, g.name || 'A faction'), el('span', null, 'jumped into ' + s.name + ' in the last hour | our standing: ' + g.standing));
  close.type = 'button'; close.title = 'Close (Esc)'; close.addEventListener('click', closePop);
  head.append(tag, title, close);
  const stats = el('div', 'popstats'), list = el('div', 'popbody');
  const cell = (k, v) => { const x = el('div'); x.append(el('div', 'k', k), el('div', 'v', String(v))); stats.append(x); };
  cell('Pilots', d ? d.count : g.count); cell('Members', d && d.members ? fmt(d.members) : '--');
  cell('Hulls seen', d ? d.known : '--'); cell('Highest tier', d && d.top_tier ? 'T' + d.top_tier : '--');
  if (!d) list.append(el('div', 'popsec', groupCard.failed ? 'The station did not answer' : 'Reading'));
  else if (!d.pilots.length) list.append(el('div', 'popsec', 'Nobody of them within the last hour'));
  else {
    for (const p of d.pilots) {
      const b = el('button', 'poprow group'), who = el('div', 'who'), hull = el('div', 'hull', p.hull ? p.hull + (p.tier ? '  T' + p.tier : '') : 'hull not seen');
      b.type = 'button';
      who.append(el('div', 'nm', p.name), el('div', 'at', 'jumped in ' + ago(p.age) + ' ago' + (p.times ? ' | met ' + p.times + (p.times === 1 ? ' time' : ' times') : ' | not met by our ships')));
      if (p.destroyed || p.hours) hull.append(el('small', null, (p.hours ? fmt(p.hours) + ' h played' : '') + (p.destroyed ? (p.hours ? ', ' : '') + fmt(p.destroyed) + ' kills' : '')));
      b.append(who, hull);
      b.title = 'Open ' + p.name + (p.tier > 1 ? ' | a tier ' + p.tier + ' hull needs Piloting ' + ({ 2: 10, 3: 20, 4: 30, 5: 50 }[p.tier] || '?') : '');
      b.addEventListener('click', () => { closePop(); showPilot(p.name); });
      list.append(b);
    }
  }
  const foot = el('div', 'popfoot'), go = el('button', 'poplink', 'Open ' + s.name);
  go.type = 'button'; go.addEventListener('click', () => { closePop(); select(s.id, false); });
  foot.append(go, el('span', null, 'who arrived, not who is still there'));
  box.replaceChildren(head, stats, list, foot);
  box.hidden = false;
  list.scrollTop = keep;
  placePop();
}

function renderPop() {
  const box = $('fleetpop');
  if (!pop) { box.hidden = true; return; }
  if (pop.kind === 'Group') { renderGroupPop(box); return; }
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
  if (r.status !== 'connected') return ['off', F.wave && F.wave.since && !F.wave.end ? 'reconnecting' : 'offline'];
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

function renderMembers() {                       // the top bar: the six members, each with its portrait and its ships; then the fleet
  const box = $('members'), by = new Map();
  box.replaceChildren();
  const purse = $('purse'), have = F.totals || {}, hour = have.rates && have.rates.windows ? have.rates.windows['1h'] : null;
  purse.replaceChildren(el('div', 'k', 'Credits'), el('div', 'v', have.ships ? fmt(have.credits) : '--'));
  if (hour) {                                     // what all wallets changed by per hour over the last hour, everything counted
    const line = el('div', 's');
    line.append(tint(hour.total_per_hour !== undefined ? hour.total_per_hour : hour.cph + hour.one_time_per_hour), ' /h');
    purse.append(line);
  }
  purse.title = 'All wallets of the fleet. Below: what they changed by per hour over the last hour, everything counted: steady money and rewards paid once';
  F.ships.forEach((r) => { if (!by.has(r.division)) by.set(r.division, []); by.get(r.division).push(r); });
  for (const a of (S ? S.roster : [])) {
    const list = by.get(a.division) || [], c = DIV[a.division] || DIV.Unassigned, b = el('button', 'member');
    const working = list.filter(isWorking).length, who = el('div', 'who');
    b.type = 'button';
    who.append(el('div', 'n', a.name), el('div', 'd', a.division));
    b.append(faceSvg(a.id, a.division, c, 30), who, el('div', 'c', String(list.length)));
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

function waveCause(w) {                          // what two readings show about a wave, never more
  return w.cause === 'engine' ? 'our ship engine restarted' : w.cause === 'update' ? 'the game changed version, ' + w.from + ' to ' + w.to : 'no engine restart and no new game version read';
}
function renderNotice() {                        // over the map: many ships off the game at once, named as what it is
  const box = $('notice'), w = F.wave;
  if (!w || !w.since) { box.hidden = true; return; }
  const at = clockZ(w.since * 1000), all = w.ships || F.ships.length;
  if (w.end) {
    box.textContent = 'All ships are back. ' + fmt(w.peak) + ' of ' + fmt(all) + ' were off the game from ' + at + ' to ' + clock(w.end * 1000) + ' ('
      + waveCause(w) + '). Runs cut in those minutes are flown again.';
  } else {
    const who = fmt(w.off) + ' of ' + fmt(all) + ' ships';
    box.textContent = w.cause === 'engine' ? 'Our ship engine restarted at ' + at + ': ' + who + ' are signing in again. It takes about four minutes and no ship is lost.'
      : w.cause === 'update' ? 'The game changed version (' + w.from + ' to ' + w.to + ') around ' + at + ': ' + who + ' are reconnecting by themselves. A restart of the game drops every player.'
        : who + ' lost the line to the game at ' + at + ' and are reconnecting by themselves. The cause is not read yet: a restart of the game for an update looks like this.';
  }
  box.className = 'notice ' + (w.end ? 'good' : 'warn');
  box.hidden = false;
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
  const time = $('clock');
  if (time) time.textContent = clockZ(Date.now());
}

function shipRow(r) {
  const [cls, what] = shipState(r), b = el('button', 'ship' + (r.name === selShip ? ' on' : ''));
  b.type = 'button';
  const who = el('div', 'who'), bars = el('div', 'bars'), cr = el('div', 'cr', r.piloting ? 'Lv ' + r.piloting : '');
  const nm = el('div', 'nm', r.name);
  if (r.flagship) {                               // a star after the name: a word would be cut off behind a long name
    const of = r.flagship_of || r.admiral || '';
    const flag = el('span', 'flag', '\u2605' + (of && of !== r.admiral ? ' ' + of : ''));
    flag.title = 'Flagship' + (of ? ' of ' + of : '');
    nm.append(flag);
  }
  who.append(nm, el('div', 'at', (r.system_name || r.system || 'position unknown') + ' | ' + what));
  bars.append(bar('hull', r.hull, r.max_hull, 0.5), bar('fuel', r.fuel, r.max_fuel, 0.25), bar('cargo', r.cargo_used, r.cargo_capacity));
  const best = (r.skill && r.skill[1] ? r.skill : r.top_skill) || ['', 0];
  cr.append(el('small', null, best[1] ? best[0].replace(/_/g, ' ').replace('deep core mining', 'deep core') + ' ' + best[1] : (r.class || '')));
  b.append(el('i', 'glyph ' + cls), who, bars, cr);
  b.title = r.name + ': hull ' + r.hull + '/' + r.max_hull + ', fuel ' + r.fuel + '/' + r.max_fuel + ', cargo ' + r.cargo_used + '/' + r.cargo_capacity
    + (r.piloting ? ' | Piloting ' + r.piloting : '') + (r.class ? ' | ' + r.class : '');
  b.addEventListener('click', () => selectShip(r.name, true));
  return b;
}

const oneDecimal = (n) => (typeof n === 'number' ? n.toFixed(1) : '--');
function crewLine(list, crew) {                  // under a division's head: what its average ship can take and deal, and its ships at work
  const line = el('div', 'crew'), n = { work: 0, move: 0, dock: 0, idle: 0, wait: 0, bad: 0, off: 0 };
  list.forEach((r) => { n[shipState(r)[0]] += 1; });
  const part = (label, value, title, cls) => { const s = el('span', cls || null); s.append(label + ' ', el('b', null, value)); s.title = title; line.append(s); };
  part('hull+shield', fmt(crew.hp), 'Hull and shield points of the average ship: what it can take');
  part('firepower', oneDecimal(crew.firepower), 'Damage per tick the weapons of the average ship deal: each weapon\'s damage divided by its cooldown, from the game\'s catalog. '
    + 'The starter\'s Pulse Laser I deals 10');
  const rest = [[n.dock, 'parked'], [n.idle, 'idle in space'], [n.bad, 'failing'], [n.off, F.wave && F.wave.since && !F.wave.end ? 'reconnecting' : 'offline']].filter((p) => p[0]);
  part('at work', (n.work + n.move + n.wait) + '/' + list.length, rest.length ? 'Without work: ' + rest.map((p) => p[0] + ' ' + p[1]).join(', ')
    : 'Every ship of the division has work' + (n.wait ? ' (' + n.wait + ' wait for ore at an empty field)' : ''), rest.length ? 'short' : null);
  return line;
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
    const crew = (((F.totals || {}).divisions || {})[division] || {}).crew, known = list.length && crew && crew.ships;
    if (known) {                                 // the division's average Piloting level; its money stands in the Metrics tab
      sum.append('Lv ', el('b', null, oneDecimal(crew.piloting)));
      sum.title = 'The average Piloting level of the division. Piloting 10, 20, 30 and 50 open the hull tiers 2 to 5';
    }
    head.append(sum); block.append(head);
    if (known) block.append(crewLine(list, crew));
    if (!list.length) block.append(el('div', 'noships', 'No ships yet'));
    if (!folded) list.forEach((r) => block.append(shipRow(r)));
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
    ['Security here', d.security || '-'], ['State as of', stampCet(d.state_at)],
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
  const own = holdBy.get(s.id) || [], site = sitesBy.get(s.id);
  if (own.length || (site && site.status !== 'dropped')) {       // what we own here and what we plan here
    panel.append(el('h3', null, 'Ours here'));
    if (own.length) panel.append(table(['Building', 'Tier', 'At', 'State'], own.map((b) => [b.name, b.level || '', b.at || '', (b.status || 'active').replace(/_/g, ' ')])));
    if (site && site.status !== 'dropped') panel.append(el('p', 'sub', 'A site for a base of ours: ' + site.status + (site.by ? ', proposed by ' + site.by : '') + '.'));
  }
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

let invMode = 'total', invItem = null;           // the Inventory tab: all we own by kind of item, or station by station; one item's card
const INV_KINDS = { raw: 'raw', refined: 'refined', component: 'part', module: 'module', consumable: 'consumable', ammo: 'ammo', drone: 'drone', other: 'other', contraband: 'contraband', unknown: 'not in catalog' };
function itemLink(id, name) { return linkButton(name, () => { invItem = id; render(); }, 'doclink'); }
function recipeRows(rows) {
  const line = (pairs) => pairs.map((p) => fmt(p[1]) + ' ' + p[0]).join(', ');
  return rows.map((r) => [r.doc ? linkButton(r.name || r.id, () => openDoc(r.doc), 'doclink') : (r.name || r.id), line(r.inputs), line(r.outputs), r.by_hand ? 'by hand' : 'facility']);
}
async function renderItem(panel, live) {
  const d = await get('/api/item?id=' + encodeURIComponent(invItem));
  if (!live()) return;
  panel.append(linkButton('Back to the inventory', () => { invItem = null; render(); }));
  if (d.error) { panel.append(el('p', 'empty', 'The catalog does not hold this item.')); return; }
  panel.append(el('h2', null, d.name), el('p', 'sub', d.description));
  panel.append(facts([['We own', fmt(d.units) + ' units'], ['Kind', INV_KINDS[d.kind] || d.kind], ['Base value', fmt(d.value) + ' cr'], ['Size', d.size]]));
  if (d.at.length) { panel.append(el('h3', null, 'Where ours lies')); panel.append(fitTable(table(['Place', 'Units'], d.at.map((a) => [a[0], fmt(a[1])]), [1]))); }
  panel.append(el('h3', null, 'Made by'));
  panel.append(d.made_by.length ? fitTable(table(['Recipe', 'Takes', 'Gives', 'Where'], recipeRows(d.made_by))) : el('p', 'empty', 'No recipe makes it: it is mined, hunted, found or bought.'));
  panel.append(el('h3', null, 'Goes into' + (d.used_total > d.used_in.length ? ' (' + d.used_in.length + ' of ' + d.used_total + ' recipes)' : '')));
  panel.append(d.used_in.length ? fitTable(table(['Recipe', 'Takes', 'Gives', 'Where'], recipeRows(d.used_in))) : el('p', 'empty', 'No recipe takes it.'));
  panel.append(el('h3', null, 'Built with it' + (d.built_total > d.built.length ? ' (' + d.built.length + ' of ' + d.built_total + ')' : '')));
  panel.append(d.built.length ? fitTable(table(['What', 'Kind', 'Units of it', 'Cost'], d.built.map((b) => [b.name, b.kind, fmt(b.units), fmt(b.cost)]), [2, 3]))
    : el('p', 'empty', 'No facility and no hull is built with it.'));
}
async function renderInventory(panel, live) {
  if (invItem) return renderItem(panel, live);
  const d = await get('/api/inventory');
  if (!live()) return;
  panel.append(el('h2', null, 'Inventory'));
  const docs = el('div', 'chips');                // the recipes: where the fleet keeps what can be made and built
  if (d.docs.master) docs.append(linkButton('Recipes: all ' + fmt(d.recipes) + ', by category', () => openDoc(d.docs.master)));
  if (d.docs.facilities) docs.append(linkButton('Facilities', () => openDoc(d.docs.facilities)));
  if (d.docs.modules) docs.append(linkButton('Modules', () => openDoc(d.docs.modules)));
  panel.append(docs);
  if (!d.written) { panel.append(el('p', 'empty', 'No storage book yet: the service that reads our storage has not written one.')); return; }
  panel.append(el('p', 'sub', 'Everything our pilots hold in station storage and in their holds, added up. Click an item to see where it lies, what makes it and what it is built into.'));
  const grid = el('div', 'kpis');
  const kpi = (k, v, sub) => { const b = el('div', 'kpi'); b.append(el('div', 'k', k), el('div', 'v', v)); if (sub) b.append(el('div', 's', sub)); grid.append(b); };
  const places = d.stations.filter((s) => s.base !== 'hold'), hold = d.stations.find((s) => s.base === 'hold');
  kpi('Kinds of item', fmt(d.total.items), fmt(d.total.units) + ' units in all');
  kpi('Worth at base value', fmt(d.total.worth), 'the catalog\'s value, not a price');
  kpi('Stations with stock', fmt(places.length), places.length ? 'most at ' + places[0].name : '');
  kpi('In the holds', hold ? fmt(hold.units) : '0', 'units our ships carry now');
  panel.append(grid);
  const pick = el('div', 'winsel');
  for (const [key, label] of [['total', 'All we own'], ['stations', 'By station']]) {
    const b = el('button', key === invMode ? 'on' : null, label);
    b.type = 'button';
    b.addEventListener('click', () => { invMode = key; render(); });
    pick.append(b);
  }
  panel.append(pick);
  const head = (title, n, units, worth) => { const h = el('h3', null, title); h.append(el('span', 'invsum', fmt(n) + ' kinds, ' + fmt(units) + ' units, worth ' + fmt(worth))); return h; };
  if (invMode === 'stations') {
    for (const s of d.stations) {
      panel.append(head(s.name, s.items, s.units, s.worth));
      panel.append(fitTable(table(['Item', 'Kind', 'Units', 'Worth'], s.rows.map((r) => [itemLink(r.id, r.name), INV_KINDS[r.kind] || r.kind, fmt(r.units), fmt(r.worth)]), [2, 3])));
    }
  } else {
    for (const g of d.groups) {
      panel.append(head(g.title, g.items, g.units, g.worth));
      panel.append(fitTable(table(['Item', 'Units', 'Stored', 'In holds', 'Value', 'Worth'],
        g.rows.map((r) => [itemLink(r.id, r.name), fmt(r.units), fmt(r.stored), fmt(r.held), fmt(r.value), fmt(r.worth)]), [1, 2, 3, 4, 5])));
    }
  }
  panel.append(el('p', 'docnote', 'Storage read through each pilot about every 40 minutes; book written ' + (d.written ? stampCet(d.written) : '--') + ', ' + fmt(d.pilots) + ' pilots read, the oldest reading '
    + (d.oldest ? stampCet(d.oldest) : '--') + '. Modules fitted on a ship and the ships themselves are not counted here.'));
}

function setWide(on) {                          // a document gets a wide panel, the Metrics tab ('metrics') a wider one; the map is resized to what is left
  const right = $('main-right'), want = on === 'metrics' ? 'metrics' : on ? 'wide' : '';
  const now = right.classList.contains('wide') ? 'wide' : right.classList.contains('metrics') ? 'metrics' : '';
  if (now === want) return;
  right.classList.toggle('wide', want === 'wide');
  right.classList.toggle('metrics', want === 'metrics');
  resize();
}

async function openDoc(path) {
  tab = 'Docs'; selShip = null; shipCard = null; docView = { path, text: '', loading: true };
  renderRoster(); render();
  try { docView = await get('/api/doc?path=' + encodeURIComponent(path)); } catch (e) { docView = { path, error: e.message }; }
  if (tab === 'Docs') render();
}

// ---- Markdown and logs as formatted text. Everything is built from DOM nodes with textContent; no HTML is parsed.
const DOC_RE = /^(reports|communications|governance|game\/(planets|players|factions|rules|routes\/guidebook|routes|fleet|catalog\/recipes|catalog\/ships|catalog))\/[A-Za-z0-9_.\-]{1,120}\.(md|log)$/;
function docTarget(target, base) {              // a link or a quoted path that names a document the station shows
  let t = String(target).split('#')[0];
  if (!t || t.includes('://') || t.startsWith('/')) return null;
  if (DOC_RE.test(t)) return t;                                    // a path from the repository's root
  if (!base || !base.includes('/')) return null;
  const parts = base.slice(0, base.lastIndexOf('/')).split('/');   // else relative to the document it stands in: a sub-folder, or `..`
  for (const seg of t.split('/')) { if (seg === '..') parts.pop(); else if (seg !== '.') parts.push(seg); }
  t = parts.join('/');
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
    top.append(name, el('span', 'tag', head[0].replace(/[[\]]/g, '')), el('span', 'tag' + (head[3] === 'error' ? ' bad' : ''), head[3] || ''), el('span', 'when', stampCet(head[1] || '')));
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
      if (isLog) panel.append(el('p', 'sub', 'The time of each entry is shown in your time (' + clockZ(Date.now()).slice(6) + '). Times inside the texts are as the members wrote them, in UTC.'));
      panel.append(isLog ? logView(docView.text, docView.cut, docView.path) : markdown(docView.text, docView.path, false));
    }
    return;
  }
  const d = await get('/api/docs');
  if (!live()) return;
  const row = (label, small, path) => { const b = linkButton(label, () => openDoc(path), 'rowlink'); if (small) b.append(el('small', null, small)); return b; };
  const report = (r) => {                        // the author in its division's colour and the time it was written, then the title
    const b = linkButton('', () => openDoc(r.path), 'rowlink report'), lead = el('span', 'lead'), who = el('b', 'who', r.author || 'unknown');
    const member = ((S && S.roster) || []).find((a) => a.id === String(r.author || '').toLowerCase());
    who.style.color = member ? (DIV[member.division] || DIV.Command) : 'var(--dim)';
    lead.append(who, el('span', 'when', stampCet(r.at || r.date || '')));
    b.append(lead, el('span', 'title', r.title));
    b.title = (r.author || 'unknown') + ', ' + (stampCet(r.at || r.date || '') || 'no time') + ': ' + r.title;
    return b;
  };
  panel.append(el('h3', null, 'Governance'));
  (d.governance || []).forEach((g) => panel.append(row(g.title, '', g.path)));
  panel.append(el('h3', null, 'Logs'));
  (d.logs || []).forEach((g) => panel.append(row(g.title, g.entries ? g.entries + ' entries, last by ' + g.last.by + ', ' + stampCet(g.last.at) : 'no entries', g.path)));
  panel.append(el('h3', null, 'Reports'));
  const reports = d.reports || [], total = d.reports_total || reports.length;
  if (reports.length) {
    panel.append(el('p', 'docnote', (total > reports.length ? 'The ' + reports.length + ' newest of ' + total : 'All ' + total) + ', newest first. Times in your time (' + clockZ(Date.now()).slice(6) + ').'));
    reports.forEach((r) => panel.append(report(r)));
  } else panel.append(el('p', 'empty', 'No report yet. One is written at every session end.'));
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
    g.fillText(clockZ(t0 * 1000), 6, h - 2);
    g.fillText(clock(t1 * 1000), w - 34, h - 2);
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
let metricsAt = 0;                               // when the Metrics tab was last drawn: it is drawn again every 30 s, not at every fleet poll
let routeOrder = { key: '', rank: new Map() };   // the place of each route row while the tab stays open on one window
function keepOrder(rows) {                       // a table that reorders under the eye cannot be read: rows keep their place, a new route joins at the end
  if (routeOrder.key !== metricWin) routeOrder = { key: metricWin, rank: new Map() };
  rows.forEach((x) => { if (!routeOrder.rank.has(x.route)) routeOrder.rank.set(x.route, routeOrder.rank.size); });
  return rows.sort((a, b2) => routeOrder.rank.get(a.route) - routeOrder.rank.get(b2.route));
}
let INCOME = { routes: [], at: 0, key: '' };

function fitTable(t) { const w = el('div', 'mtable'); w.append(t); return w; }   // a Metrics table that fits the panel

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
    ? 'All money over the last ' + span + '. Net is what the wallets changed by: steady money, which the fleet makes again and again, plus what the game paid once per pilot.'
      + (w.seed && w.seed.pilots ? ' ' + fmt(w.seed.pilots) + ' new pilots joined in this stretch: their first wallets are left out.'
        : '')
      + (w.presence && (w.presence.left || w.presence.back) ? ' A ship the engine stopped listing, or lists again, is left out with its wallet.'
        : w.ships_changed && !(w.seed && w.seed.pilots) ? ' The number of ships changed in this stretch and no record says how: the figures may be off by a ship\'s wallet.' : '')
      + (w.transfers_moved_per_hour ? ' Gifts between our own ships are neither income nor costs.' : '')
    : 'No figures for this stretch yet: the collector needs five minutes of samples.'));
  const grid = el('div', 'kpis');
  const kpi = (k, v, sub, cls) => { const b = el('div', 'kpi' + (cls ? ' ' + cls : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sub) b.append(el('div', 's', sub)); grid.append(b); return b; };
  const tone = (n) => (n < 0 ? ' neg' : n > 0 ? ' pos' : '');
  const whole = (y) => (y.total_per_hour !== undefined ? y.total_per_hour : (y.cph || 0) + (y.one_time_per_hour || 0));   // a fleet file of before 2026-11-17 has no total
  const net = w ? whole(w) : 0;
  kpi('Net / h', w ? signed(net) : '--', 'everything: steady money plus paid once', 'main' + (w ? tone(net) : ''));
  kpi('Steady net / h', w ? signed(w.cph) : '--', 'income minus costs: what repeats', 'main' + (w ? tone(w.cph) : ''));
  kpi('Paid once / h', w ? signed(w.one_time_per_hour) : '--', 'rewards once per pilot, less goods bought for them', w ? tone(w.one_time_per_hour).trim() : '');
  kpi('Net per ship / h', w ? signed(Math.round(net / (t.ships || 1))) : '--', 'everything, per ship', w ? tone(net).trim() : '');
  kpi('Steady income / h', w ? fmt(w.income_per_hour) : '--', 'sales and repeatable rewards', w && w.income_per_hour > 0 ? 'pos' : '');
  kpi('Running costs / h', w ? fmt(w.costs_per_hour) : '--', 'fuel, repairs, goods, modules', w && w.costs_per_hour > 0 ? 'neg' : '');
  const metered = w && w.fuel_cr_per_hour !== undefined;
  kpi('Fuel / h', metered ? fmt(w.fuel_cr_per_hour) : '--', metered ? fmt(w.fuel_units_per_hour) + ' units bought' : 'not measured in this stretch yet', metered && w.fuel_cr_per_hour > 0 ? 'neg' : '');
  kpi('Repairs / h', metered ? fmt(w.repair_cr_per_hour) : '--', metered ? fmt(w.hull_points_per_hour) + ' hull points' : 'not measured in this stretch yet', metered && w.repair_cr_per_hour > 0 ? 'neg' : '');
  kpi('Ships working', t.ships ? fmt(t.working) + ' of ' + fmt(t.ships) : '--',
    fmt(t.parked) + ' parked at a station' + (t.adrift ? ', ' + fmt(t.adrift) + ' in space without work' : ''));
  kpi('Credits', fmt(t.credits), fmt(t.credits_per_ship) + ' per ship');
  panel.append(grid);
  if (w && w.wallets) {                           // the books close: the wallets at the start plus the net of the stretch are the wallets now
    const made = w.wallets.end - w.wallets.start - (w.wallets.left_out || 0), check = el('p', 'sub', 'The books close: ' + fmt(w.wallets.start) + ' cr in the wallets ' + span + ' ago, ');
    check.append(tint(made), ' net in this stretch' + (w.wallets.left_out ? ', ' + signed(w.wallets.left_out) + ' with ships that joined or left' : '') + ', ' + fmt(w.wallets.end) + ' cr now.');
    if (w.unexplained_per_hour !== undefined) {   // the game's own counters of credits earned and spent, set beside the wallets
      const off = Object.entries(w.divisions || {}).filter(([, y]) => Math.abs(y.unexplained_per_hour || 0) >= 500).map(([d]) => d);
      check.append(Math.abs(w.unexplained_per_hour) < 500 && !off.length
        ? ' The game\'s own counters of credits earned and spent agree with the wallets.'
        : ' The game\'s own counters and the wallets differ by ' + fmt(Math.abs(w.unexplained_per_hour)) + ' cr an hour in this stretch' + (off.length ? ' (' + off.join(', ') + ')' : '')
          + '. No record names the cause; it may be a wallet the engine had not read again after a gift between our ships. Income, costs and net of this stretch may be '
          + 'off by that much; a longer stretch evens it out.');
    }
    panel.append(check);
  }
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
  const moneyRow = (name, working, y) => [name, working, w ? shade(y.income_per_hour, 'pos') : '--', w ? shade(y.costs_per_hour, 'neg') : '--', w ? tint(y.cph || 0) : '--',
    w ? tint(y.one_time_per_hour || 0) : '--', w ? tint(whole(y)) : '--'];
  panel.append(fitTable(table(['Division', 'Working', 'Steady income', 'Running costs', 'Steady net', 'Paid once', 'Net / h'],
    order.map(([d, adm]) => {
      const x = div[d] || {}, y = dw[d] || {}, name = el('span', null, d);
      name.style.color = DIV[d] || DIV.Unassigned; name.title = adm ? 'Admiral ' + adm : '';
      return moneyRow(name, fmt(x.working) + ' / ' + fmt(x.ships), y);
    }).concat([moneyRow(el('b', null, 'Fleet'), fmt(t.working) + ' / ' + fmt(t.ships), w || {})]), [1, 2, 3, 4, 5, 6])));
  panel.append(el('p', 'sub', 'Per hour. Steady net = steady income - running costs. Net = steady net + paid once: what the division\'s wallets changed by, '
    + 'gifts between our own ships left out.'));
  const waves = (F.waves || []).slice().reverse();     // many ships off the game at once: written down by the collector, newest first
  panel.append(el('h3', null, 'Ships off the game'));
  if (waves.length) {
    panel.append(fitTable(table(['When', 'Ships off', 'Minutes', 'What the readings show'],
      waves.map((x) => [stampOf(x.since * 1000), fmt(x.peak) + ' of ' + fmt(x.ships), x.minutes, waveCause(x)]), [1, 2])));
    panel.append(el('p', 'sub', 'A wave is many ships losing the line to the game at once. They reconnect by themselves; a run cut in those minutes is flown again.'));
  } else {
    panel.append(el('p', 'empty', 'No wave on record yet. When many ships lose the line to the game at once (the game restarts for an update, or our ship engine restarts), '
      + 'it is written down here with its time, its length and what the readings show.'));
  }
  const routesBox = el('div'), graphs = el('div');
  panel.append(el('h3', null, 'Where the money comes from, last ' + routeHours + ' hours'), routesBox, el('h3', null, 'Last ' + graphHours + ' hours'), graphs);
  panel.append(el('p', 'sub', 'How it is counted. Net: the change of the wallets. Steady income: the game\'s counter of credits earned, less the rewards paid once per pilot. '
    + 'Running costs: everything spent, less what was bought for such a reward. Paid once: those rewards less those goods; a mission pays each pilot once, so this money ends. '
    + 'Goods in storage are no money until they are sold: the Inventory tab holds them. Fuel and repairs: counted when a docked ship\'s tank or hull rises and its wallet falls. '
    + 'A route\'s figure counts only runs that read a wallet.'));
  if (Date.now() - HIST.at > 30000 || HIST.key !== metricWin) {
    try { HIST = Object.assign(await get('/api/history?q=' + graphHours), { at: Date.now(), key: metricWin }); } catch (e) { HIST = { rows: [], at: Date.now(), key: metricWin }; }
    if (!live()) return;
  }
  if (Date.now() - INCOME.at > 30000 || INCOME.key !== metricWin) {
    try { INCOME = Object.assign(await get('/api/income?q=' + routeHours), { at: Date.now(), key: metricWin }); } catch (e) { INCOME = { routes: [], at: Date.now(), key: metricWin }; }
    if (!live()) return;
  }
  const steady = keepOrder(INCOME.routes.filter((x) => !x.once && (x.runs || x.flying)).sort((a, b2) => b2.credits - a.credits));
  if (steady.length) {
    routesBox.append(fitTable(table(['Route', 'Ships now', 'Runs', 'Ship-hours', 'Credits', 'Per ship-hour'], steady.map((x) => {
      const name = el('span', null, x.route);
      name.title = x.title || '';
      return [name, x.flying || '', x.runs, x.ship_hours, tint(x.credits), x.per_ship_hour === null ? 'no reading' : tint(x.per_ship_hour)];
    }), [1, 2, 3, 4, 5])));
  } else routesBox.append(el('p', 'empty', 'No run of a repeating route in this stretch.'));
  const rows = HIST.rows || [];
  graphs.append(
    chart('Net per hour, over the ' + behind + ' minutes before:', [{ pts: trailing(rows, behind, 1), colour: '#dcae58', name: 'everything' }, { pts: trailing(rows, behind, 5), colour: '#a48be0', name: 'steady' }]),
    chart('Per hour:', [{ pts: trailing(rows, behind, 3), colour: '#58c08c', name: 'income' }, { pts: trailing(rows, behind, 4), colour: '#e06c66', name: 'costs' }]),
    chart('Ships working', [{ pts: rows.map((p) => [p[0], p[6]]), colour: '#6fa8dc' }]),
    chart('Credits, all wallets', [{ pts: rows.map((p) => [p[0], p[1]]), colour: '#dcae58' }]));
}

const TABS = { Selection: renderSelection, Metrics: renderMetrics, Inventory: renderInventory, Docs: renderDocs };
let renderSeq = 0, viewKey = '';
function render() {
  const panel = $('panel'), mine = ++renderSeq, live = () => mine === renderSeq;
  const key = [tab, selShip, selShip ? '' : selected, pilotCard ? pilotCard.name : '', docView ? docView.path : '', tab === 'Inventory' ? invMode + '/' + (invItem || '') : ''].join('|');
  const same = key === viewKey, keep = same ? panel.scrollTop : 0;
  viewKey = key;
  document.querySelectorAll('nav button').forEach((b) => b.classList.toggle('on', b.textContent === tab));
  $('rail-right-label').textContent = tab;
  if (tab !== 'Docs') setWide(tab === 'Metrics' || tab === 'Inventory' ? 'metrics' : false);
  if (tab === 'Metrics') {
    metricsAt = Date.now();
    if (!same) routeOrder.key = '';                // the tab was opened anew: the routes are sorted afresh
    if (same && panel.childElementCount) {         // a refresh of the open tab: built aside and swapped in whole, so the page keeps its height, its place and its order
      const aside = document.createDocumentFragment();
      Promise.resolve(renderMetrics(aside, live)).then(() => {
        if (!live()) return;
        const at = panel.scrollTop;
        panel.replaceChildren(aside);
        panel.scrollTop = at;
      }).catch(() => { /* the last picture stays */ });
      return;
    }
  }
  panel.replaceChildren();
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
  // kind 'wide' or 'opt': shown in a very wide window only, so that the top bar is never cut; a state that is not good always shows,
  // and the box's tooltip names all of them
  const item = (label, value, cls, kind) => { const s = el('span', kind || null); if (cls) s.append(el('i', 'dot ' + cls)); s.append(label + ' '); s.append(el('b', null, value)); box.append(s); };
  item('Time', clockZ(Date.now()));
  box.lastChild.querySelector('b').id = 'clock';
  box.lastChild.title = 'Your time (' + ZONE + '). Every time on this page is shown in it; the logs and the data keep UTC';
  item('Fleet data', fleetAgeText(), fleetLive() ? 'good' : 'bad');
  box.lastChild.querySelector('b').id = 'fleet-age';
  box.lastChild.title = 'How old the picture of our ships is. The collector reads the engine every 10 seconds, about once a game tick';
  item('Online', fmt(st.online_players));
  box.lastChild.title = 'Players in the game right now, by the game\'s own count; the station reads it every minute';
  item('Tick', fmt(st.tick), null, 'wide'); item('Game', st.version || '?', null, 'wide');
  const liveStream = L.stream || {}, streams = Boolean(liveStream.connected && liveStream.age < 60);
  item('Stream', streams ? 'live' : 'down', streams ? 'good' : 'bad', streams ? 'opt' : null);
  if (S) {
    const bad = Object.entries(S.sources).filter(([, s]) => s.error || s.age < 0).map(([n]) => n);
    item('Sources', bad.length ? 'problem: ' + bad.join(', ') : 'good', bad.length ? 'warn' : 'good', bad.length ? null : 'opt');
  }
  box.title = [...box.children].map((s) => s.textContent).join(' | ');
  const bar = box.parentElement;                 // the status box is never cut: where it would be, the search field gives way
  bar.classList.remove('tight');
  if (box.scrollWidth > box.clientWidth + 1) bar.classList.add('tight');
}

// ---------------------------------------------------------------- comms: one conversation with all six members

const chat = { after: 0, timer: 0, busy: false, first: true, unseen: 0 };
function markUnseen(n) {                         // answers that came while the messages are hidden: a count on the dock's toggle
  chat.unseen = n;
  const u = $('dock-unseen');
  u.textContent = n ? n + ' new' : '';
  u.hidden = !n;
}
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
  $('chat-input').placeholder = 'To ' + (all ? 'everyone' : to.join(', ')) + '. Click a face or type @Name to choose. Enter sends.';
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
    head.append(faceSvg(a.id, a.division, c, 18), name, el('span', null, ' ' + a.division));
  }
  head.append(el('span', 'when', clock((m.t || 0) * 1000)));
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
    if (!chat.first && shut.has('dock')) markUnseen(chat.unseen + d.messages.filter((m) => m.who !== 'suggi').length);
    if (chat.first && !log.children.length) {
      log.append(el('div', 'chathint', 'One conversation with Unity and the five Admirals. A message goes to Unity unless it names someone: click a face below or type @Name; @all reaches everyone.'));
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
    b.append(faceSvg(a.id, a.division, c, 22), el('span', null, a.name));
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
  const xs = S.systems.map((s) => s.x), ys = S.systems.map((s) => s.y), spans = [];
  bounds = S.systems.length ? { x0: Math.min(...xs), x1: Math.max(...xs), y0: Math.min(...ys), y1: Math.max(...ys) } : null;
  for (const s of S.systems) for (const id of s.lanes) { const o = sys.get(id); if (o && s.id < id) spans.push(Math.hypot(s.x - o.x, s.y - o.y)); }
  spans.sort((a, b) => a - b);
  terrR = spans.length ? 0.5 * spans[spans.length >> 1] : 250;   // half a usual lane: neighbours of one empire grow together
  homeEmpire = (sys.get(S.home) || {}).empire || '';
  sitesBy.clear();
  (S.sites || []).forEach((t) => sitesBy.set(t.system, t));
  holdBy.clear();
  ((S.holdings || {}).buildings || []).forEach((b) => { if (!holdBy.has(b.system)) holdBy.set(b.system, []); holdBy.get(b.system).push(b); });
  const spaces = new Map();
  for (const s of S.systems) { if (s.empire) { if (!spaces.has(s.empire)) spaces.set(s.empire, []); spaces.get(s.empire).push(s); } }
  realmNames = [...spaces].map(([name, list]) => ({ word: (name === 'outerrim' ? 'outer rim' : name).toUpperCase(), colour: color(list[0]),
    x: list.reduce((a, o) => a + o.x, 0) / list.length, y0: Math.min(...list.map((o) => o.y)), y1: Math.max(...list.map((o) => o.y)) }));
  realmVer++;
  const legend = $('legend');
  legend.replaceChildren();
  const head = (words) => legend.append(el('span', 'lhead', words));
  const row = (icon, words, wide) => { const span = el('span', wide ? 'lrow full' : 'lrow'); span.append(icon, words); legend.append(span); };
  const swatch = (edge, fill) => { const i = el('i', 'swatch'); i.style.borderColor = edge; i.style.background = fill; return i; };
  head('Regions');
  for (const [name, c] of Object.entries(S.empires)) {
    const colour = HEX.test(c) ? c : LAWLESS;
    row(swatch(rgba(colour, 0.75), rgba(colour, 0.22)), name === 'outerrim' ? 'outer rim' : name);
  }
  const free = el('i'); free.style.background = LAWLESS;
  row(free, 'lawless');
  row(swatch(rgba(OURS, 0.9), rgba(OURS, 0.16)), 'our space: where our ships were in the last hour, and our buildings', true);
  head('Our fleet');
  row(tokenSvg(), 'our ships: a slice per division, their number inside; outer ring: whose space', true);
  for (const kind of KINDS.slice(0, 6)) {            // the silhouette of each kind, as in the roster
    const span = el('span', 'lrow kind');
    span.append(shipSvg(kind === 'Command' ? 'Flagship' : kind, DIV[kind], 13), kind === 'Command' ? 'command group' : kind.toLowerCase());
    legend.append(span);
  }
  head('Ours');
  row(glyphSvg('storage', BUILT, 13), 'shared storage');
  row(glyphSvg('recruit', BUILT, 13), 'hiring office');
  row(glyphSvg('office', BUILT, 13), 'other office');
  row(glyphSvg('outpost', BUILT, 13), 'outpost');
  row(glyphSvg('station', BUILT, 13), 'station');
  row(glyphSvg('storage', RAISING, 13), 'amber: not active yet');
  row(glyphSvg('flag', OURS, 13), 'site chosen for a base');
  row(glyphSvg('flag', rgba(OURS, 0.7), 13, true), 'candidate site');
  head('Others');
  row(glyphSvg('pip', '#aeb5cc', 12), 'station');
  row(glyphSvg('pip', '#e8c35a', 12), 'a player faction\'s base');
  row(glyphSvg('cross', '#e06c66', 12), 'pirate stronghold');
  row(glyphSvg('threat', '#dcae58', 12), 'danger by our intel');
  row(glyphSvg('threat', '#e06c66', 12), 'high danger');
  row(el('span', 'ltag', 'TAG 5'), 'foreign faction, its pilots in the last hour', true);
  const seen = el('i', 'seen');
  row(seen, 'traffic in the last hour', true);
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
  const nowMs = Date.now();                    // our own space: every system where a ship of ours was seen in the last hour; the browser remembers it over a reload
  let moved = false;
  for (const id of shipsBy.keys()) { if (!sphere.has(id)) moved = true; sphere.set(id, nowMs); }
  for (const [id, at] of sphere) { if (nowMs - at > SPHERE_MS) { sphere.delete(id); moved = true; } }
  if (moved) realmVer++;
  if (nowMs - sphereSaved > 60000) { sphereSaved = nowMs; try { localStorage.setItem('station.sphere', JSON.stringify([...sphere])); } catch (e) { /* no storage */ } }
  renderMembers(); renderRoster(); renderNotice(); tickAges(); renderPop(); draw();
  if (tab === 'Metrics' && Date.now() - metricsAt >= 30000) render();   // not at every poll: the page under the reader stays still
  if (selShip) {
    const name = selShip;
    try {
      const d = await get('/api/ship?name=' + encodeURIComponent(name)), mark = JSON.stringify(d);
      if (selShip === name && mark !== shipMark) { shipMark = mark; shipCard = d; if (tab === 'Selection') render(); }
    } catch (e) { /* keep the last card */ }
  }
}

// ---------------------------------------------------------------- what folds away: side panels, comms messages, legend, layers

const SHUTTERS = {                               // name: [the element that folds, its button, the button's title open, and shut]
  left: ['side-left', 'hide-left', 'Hide the fleet panel', 'Show the fleet panel'],
  right: ['main-right', 'hide-right', 'Hide the right panel', 'Show the right panel'],
  dock: ['chat-dock', 'dock-toggle', 'Hide the messages', 'Show the messages'],
  layers: ['layers-box', 'layers-toggle', 'Hide the layers', 'Show the layers'],
  legend: ['legend-box', 'legend-toggle', 'Hide the legend', 'Show the legend'],
};
function applyShut(name) {
  const [box, button, open, closed] = SHUTTERS[name], on = shut.has(name), b = $(button);
  $(box).classList.toggle('shut', on);
  b.title = on ? closed : open;
  b.setAttribute('aria-expanded', on ? 'false' : 'true');
}
function toggleShut(name) {
  if (shut.has(name)) shut.delete(name); else shut.add(name);
  saveShut(); applyShut(name);
  if (name === 'dock' && !shut.has('dock')) { markUnseen(0); const log = $('chat-log'); log.scrollTop = log.scrollHeight; }
  if (name === 'left' || name === 'right') setTimeout(resize, 260);   // once the slide has ended the map takes the new width, also where no observer fires
}
function initShutters() {
  document.body.classList.add('still');          // the remembered state is shown at once, without the slide
  Object.keys(SHUTTERS).forEach((name) => { applyShut(name); $(SHUTTERS[name][1]).addEventListener('click', () => toggleShut(name)); });
  document.querySelectorAll('.rail').forEach((r) => r.addEventListener('click', () => toggleShut(r.dataset.side)));
  requestAnimationFrame(() => requestAnimationFrame(() => document.body.classList.remove('still')));
  if (!window.ResizeObserver) return;
  new ResizeObserver(() => {                     // the map column changed size (a panel slid, a tab widened): redraw at once, no blank frame
    resize();
    if (raf) { cancelAnimationFrame(raf); frame(performance.now()); }
  }).observe($('map-col'));
  new ResizeObserver(() => $('map-col').style.setProperty('--dockh', $('chat-dock').offsetHeight + 'px')).observe($('chat-dock'));   // legend and layers stay above comms
}

function init() {
  initShutters();
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
    b.addEventListener('click', () => { tab = name; if (name !== 'Selection') pilotCard = null; if (name !== 'Docs') docView = null; invItem = null; render(); });
    nav.append(b);
  }
  let drag = null, moved = false;
  canvas.addEventListener('mousedown', (e) => { cam = null; drag = [e.clientX, e.clientY, view.x, view.y]; moved = false; canvas.classList.add('drag'); });
  window.addEventListener('mouseup', () => { drag = null; canvas.classList.remove('drag'); });
  const dragTo = (e) => {
    if (Math.abs(e.clientX - drag[0]) + Math.abs(e.clientY - drag[1]) > 3) moved = true;
    view.x = drag[2] - (e.clientX - drag[0]) / view.k; view.y = drag[3] - (e.clientY - drag[1]) / view.k;
    draw();
  };
  window.addEventListener('mousemove', (e) => { if (drag && e.target !== canvas) dragTo(e); });   // a drag goes on over the boxes on the map
  canvas.addEventListener('mousemove', (e) => {
    const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
    if (drag) { dragTo(e); return; }
    const tip = $('tip'), badge = S && badgeAt(mx, my), grp = !badge && S && groupAt(mx, my), s = !badge && !grp && S && nearest(mx, my);
    hover = s ? s.id : null; hoverBadge = badge || null;
    canvas.style.cursor = badge || grp ? 'pointer' : '';
    const placeName = (b) => { const o = sys.get(b.system); return o ? o.name : b.system; };
    if (badge) {
      const at = sys.get(badge.system) || {};
      tip.textContent = badge.count + (badge.count === 1 ? ' ship' : ' ships') + ' of ours at ' + placeName(badge) + ' (' + (at.empire || 'lawless') + '): ' + badge.parts + ' | click for the card';
      tip.style.left = mx + 14 + 'px'; tip.style.top = my + 12 + 'px'; tip.hidden = false;
    } else if (grp) {
      const g = grp.group;
      tip.textContent = '[' + g.tag + '] ' + (g.name || 'a faction') + ': ' + g.count + ' pilots jumped into ' + placeName(grp) + ' in the last hour | our standing: ' + g.standing + ' | click for the pilots and their ships';
      tip.style.left = mx + 14 + 'px'; tip.style.top = my + 12 + 'px'; tip.hidden = false;
    } else if (s) {
      const ours = (shipsBy.get(s.id) || []).length, own = holdBy.get(s.id) || [], site = sitesBy.get(s.id);
      tip.textContent = s.name + (s.empire ? ' (' + s.empire + ')' : '') + ' | ' + (L.hour[s.id] || 0) + ' pilots in the last hour' + (ours ? ' | ' + ours + ' of ours' : '')
        + (own.length ? ' | ours: ' + own.map((b) => b.name + (stands(b) ? '' : ' (' + String(b.status).replace(/_/g, ' ') + ')')).join(', ') : '')
        + (site && site.status !== 'dropped' && site.status !== 'built' ? ' | a site for a base: ' + site.status : '');
      tip.style.left = mx + 14 + 'px'; tip.style.top = my + 12 + 'px'; tip.hidden = false;
    } else tip.hidden = true;
    draw();
  });
  canvas.addEventListener('mouseleave', () => { $('tip').hidden = true; hover = null; hoverBadge = null; draw(); });
  canvas.addEventListener('click', (e) => {
    if (moved || !S) return;
    const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top, badge = badgeAt(mx, my);
    if (badge) { $('tip').hidden = true; select(badge.system, false); openPop(badge.system, badge.kind); return; }   // our ships stand in the system's own place: the system is picked and their card opens
    const grp = groupAt(mx, my);
    if (grp) { $('tip').hidden = true; openGroup(grp.system, grp.group); return; }
    const s = nearest(mx, my);
    if (pop) closePop();
    if (s) select(s.id, false);
  });
  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left - W / 2, my = e.clientY - r.top - H / 2;
    const k = Math.max(minZoom(), Math.min(3, view.k * (e.deltaY < 0 ? 1.2 : 1 / 1.2)));
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
