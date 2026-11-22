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
const SHORT_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
function clock(ms) { const p = zoned(ms); return p.hour + ':' + p.minute; }                                    // 06:28
function clockZ(ms) { const p = zoned(ms); return p.hour + ':' + p.minute; }                                   // concise HH:MM (zone implied)
function stampOf(ms) {                                                                                          // concise '22 Nov 16:18'
  const p = zoned(ms), mo = SHORT_MONTHS[Math.max(0, Math.min(11, (+p.month || 1) - 1))];
  return (+p.day) + ' ' + mo + ' ' + p.hour + ':' + p.minute;
}
function stampCet(text) {                          // convert UTC ISO/file stamps to short local '22 Nov 16:18' or '22 Nov'
  const s = String(text || '').trim();
  const m = /^(\d{4})-(\d\d)-(\d\d)[ T](\d\d):(\d\d)(?::(\d\d))?/.exec(s);
  if (m) return stampOf(Date.UTC(+m[1], m[2] - 1, +m[3], +m[4], +m[5], +(m[6] || 0)));
  const d = /^(\d{4})-(\d\d)-(\d\d)$/.exec(s);
  if (d) return (+d[3]) + ' ' + SHORT_MONTHS[Math.max(0, Math.min(11, +d[2] - 1))];
  return s;
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
const LINE = { fill: 'none', stroke: 'C', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
const HEAD = { fill: 'C', 'fill-opacity': 0.22, stroke: 'C', 'stroke-width': 1.45, 'stroke-linejoin': 'round' };
const FACES = {
  unity: [                                          // Command (Unity): Sovereign Fleet Admiral -- crown crest, neural halo, panoramic star-visor & high collar
    ['circle', { cx: 20, cy: 20, r: 18, fill: 'C', 'fill-opacity': 0.08, stroke: 'C', 'stroke-opacity': 0.35, 'stroke-width': 1 }],
    ['path', { d: 'M6 36 L11 29 H29 L34 36 Z', fill: 'C', 'fill-opacity': 0.28, stroke: 'C', 'stroke-width': 1.2 }],
    ['path', { d: 'M12 11 L15.5 5.5 L20 9 L24.5 5.5 L28 11', fill: 'C', 'fill-opacity': 0.35, stroke: 'C', 'stroke-width': 1.4, 'stroke-linejoin': 'round' }],
    ['circle', { cx: 20, cy: 4.8, r: 1.5, fill: 'W' }],
    ['path', { ...HEAD, d: 'M10.5 12.5 L20 9.5 L29.5 12.5 L30.5 23.5 L25 32 H15 L9.5 23.5 Z' }],
    ['path', { d: 'M12 18.2 L20 20.2 L28 18.2 L27 23.2 L20 25 L13 23.2 Z', fill: 'K', stroke: 'C', 'stroke-width': 1.1 }],
    ['path', { d: 'M14 20.8 L20 22.3 L26 20.8', fill: 'none', stroke: 'W', 'stroke-width': 1.5, 'stroke-linecap': 'round' }],
    ['path', { ...LINE, d: 'M16.5 28 H23.5 M20 10 V15.5', 'stroke-width': 1.2 }],
  ],
  zero: [                                           // Mining (Zero): Deep-Core Exo-Prospector -- twin bore-lamps, heavy dome helm, laser visor & industrial respirator
    ['circle', { cx: 20, cy: 20, r: 18, fill: 'C', 'fill-opacity': 0.08, stroke: 'C', 'stroke-opacity': 0.32, 'stroke-width': 1 }],
    ['path', { d: 'M5.5 36 L9.5 29.5 H30.5 L34.5 36 Z', fill: 'C', 'fill-opacity': 0.25, stroke: 'C', 'stroke-width': 1.2 }],
    ['path', { d: 'M9 17 C9 8.5 31 8.5 31 17 Z', fill: 'C', 'fill-opacity': 0.42, stroke: 'C', 'stroke-width': 1.4 }],
    ['rect', { x: 15, y: 7.2, width: 10, height: 4.6, rx: 1.6, fill: 'K', stroke: 'C', 'stroke-width': 1.2 }],
    ['circle', { cx: 17.8, cy: 9.5, r: 1.2, fill: 'W' }], ['circle', { cx: 22.2, cy: 9.5, r: 1.2, fill: 'W' }],
    ['path', { ...HEAD, d: 'M9.5 17 H30.5 V26.5 L26 33 H14 L9.5 26.5 Z' }],
    ['rect', { x: 11.8, y: 19.2, width: 7.2, height: 4.6, rx: 1.4, fill: 'K', stroke: 'C', 'stroke-width': 1.1 }],
    ['rect', { x: 21, y: 19.2, width: 7.2, height: 4.6, rx: 1.4, fill: 'K', stroke: 'C', 'stroke-width': 1.1 }],
    ['line', { x1: 13.5, y1: 21.5, x2: 17.2, y2: 21.5, stroke: 'W', 'stroke-width': 1.3 }],
    ['line', { x1: 22.8, y1: 21.5, x2: 26.5, y2: 21.5, stroke: 'W', 'stroke-width': 1.3 }],
    ['rect', { x: 14.2, y: 26.2, width: 11.6, height: 5.4, rx: 1.8, fill: 'K', stroke: 'C', 'stroke-width': 1.1 }],
    ['path', { ...LINE, d: 'M17 27.6 V30.2 M20 27.6 V30.2 M23 27.6 V30.2', 'stroke-width': 1.1 }],
  ],
  mercury: [                                        // Trade (Mercury): Syndicate High-Broker -- swept Hermes cyber-wings, guild collar & HUD market monocle
    ['circle', { cx: 20, cy: 20, r: 18, fill: 'C', 'fill-opacity': 0.08, stroke: 'C', 'stroke-opacity': 0.32, 'stroke-width': 1 }],
    ['path', { d: 'M7 36 L11.5 28.5 L20 32.5 L28.5 28.5 L33 36 Z', fill: 'C', 'fill-opacity': 0.28, stroke: 'C', 'stroke-width': 1.2 }],
    ['path', { d: 'M10.5 16.5 L3.8 10.5 L6.8 16.8 L4.2 19 L10.5 21 Z', fill: 'C' }],
    ['path', { d: 'M29.5 16.5 L36.2 10.5 L33.2 16.8 L35.8 19 L29.5 21 Z', fill: 'C' }],
    ['path', { ...HEAD, d: 'M11 14 C11 8 29 8 29 14 L28.5 25 Q20 33.5 11.5 25 Z' }],
    ['polygon', { points: '20,10.2 22.2,12.8 20,15.4 17.8,12.8', fill: 'W' }],
    ['circle', { cx: 15.6, cy: 20.5, r: 3.4, fill: 'K', stroke: 'W', 'stroke-width': 1.2 }],
    ['circle', { cx: 15.6, cy: 20.5, r: 1.2, fill: 'C' }],
    ['path', { ...LINE, d: 'M15.6 15.8 V17.1 M15.6 23.9 V25.2 M10.9 20.5 H12.2', 'stroke-width': 0.9 }],
    ['path', { d: 'M22.2 19.8 L26.8 19.2 L25.8 21.6 L22.2 21.4 Z', fill: 'W' }],
    ['path', { ...LINE, d: 'M16.5 26.8 Q20.5 28.8 24 26.2', 'stroke-width': 1.3 }],
  ],
  apollo: [                                         // Logistics (Apollo): Orbital Starwright -- solar gantry arch, structural engineer helm & dual blueprint optics
    ['circle', { cx: 20, cy: 20, r: 18, fill: 'C', 'fill-opacity': 0.08, stroke: 'C', 'stroke-opacity': 0.32, 'stroke-width': 1 }],
    ['path', { d: 'M5.5 36 L8.5 29 H31.5 L34.5 36 Z', fill: 'C', 'fill-opacity': 0.28, stroke: 'C', 'stroke-width': 1.3 }],
    ['path', { ...LINE, d: 'M7.5 16 A13 13 0 0 1 32.5 16', 'stroke-width': 1.5 }],
    ['circle', { cx: 20, cy: 3.5, r: 1.6, fill: 'W' }],
    ['circle', { cx: 10.2, cy: 8.8, r: 1.3, fill: 'C' }], ['circle', { cx: 29.8, cy: 8.8, r: 1.3, fill: 'C' }],
    ['rect', { ...HEAD, x: 10, y: 11.5, width: 20, height: 20.5, rx: 4 }],
    ['path', { d: 'M10 15.5 H30', stroke: 'C', 'stroke-width': 1.8 }],
    ['rect', { x: 12.2, y: 18.2, width: 15.6, height: 5.2, rx: 1.4, fill: 'K', stroke: 'C', 'stroke-width': 1.1 }],
    ['rect', { x: 13.8, y: 19.8, width: 4.8, height: 2, rx: 0.6, fill: 'W' }],
    ['rect', { x: 21.4, y: 19.8, width: 4.8, height: 2, rx: 0.6, fill: 'W' }],
    ['path', { ...LINE, d: 'M15 27.5 H25 M17.5 29.8 H22.5', 'stroke-width': 1.3 }],
  ],
  apophis: [                                        // Military (Apophis): Praetorian Dreadnought Warlord -- swept battle-crest, armored cheek plates & V-slit visor
    ['circle', { cx: 20, cy: 20, r: 18, fill: 'C', 'fill-opacity': 0.08, stroke: 'C', 'stroke-opacity': 0.35, 'stroke-width': 1 }],
    ['path', { d: 'M6 36 L10 28.5 L20 33 L30 28.5 L34 36 Z', fill: 'C', 'fill-opacity': 0.3, stroke: 'C', 'stroke-width': 1.2 }],
    ['path', { d: 'M10.5 14 L4.5 6 L8.8 18.5 Z', fill: 'C' }],
    ['path', { d: 'M29.5 14 L35.5 6 L31.2 18.5 Z', fill: 'C' }],
    ['polygon', { points: '20,3.8 22.4,11.5 20,15 17.6,11.5', fill: 'C' }],
    ['path', { ...HEAD, d: 'M10.5 11.5 L20 8.5 L29.5 11.5 L31 23.5 L24.5 33 H15.5 L9 23.5 Z' }],
    ['polygon', { points: '11.2,18 20,22.2 28.8,18 27.4,22.4 20,25.8 12.6,22.4', fill: 'K', stroke: 'C', 'stroke-width': 1 }],
    ['polyline', { points: '13,19.6 20,23 27,19.6', fill: 'none', stroke: 'W', 'stroke-width': 1.6, 'stroke-linecap': 'round' }],
    ['path', { ...LINE, d: 'M16.5 29.2 L20 27.6 L23.5 29.2', 'stroke-width': 1.3 }],
  ],
  oracle: [                                         // Intel (Oracle): Voidborn Recon Seer -- stealth cowl hood, tri-optic sensor triangle & telemetry arcs
    ['circle', { cx: 20, cy: 20, r: 18, fill: 'C', 'fill-opacity': 0.08, stroke: 'C', 'stroke-opacity': 0.32, 'stroke-width': 1 }],
    ['path', { d: 'M6.5 36 C8.5 27 12 24 20 24 C28 24 31.5 27 33.5 36 Z', fill: 'C', 'fill-opacity': 0.22 }],
    ['path', { d: 'M20 5.5 C10 6.5 7.5 16.5 8.5 28.5 L14.5 33.5 H25.5 L31.5 28.5 C32.5 16.5 30 6.5 20 5.5 Z', fill: 'C', 'fill-opacity': 0.24, stroke: 'C', 'stroke-width': 1.45 }],
    ['path', { d: 'M12 14.5 Q20 10.5 28 14.5 L26.5 29 H13.5 Z', fill: 'K', stroke: 'C', 'stroke-width': 1 }],
    ['circle', { cx: 20, cy: 20.5, r: 4.3, fill: 'K', stroke: 'C', 'stroke-width': 1.2 }],
    ['circle', { cx: 20, cy: 20.5, r: 1.8, fill: 'W' }],
    ['circle', { cx: 14.8, cy: 16.2, r: 1.1, fill: 'C' }], ['circle', { cx: 25.2, cy: 16.2, r: 1.1, fill: 'C' }],
    ['path', { ...LINE, d: 'M5.2 16 Q3 20.5 5.2 25 M34.8 16 Q37 20.5 34.8 25', 'stroke-width': 1.2 }],
  ],
};
function faceSvg(id, division, colour, size) {
  const parts = FACES[id];
  if (!parts) return shipSvg(division === 'Command' ? 'Flagship' : division, colour, Math.round(size * 0.7));
  const NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 40 40'); svg.setAttribute('width', size); svg.setAttribute('height', size);
  svg.setAttribute('class', 'face'); svg.setAttribute('aria-hidden', 'true');
  for (const [tag, attrs] of parts) {
    const e = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v === 'C' ? colour : v === 'K' ? '#0b0e15' : v === 'W' ? '#f4f7ff' : v));
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
let noticeShut = '';                           // the wave notice closed by hand: its key (since and whether it ended)
const NOTICE_GOOD_SECONDS = 120;               // the green 'all back' notice goes by itself this long after the wave ended
let HIST = { rows: [], at: 0 };                // /api/history, for the Metrics tab
const collapsed = new Set();                   // divisions folded in the roster; default folds bulk divisions for a clean outliner
try {
  const savedFolds = localStorage.getItem('station.folded');
  if (savedFolds === null) ['Mining', 'Trade', 'Logistics', 'Military', 'Intel'].forEach((d) => collapsed.add(d));
  else JSON.parse(savedFolds).forEach((d) => collapsed.add(String(d)));
} catch (e) { /* no storage */ }
function saveFolds() { try { localStorage.setItem('station.folded', JSON.stringify([...collapsed])); } catch (e) { /* no storage */ } }
const shut = new Set();                        // what Suggi has hidden: the side panels, the messages of comms, the legend, the layers; remembered
try { JSON.parse(localStorage.getItem('station.hidden') || '[]').forEach((d) => shut.add(String(d))); } catch (e) { /* no storage */ }
function saveShut() { try { localStorage.setItem('station.hidden', JSON.stringify([...shut])); } catch (e) { /* no storage */ } }
let board = null;
let rosterMode = 'all', rosterQuery = '', rosterSort = 'name', rosterDiv = 'all', selSub = 'Overview', shipSub = 'Loadout';
const sys = new Map();
const stationsBy = new Map();
const shipsBy = new Map();                     // system id -> our ships there
const layers = { Regions: true, 'Our space': true, Lanes: true, Traffic: true, Stations: true, 'Our bases': true, Strongholds: true, Intel: true, Factions: true, Fleet: true, Names: true };
const sitesBy = new Map();                     // system id -> a site named for a base of ours (game/map/sites.tsv)
const holdBy = new Map();                      // system id -> the buildings of ours there (what the faction owns, read from the game)
try { localStorage.removeItem('station.sphere'); } catch (e) { /* no storage */ }   // the last-hour space of round 3, no longer drawn
let bounds = null, terrR = 250, homeEmpire = '';   // the galaxy's extent; the radius of the ground under one system; our empire
const view = { x: 0, y: 0, k: 0.05 };
let selected = null, hover = null, route = [], tab = 'Selection', pilotCard = null;
let selShip = null, shipCard = null, shipMark = '', docView = null;
const groupsBy = new Map();
const battleSystems = new Set();                    // system id -> the larger groups of one foreign faction seen there
let groupHits = [], infraHits = [];            // foreign tags and our own building/site pills as drawn
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

const OURS = '#86d65b';                              // our colour (Suggi, 2026-11-17: green): our space, our buildings, our sites
const BUILT = OURS, RAISING = '#dcae58';             // a building of ours the game lists as active; one it does not (being built, or down)
// One drawing per mark in a box of 12 by 12: the map paints it on the canvas, the legend shows the same path as an SVG.
const GLYPHS = {
  storage: { d: 'M1.6 2.4H10.4V4.6H1.6Z M2.3 4.6H9.7V10.2H2.3Z M4.8 6.3H7.2' },       // a chest with its lid
  recruit: { d: 'M6 1.9a2 2 0 1 0 0 4a2 2 0 1 0 0-4Z M2.3 10.4c0-2.3 1.6-3.6 3.7-3.6s3.7 1.3 3.7 3.6Z', fill: true },
  office: { d: 'M2.4 10.2V4.6L6 2 9.6 4.6V10.2Z M4.9 10.2V7.4H7.1V10.2' },
  outpost: { d: 'M6 1.3 10.1 3.65V8.35L6 10.7 1.9 8.35V3.65Z', fill: true },          // a solid hexagon
  station: { d: 'M6 1.6a4.4 4.4 0 1 0 0 8.8a4.4 4.4 0 1 0 0-8.8Z M6 4.4a1.6 1.6 0 1 1 0 3.2a1.6 1.6 0 1 1 0-3.2Z', fill: true },   // a ring: the inner circle runs the other way round, so it stays open
  fuel: { d: 'M6 1.5C6 1.5 2.6 5.5 2.6 7.6a3.4 3.4 0 0 0 6.8 0C9.4 5.5 6 1.5 6 1.5Z', fill: true },   // a drop
  foundry: { d: 'M2.2 9.8H9.8L10.6 7.3H7.8V4.6L9.4 2.8H2.6L4.2 4.6V7.3H1.4Z', fill: true },           // an industrial anvil
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
function lineHome(from) {                             // the systems on the shortest lane path from a system to our home space
  const prev = new Map([[from, null]]), queue = [from];
  while (queue.length) {
    const here = queue.shift(), s = sys.get(here);
    if (!s) continue;
    if (s.empire && s.empire === homeEmpire) {
      const out = [];
      for (let at = here; at !== null; at = prev.get(at)) out.push(sys.get(at));
      return out;
    }
    for (const next of s.lanes) { if (sys.has(next) && !prev.has(next)) { prev.set(next, here); queue.push(next); } }
  }
  return [sys.get(from)].filter(Boolean);
}
function ourSpace() {                                // our space: home (our empire's space) and a line out to each building of ours beyond it
  const home = homeEmpire ? S.systems.filter((s) => s.empire === homeEmpire) : [];
  const far = [...holdBy.keys()].map((id) => sys.get(id)).filter((s) => s && s.empire !== homeEmpire);
  return { home, far, lines: far.map((s) => lineHome(s.id)) };
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
      for (const [empire, list] of realms) { if (!(layers['Our space'] && empire === homeEmpire)) area(list, color(list[0]), 0.1, 0.5, R); }   // our home is drawn as our space
    }
    if (layers['Our space']) {
      const ours = ourSpace();
      area(ours.home, OURS, 0.1, 0.6, R);
      for (const line of ours.lines) area(line, OURS, 0.16, 0.8, R * 0.36);   // the lines going out, along the lanes
      for (const s of ours.far) area([s], OURS, 0.18, 0.85, R * 0.75);
    }
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
      ctx.fillStyle = rgba(n.home && layers['Our space'] ? OURS : n.colour, (0.55 * fade).toFixed(2));
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
  badgeHits = []; groupHits = []; infraHits = [];
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
    if (own.length || planned) {                                    // ours: beacon halo + frosted building/site pill with glyphs & smart tag
      const kinds = new Map(), row = [];
      const based = own.some((b) => b.kind === 'outpost' || b.kind === 'station');
      const chosen = planned && site.status === 'chosen';
      const siteInfo = ((OPS.data && OPS.data.empire && OPS.data.empire.sites) || []).find((x) => x.system === s.id);
      const pctTag = siteInfo && siteInfo.need_pct !== null && siteInfo.need_pct !== undefined ? ' ' + Math.round(siteInfo.need_pct) + '%' : '';
      // Beacon ring around the star so our buildings & chosen sites stand out at galaxy zoom
      const haloR = (ours ? q + 3.8 : q + 5.5);
      ctx.save();
      if (based) {
        ctx.strokeStyle = rgba(OURS, 0.92); ctx.lineWidth = 2.0;
        ctx.beginPath(); ctx.arc(x, y, haloR, 0, 6.2832); ctx.stroke();
        ctx.strokeStyle = rgba(OURS, 0.28); ctx.lineWidth = 4.5;
        ctx.beginPath(); ctx.arc(x, y, haloR + 2.2, 0, 6.2832); ctx.stroke();
      } else if (own.length) {
        ctx.strokeStyle = 'rgba(110, 220, 165, 0.85)'; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.arc(x, y, haloR, 0, 6.2832); ctx.stroke();
      } else if (chosen) {
        ctx.setLineDash([3.5, 3]); ctx.strokeStyle = '#e8c35a'; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.arc(x, y, haloR, 0, 6.2832); ctx.stroke();
      }
      ctx.restore();
      for (const b of own) { if (based && b.part) continue; if (!kinds.has(b.kind)) kinds.set(b.kind, true); if (!stands(b)) kinds.set(b.kind, false); }
      for (const [kind, done] of kinds) row.push([kind, done ? BUILT : RAISING, false]);
      if (planned) row.push(['flag', chosen ? '#e8c35a' : rgba(OURS, 0.72), !chosen]);
      const showTag = s.id === selected || s.id === hover || ((based || own.length || chosen) ? k >= 0.055 : k >= 0.11);
      let tagWord = '';
      if (showTag) {
        if (based) tagWord = own.some((b) => b.kind === 'station') ? 'STATION' : 'OUTPOST';
        else if (own.length) {
          const tags = [];
          if (kinds.has('recruit')) tags.push('200 CAP');
          if (kinds.has('foundry')) tags.push('FOUNDRY');
          if (kinds.has('storage')) tags.push(tags.length ? 'STORE' : 'LOCKBOX');
          if (kinds.has('fuel')) tags.push('FUEL');
          if (!tags.length) tags.push('OFFICE');
          tagWord = tags.slice(0, 2).join('+');
        } else if (chosen) tagWord = 'NEXT SITE' + pctTag;
        else if (planned) tagWord = 'SITE' + pctTag;
      }
      if (row.length && (based || own.length || chosen || k >= 0.045 || s.id === selected || s.id === hover)) {
        ctx.save();
        ctx.font = '600 9.5px ui-monospace, SFMono-Regular, Consolas, monospace';
        const iconSpan = row.length * 13 + 2;
        const textW = tagWord ? ctx.measureText(tagWord).width + 6 : 0;
        const pw = iconSpan + textW + 6, ph = 16;
        const px = x - pw / 2, py = y - q - ph - 7;
        pill(px, py, pw, ph);
        ctx.fillStyle = 'rgba(11, 16, 25, 0.92)'; ctx.fill();
        ctx.strokeStyle = based ? rgba(OURS, 0.85) : own.length ? 'rgba(110, 220, 165, 0.7)' : chosen ? 'rgba(232, 195, 90, 0.8)' : rgba(OURS, 0.42);
        ctx.lineWidth = based || chosen ? 1.25 : 1; ctx.stroke();
        row.forEach(([gname, colour, hollow], i) => glyph(ctx, gname, px + 9.5 + i * 13, py + ph / 2, 11, colour, hollow));
        if (tagWord) {
          ctx.textBaseline = 'middle';
          ctx.fillStyle = based ? '#b8f297' : own.length ? '#9fe8c3' : chosen ? '#f3d783' : '#b7d9a5';
          ctx.fillText(tagWord, px + iconSpan + 4, py + ph / 2 + 0.5);
        }
        ctx.restore();
        infraHits.push({ x: px, y: py, w: pw, h: ph, system: s.id, own, site, siteInfo });
      }
    }
    if (s.id === selected) {
      const beat = (Math.sin(t * 2.6) + 1) / 2, ring = ours ? q + 4.5 : q + 8.5;
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1.8;
      ctx.beginPath(); ctx.arc(x, y, ring, 0, 6.2832); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,' + (0.3 * (1 - beat)).toFixed(2) + ')'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(x, y, ring + 0.5 + beat * 6, 0, 6.2832); ctx.stroke();
    }
    if (battleSystems.has(s.id)) {
      const beat = (Math.sin(t * 4.2) + 1) / 2, ring = (ours ? q + 6 : q + 9);
      ctx.strokeStyle = 'rgba(224,108,102,0.9)'; ctx.lineWidth = 1.6;
      ctx.beginPath(); ctx.arc(x, y, ring, 0, 6.2832); ctx.stroke();
      ctx.strokeStyle = 'rgba(224,108,102,' + (0.5 * (1 - beat)).toFixed(2) + ')'; ctx.lineWidth = 1.4;
      ctx.beginPath(); ctx.arc(x, y, ring + 1 + beat * 11, 0, 6.2832); ctx.stroke();
    }
    if (rivalFocus && (rivalFocus.bases.has(s.id) || rivalFocus.systems.has(s.id))) {
      const isRivalBase = rivalFocus.bases.has(s.id);
      const beat = (Math.sin(t * 3.1) + 1) / 2, ring = (ours ? q + 7 : q + 9.5);
      const rc = isRivalBase ? '#ff6b6b' : '#f0b45a';
      ctx.save();
      if (!isRivalBase) ctx.setLineDash([4, 3]);
      ctx.strokeStyle = rc; ctx.lineWidth = isRivalBase ? 2.2 : 1.6;
      ctx.beginPath(); ctx.arc(x, y, ring, 0, 6.2832); ctx.stroke();
      ctx.setLineDash([]);
      if (isRivalBase) {
        ctx.strokeStyle = 'rgba(255,107,107,' + (0.42 * (1 - beat)).toFixed(2) + ')'; ctx.lineWidth = 2.0;
        ctx.beginPath(); ctx.arc(x, y, ring + 1.5 + beat * 8, 0, 6.2832); ctx.stroke();
      }
      ctx.font = '600 9.5px ui-monospace, SFMono-Regular, Consolas, monospace';
      const rtag = rivalFocus.tag + (isRivalBase ? ' BASE' : ' SEEN');
      const tw = ctx.measureText(rtag).width + 10, rx = x - tw / 2, ry = y - ring - 17;
      pill(rx, ry, tw, 14);
      ctx.fillStyle = isRivalBase ? 'rgba(42,14,18,0.92)' : 'rgba(38,28,12,0.9)'; ctx.fill();
      ctx.strokeStyle = rc; ctx.lineWidth = 1.1; ctx.stroke();
      ctx.textBaseline = 'middle'; ctx.fillStyle = isRivalBase ? '#ffb3b3' : '#f7d494';
      ctx.fillText(rtag, rx + 5, ry + 7.5);
      ctx.restore();
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
  const taken = badgeHits.concat(groupHits, infraHits).map((b) => [b.x, b.y, b.x + b.w, b.y + b.h]);
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
function purseNet(y) {                         // the net of everything of the whole purse an hour: wallets and treasury as one
  const total = y.total_per_hour !== undefined ? y.total_per_hour : (y.cph || 0) + (y.one_time_per_hour || 0);   // a fleet file of before 2026-11-17 has no total
  return y.purse_per_hour !== undefined ? y.purse_per_hour : total;
}
function tint(n) { return el('span', n < 0 ? 'neg' : n > 0 ? 'pos' : null, signed(n)); }   // a signed number: green above zero, red below
function shade(n, cls) {                       // an amount without a sign: income green, a cost red; below zero it cannot be: amber
  const s = el('span', n > 0 ? cls : n < 0 ? 'warn' : null, fmt(n));
  if (n < 0) s.title = 'Below zero: this cannot be. A fault of the books, e.g. ships that changed division inside the stretch';
  return s;
}
function liveAge() { return F.age < 0 ? -1 : F.age + Math.round((Date.now() - fetchedAt) / 1000); }

function isWorking(r) { return ['work', 'move', 'wait'].includes(shipState(r)[0]); }

function renderMembers() {                       // the top bar: dual purse (Liquid Credits + 24h /h & Enterprise Value), six bespoke Admiral cards, and Fleet total
  const box = $('members'), by = new Map();
  box.replaceChildren();
  const purse = $('purse'), have = F.totals || {};
  const wins = (have.rates && have.rates.windows) || {};
  const win24 = wins['24h'] || wins[metricWin] || null;
  const treasury = (S && S.holdings && S.holdings.treasury) || 0;
  const liquid = (have.credits || 0) + treasury;
  const bs = (OPS.data && OPS.data.balance_sheet) || null;
  const netWorth = bs && bs.net_worth ? bs.net_worth : null;

  purse.replaceChildren();
  const cCol = el('div', 'pcol');
  cCol.append(el('div', 'k', 'Credits'), el('div', 'v', have.ships ? fmt(liquid) : '--'));
  if (win24) {
    const line = el('div', 's');
    line.append(tint(purseNet(win24)), ' /h ', el('span', 'win', wins['24h'] ? '24h' : WINDOWS[metricWin][0].toLowerCase()));
    cCol.append(line);
  }
  cCol.title = 'Liquid Purse: ship wallets (' + fmt(have.credits) + ' cr) + faction treasury (' + fmt(treasury) + ' cr). Rate below is net cash flow /h over 24 hours.';

  const eCol = el('div', 'pcol ent');
  eCol.append(el('div', 'k', 'Enterprise'), el('div', 'v', netWorth ? fmtCompact(netWorth) + ' cr' : '--'));
  const eSub = el('div', 's', bs ? 'vault ' + fmtCompact(bs.vault_worth || 0) + ' + bases' : 'loading balance sheet');
  eCol.append(eSub);
  if (bs) {
    eCol.title = 'Consolidated Enterprise Value: ' + fmt(bs.net_worth) + ' cr\n'
      + '- Liquid Cash: ' + fmt(bs.liquid_cash) + ' cr\n'
      + '- Station Vault Inventory: ' + fmt(bs.vault_worth) + ' cr\n'
      + '- Fleet Hulls & Fitted Modules: ' + fmt(bs.fleet_book) + ' cr\n'
      + '- Sovereign Facilities: ' + fmt(bs.facility_invested) + ' cr\nClick to open Metrics.';
  }
  purse.onclick = () => { tab = 'Metrics'; render(); };
  purse.append(cCol, eCol);

  F.ships.forEach((r) => { if (!by.has(r.division)) by.set(r.division, []); by.get(r.division).push(r); });
  for (const a of (S ? S.roster : [])) {
    const list = by.get(a.division) || [], c = DIV[a.division] || DIV.Unassigned, b = el('button', 'member');
    const working = list.filter(isWorking).length, who = el('div', 'who');
    b.type = 'button';
    const med = el('span', 'face-medallion');
    med.append(faceSvg(a.id, a.division, c, 30));
    who.append(el('div', 'n', a.name), el('div', 'd', a.division));
    const cnt = el('div', 'c', String(list.length));
    if (working < list.length) cnt.classList.add('has-idle');
    b.append(med, who, cnt);
    b.style.setProperty('--c', c);
    b.title = a.name + ' (' + a.rank + ' -- ' + a.division + '): ' + working + '/' + list.length + ' active | Click to message ' + a.name;
    b.addEventListener('click', () => openCommsFor(a.id));
    box.append(b);
  }
  const t = F.totals || {}, all = el('div', 'member total'), who = el('div', 'who');
  who.append(el('div', 'n', 'Fleet'), el('div', 'd', t.ships ? (t.working || 0) + ' active' : 'no data'));
  all.append(who, el('div', 'c', fmt(t.ships)));
  all.title = 'Total Fleet: ' + fmt(t.working) + ' active, ' + fmt(t.parked) + ' docked, ' + fmt(t.adrift) + ' adrift';
  box.append(all);
}

function waveCause(w) {                          // what two readings show about a wave, never more
  return w.cause === 'engine' ? 'our ship engine restarted' : w.cause === 'update' ? 'the game changed version, ' + w.from + ' to ' + w.to : 'no engine restart and no new game version read';
}
function renderNotice() {                        // over the map: many ships off the game at once, named as what it is
  const box = $('notice'), w = F.wave;
  if (!w || !w.since) { box.hidden = true; return; }
  const key = w.since + ':' + (w.end ? 'end' : 'on');
  if (key === noticeShut || (w.end && Date.now() / 1000 - w.end > NOTICE_GOOD_SECONDS)) { box.hidden = true; return; }
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
  const shut = el('button', 'close', '\u00d7');
  shut.type = 'button'; shut.title = 'Close';
  shut.addEventListener('click', () => { noticeShut = key; box.hidden = true; });
  box.append(shut);
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

function isUpgradedHull(clsName) {
  return Boolean(clsName && !/^threshold$/i.test(String(clsName).trim()));
}

function shipRow(r) {
  const [cls, what] = shipState(r), b = el('button', 'ship' + (r.name === selShip ? ' on' : ''));
  b.type = 'button';
  const who = el('div', 'who'), bars = el('div', 'bars'), cr = el('div', 'cr');
  const lvSpan = el('span', !isUpgradedHull(r.class) && (r.piloting || 0) >= 10 ? 'ready-lv' : null, r.piloting ? 'Lv ' + r.piloting : '');
  cr.append(lvSpan);
  const nm = el('div', 'nm', r.name);
  if (r.flagship) {
    const of = r.flagship_of || r.admiral || '';
    const flag = el('span', 'flag', '\u2605' + (of && of !== r.admiral ? ' ' + of : ''));
    flag.title = 'Flagship' + (of ? ' of ' + of : '');
    nm.append(flag);
  }
  if (isUpgradedHull(r.class)) nm.append(el('span', 't2badge', r.class));
  const locTxt = (r.system_name || r.system || '?') + ' - ' + what;
  who.append(nm, el('div', 'at', locTxt));
  bars.append(bar('hull', r.hull, r.max_hull, 0.5), bar('fuel', r.fuel, r.max_fuel, 0.25), bar('cargo', r.cargo_used, r.cargo_capacity));
  const best = (r.skill && r.skill[1] ? r.skill : r.top_skill) || ['', 0];
  cr.append(el('small', null, best[1] ? best[0].replace(/_/g, ' ').replace('deep core mining', 'core').replace('asteroid mining', 'mining') + ' ' + best[1] : (r.class || '')));
  b.append(el('i', 'glyph ' + cls), who, bars, cr);
  b.title = r.name + ' (' + (r.class || 'Threshold') + ') | hull ' + r.hull + '/' + r.max_hull + ', fuel ' + r.fuel + '/' + r.max_fuel
    + ', cargo ' + r.cargo_used + '/' + r.cargo_capacity + (r.piloting ? ' | Piloting ' + r.piloting : '');
  b.addEventListener('click', () => selectShip(r.name, true));
  b.addEventListener('dblclick', () => {
    selectShip(r.name, true);
    if (r.system && sys.has(r.system)) { const o = sys.get(r.system); flyTo(o.x, o.y, Math.max(view.k, 0.28)); }
  });
  return b;
}

const oneDecimal = (n) => (typeof n === 'number' ? n.toFixed(1) : '--');

function shipAlert(r) {
  const cls = shipState(r)[0];
  if (cls === 'bad' || cls === 'off') return true;
  if (r.max_hull > 0 && r.hull / r.max_hull < 0.6) return true;
  if (r.max_fuel > 0 && r.fuel / r.max_fuel < 0.25) return true;
  if (typeof r.credits === 'number' && r.credits < 10000) return true;
  return false;
}
function shipMatches(r) {
  const [cls, what] = shipState(r);
  if (rosterMode === 'active' && !['work', 'move', 'wait'].includes(cls)) return false;
  if (rosterMode === 'idle' && !['dock', 'idle'].includes(cls)) return false;
  if (rosterMode === 'alert' && !shipAlert(r)) return false;
  if (rosterQuery) {
    const hay = (r.name + ' ' + (r.system_name || r.system || '') + ' ' + what + ' ' + (r.division || '') + ' ' + (r.class || '')).toLowerCase();
    if (!hay.includes(rosterQuery)) return false;
  }
  return true;
}
function sortShips(list) {
  const out = list.slice();
  if (rosterSort === 'health') {
    const score = (r) => Math.min(r.max_hull > 0 ? r.hull / r.max_hull : 1, r.max_fuel > 0 ? r.fuel / r.max_fuel : 1) + (shipAlert(r) ? -1 : 0);
    out.sort((a, b) => score(a) - score(b) || a.name.localeCompare(b.name));
  } else if (rosterSort === 'credits') {
    out.sort((a, b) => (a.credits || 0) - (b.credits || 0) || a.name.localeCompare(b.name));
  } else if (rosterSort === 'piloting') {
    out.sort((a, b) => (b.piloting || 0) - (a.piloting || 0) || a.name.localeCompare(b.name));
  }
  return out;
}
function divMeter(list) {
  const m = el('div', 'divbar'), n = list.length || 1;
  let w = 0, id = 0, bad = 0;
  list.forEach((r) => {
    const c = shipState(r)[0];
    if (c === 'work' || c === 'move' || c === 'wait') w++;
    else if (c === 'dock' || c === 'idle') id++;
    else bad++;
  });
  if (w) { const s = el('i', 'w'); s.style.width = (100 * w / n).toFixed(1) + '%'; m.append(s); }
  if (id) { const s = el('i', 'id'); s.style.width = (100 * id / n).toFixed(1) + '%'; m.append(s); }
  if (bad) { const s = el('i', 'b'); s.style.width = (100 * bad / n).toFixed(1) + '%'; m.append(s); }
  m.title = w + ' working, ' + id + ' idle/parked, ' + bad + ' failing/offline';
  return m;
}
function setRosterMode(mode) {
  rosterMode = mode;
  document.querySelectorAll('#rfilters .rf').forEach((b) => b.classList.toggle('on', b.dataset.mode === mode));
  renderRoster();
}
function ensureDivStrip(divisions) {
  const tools = $('roster-tools');
  if (!tools) return;
  let strip = $('divstrip');
  if (!strip) {
    strip = el('div', 'divstrip');
    strip.id = 'divstrip';
    tools.prepend(strip);
  }
  strip.replaceChildren();
  const shortLbl = { Command: 'Cmd', Mining: 'Min', Trade: 'Trd', Logistics: 'Log', Military: 'Mil', Intel: 'Int', Unassigned: 'Un' };
  const items = [['all', 'All', 'var(--accent)']].concat(divisions.map(([d]) => [d, shortLbl[d] || d.slice(0, 3), DIV[d] || DIV.Unassigned]));
  for (const [key, lbl, col] of items) {
    const b = el('button', 'divchip' + (rosterDiv === key ? ' on' : ''), lbl);
    b.type = 'button';
    b.style.setProperty('--c', col);
    b.title = key === 'all' ? 'Show all 6 divisions' : 'Focus ' + key + ' division';
    b.addEventListener('click', () => { rosterDiv = rosterDiv === key && key !== 'all' ? 'all' : key; renderRoster(); });
    strip.append(b);
  }
}
function renderRoster() {
  const box = $('roster'), keep = box.scrollTop, by = new Map();
  box.replaceChildren();
  const counts = { all: F.ships.length, active: 0, idle: 0, alert: 0 };
  F.ships.forEach((r) => {
    const c = shipState(r)[0];
    if (['work', 'move', 'wait'].includes(c)) counts.active++;
    if (['dock', 'idle'].includes(c)) counts.idle++;
    if (shipAlert(r)) counts.alert++;
    if (!by.has(r.division)) by.set(r.division, []);
    by.get(r.division).push(r);
  });
  document.querySelectorAll('#rfilters .rf').forEach((b) => {
    const m = b.dataset.mode, lbl = m === 'all' ? 'All' : m === 'active' ? 'Active' : m === 'idle' ? 'Idle' : 'Alerts';
    b.textContent = counts[m] && m !== 'all' ? lbl + ' ' + counts[m] : lbl;
    b.classList.toggle('on', m === rosterMode);
    b.classList.toggle('haswarn', m === 'idle' && counts.idle > 0);
    b.classList.toggle('hasbad', m === 'alert' && counts.alert > 0);
  });
  const divisions = (S ? S.roster : []).filter((a) => a.division !== 'Command' || by.has('Command')).map((a) => [a.division, a]);
  if (by.has('Unassigned')) divisions.push(['Unassigned', null]);
  ensureDivStrip(divisions);

  const filtering = rosterMode !== 'all' || Boolean(rosterQuery) || rosterDiv !== 'all';
  let shownTotal = 0;

  for (const [division, admiral] of divisions) {
    if (rosterDiv !== 'all' && division !== rosterDiv) continue;
    const raw = by.get(division) || [];
    const list = (rosterMode !== 'all' || rosterQuery) ? sortShips(raw.filter(shipMatches)) : sortShips(raw);
    if ((rosterMode !== 'all' || rosterQuery) && !list.length) continue;
    shownTotal += list.length;

    let atWork = 0;
    raw.forEach((r) => { const st = shipState(r)[0]; if (st === 'work' || st === 'move' || st === 'wait') atWork++; });
    const forceOpen = rosterMode !== 'all' || Boolean(rosterQuery) || rosterDiv === division;
    const folded = !forceOpen && collapsed.has(division);
    const c = DIV[division] || DIV.Unassigned;

    const block = el('div', 'div');
    const card = el('div', 'divcard');
    const head = el('div', 'divhead');
    head.style.borderLeftColor = c;

    const toggleDivisionFold = () => {
      if (rosterDiv === division) {
        rosterDiv = 'all';
        collapsed.add(division);
      } else if (folded) {
        collapsed.delete(division);
      } else {
        collapsed.add(division);
      }
      saveFolds();
      renderRoster();
    };

    const name = el('button', 'name', division);
    name.type = 'button';
    const fold = el('span', 'fold', folded ? '+' : '-');
    name.prepend(fold);
    fold.after(shipSvg(division === 'Command' ? 'Flagship' : division, c, 13));
    name.style.color = c;
    name.title = (folded ? 'Unfold ' : 'Fold ') + division + ' (' + raw.length + ' ships)';
    name.setAttribute('aria-expanded', folded ? 'false' : 'true');
    name.addEventListener('click', toggleDivisionFold);
    head.append(name);

    if (admiral) {
      const b = linkButton('@' + admiral.name, (ev) => { if (ev && ev.stopPropagation) ev.stopPropagation(); openCommsFor(admiral.id); }, 'adm');
      b.title = 'Message ' + admiral.name + ' in Comms';
      head.append(b);
    }

    const metaRight = el('span', 'divmeta');
    metaRight.style.cursor = 'pointer';
    metaRight.addEventListener('click', toggleDivisionFold);
    const crew = (((F.totals || {}).divisions || {})[division] || {}).crew;
    if (crew && crew.ships) {
      const lvEl = el('span', 'divcph', 'Lv ' + oneDecimal(crew.piloting));
      lvEl.title = 'Avg Piloting ' + oneDecimal(crew.piloting) + ' | Avg Hull+Shield ' + fmt(crew.hp) + ' | Avg Firepower ' + oneDecimal(crew.firepower);
      metaRight.append(lvEl);
    }
    const wp = el('span', 'divpill' + (atWork < raw.length ? ' warn' : ''), atWork + '/' + raw.length);
    wp.title = atWork + ' active of ' + raw.length + ' ships (click to fold/unfold)';
    metaRight.append(wp);
    head.append(metaRight);

    card.append(head);
    if (raw.length) card.append(divMeter(raw));
    block.append(card);

    if (!raw.length) block.append(el('div', 'noships', 'No ships assigned'));
    if (!folded) list.forEach((r) => block.append(shipRow(r)));
    box.append(block);
  }
  const meta = $('roster-meta');
  if (meta) {
    if (filtering) {
      meta.replaceChildren(el('span', null, (rosterDiv !== 'all' ? rosterDiv + ': ' : 'Showing ') + shownTotal + ' of ' + F.ships.length + ' ships'));
      const clr = el('button', 'mini', 'Reset');
      clr.type = 'button';
      clr.addEventListener('click', () => { rosterMode = 'all'; rosterDiv = 'all'; rosterQuery = ''; const inp = $('roster-filter'); if (inp) inp.value = ''; renderRoster(); });
      meta.append(clr);
      meta.hidden = false;
    } else meta.hidden = true;
  }
  if (filtering && !shownTotal) box.append(el('p', 'empty', 'No ships match this filter.'));
  box.scrollTop = keep;
  const all = $('fold-all'), names = divisions.map((d) => d[0]), everyFolded = names.length > 0 && names.every((d) => collapsed.has(d));
  all.textContent = everyFolded ? 'Unfold all' : 'Fold all';
  all.onclick = () => { rosterDiv = 'all'; names.forEach((d) => (everyFolded ? collapsed.delete(d) : collapsed.add(d))); saveFolds(); renderRoster(); };
  const fresh = $('fleet-fresh'), ok = fleetLive();
  fresh.textContent = ok ? F.ships.length + ' ships' : (F.age < 0 ? 'no data' : 'stale');
  fresh.className = 'fresh' + (ok ? '' : ' bad');
  renderAlerts();
}

function renderShip(panel) {
  setWide('metrics');
  const d = shipCard;
  const barTop = el('div', 'reader-bar');
  const backBtn = el('button', 'subtab', '<- System');
  backBtn.type = 'button';
  backBtn.addEventListener('click', () => { selShip = null; shipCard = null; shipMark = ''; renderRoster(); draw(); render(); });
  barTop.append(backBtn);
  if (d && d.system && sys.has(d.system)) {
    const centerBtn = el('button', 'rf', 'Center on Map');
    centerBtn.type = 'button';
    centerBtn.addEventListener('click', () => { const s = sys.get(d.system); flyTo(s.x, s.y, Math.max(view.k, 0.35)); });
    barTop.append(centerBtn);
  }
  panel.append(barTop);

  if (!d) { panel.append(el('p', 'empty', 'Loading ship telemetry...')); return; }
  if (d.error) { panel.append(el('p', 'empty', 'No telemetry file for this ship.')); return; }

  const [cls, what] = shipState(d);
  const hero = el('div', 'sel-hero');
  const heroLeft = el('div');
  heroLeft.append(el('h2', null, d.name));
  const sub = el('div', 'sel-sub');
  sub.append(divTag(d.division));
  if (d.admiral) sub.append(el('span', 'pill', 'Adm. ' + d.admiral));
  sub.append(el('span', 'pill ' + (cls === 'bad' ? 'bad' : cls === 'idle' || cls === 'wait' ? 'warn' : cls === 'work' ? 'good' : 'info'), what));
  heroLeft.append(sub);
  hero.append(heroLeft);
  panel.append(hero);

  const skills = Object.entries(d.skills || {}).sort((x, y) => (y[1].level - x[1].level) || (y[1].xp - x[1].xp));
  const pLv = ((d.skills || {}).piloting || {}).level || d.piloting || 0;
  const topSk = skills.find(([k]) => k !== 'piloting') || skills[0];
  const readyT2 = !isUpgradedHull(d.class) && pLv >= 10;

  const kgrid = el('div', 'kpis');
  const skpi = (k, v, sTxt, c) => { const b = el('div', 'kpi' + (c ? ' ' + c : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sTxt) b.append(el('div', 's', sTxt)); kgrid.append(b); };
  skpi('Hull & Empire', d.class || 'Threshold', (d.empire || 'voidborn') + (readyT2 ? ' | READY FOR T2 HULL' : ''), isUpgradedHull(d.class) ? 'main pos' : readyT2 ? 'warn' : '');
  skpi('Pilot Wallet', fmt(d.credits) + ' cr', d.docked ? 'Docked: ' + d.docked : (d.system_name || d.system || 'in space'), d.credits >= 30000 ? 'pos' : d.credits < 10000 ? 'warn' : '');
  skpi('Piloting & Specialty', 'Piloting ' + pLv, topSk ? topSk[0].replace(/_/g, ' ') + ' Lv ' + topSk[1].level : 'no specialty yet', pLv >= 10 ? 'pos' : '');
  const loopTxt = d.loop && d.loop.type ? d.loop.type : what;
  const failN = d.loop_failures || 0;
  skpi('Active Loop', loopTxt, failN ? failN + ' failure(s): ' + (d.loop_last_failure || '') : (d.loop && d.loop.last_step ? 'step: ' + d.loop.last_step : 'nominal'), failN ? 'neg' : '');
  panel.append(kgrid);

  const vcard = el('div', 'icard vitals-card');
  const g = el('div', 'gauges');
  for (const [k, kind, a, b, low] of [['Hull', 'hull', d.hull, d.max_hull, 0.5], ['Shield', 'shield', d.shield, d.max_shield, 0],
    ['Fuel', 'fuel', d.fuel, d.max_fuel, 0.25], ['Cargo', 'cargo', d.cargo_used, d.cargo_capacity, 0]]) {
    g.append(el('span', 'k', k), bar(kind, a, b, low), el('span', 'v', fmt(a) + ' / ' + fmt(b)));
  }
  vcard.append(g);
  panel.append(vcard);

  const subBar = el('div', 'subtabs');
  for (const [id, lbl] of [['Loadout', 'Loadout & Cargo (' + (d.modules || []).length + ')'], ['Skills', 'Skills (' + skills.length + ')'], ['Missions', 'Missions & Record']]) {
    const sb = el('button', 'subtab' + (shipSub === id ? ' on' : ''), lbl);
    sb.type = 'button';
    sb.addEventListener('click', () => { shipSub = id; render(); });
    subBar.append(sb);
  }
  panel.append(subBar);

  if (shipSub === 'Skills') {
    const scard = el('div', 'icard');
    if (!skills.length) scard.append(el('p', 'empty', 'No skill trained yet.'));
    else {
      const lv = el('div', 'levels');
      for (const [k, v] of skills) {
        const row = el('div', 'lv'), b = el('div', 'bar xp'), i = el('i');
        i.style.width = pct(v.xp, v.next) + '%'; b.append(i);
        row.title = k.replace(/_/g, ' ') + ': level ' + v.level + ', ' + fmt(v.xp) + ' / ' + fmt(v.next) + ' XP';
        row.append(el('span', 'n', k.replace(/_/g, ' ')), el('b', null, String(v.level)), b);
        lv.append(row);
      }
      scard.append(lv);
    }
    panel.append(scard);
    return;
  }

  if (shipSub === 'Missions') {
    panel.append(el('h3', null, 'Accepted Missions (' + (d.mission_list || []).length + ' / 5)'));
    if (!(d.mission_list || []).length) panel.append(el('p', 'empty', 'No active mission contracts on this ship.'));
    for (const m of d.mission_list || []) {
      const box = el('div', 'icard'), top = el('div', 'ichead'), b = el('div', 'bar'), i = el('i');
      top.append(el('b', null, m.title), el('span', 'pill good', fmt(m.credits) + ' cr'));
      i.style.width = Math.round(m.percent) + '%'; b.append(i);
      box.append(top, b);
      m.objectives.forEach((o) => box.append(el('div', 'ibsub', (o.done ? '[done] ' : '[' + o.current + '/' + o.required + '] ') + o.text)));
      panel.append(box);
    }
    panel.append(el('h3', null, 'Lifetime Service Record'));
    const rcard = el('div', 'icard');
    rcard.append(facts(Object.entries(d.stats || {}).map(([k, v]) => [k.replace(/_/g, ' '), fmt(v)])));
    panel.append(rcard);
    return;
  }

  // Default: Loadout, Position & Cargo
  const loc = d.system && sys.has(d.system) ? sysLink(d.system) : (d.system_name || 'unknown');
  const pcard = el('div', 'icard');
  pcard.append(facts([
    ['System', loc],
    ['Location / Vector', d.jumping ? 'jumping lanes' : d.in_transit ? 'in transit -> ' + (d.dest_poi || '?') : (d.poi_name || '-')],
    ['Home Base', d.home_base || '-'],
    ['Security / Updated', (d.security || '-') + ' | ' + stampCet(d.state_at)],
  ]));
  panel.append(pcard);

  panel.append(el('h3', null, 'Fitted Modules (' + (d.modules || []).length + ')'));
  const mcard = el('div', 'icard');
  if ((d.modules || []).length) mcard.append(fitTable(table(['Module', 'Category', 'Slot'], d.modules.map((m) => [m.name, m.kind, el('span', 'pill info', m.slot)]))));
  else mcard.append(el('p', 'empty', 'No modules fitted.'));
  panel.append(mcard);

  panel.append(el('h3', null, 'Cargo Hold (' + fmt(d.cargo_used) + ' / ' + fmt(d.cargo_capacity) + ')'));
  const ccard = el('div', 'icard');
  if ((d.cargo || []).length) ccard.append(fitTable(table(['Item', 'Units'], d.cargo.map((c) => [c.item ? itemLink(c.item, c.name || c.item) : (c.name || '?'), fmt(c.quantity)]), [1])));
  else ccard.append(el('p', 'empty', 'Cargo hold empty.'));
  panel.append(ccard);
}

async function selectShip(name, center) {
  selShip = name; shipCard = null; shipMark = ''; pilotCard = null; docView = null; tab = 'Selection';
  const row = F.ships.find((r) => r.name === name);
  if (row && row.division && collapsed.has(row.division)) {
    collapsed.delete(row.division);
    saveFolds();
  }
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

let INVCACHE = { at: 0, value: null };
async function inventoryOf() {
  if (Date.now() - INVCACHE.at < 60000 && INVCACHE.value) return INVCACHE.value;
  try { INVCACHE = { at: Date.now(), value: await get('/api/inventory') }; } catch (e) { return INVCACHE.value; }
  return INVCACHE.value;
}
async function renderSelection(panel, live) {
  if (selShip) { renderShip(panel); return; }
  if (pilotCard) { renderPilot(panel, pilotCard); return; }
  setWide('metrics');
  if (!selected) { panel.append(el('p', 'empty', 'Select a star system on the galaxy map or click any ship in the Fleet Outliner.')); return; }
  const s = sys.get(selected);
  const intel = S.intel.systems[s.id];
  const own = holdBy.get(s.id) || [], site = sitesBy.get(s.id), ours = shipsBy.get(s.id) || [], st = stationsBy.get(s.id) || [];

  const hero = el('div', 'sel-hero');
  const heroLeft = el('div');
  heroLeft.append(el('h2', null, s.name));
  const sub = el('div', 'sel-sub');
  sub.append(el('span', 'pill ' + (s.empire ? 'info' : 'warn'), s.empire || 'lawless'));
  if (s.home) sub.append(el('span', 'pill good', 'empire capital'));
  if (s.stronghold) sub.append(el('span', 'pill bad', 'pirate stronghold'));
  if (intel) {
    sub.append(el('span', 'pill ' + (intel.standing === 'ally' || intel.standing === 'home' ? 'good' : intel.standing === 'hostile' ? 'bad' : ''), intel.standing));
    if (intel.threat && intel.threat !== 'none') sub.append(el('span', 'pill ' + (intel.threat === 'high' ? 'bad' : 'warn'), 'threat: ' + intel.threat));
  }
  heroLeft.append(sub);
  const centerBtn = el('button', 'maploc', 'Center');
  centerBtn.type = 'button';
  centerBtn.addEventListener('click', () => flyTo(s.x, s.y, Math.max(view.k, 0.32)));
  hero.append(heroLeft, centerBtn);
  panel.append(hero);

  const named = new Set(st.map((t) => t.name)), bases = new Set(own.map((b) => b.base).filter(Boolean));
  const inv = await inventoryOf();
  if (!live()) return;
  const goods = inv ? inv.stations.filter((x) => named.has(x.name) || bases.has(x.base)) : [];
  const worth = goods.reduce((a, x) => a + (x.worth || 0), 0), units = goods.reduce((a, x) => a + (x.units || 0), 0);
  const wallets = ours.reduce((a, r) => a + (r.credits || 0), 0);
  const workingHere = ours.filter((r) => ['work', 'move', 'wait'].includes(shipState(r)[0])).length;
  const siteRich = ((OPS.data && OPS.data.empire && OPS.data.empire.sites) || []).find((x) => x.system === s.id);

  const kgrid = el('div', 'kpis');
  const ykpi = (k, v, sTxt, c) => { const b = el('div', 'kpi' + (c ? ' ' + c : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sTxt) b.append(el('div', 's', sTxt)); kgrid.append(b); };
  ykpi('Our Fleet Here', fmt(ours.length) + ' ships', ours.length ? workingHere + ' active | ' + fmtCompact(wallets) + ' cr wallets' : 'no CLTV ships in system', ours.length ? 'main pos' : '');
  ykpi('Vault Stock Here', units ? fmtCompact(worth) + ' cr' : '0 cr', units ? fmt(units) + ' units stored' : 'no stored inventory', worth > 0 ? 'pos' : '');
  const fpVal = own.length ? own.length + (own.length === 1 ? ' asset' : ' assets') : (siteRich && siteRich.status !== 'built' ? siteRich.status.toUpperCase() : '0 assets');
  const fpSub = own.length ? 'CLTV sovereign / leased' : (siteRich && siteRich.need_pct != null ? siteRich.need_pct + '% kit ready' : st.length + ' public station(s)');
  ykpi('Our Footprint', fpVal, fpSub, own.length ? 'pos' : siteRich ? 'warn' : '');
  ykpi('Distance & Traffic', (s.jumps < 0 ? 'isolated' : s.jumps + 'j from Home'), (L.hour[s.id] || 0) + ' pilots (1h) | ' + (L.day[s.id] || 0) + ' (24h)', '');
  panel.append(kgrid);

  const subBar = el('div', 'subtabs');
  for (const [id, lbl] of [['Overview', 'Colony & Stations'], ['Ships', 'Our Ships (' + ours.length + ')'], ['Intel', 'Intel & Traffic']]) {
    const sb = el('button', 'subtab' + (selSub === id ? ' on' : ''), lbl);
    sb.type = 'button';
    sb.addEventListener('click', () => { selSub = id; render(); });
    subBar.append(sb);
  }
  panel.append(subBar);

  if (selSub === 'Ships') {
    if (!ours.length) {
      panel.append(el('p', 'empty', 'No Collective ships are currently in ' + s.name + '.'));
      return;
    }
    const byDiv = {};
    ours.forEach((r) => { byDiv[r.division] = (byDiv[r.division] || 0) + 1; });
    const dchips = el('div', 'chips');
    for (const [dv, cnt] of Object.entries(byDiv)) dchips.append(el('span', 'pill info', dv + ': ' + cnt));
    if (ours.length > 25) dchips.append(linkButton('Open floating map card (' + ours.length + ')', () => openPop(s.id, 'All')));
    panel.append(dchips);

    const scard = el('div', 'icard');
    scard.append(fitTable(table(['Ship', 'Div', 'Task', 'Cargo', 'Lv'],
      ours.slice(0, 40).map((r) => [
        shipLink(r.name),
        r.division.slice(0, 3),
        shipState(r)[1],
        r.cargo_used + '/' + r.cargo_capacity,
        r.piloting || '-',
      ]), [3, 4])));
    panel.append(scard);
    return;
  }

  if (selSub === 'Intel') {
    const box = el('div');
    panel.append(box);
    box.append(el('p', 'sub', 'Loading live traffic & scout dossier...'));
    try {
      const d = await get('/api/system?id=' + encodeURIComponent(s.id));
      if (!live()) return;
      box.replaceChildren();
      box.append(el('h3', null, 'Foreign Factions Active (Last 1h)'));
      const gcard = el('div', 'icard');
      if (d.groups.length) {
        gcard.append(fitTable(table(['Tag', 'Faction', 'Pilots', 'Standing'],
          d.groups.map((g) => [el('span', 'rtag', '[' + g.tag + ']'), g.name || '-', g.count, el('span', 'pill ' + (g.standing === 'hostile' ? 'bad' : g.standing === 'ally' ? 'good' : ''), g.standing)]), [2])));
      } else gcard.append(el('p', 'empty', 'Zero foreign multi-pilot groups jumped here in the last hour (' + fmt(d.pilot_count) + ' solo jumps in 24h).'));
      box.append(gcard);

      if (d.battles.length) {
        box.append(el('h3', null, 'Recent Combat Engagements'));
        const bcard = el('div', 'icard');
        bcard.append(fitTable(table(['Type', 'Participants', 'Losses'], d.battles.map((b) => [b.category, b.pilots.join(', '), b.lost.join(', ') || 'none']))));
        box.append(bcard);
      }
      if (d.intel) {
        box.append(el('h3', null, 'Scouted System Dossier'));
        const icard = el('div', 'icard doc-reader-card');
        icard.append(markdown(d.intel_text, d.intel.file, false));
        box.append(icard);
      } else {
        box.append(el('p', 'empty', 'No scout dossier filed yet for ' + s.name + '.'));
      }
    } catch (e) { if (live()) box.replaceChildren(el('p', 'empty', 'Detail unavailable: ' + e.message)); }
    return;
  }

  // Default Sub-Tab: Colony, Our Buildings, Stations & Jump Lanes
  if (own.length) {
    panel.append(el('h3', null, 'Our Sovereign Bases & Facilities (' + own.length + ')'));
    const richB = ((OPS.data && OPS.data.empire && OPS.data.empire.buildings) || []).filter((x) => x.system === s.id);
    const list = richB.length ? richB : own;
    const bwrap = el('div', 'icards');
    for (const b of list) {
      const ok = stands(b), card = el('div', 'icard' + (ok ? ' ownbase' : ' sitecard'));
      const head = el('div', 'ichead');
      head.append(glyphSvg(b.kind || 'office', ok ? BUILT : RAISING, 15), el('b', null, b.name));
      head.append(el('span', 'pill ' + (ok ? 'good' : 'warn'), (b.status || 'active').replace(/_/g, ' ')));
      card.append(head);
      const meta = [];
      if (b.at && b.at !== 'our own base') meta.push('at ' + b.at);
      if (b.purpose) meta.push(b.purpose);
      if (b.rent) meta.push('rent ' + fmt(b.rent) + ' cr');
      else if (b.kind === 'outpost' || b.kind === 'station' || b.part) meta.push('sovereign (0 cr rent)');
      if (meta.length) card.append(el('div', 'icsub', meta.join(' | ')));
      if (b.fuel !== null && b.fuel !== undefined) {
        card.append(el('div', 'ibsub', 'Fuel bunker reserve: ' + fmt(b.fuel) + ' / 50,000'), pbar(b.fuel, 50000, b.fuel >= 5000 ? 'good' : 'warn'));
      }
      bwrap.append(card);
    }
    panel.append(bwrap);
  }

  if (siteRich && siteRich.status !== 'built') {
    const sc = el('div', 'icard sitecard');
    const sh = el('div', 'ichead');
    sh.append(glyphSvg('flag', siteRich.status === 'chosen' ? '#e8c35a' : OURS, 14, siteRich.status !== 'chosen'),
      el('b', null, siteRich.status === 'chosen' ? 'Chosen Expansion Site' : 'Candidate Expansion Site'),
      el('span', 'pill ' + (siteRich.status === 'chosen' ? 'warn' : 'info'), siteRich.status.toUpperCase()));
    sc.append(sh);
    if (siteRich.need_pct !== null && siteRich.need_pct !== undefined) {
      sc.append(el('div', 'ibsub', 'Kit readiness (' + siteRich.need_id + '): ' + siteRich.need_pct + '%'), pbar(siteRich.need_pct, 100, siteRich.need_pct >= 99 ? 'good' : 'warn'));
    }
    if (siteRich.note) sc.append(el('div', 'ibsub', siteRich.note));
    panel.append(sc);
  }

  const theirs = (t) => (t.tag && t.tag === S.our_tag ? 'CLTV (Ours)' : t.faction ? t.faction + (t.tag ? ' [' + t.tag + ']' : '') : t.empire ? t.empire : 'independent');
  const heldAt = (name) => { const x = inv && inv.stations.find((y) => y.name === name); return x ? fmtCompact(x.worth) + ' cr' : '-'; };
  panel.append(el('h3', null, 'Stations & Port Services (' + st.length + ')'));
  const stCard = el('div', 'icard');
  if (st.length) {
    stCard.append(fitTable(table(['Station', 'Owner', 'Our Stock', 'Services'],
      st.map((t) => [
        t.name,
        t.tag === S.our_tag ? el('span', 'pill good', 'CLTV') : theirs(t),
        heldAt(t.name),
        el('span', 'rmeta-sub', (t.services || []).join(', ') || (t.type || 'port')),
      ]), [2])));
  } else stCard.append(el('p', 'empty', 'Zero public stations in this system.'));
  panel.append(stCard);

  panel.append(el('h3', null, 'Hyperlanes (' + s.lanes.length + ')' + (route.length > 1 ? ' & Route from Home (' + (route.length - 1) + 'j)' : '')));
  const navCard = el('div', 'icard');
  const lanes = el('div', 'chips');
  s.lanes.forEach((id) => lanes.append(sysLink(id)));
  navCard.append(el('div', 'icsub', 'Adjacent lanes:'), lanes);
  if (route.length > 1) {
    const way = el('div', 'chips');
    route.forEach((id) => way.append(sysLink(id)));
    navCard.append(el('div', 'icsub', 'Shortest path from Home:'), way);
  }
  panel.append(navCard);
}

function renderPilot(panel, d) {
  setWide('metrics');
  const barTop = el('div', 'reader-bar');
  const backBtn = el('button', 'subtab', '<- System');
  backBtn.type = 'button';
  backBtn.addEventListener('click', () => { pilotCard = null; render(); });
  barTop.append(backBtn);
  panel.append(barTop);

  panel.append(el('h2', null, d.name));
  if (d.intel) {
    const chips = el('div', 'chips');
    chips.append(el('span', 'pill ' + (d.intel.standing === 'hostile' ? 'bad' : 'info'), d.intel.standing),
      el('span', 'pill ' + (d.intel.threat === 'high' ? 'bad' : 'warn'), 'threat ' + d.intel.threat),
      linkButton('Open Dossier', () => openDoc(d.intel.file)));
    panel.append(chips);
  }
  const rows = [];
  if (d.seen) rows.push(['Last jump', sysLink(d.seen.system)], ['Seen', ago(d.seen.age) + ' ago'], ['Faction', d.seen.tag || 'none'], ['Empire', d.seen.empire]);
  else rows.push(['Last jump', 'not seen in last 24h']);
  if (d.profile) {
    rows.push(['Registered', d.profile.created], ['Faction (feed)', d.profile.faction || 'none'], ['Empire (feed)', d.profile.empire]);
    for (const [k, v] of Object.entries(d.profile.stats)) rows.push([k.replace(/_/g, ' '), fmt(v)]);
  }
  const card = el('div', 'icard');
  card.append(facts(rows));
  panel.append(card);
}

let invMode = 'total', invItem = null, invCat = 'all', invSort = 'worth', invQuery = '';
const INV_KINDS = { raw: 'raw', refined: 'refined', component: 'part', module: 'module', consumable: 'consumable', ammo: 'ammo', drone: 'drone', other: 'other', contraband: 'contraband', unknown: 'other' };
const INV_PILL = { raw: '', refined: 'info', component: 'good', module: 'warn', ammo: 'bad', consumable: 'info' };

function itemLink(id, name) { return linkButton(name, () => { tab = 'Inventory'; invItem = id; render(); }, 'doclink'); }
function kindPill(k) {
  const lbl = INV_KINDS[k] || k || 'item';
  return el('span', 'pill ' + (INV_PILL[k] || ''), lbl);
}
function recipeRows(rows) {
  const line = (pairs) => pairs.map((p) => fmt(p[1]) + ' ' + p[0]).join(', ');
  return rows.map((r) => [
    r.doc ? linkButton(r.name || r.id, () => openDoc(r.doc), 'doclink') : (r.name || r.id),
    line(r.inputs),
    line(r.outputs),
    el('span', 'pill ' + (r.by_hand ? 'good' : 'info'), r.by_hand ? 'ship craft' : 'facility'),
  ]);
}

async function renderItem(panel, live) {
  const d = await get('/api/item?id=' + encodeURIComponent(invItem));
  if (!live()) return;
  const topBar = el('div', 'reader-bar');
  const backBtn = el('button', 'subtab on', '<- Back to Inventory');
  backBtn.type = 'button';
  backBtn.addEventListener('click', () => { invItem = null; render(); });
  topBar.append(backBtn);
  panel.append(topBar);
  if (d.error) { panel.append(el('p', 'empty', 'The catalog does not hold this item.')); return; }

  const titleRow = el('div', 'ichead');
  titleRow.append(el('h2', 'inline-h2', d.name), kindPill(d.kind));
  panel.append(titleRow);
  if (d.description) panel.append(el('p', 'sub', d.description));

  const totalWorth = (d.units || 0) * (d.value || 0);
  const kgrid = el('div', 'kpis');
  const ikpi = (k, v, sub, cls) => { const b = el('div', 'kpi' + (cls ? ' ' + cls : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sub) b.append(el('div', 's', sub)); kgrid.append(b); };
  ikpi('Fleet stock', fmt(d.units) + ' units', d.at.length + ' location' + (d.at.length === 1 ? '' : 's'), d.units > 0 ? 'main pos' : '');
  ikpi('Catalog worth', fmtCompact(totalWorth) + ' cr', fmt(d.value) + ' cr base value / unit', totalWorth > 0 ? 'pos' : '');
  ikpi('Cargo volume', (d.size || 1) + ' vol / unit', fmt((d.units || 0) * (d.size || 1)) + ' total hold vol', '');
  ikpi('Industrial uses', fmt((d.used_total || 0) + (d.built_total || 0)), fmt(d.used_total || 0) + ' recipes | ' + fmt(d.built_total || 0) + ' builds', '');
  panel.append(kgrid);

  if (d.at.length) {
    panel.append(el('h3', null, 'Where our stock sits (' + d.at.length + ' places)'));
    const maxU = Math.max(1, ...d.at.map((a) => a[1]));
    const card = el('div', 'icard');
    card.append(fitTable(table(['Station / Hold', 'Share', 'Units', 'Base Worth'],
      d.at.map((a) => {
        const pctShare = Math.round((100 * a[1]) / Math.max(1, d.units));
        const barCell = el('div', 'progcell');
        barCell.append(el('span', 'rmeta-sub', pctShare + '%'), pbar(a[1], maxU, pctShare >= 40 ? 'good' : ''));
        return [a[0], barCell, fmt(a[1]), fmt(a[1] * (d.value || 0)) + ' cr'];
      }), [2, 3])));
    panel.append(card);
  }

  panel.append(el('h3', null, 'Crafted by (' + d.made_by.length + ')'));
  if (d.made_by.length) {
    const c1 = el('div', 'icard');
    c1.append(fitTable(table(['Recipe', 'Inputs', 'Outputs', 'Method'], recipeRows(d.made_by))));
    panel.append(c1);
  } else {
    panel.append(el('p', 'empty', 'Primary resource: mined, harvested, hunted or bought at stations.'));
  }

  panel.append(el('h3', null, 'Feeds into recipes' + (d.used_total > d.used_in.length ? ' (' + d.used_in.length + ' of ' + d.used_total + ')' : ' (' + d.used_in.length + ')')));
  if (d.used_in.length) {
    const c2 = el('div', 'icard');
    c2.append(fitTable(table(['Recipe', 'Inputs', 'Outputs', 'Method'], recipeRows(d.used_in))));
    panel.append(c2);
  } else {
    panel.append(el('p', 'empty', 'Not consumed as a crafting input.'));
  }

  panel.append(el('h3', null, 'Builds facilities & ship hulls' + (d.built_total > d.built.length ? ' (' + d.built.length + ' of ' + d.built_total + ')' : ' (' + d.built.length + ')')));
  if (d.built.length) {
    const c3 = el('div', 'icard');
    c3.append(fitTable(table(['Target', 'Type', 'Qty Needed', 'Build Fee'],
      d.built.map((b) => [b.name, el('span', 'pill ' + (b.kind === 'hull' ? 'info' : 'good'), b.kind), fmt(b.units), fmtCompact(b.cost) + ' cr']), [2, 3])));
    panel.append(c3);
  } else {
    panel.append(el('p', 'empty', 'Not directly required in a hull or station facility blueprint.'));
  }
}

async function renderInventory(panel, live) {
  if (invItem) return renderItem(panel, live);
  const [d, ops] = await Promise.all([inventoryOf(), opsOf()]);
  if (!live()) return;
  if (!d || !d.written) {
    panel.append(el('h2', null, 'Inventory & Supply Ledger'));
    panel.append(el('p', 'empty', 'Waiting on first ledger storage pass...'));
    return;
  }

  const places = d.stations.filter((s) => s.base !== 'hold'), hold = d.stations.find((s) => s.base === 'hold');
  const supList = (ops && ops.supply) || [];
  const supOk = supList.filter((x) => x.state === 'OK').length;

  panel.append(el('h2', null, 'Inventory, Vaults & Supply Chains'));
  panel.append(el('p', 'sub', 'Unified material balance across sovereign bases, station lockboxes and active ship holds. Updated ' + stampCet(d.written) + ' across ' + fmt(d.pilots) + ' ships.'));

  const grid = el('div', 'kpis');
  const ikpi = (k, v, sub, cls) => { const b = el('div', 'kpi' + (cls ? ' ' + cls : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sub) b.append(el('div', 's', sub)); grid.append(b); };
  ikpi('Total catalog worth', fmtCompact(d.total.worth) + ' cr', fmt(d.total.items) + ' item types | ' + fmt(d.total.units) + ' total units', 'main pos');
  ikpi('Station vaults', fmt(places.length) + ' stations', places.length ? 'top hub: ' + places[0].name : 'none', 'pos');
  ikpi('In ship cargo holds', hold ? fmt(hold.units) + ' units' : '0 units', hold ? fmt(hold.items) + ' item types in flight' : 'holds clear', '');
  ikpi('Supply buffers', supList.length ? supOk + ' / ' + supList.length + ' OK' : '--',
    supList.length && supOk < supList.length ? (supList.length - supOk) + ' buffer(s) below keep target' : 'all tracked buffers stocked',
    supList.length && supOk < supList.length ? 'warn' : 'pos');
  panel.append(grid);

  const subBar = el('div', 'subtabs');
  const modes = [
    ['total', 'All Stock (' + fmt(d.total.items) + ')'],
    ['stations', 'By Station & Base (' + fmt(d.stations.length) + ')'],
    ['supply', 'Supply & Build Stock'],
    ['catalog', 'Recipes & Blueprints (' + fmt(d.recipes || 0) + ')'],
  ];
  for (const [key, label] of modes) {
    const b = el('button', 'subtab' + (invMode === key ? ' on' : ''), label);
    b.type = 'button';
    b.addEventListener('click', () => { invMode = key; render(); });
    subBar.append(b);
  }
  panel.append(subBar);

  if (invMode === 'catalog') {
    const cards = el('div', 'icards');
    const cdefs = [
      [d.docs && d.docs.master, 'Master Recipe & Craftbook Index', 'All ' + fmt(d.recipes || 0) + ' crafting & refining recipes organized by industrial discipline.', 'CRAFTBOOK'],
      [d.docs && d.docs.facilities, 'Station & Sovereign Base Facilities', 'Build costs, input materials, upkeep rent and prerequisite chains for every facility.', 'FACILITIES'],
      [d.docs && d.docs.modules, 'Ship Weapons, Harvesters & Utility Modules', 'Slot stats, CPU/power draw, skill requirements and crafting bills of materials.', 'MODULES'],
      ['game/routes/master-index.md', 'Active Fleet Route & Plan Directory', 'Every mining, trade, hunt, mission and logistics circuit across all divisions.', 'ROUTES'],
    ];
    for (const [docPath, title, desc, badge] of cdefs) {
      if (!docPath) continue;
      const c = el('div', 'icard doc-card');
      const h = el('div', 'ichead');
      const btn = el('button', 'sysjump', title);
      btn.type = 'button';
      btn.addEventListener('click', () => openDoc(docPath));
      h.append(btn, el('span', 'pill info', badge));
      c.append(h, el('div', 'ibsub', desc));
      cards.append(c);
    }
    panel.append(cards);
    return;
  }

  if (invMode === 'supply') {
    const needs = (ops && ops.needs) || [];
    const reqs = (ops && ops.requests) || [];
    panel.append(el('h3', null, 'Standing supply buffers (' + supList.length + ')'));
    if (!supList.length) {
      panel.append(el('p', 'empty', 'No supply chains configured.'));
    } else {
      const scard = el('div', 'icard');
      scard.append(fitTable(table(['Chain', 'Item', 'Hub / Base', 'Buffer Progress', 'State'],
        supList.map((s) => {
          const haveVal = s.have !== undefined ? s.have : (s.stock || 0);
          const pctFill = s.keep > 0 ? Math.min(100, Math.round((100 * haveVal) / s.keep)) : 0;
          const pCell = el('div', 'progcell');
          pCell.append(el('span', 'mono', fmt(haveVal) + ' / ' + fmt(s.keep)), pbar(pctFill, 100, s.state === 'OK' ? 'good' : 'warn'));
          const isFull = s.state === 'OK' && pctFill >= 100;
          return [
            s.chain,
            s.item ? itemLink(s.item, s.item.replace(/_/g, ' ')) : '--',
            s.place || '--',
            pCell,
            el('span', 'pill ' + (s.state === 'OK' ? 'good' : s.state === 'SHORT' ? 'warn' : 'bad'), isFull ? 'STOCKED' : s.state),
          ];
        }))));
      panel.append(scard);
    }
    panel.append(el('h3', null, 'Open priority build & upgrade needs (' + needs.length + ')'));
    if (!needs.length) {
      panel.append(el('p', 'empty', 'All priority build bills of materials are complete!'));
    } else {
      const ncards = el('div', 'icards');
      for (const n of needs) {
        const nc = el('div', 'icard' + (n.stocked || n.pct >= 99 ? ' ownbase' : ' sitecard'));
        const nh = el('div', 'ichead');
        const pTag = String(n.priority || '').startsWith('P') ? n.priority : 'P' + n.priority;
        nh.append(el('b', null, '[' + pTag + '] ' + n.id), el('span', 'rmeta-sub', n.owner || n.division || ''),
          el('span', 'pill ' + (n.stocked || n.pct >= 99 ? 'good' : 'warn'), n.stocked ? 'STOCKED' : n.pct.toFixed(1) + '%'));
        nc.append(nh, pbar(n.pct, 100, n.stocked || n.pct >= 99 ? 'good' : 'warn'));
        if (n.project) nc.append(el('div', 'ibsub', n.project));
        if (!n.stocked && (n.short || n.fee)) nc.append(el('div', 'rmeta-sub', 'Remaining: ' + [n.short, n.fee ? fmt(n.fee) + ' cr fee' : ''].filter(Boolean).join(' | ')));
        ncards.append(nc);
      }
      panel.append(ncards);
    }
    if (reqs.length) {
      panel.append(el('h3', null, 'Active division requests (' + reqs.length + ' open/accepted)'));
      const rcard = el('div', 'icard');
      rcard.append(fitTable(table(['State', 'Entry', 'From -> To', 'Updated', 'Need / Status'],
        reqs.map((r) => [
          el('span', 'pill ' + (r.state === 'OPEN' ? 'warn' : 'info'), r.state),
          linkButton(r.ent, () => openDoc('communications/requests.log'), 'doclink'),
          r.by + ' -> ' + r.to,
          stampCet(r.when),
          r.need + (r.answer ? ' [' + r.answer + ']' : ''),
        ]))));
      panel.append(rcard);
    }
    return;
  }

  // Filter & Search toolbar for 'total' and 'stations'
  const filterWrap = el('div', 'inv-toolbar');
  const sRow = el('div', 'rsearch');
  const sInp = el('input');
  sInp.type = 'search';
  sInp.placeholder = invMode === 'stations' ? 'Filter stations or items (e.g. silicon, node beta, polymer)...' : 'Search items (e.g. silicon, polymer, laser, fuel)...';
  sInp.value = invQuery;
  const clearBtn = el('button', 'rf', 'Clear');
  clearBtn.type = 'button';
  sRow.append(sInp, clearBtn);
  filterWrap.append(sRow);

  if (invMode === 'total') {
    const cBar = el('div', 'sortbar');
    const cats = [
      ['all', 'All'],
      ['raw', 'Raw Ores'],
      ['refined', 'Refined'],
      ['component', 'Components'],
      ['module', 'Modules'],
      ['ammo', 'Ammo & Fuel'],
    ];
    for (const [cid, clbl] of cats) {
      const b = el('button', 'rf' + (invCat === cid ? ' on' : ''), clbl);
      b.type = 'button';
      b.addEventListener('click', () => { invCat = cid; render(); });
      cBar.append(b);
    }
    cBar.append(el('span', 'sortlbl', ' | Sort:'));
    for (const [sid, slbl] of [['worth', 'Worth'], ['units', 'Units'], ['held', 'In Holds']]) {
      const b = el('button', 'rf' + (invSort === sid ? ' on' : ''), slbl);
      b.type = 'button';
      b.addEventListener('click', () => { invSort = sid; render(); });
      cBar.append(b);
    }
    filterWrap.append(cBar);
  }
  panel.append(filterWrap);

  const bodyBox = el('div');
  panel.append(bodyBox);

  const ownBaseIds = new Set((((ops && ops.empire && ops.empire.buildings) || []).map((b) => b.base).filter(Boolean)));
  const ownSysByBase = new Map();
  for (const b of ((ops && ops.empire && ops.empire.buildings) || [])) {
    if (b.base && b.system) ownSysByBase.set(b.base, b.system);
    if (b.at && b.system) ownSysByBase.set(b.at.toLowerCase(), b.system);
  }

  const drawInvBody = () => {
    bodyBox.replaceChildren();
    const q = invQuery.trim().toLowerCase();
    if (invMode === 'stations') {
      const cards = el('div', 'icards');
      const ordered = [...d.stations].sort((a, b) => {
        const aRank = a.base === 'hold' ? 2 : ownBaseIds.has(a.base) ? 0 : 1;
        const bRank = b.base === 'hold' ? 2 : ownBaseIds.has(b.base) ? 0 : 1;
        return aRank - bRank || b.worth - a.worth;
      });
      let shown = 0;
      for (const s of ordered) {
        const stMatch = !q || s.name.toLowerCase().includes(q) || (s.base || '').toLowerCase().includes(q);
        const rows = stMatch ? s.rows : s.rows.filter((r) => r.name.toLowerCase().includes(q) || r.id.toLowerCase().includes(q));
        if (!rows.length) continue;
        shown++;
        const isOurHub = ownBaseIds.has(s.base) || /cltv|outpost/i.test(s.name);
        const isHold = s.base === 'hold';
        const card = el('div', 'icard' + (isOurHub ? ' ownbase' : ''));
        const ch = el('div', 'ichead');
        const sysHit = ownSysByBase.get(s.base) || ownSysByBase.get((s.name || '').toLowerCase())
          || [...stationsBy.entries()].find(([_sid, list]) => list.some((t) => t.name === s.name))?.[0];
        if (sysHit && sys.has(sysHit)) {
          const jb = el('button', 'sysjump', s.name);
          jb.type = 'button';
          jb.addEventListener('click', () => select(sysHit, true));
          ch.append(jb);
        } else {
          ch.append(el('b', null, s.name));
        }
        ch.append(el('span', 'pill ' + (isOurHub ? 'good' : isHold ? 'info' : ''), isOurHub ? 'OUR HUB' : isHold ? 'IN FLIGHT' : 'STATION VAULT'));
        card.append(ch);
        card.append(el('div', 'icsub', fmt(rows.length) + ' item types | ' + fmt(s.units) + ' units | ~' + fmtCompact(s.worth) + ' cr base worth'));
        card.append(fitTable(table(['Item', 'Category', 'Units', 'Base Worth'],
          rows.map((r) => [itemLink(r.id, r.name), kindPill(r.kind), fmt(r.units), fmtCompact(r.worth) + ' cr']), [2, 3])));
        cards.append(card);
      }
      if (!shown) bodyBox.append(el('p', 'empty', 'No station or item matches "' + invQuery + '".'));
      else bodyBox.append(cards);
      return;
    }

    // All Stock mode: flatten and filter cleanly
    const flat = [];
    for (const g of d.groups) {
      for (const r of g.rows) flat.push(r);
    }
    const filtered = flat.filter((r) => {
      if (invCat === 'ammo') {
        if (r.kind !== 'ammo' && r.kind !== 'consumable' && !/fuel|cell|ammo/i.test(r.id)) return false;
      } else if (invCat !== 'all' && r.kind !== invCat) {
        return false;
      }
      if (q && !r.name.toLowerCase().includes(q) && !r.id.toLowerCase().includes(q)) return false;
      return true;
    });
    const sorters = {
      worth: (a, b) => b.worth - a.worth || b.units - a.units,
      units: (a, b) => b.units - a.units || b.worth - a.worth,
      held: (a, b) => b.held - a.held || b.units - a.units,
    };
    filtered.sort(sorters[invSort] || sorters.worth);

    if (!filtered.length) {
      bodyBox.append(el('p', 'empty', 'No items match the current filter.'));
      return;
    }
    const card = el('div', 'icard');
    const sumWorth = filtered.reduce((a, r) => a + (r.worth || 0), 0);
    const sumUnits = filtered.reduce((a, r) => a + (r.units || 0), 0);
    card.append(el('div', 'icsub', 'Showing ' + fmt(filtered.length) + ' item types | ' + fmt(sumUnits) + ' units | ~' + fmtCompact(sumWorth) + ' cr catalog worth'));
    card.append(fitTable(table(['Item', 'Category', 'Total', 'In Vaults', 'In Holds', 'Unit Val', 'Worth'],
      filtered.map((r) => [
        itemLink(r.id, r.name),
        kindPill(r.kind),
        fmt(r.units),
        fmt(r.stored),
        r.held ? fmt(r.held) : '--',
        fmt(r.value),
        fmtCompact(r.worth) + ' cr',
      ]), [2, 3, 4, 5, 6])));
    bodyBox.append(card);
  };

  sInp.addEventListener('input', () => { invQuery = sInp.value; drawInvBody(); });
  clearBtn.addEventListener('click', () => { invQuery = ''; sInp.value = ''; drawInvBody(); });
  drawInvBody();
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
const DOC_RE = /^(reports|communications|governance|game\/(planets|players|factions|rules|routes\/guidebook(?:\/[a-z]+)?|routes|fleet|catalog\/recipes|catalog\/ships|catalog))\/[A-Za-z0-9_.\-]{1,120}\.(md|log)$/;
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
let docSub = 'Reports', docAuthor = 'all', docQuery = '', logQuery = '', logAuthor = 'all';
let DOCSCACHE = { data: null, at: 0 };
let playbookDiv = 'mining', playbookChap = 'card', PLAYBOOKS = { at: 0, data: null };
let progHorizon = 'all', PROGCACHE = { at: 0, data: null };
async function docsOf() {
  if (Date.now() - DOCSCACHE.at < 30000 && DOCSCACHE.data) return DOCSCACHE.data;
  try { DOCSCACHE = { data: await get('/api/docs'), at: Date.now() }; } catch (e) { return DOCSCACHE.data; }
  return DOCSCACHE.data;
}

function logView(text, cut, base, filterText, authorFilter) {   // an append-only log as entry cards, newest first, with optional instant filter
  const out = el('div', 'entries'), parts = String(text).split(/^(?=## \[ENT-\d+\])/m);
  const entries = parts.filter((p) => p.startsWith('## [ENT-'));
  if (!entries.length) { out.append(markdown(text, base, true)); return out; }
  const q = String(filterText || '').trim().toLowerCase();
  const af = String(authorFilter || 'all').toLowerCase();
  const matched = entries.filter((raw) => {
    if (af !== 'all') {
      const nl0 = raw.indexOf('\n'), h0 = (nl0 < 0 ? raw : raw.slice(0, nl0)).replace(/^## /, '').split('|').map((s) => s.trim());
      const who0 = (h0[2] || '').toLowerCase();
      if (who0 !== af && !raw.toLowerCase().includes('@' + af)) return false;
    }
    if (q && !raw.toLowerCase().includes(q)) return false;
    return true;
  });
  if (!matched.length) {
    out.append(el('p', 'empty', 'No log entry matches the active filter.'));
    return out;
  }
  for (const raw of [...matched].reverse()) {
    const nl = raw.indexOf('\n'), head = (nl < 0 ? raw : raw.slice(0, nl)).replace(/^## /, '').split('|').map((s) => s.trim());
    const card = el('div', 'entry icard-entry'), top = el('div', 'entryhead'), who = head[2] || '';
    const member = ((S && S.roster) || []).find((a) => a.name === who || a.id === who.toLowerCase());
    const name = el('b', null, who || 'unknown');
    name.style.color = member ? (DIV[member.division] || DIV.Command) : 'var(--dim)';
    card.style.borderLeftColor = member ? (DIV[member.division] || DIV.Command) : 'var(--line2)';
    const kind = head[3] || '';
    const kindCls = kind === 'error' ? 'bad' : kind === 'closed' || kind === 'report' ? 'good' : kind === 'request' ? 'warn' : 'info';
    top.append(name, el('span', 'pill', head[0].replace(/[[\]]/g, '')), kind ? el('span', 'pill ' + kindCls, kind) : '', el('span', 'when', stampCet(head[1] || '')));
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

async function playbooksOf(force) {
  const now = Date.now();
  if (!force && PLAYBOOKS.data && now - PLAYBOOKS.at < 30000) return PLAYBOOKS.data;
  try {
    const res = await get('/api/playbooks');
    if (res && res.divisions) PLAYBOOKS = { at: now, data: res };
  } catch (_e) {}
  return PLAYBOOKS.data;
}

function renderPlaybooksSubtab(panel, pbData, live) {
  if (!pbData || !pbData.divisions || !pbData.divisions.length) {
    panel.append(el('p', 'empty', 'Loading live division playbooks and telemetry anchors...'));
    return;
  }
  const divs = pbData.divisions;
  const active = divs.find((x) => x.division === playbookDiv) || divs[0];
  playbookDiv = active.division;

  const dBar = el('div', 'pb-divbar');
  for (const dv of divs) {
    const col = DIV[dv.title] || DIV.Command;
    const isOn = dv.division === active.division;
    const btn = el('button', 'pb-divpill' + (isOn ? ' on' : ''));
    btn.type = 'button';
    if (isOn) { btn.style.borderColor = col; btn.style.boxShadow = 'inset 0 0 0 1px ' + col; }
    const dot = el('span', 'pb-dot');
    dot.style.background = col;
    const warnN = ((dv.curation && dv.curation.near_count) || 0) + ((dv.curation && dv.curation.over_count) || 0) + (((dv.curation && dv.curation.drift_warnings) || []).length);
    btn.append(
      dot,
      el('span', 'pb-dname', dv.title),
      el('span', 'pb-dmeta', dv.member + ' | ' + fmt((dv.fleet && dv.fleet.ships_total) || 0) + 'sh'),
      warnN ? el('span', 'pill warn', String(warnN)) : ''
    );
    btn.addEventListener('click', () => { playbookDiv = dv.division; playbookChap = 'card'; render(); });
    dBar.append(btn);
  }
  panel.append(dBar);

  const fl = active.fleet || {}, cur = active.curation || {}, caps = pbData.caps || {};
  const chaps = cur.chapters || [], drifts = cur.drift_warnings || [];
  const totalChars = chaps.reduce((a, c) => a + (c.chars || 0), 0);
  const totalEntries = chaps.reduce((a, c) => a + (c.entries || 0), 0);
  const readyNeeds = (active.open_needs || []).filter((n) => n.ready_to_close).length;

  const banner = el('div', 'icard pb-anchor-head');
  banner.style.borderLeft = '3px solid ' + (DIV[active.title] || DIV.Command);
  const bTop = el('div', 'pb-head-row');
  bTop.append(
    el('b', null, active.title + ' Division -- Live Ground-Truth Anchor (' + active.member + ')'),
    el('span', 'pill good', 'Catalog ' + (active.catalog_version || '--')),
    el('span', 'when', 'Auto-computed ' + stampCet(active.computed_at || ''))
  );
  banner.append(
    bTop,
    el('p', 'sub', 'Anchor-and-Delta loop: ship builds, skill rungs, open priorities and open requests below update automatically from read.db; curated guidebook chapters stay capped (card ' + fmt(caps.card || 4500) + ', chapter ' + fmt(caps.chapter || 12000) + ', warn >=85%) and archive retired entries into doc_versions.')
  );
  panel.append(banner);

  const pKpis = el('div', 'kpis');
  const pk = (k, v, sub, cls) => { const b = el('div', 'kpi' + (cls ? ' ' + cls : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sub) b.append(el('div', 's', sub)); pKpis.append(b); };
  const hullSummary = (fl.hulls || []).slice(0, 2).map((h) => h.class + ' (T' + h.tier + ') x' + h.count).join(', ') || 'no hulls';
  pk('Live Fleet & Hulls', fmt(fl.ships_total || 0) + ' ships', (fl.flying || 0) + ' flying, ' + (fl.docked || 0) + ' docked | ' + hullSummary, 'pos');
  pk('Tier 2+ Readiness', fmt(fl.ready_pilots || 0) + ' ready', 'Piloting avg ' + (fl.avg_piloting != null ? fl.avg_piloting.toFixed(1) : '0') + ' | max ' + fmt(fl.max_piloting || 0), (fl.ready_pilots || 0) > 0 ? 'warn' : '');
  pk('Open Priorities & Reqs', fmt((active.open_needs || []).length) + ' needs | ' + fmt((active.open_requests || []).length) + ' reqs', readyNeeds ? readyNeeds + ' priority 100% stocked (ready)' : 'live from needs.tsv & requests.log', readyNeeds ? 'pos' : '');
  pk('Guidebook Cap Health', (cur.max_pct != null ? cur.max_pct.toFixed(0) : '0') + '% peak', fmt(totalEntries) + ' entries (' + fmt(totalChars) + ' chars) | ' + drifts.length + ' drift check(s)', cur.over_count ? 'neg' : (cur.near_count || drifts.length ? 'warn' : 'pos'));
  panel.append(pKpis);

  const twoCol = el('div', 'pb-grid');

  const buildCard = el('div', 'icard');
  const es = active.empty_slots || {};
  buildCard.append(el('h3', null, 'Live Ship Builds & Module Loadouts'), el('p', 'sub', 'Fitted modules across active ships | Empty slots: ' + fmt(es.weapon || 0) + 'W / ' + fmt(es.defense || 0) + 'D / ' + fmt(es.utility || 0) + 'U'));
  if ((active.ship_builds || []).length) {
    buildCard.append(fitTable(table(
      ['Hull', 'Tier', 'Fitted Loadout', 'Ships'],
      active.ship_builds.map((b) => [b.hull, 'T' + b.tier, b.loadout, fmt(b.ships)]),
      [3]
    )));
  } else {
    buildCard.append(el('p', 'empty', 'No ships in this division.'));
  }
  if ((fl.next_unlocks || []).length) {
    buildCard.append(el('div', 'pb-subhead', 'Catalog Upgrade Ladder (Tier 1-3)'), fitTable(table(
      ['Catalog Hull', 'Tier', 'Piloting', 'Hold', 'Slots'],
      fl.next_unlocks.slice(0, 4).map((u) => [u.name, 'T' + u.tier, 'P' + u.piloting_req, fmt(u.cargo), u.slots]),
      [2, 3]
    )));
  }
  twoCol.append(buildCard);

  const lvlCard = el('div', 'icard');
  lvlCard.append(el('h3', null, 'Live Skill Leveling Rungs & XP Velocity'), el('p', 'sub', 'Pilot skill distribution (ship_skills) & empirical 24h XP/ship-h'));
  if ((active.leveling && active.leveling.skills || []).length) {
    lvlCard.append(fitTable(table(
      ['Skill', 'Avg', 'Range', '24h XP/sh-h'],
      active.leveling.skills.map((s) => [s.name, s.avg.toFixed(1), s.min + '..' + s.max, s.xp_per_ship_h != null ? s.xp_per_ship_h.toFixed(1) : '--']),
      [1, 3]
    )));
  } else {
    lvlCard.append(el('p', 'empty', 'No skill telemetry recorded yet.'));
  }
  if ((active.leveling && active.leveling.top_xp_routes || []).length) {
    lvlCard.append(el('div', 'pb-subhead', 'Top Empirical Training Routes (24h)'), fitTable(table(
      ['Route', 'Kind', 'XP/sh-h', '24h cr/h'],
      active.leveling.top_xp_routes.slice(0, 4).map((r) => [r.route, r.kind, r.xp_per_ship_h.toFixed(1), r.cph_24h != null ? fmt(r.cph_24h) : '--']),
      [2, 3]
    )));
  }
  twoCol.append(lvlCard);
  panel.append(twoCol);

  const qGrid = el('div', 'pb-grid');
  const needCard = el('div', 'icard');
  needCard.append(el('h3', null, 'Open Division Priorities (needs.tsv)'), el('p', 'sub', 'Auto-reconciled against live stock, facilities & hulls'));
  if ((active.open_needs || []).length) {
    needCard.append(fitTable(table(
      ['Pri', 'Need', 'Target', 'Covered', 'Status / Short'],
      active.open_needs.slice(0, 8).map((n) => [
        'P' + n.priority,
        n.id,
        n.ref + ' x' + fmt(n.units),
        n.covered.toFixed(0) + '%',
        n.ready_to_close ? 'READY (100% stocked)' : (n.short_items || n.craft || (n.fee ? 'fee ' + fmt(n.fee) + ' cr' : 'in progress')).slice(0, 56)
      ]),
      [3]
    )));
  } else {
    needCard.append(el('p', 'empty', '0 open material/facility priorities for ' + active.title + '.'));
  }
  qGrid.append(needCard);

  const reqCard = el('div', 'icard');
  reqCard.append(el('h3', null, 'Open Division Requests (requests.log)'), el('p', 'sub', 'Active engineering & coordination requests involving ' + active.member));
  if ((active.open_requests || []).length) {
    for (const rq of active.open_requests.slice(0, 6)) {
      const row = el('div', 'pb-reqrow');
      row.append(
        el('span', 'pill ' + (rq.stale_days ? 'bad' : (rq.state === 'ACCEPTED' ? 'good' : 'warn')), rq.ent + ' ' + rq.state + (rq.stale_days ? ' STALE' : '')),
        el('b', null, ' ' + rq.from + ' -> ' + rq.to + ' '),
        el('span', 'when', '(' + stampCet(rq.when) + ') '),
        el('div', 'pb-reqtxt', rq.need)
      );
      reqCard.append(row);
    }
  } else {
    reqCard.append(el('p', 'empty', '0 open requests involving ' + active.member + '.'));
  }
  qGrid.append(reqCard);
  panel.append(qGrid);

  const capCard = el('div', 'icard');
  capCard.append(
    el('h3', null, 'Capped Guidebook Chapters & Drift Guard (' + chaps.length + ' chapters)'),
    el('p', 'sub', 'Click any chapter below to inspect its curated tactical entries inline. Chapters >=85% trigger proactive curation; retired entries archive to doc_versions.')
  );
  if (drifts.length) {
    const dBox = el('div', 'pb-driftbox');
    dBox.append(el('b', null, 'Empirical Drift & Freshness Checks (' + drifts.length + '):'));
    for (const w of drifts) {
      dBox.append(el('div', 'pb-driftline', '[' + w.chapter + '.md :: ' + w.entry + '] ' + w.detail));
    }
    capCard.append(dBox);
  }

  const cStrip = el('div', 'pb-chapbar');
  if (!chaps.some((c) => c.chapter === playbookChap) && chaps.length) playbookChap = chaps[0].chapter;
  const readerWrap = el('div', 'pb-chapreader');

  const loadChapterInline = async (ch) => {
    readerWrap.replaceChildren(el('p', 'empty', 'Loading ' + ch.path + '...'));
    try {
      const res = await get('/api/doc?path=' + encodeURIComponent(ch.path));
      if (!live()) return;
      readerWrap.replaceChildren();
      const headRow = el('div', 'pb-chaphead');
      const fullBtn = el('button', 'rf', 'Open Full Reader ->');
      fullBtn.type = 'button';
      fullBtn.addEventListener('click', () => openDoc(ch.path));
      headRow.append(
        el('b', null, ch.path + ' (' + ch.entries + ' entries, ' + fmt(ch.chars) + ' / ' + fmt(ch.cap) + ' chars, ' + ch.pct.toFixed(1) + '%)'),
        fullBtn
      );
      readerWrap.append(headRow);
      if (res && res.text) {
        readerWrap.append(markdown(res.text, ch.path, false));
      } else {
        readerWrap.append(el('p', 'empty', (res && res.error) || 'Empty chapter.'));
      }
    } catch (_e) {
      readerWrap.replaceChildren(el('p', 'empty', 'Could not load chapter.'));
    }
  };

  for (const ch of chaps) {
    const isSel = ch.chapter === playbookChap;
    const cBtn = el('button', 'pb-chappill ' + ch.band + (isSel ? ' on' : ''));
    cBtn.type = 'button';
    const fill = el('span', 'pb-meter-fill ' + ch.band);
    fill.style.width = Math.min(100, Math.max(2, ch.pct)) + '%';
    const meter = el('span', 'pb-meter');
    meter.append(fill);
    cBtn.append(
      el('span', 'pb-cname', ch.chapter + '.md'),
      el('span', 'pb-cpct', ch.pct.toFixed(0) + '% (' + ch.entries + ')'),
      meter
    );
    cBtn.addEventListener('click', () => { playbookChap = ch.chapter; render(); });
    cStrip.append(cBtn);
  }
  capCard.append(cStrip, readerWrap);
  panel.append(capCard);

  const selChap = chaps.find((c) => c.chapter === playbookChap);
  if (selChap) loadChapterInline(selChap);
}

async function progressionOf(force) {
  const now = Date.now();
  if (!force && PROGCACHE.data && now - PROGCACHE.at < 30000) return PROGCACHE.data;
  try {
    const res = await get('/api/progression');
    if (res && res.summary) PROGCACHE = { at: now, data: res };
  } catch (_e) {}
  return PROGCACHE.data;
}

function renderProgressionSubtab(panel, prData) {
  if (!prData || !prData.summary) {
    panel.append(el('p', 'empty', 'Loading enterprise progression roadmap and milestone chronicle...'));
    return;
  }
  const s = prData.summary, rungs = prData.rungs || [], miles = prData.milestones || [];
  const avgPct = rungs.length ? (rungs.reduce((a, r) => a + (r.pct || 0), 0) / rungs.length) : 0;

  const headCard = el('div', 'icard pb-anchor-head');
  headCard.style.borderLeft = '3px solid var(--good)';
  const hTop = el('div', 'pb-head-row');
  hTop.append(
    el('b', null, 'Enterprise Progression Guide & Milestone Chronicle -- Campaign Day ' + fmt(s.days_active || 1)),
    el('span', 'pill good', fmt(miles.length) + ' Milestones Achieved'),
    el('span', 'when', 'Updated ' + stampCet(s.computed_at || ''))
  );
  const fullDocBtn = el('button', 'rf', 'Open Blueprint Markdown ->');
  fullDocBtn.type = 'button';
  fullDocBtn.addEventListener('click', () => openDoc('governance/progression-roadmap.md'));
  hTop.append(fullDocBtn);
  headCard.append(
    hTop,
    el('p', 'sub', 'Tracks where The Collective came from (since 14 Nov Founding), where we stand right now, and our 12 strategic rungs across Days, Weeks, and Months toward S1-S5 and G1-G5.')
  );
  panel.append(headCard);

  const kpis = el('div', 'kpis');
  const pk = (k, v, sub, cls) => { const b = el('div', 'kpi' + (cls ? ' ' + cls : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sub) b.append(el('div', 's', sub)); kpis.append(b); };
  pk('Enterprise Net Worth', fmt(s.enterprise_value || 0) + ' cr', fmt(s.liquid_purse || 0) + ' cash | ' + fmt(s.vault_worth || 0) + ' vault | ' + fmt(s.facility_worth || 0) + ' fac', 'main pos');
  pk('Armada & Seating', fmt(s.ships_total || 0) + ' / 500 ships', fmt(s.seats_used || 0) + ' / ' + fmt(s.seats_cap || 0) + ' seated in [CLTV]', 'pos');
  pk('Tier 2+ & Tech Rung', fmt(s.p10_ready || 0) + ' P10+ ready', fmt(s.t1_plus || 0) + ' T1+ hulls | ' + fmt(s.t3_mods || 0) + ' T2/T3 key mods', (s.p10_ready || 0) > 0 ? 'warn' : '');
  pk('12-Rung Roadmap Avg', avgPct.toFixed(1) + '%', fmt(s.outposts || 0) + '/8 outposts | ' + fmt(s.stations || 0) + ' stations | ' + fmt(s.systems_charted || 0) + '/' + fmt(s.total_systems || 506) + ' sys', 'pos');
  panel.append(kpis);

  const hFilter = el('div', 'sortbar');
  hFilter.append(el('span', 'sortlbl', 'Horizon:'));
  for (const [id, lbl] of [['all', 'All Horizons (12)'], ['Days', 'Immediate (Days)'], ['Weeks', 'Mid-Term (Weeks)'], ['Months', 'Long-Term (Months)']]) {
    const fb = el('button', 'rf' + (progHorizon === id ? ' on' : ''), lbl);
    fb.type = 'button';
    fb.addEventListener('click', () => { progHorizon = id; render(); });
    hFilter.append(fb);
  }
  panel.append(hFilter);

  const rungCard = el('div', 'icard');
  rungCard.append(el('h3', null, 'Where We Are Going -- Strategic Progression Ladder (S1-S5, G1-G5)'));
  const rungList = el('div', 'pr-rungs');
  for (const r of rungs) {
    if (progHorizon !== 'all' && !String(r.horizon || '').startsWith(progHorizon)) continue;
    const row = el('div', 'pr-rung');
    const top = el('div', 'pr-rung-top');
    const hCls = String(r.horizon).startsWith('Days') ? 'warn' : (String(r.horizon).startsWith('Weeks') ? 'info' : '');
    const pctCls = r.pct >= 90 ? 'good' : (r.pct >= 50 ? 'warn' : '');
    top.append(
      el('span', 'pill ' + hCls, r.horizon),
      el('span', 'pill', r.orders),
      el('b', 'pr-rtitle', r.title),
      el('span', 'pill ' + pctCls, r.pct.toFixed(1) + '%')
    );
    const bar = el('div', 'pr-bar');
    const fill = el('div', 'pr-bar-fill' + (r.pct >= 90 ? ' good' : (r.pct >= 45 ? ' mid' : ' low')));
    fill.style.width = Math.min(100, Math.max(2, r.pct)) + '%';
    bar.append(fill);
    const meta = el('div', 'pr-rmeta');
    meta.append(
      el('span', null, 'Now: ' + r.current + '  ->  Target: ' + r.target),
      el('div', 'pr-rbottle', 'Rate-limiting step: ' + r.bottleneck)
    );
    row.append(top, bar, meta);
    rungList.append(row);
  }
  rungCard.append(rungList);
  panel.append(rungCard);

  const mCard = el('div', 'icard');
  mCard.append(el('h3', null, 'Where We Came From -- Verified Milestone Chronicle (' + miles.length + ')'), el('p', 'sub', 'Chronological breakthroughs from Day 1 Founding plus live auto-detected empire unlocks.'));
  const tl = el('div', 'pr-timeline');
  for (const m of [...miles].reverse()) {
    const item = el('div', 'pr-mile');
    const mTop = el('div', 'pr-mile-top');
    mTop.append(el('span', 'pill good', m.date), el('span', 'pill', m.era), el('b', null, m.title));
    item.append(mTop, el('div', 'pr-mile-det', m.detail));
    tl.append(item);
  }
  mCard.append(tl);
  panel.append(mCard);

  const pGrid = el('div', 'pb-grid');
  if ((prData.weekly || []).length) {
    const wCard = el('div', 'icard');
    wCard.append(el('h3', null, 'Weekly Trajectory Ledger'), el('p', 'sub', 'Rolling ISO-week operating cashflow & peak purse (stats_money_hour)'));
    wCard.append(fitTable(table(
      ['Week', 'Span', 'Hrs', 'Income', 'Costs', 'Steady Net', 'Once Net', 'Peak Purse'],
      prData.weekly.map((w) => [w.period, w.span, fmt(w.active_hours), fmt(w.income), fmt(w.costs), (w.steady_net >= 0 ? '+' : '') + fmt(w.steady_net), (w.paid_once >= 0 ? '+' : '') + fmt(w.paid_once), fmt(w.peak_purse)]),
      [2, 3, 4, 5, 6, 7]
    )));
    pGrid.append(wCard);
  }
  if ((prData.monthly || []).length) {
    const moCard = el('div', 'icard');
    moCard.append(el('h3', null, 'Monthly Trajectory Ledger'), el('p', 'sub', 'Rolling calendar-month operating summary'));
    moCard.append(fitTable(table(
      ['Month', 'Span', 'Hrs', 'Steady Net', 'Once Net', 'Peak Purse'],
      prData.monthly.map((m) => [m.period, m.span, fmt(m.active_hours), (m.steady_net >= 0 ? '+' : '') + fmt(m.steady_net), (m.paid_once >= 0 ? '+' : '') + fmt(m.paid_once), fmt(m.peak_purse)]),
      [2, 3, 4, 5]
    )));
    pGrid.append(moCard);
  }
  if (pGrid.childNodes.length) panel.append(pGrid);
}

async function renderDocs(panel, live) {
  setWide(docView ? 'wide' : 'metrics');
  const d = await docsOf();
  if (!live()) return;

  if (docView) {
    const isLog = docView.path.endsWith('.log');
    const isReport = docView.path.startsWith('reports/');
    const isGov = docView.path.startsWith('governance/');
    const bar = el('div', 'reader-bar');
    const backBtn = el('button', 'subtab', '<- Docs');
    backBtn.type = 'button';
    backBtn.addEventListener('click', () => { docView = null; render(); });
    bar.append(backBtn);

    const nav = el('div', 'reader-nav');
    if (isLog && d && d.logs) {
      bar.append(el('span', 'reader-sep'));
      for (const lg of d.logs) {
        const active = lg.path === docView.path;
        const baseLbl = docTitle(lg.name || lg.path);
        const lbl = lg.entries != null ? baseLbl + ' (' + fmt(lg.entries) + ')' : baseLbl;
        const cls = 'rf' + (active ? ' on' : (lg.name === 'errors' && lg.entries > 0 ? ' haswarn' : ''));
        const lb = el('button', cls, lbl);
        lb.type = 'button';
        lb.addEventListener('click', () => { if (!active) openDoc(lg.path); });
        nav.append(lb);
      }
      bar.append(nav);
    } else if (isReport && d && d.reports && d.reports.length) {
      bar.append(el('span', 'reader-sep'));
      const idx = d.reports.findIndex((r) => r.path === docView.path);
      const newer = idx > 0 ? d.reports[idx - 1] : null;
      const older = idx >= 0 && idx + 1 < d.reports.length ? d.reports[idx + 1] : null;
      const prevBtn = el('button', 'rf', newer ? '<- Newer (' + (newer.author || '') + ')' : '<- Newest');
      prevBtn.type = 'button'; prevBtn.disabled = !newer;
      if (newer) prevBtn.addEventListener('click', () => openDoc(newer.path));
      const nextBtn = el('button', 'rf', older ? 'Older (' + (older.author || '') + ') ->' : 'Oldest ->');
      nextBtn.type = 'button'; nextBtn.disabled = !older;
      if (older) nextBtn.addEventListener('click', () => openDoc(older.path));
      const logsJump = el('button', 'rf', 'Command Logs');
      logsJump.type = 'button';
      logsJump.addEventListener('click', () => { docView = null; docSub = 'Logs'; render(); });
      nav.append(prevBtn, nextBtn, logsJump);
      bar.append(nav);
    } else if (docView.path.startsWith('game/routes/guidebook/') && d && d.knowledge) {
      const parts = docView.path.split('/');
      const gDiv = parts.length >= 5 ? parts[3] : '';
      const sibs = d.knowledge.filter((k) => gDiv && k.path.startsWith('game/routes/guidebook/' + gDiv + '/'));
      bar.append(el('span', 'reader-sep'));
      const pbJump = el('button', 'rf', '<- ' + (gDiv ? gDiv.charAt(0).toUpperCase() + gDiv.slice(1) + ' Playbook' : 'Playbooks'));
      pbJump.type = 'button';
      pbJump.addEventListener('click', () => { if (gDiv) playbookDiv = gDiv; docView = null; docSub = 'Playbooks'; render(); });
      nav.append(pbJump);
      for (const sb of sibs) {
        const active = sb.path === docView.path;
        const chStem = sb.path.split('/').pop().replace(/\.md$/, '');
        const gb = el('button', 'rf' + (active ? ' on' : ''), chStem);
        gb.type = 'button';
        gb.addEventListener('click', () => { if (!active) openDoc(sb.path); });
        nav.append(gb);
      }
      bar.append(nav);
    } else if (isGov && d && d.governance) {
      bar.append(el('span', 'reader-sep'));
      for (const g of d.governance) {
        const active = g.path === docView.path;
        const gb = el('button', 'rf' + (active ? ' on' : ''), docTitle(g.path));
        gb.type = 'button';
        gb.addEventListener('click', () => { if (!active) openDoc(g.path); });
        nav.append(gb);
      }
      bar.append(nav);
    }

    bar.append(el('span', 'rmeta-sub reader-path', docView.path));
    panel.append(bar);
    panel.append(el('h2', null, docView.title || docTitle(docView.path)));
    if (docView.loading) { panel.append(el('p', 'empty', 'Loading document...')); return; }
    if (docView.error) { panel.append(el('p', 'empty', docView.error)); return; }
    if (docView.cut) panel.append(el('p', 'sub', isLog ? 'Showing newest entries from log tail.' : 'Showing first section of large file.'));

    if (isLog) {
      const aBar = el('div', 'sortbar');
      aBar.append(el('span', 'sortlbl', 'Admiral / author:'));
      const logAuthors = ['all', 'Unity', 'Zero', 'Mercury', 'Apollo', 'Apophis', 'Oracle', 'Trinity'];
      const wrap = el('div');
      const redrawLog = () => { wrap.replaceChildren(logView(docView.text, docView.cut, docView.path, logQuery, logAuthor)); };
      const refreshAuthorPills = () => {
        for (const ch of aBar.querySelectorAll('button.rf')) {
          ch.classList.toggle('on', ch.dataset.author === logAuthor);
        }
      };
      for (const a of logAuthors) {
        const ab = el('button', 'rf' + (logAuthor === a ? ' on' : ''), a === 'all' ? 'All' : a);
        ab.type = 'button';
        ab.dataset.author = a;
        ab.addEventListener('click', () => { logAuthor = a; refreshAuthorPills(); redrawLog(); });
        aBar.append(ab);
      }
      panel.append(aBar);

      const sRow = el('div', 'rsearch');
      const inp = el('input');
      inp.type = 'search';
      inp.placeholder = 'Filter log entries by @agent, ENT-#, or keyword...';
      inp.value = logQuery;
      const clr = el('button', 'rf', 'Reset');
      clr.type = 'button';
      sRow.append(inp, clr);
      panel.append(sRow);
      panel.append(wrap);
      inp.addEventListener('input', () => { logQuery = inp.value; redrawLog(); });
      clr.addEventListener('click', () => { logQuery = ''; logAuthor = 'all'; inp.value = ''; refreshAuthorPills(); redrawLog(); });
      redrawLog();
    } else {
      const card = el('div', 'icard doc-reader-card');
      card.append(markdown(docView.text, docView.path, false));
      panel.append(card);
    }
    return;
  }

  if (!d) { panel.append(el('p', 'empty', 'Loading fleet archives...')); return; }
  const reports = d.reports || [], logs = d.logs || [], gov = d.governance || [], know = d.knowledge || [];
  const totalEntries = logs.reduce((a, x) => a + (x.entries || 0), 0);
  const srcList = Object.entries((S && S.sources) || {});
  const srcBad = srcList.filter(([_n, s]) => s.error).length;

  panel.append(el('h2', null, 'Briefings, Command Logs & Reference'));
  panel.append(el('p', 'sub', 'Turn briefings by Admiral, live coordination logs, constitutional rules and game reference manuals.'));

  const kgrid = el('div', 'kpis');
  const dkpi = (k, v, sub, cls) => { const b = el('div', 'kpi' + (cls ? ' ' + cls : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sub) b.append(el('div', 's', sub)); kgrid.append(b); };
  dkpi('Admiral briefings', fmt(d.reports_total || reports.length) + ' filed', reports[0] ? 'latest: ' + (reports[0].author || '') + ' ' + stampCet(reports[0].at || reports[0].date) : 'none yet', 'main pos');
  dkpi('Coordination logs', fmt(logs.length) + ' active logs', fmt(totalEntries) + ' total ENT records', 'pos');
  dkpi('Governance & guides', fmt(gov.length + know.length) + ' docs', fmt(gov.length) + ' charter | ' + fmt(know.length) + ' manuals', '');
  dkpi('Station feeds', (srcList.length - srcBad) + ' / ' + srcList.length + ' OK', srcBad ? srcBad + ' feed error(s)' : 'all public feeds healthy', srcBad ? 'warn' : 'pos');
  panel.append(kgrid);

  const subBar = el('div', 'subtabs');
  const tabs = [
    ['Progression', 'Progression'],
    ['Playbooks', 'Playbooks (6)'],
    ['Reports', 'Briefings (' + reports.length + ')'],
    ['Logs', 'Command Logs (' + logs.length + ')'],
    ['Governance', 'Governance (' + gov.length + ')'],
    ['Reference', 'Manuals & Feeds (' + know.length + ')'],
  ];
  for (const [id, lbl] of tabs) {
    const b = el('button', 'subtab' + (docSub === id ? ' on' : ''), lbl);
    b.type = 'button';
    b.addEventListener('click', () => { docSub = id; render(); });
    subBar.append(b);
  }
  panel.append(subBar);

  if (docSub === 'Progression') {
    const prData = await progressionOf(false);
    if (!live()) return;
    renderProgressionSubtab(panel, prData);
    return;
  }

  if (docSub === 'Playbooks') {
    const pbData = await playbooksOf(false);
    if (!live()) return;
    renderPlaybooksSubtab(panel, pbData, live);
    return;
  }

  if (docSub === 'Logs') {
    const cards = el('div', 'icards');
    for (const lg of logs) {
      const isErr = lg.name === 'errors';
      const isOrd = lg.name === 'orders';
      const card = el('div', 'icard doc-card' + (isOrd ? ' ownbase' : ''));
      const ch = el('div', 'ichead');
      const btn = el('button', 'sysjump', lg.title || lg.name);
      btn.type = 'button';
      btn.addEventListener('click', () => openDoc(lg.path));
      ch.append(btn, el('span', 'pill ' + (isErr ? 'warn' : isOrd ? 'good' : 'info'), fmt(lg.entries) + ' entries'));
      card.append(ch);
      if (lg.desc) card.append(el('div', 'icsub', lg.desc));
      if (lg.last) {
        const meta = el('div', 'log-last');
        meta.append(el('span', 'rtag', lg.last.ent), ' by ', el('b', null, lg.last.by), ' | ', el('span', 'mono', stampCet(lg.last.at)));
        card.append(meta);
        if (lg.last.preview) card.append(el('div', 'ibsub', lg.last.preview));
      }
      cards.append(card);
    }
    panel.append(cards);
    return;
  }

  if (docSub === 'Governance') {
    const cards = el('div', 'icards');
    for (const g of gov) {
      const fname = g.path.split('/').pop();
      const card = el('div', 'icard doc-card' + (fname.includes('constitution') || fname.includes('empire') ? ' ownbase' : ''));
      const ch = el('div', 'ichead');
      const btn = el('button', 'sysjump', g.title);
      btn.type = 'button';
      btn.addEventListener('click', () => openDoc(g.path));
      ch.append(btn, el('span', 'pill good', fname));
      card.append(ch);
      cards.append(card);
    }
    panel.append(cards);
    return;
  }

  if (docSub === 'Reference') {
    const sRow = el('div', 'rsearch');
    const inp = el('input');
    inp.type = 'search';
    inp.placeholder = 'Filter manuals, route plans, guidebooks or rules...';
    inp.value = docQuery;
    const clr = el('button', 'rf', 'Clear');
    clr.type = 'button';
    sRow.append(inp, clr);
    panel.append(sRow);

    const refBox = el('div');
    panel.append(refBox);
    const drawRef = () => {
      refBox.replaceChildren();
      const q = docQuery.trim().toLowerCase();
      const groups = new Map();
      for (const k of know) {
        if (q && !k.title.toLowerCase().includes(q) && !k.path.toLowerCase().includes(q)) continue;
        const grp = k.group || 'Reference';
        if (!groups.has(grp)) groups.set(grp, []);
        groups.get(grp).push(k);
      }
      for (const [gname, items] of groups) {
        refBox.append(el('h3', null, gname + ' (' + items.length + ')'));
        const c = el('div', 'icard');
        c.append(fitTable(table(['Document', 'Path'],
          items.map((it) => [linkButton(it.title, () => openDoc(it.path), 'doclink'), el('span', 'rmeta-sub', it.path)]))));
        refBox.append(c);
      }
      if (!groups.size) refBox.append(el('p', 'empty', 'No reference document matches "' + docQuery + '".'));
    };
    inp.addEventListener('input', () => { docQuery = inp.value; drawRef(); });
    clr.addEventListener('click', () => { docQuery = ''; inp.value = ''; drawRef(); });
    drawRef();

    panel.append(el('h3', null, 'Station public feed health'));
    const fcard = el('div', 'icard');
    fcard.append(fitTable(table(['Feed', 'Freshness', 'Status'],
      srcList.map(([n, s]) => [
        n,
        ago(s.age) + (s.age < 0 ? '' : ' ago'),
        el('span', 'pill ' + (s.error ? 'bad' : 'good'), s.error ? s.error : 'OK'),
      ]))));
    panel.append(fcard);
    return;
  }

  // Default sub-tab: Briefings & Reports
  const aBar = el('div', 'sortbar');
  const authors = ['all', 'Unity', 'Zero', 'Mercury', 'Apollo', 'Apophis', 'Oracle'];
  for (const a of authors) {
    const b = el('button', 'rf' + (docAuthor === a ? ' on' : ''), a === 'all' ? 'All Admirals' : a);
    b.type = 'button';
    b.addEventListener('click', () => { docAuthor = a; render(); });
    aBar.append(b);
  }
  panel.append(aBar);

  const sRow = el('div', 'rsearch');
  const inp = el('input');
  inp.type = 'search';
  inp.placeholder = 'Search report titles (e.g. recruitment, strict classes, whale, hull)...';
  inp.value = docQuery;
  const clr = el('button', 'rf', 'Clear');
  clr.type = 'button';
  sRow.append(inp, clr);
  panel.append(sRow);

  const repBox = el('div');
  panel.append(repBox);
  const drawReports = () => {
    repBox.replaceChildren();
    const q = docQuery.trim().toLowerCase();
    const shown = reports.filter((r) => {
      if (docAuthor !== 'all' && String(r.author || '').toLowerCase() !== docAuthor.toLowerCase()) return false;
      if (q && !String(r.title || '').toLowerCase().includes(q) && !String(r.author || '').toLowerCase().includes(q)) return false;
      return true;
    });
    if (!shown.length) {
      repBox.append(el('p', 'empty', 'No reports match this filter.'));
      return;
    }
    const cards = el('div', 'icards');
    for (const r of shown) {
      const member = ((S && S.roster) || []).find((a) => a.id === String(r.author || '').toLowerCase() || a.name === r.author);
      const divName = member ? member.division : 'Command';
      const col = DIV[divName] || DIV.Command;
      const card = el('div', 'icard doc-card report-card');
      card.style.borderLeft = '3px solid ' + col;
      const ch = el('div', 'ichead');
      const whoEl = el('b', null, r.author || 'Unknown');
      whoEl.style.color = col;
      ch.append(whoEl, el('span', 'rmeta-sub', divName), el('span', 'pill', stampCet(r.at || r.date || '')));
      card.append(ch);
      const tBtn = el('button', 'sysjump report-jump', r.title);
      tBtn.type = 'button';
      tBtn.addEventListener('click', () => openDoc(r.path));
      card.append(tBtn);
      cards.append(card);
    }
    repBox.append(cards);
  };
  inp.addEventListener('input', () => { docQuery = inp.value; drawReports(); });
  clr.addEventListener('click', () => { docQuery = ''; inp.value = ''; drawReports(); });
  drawReports();
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
let metricWin = '24h';   // a trailing day by default (Suggi, 2026-11-17): one purchase or a gift in transit bends an hour, a day far less
let metricsAt = 0;                               // when the Metrics tab was last drawn: it is drawn again every 30 s, not at every fleet poll
let routeOrder = { key: '', rank: new Map() };   // the place of each route row while the tab stays open on one window
function keepOrder(rows) {                       // a table that reorders under the eye cannot be read: rows keep their place, a new route joins at the end
  if (routeOrder.key !== metricWin) routeOrder = { key: metricWin, rank: new Map() };
  rows.forEach((x) => { if (!routeOrder.rank.has(x.route)) routeOrder.rank.set(x.route, routeOrder.rank.size); });
  return rows.sort((a, b2) => routeOrder.rank.get(a.route) - routeOrder.rank.get(b2.route));
}
let INCOME = { routes: [], at: 0, key: '' };
let OPS = { data: null, at: 0 };
let DIPLO = { data: null, at: 0 };
let empSub = 'Infrastructure', empSort = 'wealth', rivalFocus = null;
async function opsOf() {
  if (Date.now() - OPS.at < 30000 && OPS.data) return OPS.data;
  try { OPS = { data: await get('/api/ops'), at: Date.now() }; } catch (e) { return OPS.data; }
  return OPS.data;
}
async function diploOf() {
  if (Date.now() - DIPLO.at < 45000 && DIPLO.data) return DIPLO.data;
  try { DIPLO = { data: await get('/api/diplomacy'), at: Date.now() }; } catch (e) { return DIPLO.data; }
  return DIPLO.data;
}
function focusRivalOnMap(tag, name, baseSyss, sightSyss) {
  const bSet = new Set((baseSyss || []).filter((id) => sys.has(id)));
  const sSet = new Set((sightSyss || []).filter((id) => sys.has(id)));
  if (!bSet.size && !sSet.size) return;
  rivalFocus = { tag, name, bases: bSet, systems: sSet };
  const pts = [...(bSet.size ? bSet : sSet)].map((id) => sys.get(id)).filter(Boolean);
  if (pts.length === 1) {
    flyTo(pts[0].x, pts[0].y, Math.max(view.k, 0.22));
  } else if (pts.length > 1) {
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    pts.forEach((p) => { if (p.x < x0) x0 = p.x; if (p.x > x1) x1 = p.x; if (p.y < y0) y0 = p.y; if (p.y > y1) y1 = p.y; });
    const wrap = $('mapwrap') || document.body;
    const W = Math.max(360, (wrap.clientWidth || 900) - 80), H = Math.max(260, (wrap.clientHeight || 600) - 80);
    const spanX = Math.max(180, x1 - x0), spanY = Math.max(180, y1 - y0);
    const nk = Math.max(0.06, Math.min(0.32, Math.min(W / spanX, H / spanY) * 0.72));
    flyTo((x0 + x1) / 2, (y0 + y1) / 2, nk);
  }
  renderAlerts();
  draw();
}
async function loadOps() {
  await opsOf();
  battleSystems.clear();
  ((OPS.data && OPS.data.alerts && OPS.data.alerts.battles) || []).forEach((b) => { if (b.system) battleSystems.add(b.system); });
  if (S) { status(); renderMembers(); }
  renderAlerts();
  draw();
}
function pbar(val, max, cls) {
  const w = el('span', 'pbar ' + (cls || '')), fill = el('i');
  fill.style.width = pct(val, max) + '%';
  w.append(fill);
  return w;
}
function renderAlerts() {
  const barEl = $('alertbar');
  if (!barEl) return;
  barEl.replaceChildren();
  const chips = [];
  const addChip = (cls, label, title, go) => {
    const b = el('button', 'achip ' + cls, label);
    b.type = 'button'; b.title = title;
    b.addEventListener('click', go);
    chips.push(b);
  };
  if (rivalFocus) {
    const nb = rivalFocus.bases.size, ns = rivalFocus.systems.size;
    addChip('info', 'RIVAL MAP: [' + rivalFocus.tag + '] ' + rivalFocus.name + ' (' + nb + ' base' + (nb === 1 ? '' : 's') + ', ' + ns + ' seen) [x]',
      'Click to clear rival faction overlay on the map', () => { rivalFocus = null; renderAlerts(); draw(); });
  }
  const ops = OPS.data;
  if (ops) {
    const sv = ops.services || {};
    if (sv.down && sv.down.length) {
      addChip('bad', 'Service down: ' + sv.down.join(', '), 'Open Metrics readiness', () => { tab = 'Metrics'; render(); });
    }
    const battles = (ops.alerts && ops.alerts.battles) || [];
    battles.slice(0, 2).forEach((b) => {
      addChip('bad', (b.category || 'battle').toUpperCase() + ': ' + (b.system_name || b.system), 'Jump camera to battle system',
        () => { if (sys.has(b.system)) select(b.system, true); else { tab = 'Metrics'; render(); } });
    });
    const fac = (ops.readiness && ops.readiness.faction) || {};
    if (fac.limit && fac.members >= fac.limit - 2) {
      addChip('warn', 'Faction cap ' + fac.members + '/' + fac.limit, 'Open Metrics needs (recruitment-center)', () => { tab = 'Metrics'; render(); });
    }
    const shorts = (ops.supply || []).filter((x) => x.state === 'SHORT');
    if (shorts.length) {
      const top = shorts[0];
      addChip('warn', 'Supply short: ' + top.chain + (shorts.length > 1 ? ' (+' + (shorts.length - 1) + ')' : ''), 'Open Metrics supply chains', () => { tab = 'Metrics'; render(); });
    }
    const mad = ((ops.alerts && ops.alerts.mad) || []).filter((m) => m.verdict.startsWith('OUT'));
    if (mad.length) {
      addChip('warn', mad.length + ' MAD anomal' + (mad.length === 1 ? 'y' : 'ies'), 'Open Metrics anomaly table', () => { tab = 'Metrics'; render(); });
    }
  }
  const idleCount = F.ships.filter((r) => ['dock', 'idle'].includes(shipState(r)[0])).length;
  if (idleCount > 0) {
    addChip('info', idleCount + ' idle ship' + (idleCount === 1 ? '' : 's'), 'Filter Fleet outliner to Idle ships', () => {
      if (shut.has('left')) toggleShut('left');
      setRosterMode('idle');
    });
  }
  if (!chips.length) { barEl.hidden = true; return; }
  chips.forEach((c) => barEl.append(c));
  const noticeOpen = $('notice') && !$('notice').hidden;
  barEl.classList.toggle('below-notice', Boolean(noticeOpen));
  barEl.hidden = false;
}
function toggleHelp(force) {
  const card = $('helpcard');
  if (!card) return;
  const show = force !== undefined ? force : card.hidden;
  if (!show) { card.hidden = true; return; }
  card.replaceChildren(
    el('div', 'helphead', 'Command Station Shortcuts'),
    table(['Key', 'Action'], [
      ['F / H / G', 'Camera: Fit Fleet / Home / Galaxy'],
      ['1 / 2 / 3 / 4', 'Right panel: Selection / Metrics / Inventory / Docs'],
      ['[ / ]', 'Toggle left Fleet outliner / right Inspector'],
      ['/', 'Focus global system & pilot search'],
      ['Double-click ship', 'Snap camera onto ship system'],
      ['Esc', 'Close card / shortcuts / blur search'],
    ])
  );
  card.hidden = false;
}

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
  const net = w ? purseNet(w) : 0, own = w && w.treasury_own_per_hour !== undefined;
  kpi('Net / h', w ? signed(net) : '--', own ? 'everything: steady money, paid once and the treasury\'s own' : 'everything: steady money plus paid once', 'main' + (w ? tone(net) : ''));
  kpi('Steady net / h', w ? signed(w.cph) : '--', 'income minus costs: what repeats', 'main' + (w ? tone(w.cph) : ''));
  kpi('Paid once / h', w ? signed(w.one_time_per_hour) : '--', 'rewards once per pilot, less goods bought for them', w ? tone(w.one_time_per_hour).trim() : '');
  kpi('Net per ship / h', w ? signed(Math.round(net / (t.ships || 1))) : '--', 'everything, per ship', w ? tone(net).trim() : '');
  kpi('Treasury, own / h', own ? signed(w.treasury_own_per_hour) : '--', own ? 'rent and buildings it paid, less money in besides our deposits' : 'not read at both ends of this stretch yet',
    own ? tone(w.treasury_own_per_hour).trim() : '');
  kpi('Steady income / h', w ? fmt(w.income_per_hour) : '--', w && w.income_per_hour < 0 ? 'below zero: a fault of the books' : 'sales and repeatable rewards',
    w && w.income_per_hour > 0 ? 'pos' : w && w.income_per_hour < 0 ? 'warn' : '');
  kpi('Running costs / h', w ? fmt(w.costs_per_hour) : '--', w && w.costs_per_hour < 0 ? 'below zero: money came in that no counter names; read the longer stretch' : 'fuel, repairs, goods, modules',
    w && w.costs_per_hour > 0 ? 'neg' : w && w.costs_per_hour < 0 ? 'warn' : '');   // a cost below zero is a fault of the books, never good news
  const metered = w && w.fuel_cr_per_hour !== undefined;
  kpi('Fuel / h', metered ? fmt(w.fuel_cr_per_hour) : '--', metered ? fmt(w.fuel_units_per_hour) + ' units bought' : 'not measured in this stretch yet', metered && w.fuel_cr_per_hour > 0 ? 'neg' : '');
  kpi('Repairs / h', metered ? fmt(w.repair_cr_per_hour) : '--', metered ? fmt(w.hull_points_per_hour) + ' hull points' : 'not measured in this stretch yet', metered && w.repair_cr_per_hour > 0 ? 'neg' : '');
  kpi('Ships working', t.ships ? fmt(t.working) + ' of ' + fmt(t.ships) : '--',
    fmt(t.parked) + ' parked at a station' + (t.adrift ? ', ' + fmt(t.adrift) + ' in space without work' : ''));
  const purse = (S.holdings && S.holdings.treasury) || 0;   // the faction's treasury: the fleet's main purse (D225)
  kpi('Credits', fmt((t.credits || 0) + purse), 'wallets ' + fmt(t.credits) + ' + purse ' + fmt(purse) + '; ' + fmt(t.credits_per_ship) + ' a ship');
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
    if (w.treasury) {                              // the treasury's own books: its readings, our deposits between them, the rest its own
      const x = w.treasury;
      check.append(' The treasury read ' + fmt(x.start) + ' cr at ' + stampOf(x.read_from * 1000) + ' and ' + fmt(x.end) + ' cr at ' + stampOf(x.read_to * 1000)
        + ': ' + fmt(x.deposited) + ' cr deposited by our ships, ', tint(x.own), ' its own (rent, buildings, money paid out or in).');
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
  if (div.Unassigned || dw.Unassigned) order.push(['Unassigned', '']);   // station/fleet.py window: money no division holds
  const moneyRow = (name, working, y) => [name, working, w ? shade(y.income_per_hour, 'pos') : '--', w ? shade(y.costs_per_hour, 'neg') : '--', w ? tint(y.cph || 0) : '--',
    w ? tint(y.one_time_per_hour || 0) : '--', w ? tint(whole(y)) : '--'];
  panel.append(fitTable(table(['Division', 'Working', 'Steady income', 'Running costs', 'Steady net', 'Paid once', 'Net / h'],
    order.map(([d, adm]) => {
      const x = div[d] || {}, y = dw[d] || {}, name = el('span', null, d);
      name.style.color = DIV[d] || DIV.Unassigned; name.title = adm ? 'Admiral ' + adm : '';
      return moneyRow(name, fmt(x.working) + ' / ' + fmt(x.ships), y);
    }).concat(w && w.treasury_own_per_hour !== undefined ? [['Treasury, own', '', '', '', '', '', tint(w.treasury_own_per_hour)]] : [])
      .concat([moneyRow(el('b', null, 'Fleet'), fmt(t.working) + ' / ' + fmt(t.ships), w || {}).map((cell, i) => (i === 6 && w ? tint(purseNet(w)) : cell))]), [1, 2, 3, 4, 5, 6])));
  panel.append(el('p', 'sub', 'Per hour. Steady net = steady income - running costs. Net = steady net + paid once: what the division\'s wallets changed by, '
    + 'gifts between our own ships and deposits into the treasury left out. The fleet\'s net adds the treasury\'s own line: the divisions and the treasury add up to it.'));
  const ops = await opsOf();
  if (!live()) return;
  if (ops) {
    panel.append(el('h3', null, 'Fleet readiness & bottlenecks'));
    const rgrid = el('div', 'kpis');
    const rkpi = (k, v, sub, cls) => { const b = el('div', 'kpi' + (cls ? ' ' + cls : '')); b.append(el('div', 'k', k), el('div', 'v', v)); if (sub) b.append(el('div', 's', sub)); rgrid.append(b); };
    const bs = ops.balance_sheet || null;
    if (bs) {
      panel.insertBefore(el('h3', null, 'Consolidated balance sheet & enterprise net worth'), panel.lastChild);
      const bgrid = el('div', 'kpis');
      const bkpi = (k, v, sub, cls) => { const d = el('div', 'kpi' + (cls ? ' ' + cls : '')); d.append(el('div', 'k', k), el('div', 'v', v)); if (sub) d.append(el('div', 's', sub)); bgrid.append(d); };
      bkpi('Enterprise net worth', fmtCompact(bs.net_worth) + ' cr', fmtCompact(Math.round(bs.net_worth / Math.max(1, t.ships || 246))) + ' / ship (cash + vaults + ships + bases)', 'main pos');
      bkpi('Liquid purse', fmtCompact(bs.liquid_cash) + ' cr', 'wallets ' + fmtCompact(bs.wallets) + ' + treasury ' + fmtCompact(bs.treasury), 'pos');
      bkpi('Vault stock @ bid', fmtCompact(bs.vault_worth) + ' cr', bs.handed_over_24h ? '24h handed over: ' + fmtCompact(bs.handed_over_24h) + ' cr' : 'ores, refined parts & hunt loot stored', 'pos');
      bkpi('Fleet & facilities', fmtCompact((bs.fleet_book || 0) + (bs.facility_invested || 0)) + ' cr', 'ships/fits ' + fmtCompact(bs.fleet_book) + ' + facilities ' + fmtCompact(bs.facility_invested), '');
      panel.insertBefore(bgrid, panel.lastChild);
    }
    const fac = (ops.readiness || {}).faction || {};
    const capPct = fac.limit ? Math.round((fac.members / fac.limit) * 100) : 0;
    const nextSeatBldg = !fac.limit ? 'not read' : fac.limit < 100 ? 'next: Recruitment Desk (100)' : fac.limit < 200 ? 'next: Recruitment Center (200)' : fac.limit < 400 ? 'next: Guild Hall Recruiting (400)' : fac.limit < 1000 ? 'next: Grand Recruitment Bureau (1,000)' : 'multi-station +25% offices';
    rkpi('Faction seats', fac.limit ? fmt(fac.members) + ' / ' + fmt(fac.limit) : '--',
      fac.limit ? (fac.members >= fac.limit - 2 ? 'at cap -- ' + nextSeatBldg : (fac.limit - fac.members) + ' open (' + nextSeatBldg + ')') : 'not read',
      capPct >= 95 ? 'warn' : 'pos');
    const tf = ops.tech_frontier || {};
    const hulls = (ops.readiness || {}).hulls || [];
    const byTier = new Map();
    hulls.forEach((h) => byTier.set(h.tier, (byTier.get(h.tier) || 0) + h.count));
    const tierTxt = [...byTier.entries()].sort((x, y) => y[0] - x[0]).map(([tr, n]) => fmt(n) + ' T' + tr).join(', ') || '--';
    const ftTier = tf.target_tier || 2;
    rkpi('Active hull frontier: T' + ftTier, tf.ready_pilots !== undefined ? fmt(tf.at_or_above || 0) + ' / ' + fmt(tf.ready_pilots) + ' T' + ftTier + '+' : tierTxt,
      'Piloting avg ' + (tf.avg_piloting || '--') + ' / max ' + (tf.max_piloting || '--') + ' | ' + tierTxt + ' | next: ' + (tf.next_milestone || ''),
      (tf.ready_pilots || 0) > (tf.at_or_above || 0) ? 'warn' : 'pos');
    const mods = (ops.readiness || {}).modules || [];
    rkpi('Advanced modules (T2-T5)', mods.length ? fmt(mods.reduce((acc, m) => acc + m.count, 0)) + ' fitted' : '0',
      mods.length ? mods.slice(0, 3).map((m) => m.name + ': ' + m.count).join(', ') : 'no T2+ modules fitted yet', mods.length ? 'pos' : 'warn');
    const eff = ops.efficiency || null;
    if (eff) {
      const jl = eff.jump_loops || { hours: 0, credits: 0 }, cn = eff.census || { hours: 0, credits: 0 };
      rkpi('24h flight efficiency', (eff.productive_pct || 0) + '% productive',
        'jump loops: ' + jl.hours + 'h (' + fmtCompact(jl.credits) + ' cr) | census: ' + cn.hours + 'h (' + fmtCompact(cn.credits) + ' cr)',
        (eff.productive_pct || 0) < 65 ? 'warn' : 'pos');
    }
    const bw = ops.birth_wave || null;
    if (bw) {
      rkpi('Next birth rollout: Wave ' + bw.wave, (t.ships || 246) + ' -> ' + bw.target + ' (+' + bw.add_ships + ')',
        'gate: ' + bw.gate, '');
    }
    const fr = ops.freshness || {};
    const frCls = fr.max_s < 0 ? '' : fr.max_s <= 35 ? 'pos' : fr.max_s <= 90 ? 'warn' : 'neg';
    rkpi('Pilot tick & services', fr.ships ? fr.median_s + 's med / p95 ' + fr.p95_s + 's' : '--',
      ((ops.services || {}).running || 0) + '/' + ((ops.services || {}).total || 10) + ' services up | ' + fmt(ops.contracts_count || 0) + ' contracts logged', frCls);
    panel.append(rgrid);

    const mad = (ops.alerts && ops.alerts.mad) || [], raids = (ops.alerts && ops.alerts.battles) || [];
    panel.append(el('h3', null, 'Alerts & anomalies'));
    if (mad.length || raids.length) {
      if (mad.length) {
        panel.append(fitTable(table(['Figure', 'Verdict', 'Detail'],
          mad.map((m) => [m.figure, el('span', 'pill ' + (m.verdict.includes('LOW') || m.verdict.includes('HIGH') ? 'bad' : 'warn'), m.verdict), m.detail]))));
      }
      if (raids.length) {
        panel.append(fitTable(table(['System', 'Kind', 'Status', 'Lost', 'Factions'],
          raids.map((b) => [sys.has(b.system) ? sysLink(b.system) : b.system_name, b.category, b.status, fmt(b.destroyed), (b.tags || []).join(', ') || '--']), [3])));
      }
    } else {
      panel.append(el('p', 'empty', 'No statistical anomalies (MAD) or active non-pirate battles.'));
    }

    if (F.ships.length) {
      const strip = el('div', 'compbar');
      strip.append(divMeter(F.ships));
      panel.append(strip);
    }

    const sup = ops.supply || [];
    if (sup.length) {
      panel.append(el('h3', null, 'Supply chains'));
      panel.append(fitTable(table(['Chain', 'Item', 'Place', 'Have / Keep', 'Hours', 'State'],
        sup.map((x) => {
          const stCls = x.state === 'OK' ? 'good' : x.state === 'LOW' ? 'warn' : 'bad';
          const cell = el('div', 'progcell');
          cell.append(el('span', null, fmt(x.have) + ' / ' + fmt(x.keep)));
          if (x.keep > 0) cell.append(pbar(x.have, x.keep, stCls));
          return [x.chain, x.item, x.place, cell, x.hours === null ? '--' : x.hours + 'h', el('span', 'pill ' + stCls, x.state)];
        }), [4])));
    }

    const needs = ops.needs || [];
    if (needs.length) {
      panel.append(el('h3', null, 'Open priority needs'));
      panel.append(fitTable(table(['P', 'Need', 'Owner', 'Covered', 'Missing / Fee'],
        needs.map((n) => {
          const stCls = n.colour === 'green' ? 'good' : n.colour === 'red' ? 'bad' : 'warn';
          const gap = n.stocked ? 'standing reserve stocked' : ([n.short, n.fee ? fmt(n.fee) + ' cr fee' : ''].filter(Boolean).join(' | ') || 'ready to build');
          const cov = el('div', 'progcell');
          cov.append(el('span', 'pill ' + stCls, n.stocked ? 'STOCKED' : n.pct + '%'), pbar(n.pct, 100, stCls));
          return [n.priority, n.id, n.owner, cov, gap];
        }))));
    }

    const reqs = ops.requests || [];
    if (reqs.length) {
      panel.append(el('h3', null, 'Active division requests (' + reqs.length + ' open / accepted)'));
      panel.append(fitTable(table(['State', 'Entry', 'Route', 'Updated', 'Summary'],
        reqs.slice(0, 12).map((r) => [
          el('span', 'pill ' + (r.state === 'OPEN' ? 'warn' : 'info'), r.state),
          linkButton(r.ent, () => openDoc('communications/requests.log'), 'doclink'),
          r.by + ' -> ' + r.to,
          stampCet(r.when),
          r.need + (r.answer ? ' [' + r.answer + ']' : ''),
        ]))));
    }
  }
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

function fmtCompact(n) {
  const v = Number(n || 0);
  if (Math.abs(v) >= 1e9) return (v / 1e9).toFixed(2) + 'B';
  if (Math.abs(v) >= 1e6) return (v / 1e6).toFixed(2) + 'M';
  if (Math.abs(v) >= 1e4) return (v / 1e3).toFixed(1) + 'k';
  return fmt(v);
}

function relPowerPill(rel) {
  const map = {
    US: ['good', 'OUR EMPIRE'],
    Overwhelming: ['bad', 'OVERWHELMING'],
    Superior: ['warn', 'SUPERIOR'],
    Equivalent: ['info', 'EQUIVALENT'],
    Inferior: ['good', 'INFERIOR'],
    Pathetic: ['', 'PATHETIC'],
  };
  const [cls, lbl] = map[rel] || ['', rel || '--'];
  return el('span', 'pill ' + cls, lbl);
}

async function renderEmpire(panel, live) {
  const [ops, inv, dip] = await Promise.all([opsOf(), inventoryOf(), diploOf()]);
  if (!live()) return;
  const emp = (ops && ops.empire) || { rent: {}, buildings: [], sites: [] };
  const fac = (ops && ops.readiness && ops.readiness.faction) || {};
  const bldgs = emp.buildings.length ? emp.buildings : ((S && S.holdings && S.holdings.buildings) || []);
  const our = (dip && dip.our) || {};
  const ranks = our.ranks || {};

  panel.append(el('h2', null, 'Empire, Diplomacy & Galactic Standings'));
  panel.append(el('p', 'sub', 'Grand-strategy command ledger: sovereign bases & buildings, galactic rival rankings, alliance blocs, active wars and external comms.'));

  const subBar = el('div', 'subtabs');
  const commsSum = (dip && dip.comms && dip.comms.summary) || {};
  const subDefs = [
    ['Infrastructure', 'Infrastructure (' + bldgs.length + ')'],
    ['Rivals', 'Rivals & Rankings (' + ((dip && dip.total_factions) || 0) + ')'],
    ['Diplomacy', 'Diplomacy & Wars (' + (((dip && dip.alliances) || []).length) + ' blocs)'],
    ['Comms', 'Comms & Hails (' + ((commsSum.direct_human_in || 0) + '/' + (commsSum.local_human || 0)) + ')'],
  ];
  for (const [id, label] of subDefs) {
    const b = el('button', 'subtab' + (empSub === id ? ' on' : ''), label);
    b.type = 'button';
    b.addEventListener('click', () => { empSub = id; render(); });
    subBar.append(b);
  }
  panel.append(subBar);

  if (empSub === 'Rivals') {
    renderEmpireRivals(panel, dip);
    return;
  }
  if (empSub === 'Diplomacy') {
    renderEmpireDiplomacy(panel, dip);
    return;
  }
  if (empSub === 'Comms') {
    renderEmpireComms(panel, dip);
    return;
  }

  // ---- Sub-tab 1: Infrastructure & Fleet Hulls ----
  const outposts = bldgs.filter((b) => b.kind === 'outpost'), stations = bldgs.filter((b) => b.kind === 'station');
  const facOnly = bldgs.filter((b) => b.kind !== 'outpost' && b.kind !== 'station');
  const bySys = new Map();
  for (const b of bldgs) { if (!bySys.has(b.system)) bySys.set(b.system, []); bySys.get(b.system).push(b); }

  const kgrid = el('div', 'kpis');
  const ekpi = (k, v, sub, cls) => { const d = el('div', 'kpi' + (cls ? ' ' + cls : '')); d.append(el('div', 'k', k), el('div', 'v', v)); if (sub) d.append(el('div', 's', sub)); kgrid.append(d); };
  ekpi('Sovereign bases', outposts.length + ' / 8 outposts', stations.length + ' / 5 player stations built', outposts.length || stations.length ? 'main pos' : '');
  ekpi('Station buildings', fmt(facOnly.length) + ' active', 'across ' + bySys.size + ' star systems', 'pos');
  const seatsOpen = Math.max(0, (fac.limit || 0) - (fac.members || 0));
  ekpi('Faction seats', fac.limit ? fmt(fac.members) + ' / ' + fmt(fac.limit) : '--',
    seatsOpen ? seatsOpen + ' open seats (Recruitment Center active)' : 'at seat cap', seatsOpen ? 'pos' : 'warn');
  ekpi('Facility rent / day', fmt((emp.rent && emp.rent.per_day) || 0) + ' cr',
    fmt((emp.rent && emp.rent.per_cycle) || 0) + ' cr/cycle at NPC stations (0 on our bases)', '');
  panel.append(kgrid);

  if (our.hulls && our.hulls.length) {
    panel.append(el('h3', null, 'Active fleet hull lineage (' + fmt(our.fleet_ships || 246) + ' ships -- multi-empire 500/600 rollout in Docs -> Birth plans)'));
    panel.append(fitTable(table(['Hull class', 'Design empire', 'Tier', 'Role category', 'Ships'],
      our.hulls.map((h) => [
        h.class,
        el('span', 'pill ' + (h.empire === 'voidborn' ? 'good' : 'warn'), h.empire),
        'T' + h.tier,
        h.category || '--',
        fmt(h.count),
      ]), [4])));
  }

  panel.append(el('h3', null, 'Where our buildings stand (' + bySys.size + ' systems)'));
  if (!bySys.size) {
    panel.append(el('p', 'empty', 'No bases or buildings recorded yet.'));
  } else {
    const cards = el('div', 'icards');
    const orderedSys = [...bySys.entries()].sort((a, b) => {
      const aBase = a[1].some((x) => x.kind === 'outpost' || x.kind === 'station') ? 0 : 1;
      const bBase = b[1].some((x) => x.kind === 'outpost' || x.kind === 'station') ? 0 : 1;
      return aBase - bBase || b[1].length - a[1].length;
    });
    for (const [sid, list] of orderedSys) {
      const sObj = sys.get(sid) || { name: sid, empire: '' };
      const hasOwnBase = list.some((x) => x.kind === 'outpost' || x.kind === 'station');
      const card = el('div', 'icard' + (hasOwnBase ? ' ownbase' : ''));
      const head = el('div', 'ichead');
      const goBtn = el('button', 'sysjump', sObj.name || sid);
      goBtn.type = 'button';
      goBtn.addEventListener('click', () => { select(sid, true); });
      const zone = sObj.empire ? sObj.empire + ' space' : 'lawless frontier';
      const shipsHere = (shipsBy.get(sid) || []).length;
      const baseIds = new Set(list.map((b) => b.base).filter(Boolean));
      const stNames = new Set((stationsBy.get(sid) || []).map((t) => t.name));
      const worthHere = inv ? inv.stations.filter((x) => stNames.has(x.name) || baseIds.has(x.base)).reduce((a, x) => a + (x.worth || 0), 0) : 0;
      head.append(goBtn, el('span', 'pill ' + (hasOwnBase ? 'good' : ''), hasOwnBase ? 'OUR BASE' : 'NPC STATION'));
      card.append(head);
      card.append(el('div', 'icsub', zone + ' | ' + shipsHere + ' ships here' + (worthHere ? ' | ~' + fmt(worthHere) + ' cr stored' : '')));
      const blist = el('div', 'iblist');
      for (const b of list) {
        const ok = stands(b), row = el('div', 'ibldg');
        const bh = el('div', 'ibhead');
        bh.append(glyphSvg(b.kind || 'office', ok ? BUILT : RAISING, 15), el('b', null, b.name));
        bh.append(el('span', 'pill ' + (ok ? 'good' : 'warn'), (b.status || 'active').replace(/_/g, ' ')));
        row.append(bh);
        const details = [];
        if (b.at && b.at !== 'our own base' && !b.part) details.push('at ' + b.at);
        if (b.part && b.at) details.push('inside ' + b.at);
        if (b.purpose) details.push(b.purpose);
        if (b.fuel !== null && b.fuel !== undefined) details.push('bunker: ' + fmt(b.fuel) + ' / 50,000 fuel');
        if (b.rent) details.push('rent: ' + fmt(b.rent) + ' cr/cycle');
        else details.push('0 cr rent');
        row.append(el('div', 'ibsub', details.join(' | ')));
        blist.append(row);
      }
      card.append(blist);
      cards.append(card);
    }
    panel.append(cards);
  }

  const sites = (emp.sites || []).filter((x) => x.status !== 'built' && x.status !== 'dropped');
  const chosenSites = sites.filter((x) => x.status === 'chosen');
  const candSites = sites.filter((x) => x.status !== 'chosen');

  if (chosenSites.length) {
    panel.append(el('h3', null, 'Next chosen build sites (' + chosenSites.length + ')'));
    const cwrap = el('div', 'icards');
    for (const st of chosenSites) {
      const sObj = sys.get(st.system) || { name: st.system };
      const card = el('div', 'icard sitecard');
      const ch = el('div', 'ichead');
      const goBtn = el('button', 'sysjump', sObj.name || st.system);
      goBtn.type = 'button';
      goBtn.addEventListener('click', () => { select(st.system, true); });
      ch.append(glyphSvg('flag', '#e8c35a', 15), goBtn, el('span', 'pill warn', st.need_pct !== null && st.need_pct !== undefined ? 'CHOSEN - ' + st.need_pct + '%' : 'CHOSEN'));
      card.append(ch);
      if (st.need_pct !== null && st.need_pct !== undefined) {
        card.append(el('div', 'ibsub', 'Supply progress (' + st.need_id + '): ' + st.need_pct + '% stocked -- turns green on the map automatically once deployed'), pbar(st.need_pct, 100, st.need_pct >= 99 ? 'good' : 'warn'));
      } else {
        card.append(el('div', 'ibsub', 'Queued after active priority builds -- turns green on the map automatically once deployed'));
      }
      if (st.note) card.append(el('div', 'ibsub', st.note));
      cwrap.append(card);
    }
    panel.append(cwrap);
  }

  if (candSites.length) {
    panel.append(el('h3', null, 'Candidate station & frontier sites (' + candSites.length + ')'));
    panel.append(fitTable(table(['System', 'Proposed by', 'Readiness', 'Strategic note'],
      candSites.map((st) => {
        const sObj = sys.get(st.system);
        const link = sObj ? sysLink(st.system) : st.system;
        const rdy = st.need_pct !== null && st.need_pct !== undefined ? el('span', 'pill warn', st.need_pct + '%') : '--';
        return [link, st.by || '--', rdy, (st.note || '').slice(0, 140)];
      }))));
  }
}

function renderEmpireRivals(panel, dip) {
  if (!dip) { panel.append(el('p', 'empty', 'Loading galactic faction intelligence...')); return; }
  const our = dip.our || {}, ranks = our.ranks || {}, list = [...(dip.rivals || [])];
  const topWealth = list.reduce((m, r) => (r.wealth > (m ? m.wealth : 0) ? r : m), null);

  const kgrid = el('div', 'kpis');
  const ekpi = (k, v, sub, cls) => { const d = el('div', 'kpi' + (cls ? ' ' + cls : '')); d.append(el('div', 'k', k), el('div', 'v', v)); if (sub) d.append(el('div', 's', sub)); kgrid.append(d); };
  ekpi('Our galactic ranks',
    'Members #' + (ranks.member_count || '--') + ' | Dmg #' + (ranks.damage_dealt || '--'),
    'Facilities #' + (ranks.facility_investment || '--') + ' | Missions #' + (ranks.missions_completed || '--') + ' of ' + fmt(dip.total_factions) + ' factions',
    'main pos');
  ekpi('#1 Galactic superpower',
    topWealth ? '[' + topWealth.tag + '] ' + fmtCompact(topWealth.wealth) + ' cr' : '--',
    topWealth ? topWealth.name + ' (' + fmt(topWealth.members) + ' members, ' + topWealth.bases + ' bases)' : '',
    'warn');
  ekpi('Our tech & pilot level',
    'Max Lv ' + (our.max_piloting || 0) + ' (Avg ' + (our.avg_piloting || 0) + ')',
    'T2 unlocked | Voidborn >=1: ' + fmt(our.voidborn_skilled || 0) + '/' + fmt(our.fleet_ships || 246),
    'pos');
  ekpi('Head-start clock',
    '7 days old',
    fmt(our.fleet_ships || 246) + ' ships built vs rivals 60-280d old',
    'pos');
  panel.append(kgrid);

  const sortBar = el('div', 'sortbar');
  sortBar.append(el('span', 'sortlbl', 'Rank ledger by:'));
  const sorts = [
    ['wealth', 'Wealth / Earned'],
    ['members', 'Members'],
    ['bases', 'Sovereign Bases'],
    ['kills', 'Combat Kills'],
    ['tech', 'Observed Tech / Lv'],
  ];
  for (const [sid, slbl] of sorts) {
    const b = el('button', 'rf' + (empSort === sid ? ' on' : ''), slbl);
    b.type = 'button';
    b.addEventListener('click', () => { empSort = sid; render(); });
    sortBar.append(b);
  }
  if (rivalFocus) {
    const clr = el('button', 'rf haswarn', 'Clear map overlay [' + rivalFocus.tag + ']');
    clr.type = 'button';
    clr.addEventListener('click', () => { rivalFocus = null; renderAlerts(); draw(); render(); });
    sortBar.append(clr);
  }
  panel.append(sortBar);

  const cmp = {
    wealth: (a, b) => b.wealth - a.wealth || b.members - a.members,
    members: (a, b) => b.members - a.members || b.wealth - a.wealth,
    bases: (a, b) => b.bases - a.bases || b.wealth - a.wealth,
    kills: (a, b) => b.kills - a.kills || b.kills_pvp - a.kills_pvp,
    tech: (a, b) => b.max_tier - a.max_tier || b.avg_tier - a.avg_tier || b.sighted - a.sighted,
  }[empSort] || ((a, b) => b.wealth - a.wealth);
  list.sort(cmp);

  const tbl = el('table', 'mtable rival-table');
  const thead = el('thead'), trH = el('tr');
  ['#', 'Faction', 'Rel. Power', 'Members', 'Bases', 'Wealth / Earned', 'Obs. Hull / Lv', 'Kills', 'Age', 'Map'].forEach((h, idx) => {
    const th = el('th', [3, 4, 5, 7, 8].includes(idx) ? 'num' : null, h);
    trH.append(th);
  });
  thead.append(trH);
  tbl.append(thead);

  const tbody = el('tbody');
  list.slice(0, 35).forEach((r, idx) => {
    const tr = el('tr', r.tag === 'CLTV' ? 'us-row' : (rivalFocus && rivalFocus.tag === r.tag ? 'focus-row' : null));
    tr.append(el('td', 'mono', String(idx + 1)));

    const fCell = el('td');
    const fTop = el('div', 'rname');
    fTop.append(el('span', 'rtag', '[' + r.tag + ']'), ' ', el('b', null, r.name));
    fCell.append(fTop);
    const metaBits = [];
    if (r.empire && r.empire !== '--') metaBits.push(r.empire);
    if (r.allies && r.allies.length) metaBits.push('allies: ' + r.allies.slice(0, 4).join(',') + (r.allies.length > 4 ? '+' + (r.allies.length - 4) : ''));
    if (r.wars && r.wars.length) metaBits.push('AT WAR: ' + r.wars.join(','));
    if (metaBits.length) fCell.append(el('div', 'rmeta-sub', metaBits.join(' | ')));
    tr.append(fCell);

    const pCell = el('td');
    pCell.append(relPowerPill(r.rel_power));
    tr.append(pCell);

    const mTxt = r.tag === 'CLTV' && r.fleet_ships ? fmt(r.members) + ' (' + fmt(r.fleet_ships) + ')' : fmt(r.members);
    tr.append(el('td', 'num', mTxt));
    tr.append(el('td', 'num', r.bases ? fmt(r.bases) : '--'));

    const wCell = el('td', 'num');
    wCell.append(el('div', null, fmtCompact(r.wealth) + ' cr'));
    wCell.append(el('div', 'rmeta-sub', r.wealth_src === 'net_worth' ? 'net worth' : r.wealth_src === 'purse' ? 'live purse' : 'lifetime earned'));
    tr.append(wCell);

    const tCell = el('td');
    if (r.tag === 'CLTV') {
      tCell.append(el('div', 'mono', 'T' + r.max_tier + ' | Lv ' + r.est_piloting));
      tCell.append(el('div', 'rmeta-sub', 'avg Lv ' + (r.avg_piloting || 0)));
    } else if (r.sighted > 0) {
      tCell.append(el('div', 'mono', 'Max T' + r.max_tier + ' / Avg ' + r.avg_tier.toFixed(1)));
      tCell.append(el('div', 'rmeta-sub', 'Lv ' + r.est_piloting + '+ (' + fmt(r.sighted) + ' seen)'));
    } else {
      tCell.append(el('span', 'rmeta-sub', 'unsighted'));
    }
    tr.append(tCell);

    const kCell = el('td', 'num');
    kCell.append(el('div', null, fmtCompact(r.kills)));
    if (r.kills_pvp > 0) kCell.append(el('div', 'rmeta-sub', fmt(r.kills_pvp) + ' PvP'));
    tr.append(kCell);

    tr.append(el('td', 'num', r.age_days ? r.age_days + 'd' : '--'));

    const mapCell = el('td');
    const hasMap = (r.base_systems && r.base_systems.length) || (r.sight_systems && r.sight_systems.length);
    if (hasMap) {
      const isOn = rivalFocus && rivalFocus.tag === r.tag;
      const mBtn = el('button', 'maploc' + (isOn ? ' on' : ''), isOn ? 'Shown' : 'Locate');
      mBtn.type = 'button';
      mBtn.title = 'Highlight ' + r.name + ' bases and sighted fleets on the Galaxy Map';
      mBtn.addEventListener('click', () => {
        if (rivalFocus && rivalFocus.tag === r.tag) { rivalFocus = null; renderAlerts(); draw(); render(); }
        else { focusRivalOnMap(r.tag, r.name, r.base_systems, r.sight_systems); render(); }
      });
      mapCell.append(mBtn);
    } else {
      mapCell.append(el('span', 'rmeta-sub', '--'));
    }
    tr.append(mapCell);
    tbody.append(tr);
  });
  tbl.append(tbody);
  panel.append(fitTable(tbl));
}

function renderEmpireDiplomacy(panel, dip) {
  if (!dip) { panel.append(el('p', 'empty', 'Loading diplomatic intelligence...')); return; }
  const our = dip.our || {};
  const alliances = dip.alliances || [], wars = dip.wars || [], rivalries = dip.rivalries || [], battles = dip.battles || [];

  const kgrid = el('div', 'kpis');
  const ekpi = (k, v, sub, cls) => { const d = el('div', 'kpi' + (cls ? ' ' + cls : '')); d.append(el('div', 'k', k), el('div', 'v', v)); if (sub) d.append(el('div', 's', sub)); kgrid.append(d); };
  ekpi('Our posture', our.at_war ? 'AT WAR' : 'Armed Neutrality', 'Never fire first; diplomacy & war Suggi-reserved', our.at_war ? 'neg' : 'main pos');
  ekpi('Our treaties & wars', (our.allies || []).length + ' allies | ' + (our.wars || []).length + ' wars', (our.enemies || []).length + ' marked enemies', 'pos');
  ekpi('Galactic alliance blocs', fmt(alliances.length) + ' coalitions', 'multi-faction mutual defense / trade blocs', '');
  ekpi('Active wars & rivalries', fmt(wars.length) + ' wars | ' + fmt(rivalries.length) + ' feuds', fmt(battles.length) + ' recent combat engagements logged', wars.length ? 'warn' : '');
  panel.append(kgrid);

  panel.append(el('h3', null, 'Major galactic alliance blocs & federations (' + alliances.length + ')'));
  if (!alliances.length) {
    panel.append(el('p', 'empty', 'No multi-faction alliances declared in the public registry.'));
  } else {
    const cards = el('div', 'icards');
    for (const bloc of alliances.slice(0, 12)) {
      const card = el('div', 'icard');
      const head = el('div', 'ichead');
      head.append(el('b', null, bloc.lead_name + ' Coalition (' + bloc.factions.length + ' factions)'));
      if ((bloc.base_systems && bloc.base_systems.length) || (bloc.sight_systems && bloc.sight_systems.length)) {
        const lBtn = el('button', 'maploc', 'Show bloc on map');
        lBtn.type = 'button';
        lBtn.addEventListener('click', () => {
          focusRivalOnMap(bloc.lead_tag + '+', bloc.lead_name + ' Coalition', bloc.base_systems, bloc.sight_systems);
        });
        head.append(lBtn);
      }
      head.append(el('span', 'pill warn', fmt(bloc.total_members) + ' pilots | ' + bloc.total_bases + ' bases'));
      card.append(head);
      card.append(el('div', 'icsub', 'Combined wealth / earned: ~' + fmtCompact(bloc.total_wealth) + ' cr'));
      const tagsWrap = el('div', 'bloc-members');
      for (const m of bloc.factions) {
        tagsWrap.append(el('span', 'pill', '[' + m.tag + '] ' + m.name + ' (' + m.members + (m.bases ? ', ' + m.bases + 'b' : '') + ')'));
      }
      card.append(tagsWrap);
      cards.append(card);
    }
    panel.append(cards);
  }

  panel.append(el('h3', null, 'Declared faction wars & hostile markings'));
  if (!wars.length && !rivalries.length) {
    panel.append(el('p', 'empty', 'Zero formal faction-vs-faction wars or enemy markings active in the current feed.'));
  } else {
    const wrows = [];
    for (const w of wars) {
      wrows.push([el('span', 'pill bad', 'ACTIVE WAR'), '[' + w.a_tag + '] ' + w.a_name + ' (' + w.a_members + ')', '[' + w.b_tag + '] ' + w.b_name + ' (' + w.b_members + ')']);
    }
    for (const rv of rivalries) {
      wrows.push([el('span', 'pill warn', 'ENEMY MARK'), '[' + rv.from_tag + '] ' + rv.from_name, '[' + rv.to_tag + '] ' + rv.to_name + ' (' + rv.to_members + ')']);
    }
    panel.append(fitTable(table(['State', 'Side A', 'Side B'], wrows)));
  }

  if (battles.length) {
    panel.append(el('h3', null, 'Recent galaxy combat feed (' + battles.length + ')'));
    panel.append(fitTable(table(['System', 'Type', 'State', 'Factions', 'Kills', 'Belligerents'],
      battles.slice(0, 15).map((b) => [
        sys.has(b.system) ? sysLink(b.system) : (b.system_name || b.system),
        b.category || 'combat',
        el('span', 'pill ' + (b.status === 'active' ? 'bad' : ''), b.status || '--'),
        b.tags || '--',
        fmt(b.destroyed || 0),
        (b.pilots || '').slice(0, 56),
      ]), [4])));
  }
}

function renderEmpireComms(panel, dip) {
  if (!dip || !dip.comms) { panel.append(el('p', 'empty', 'Loading communications ledger...')); return; }
  const c = dip.comms, s = c.summary || {};

  const kgrid = el('div', 'kpis');
  const ekpi = (k, v, sub, cls) => { const d = el('div', 'kpi' + (cls ? ' ' + cls : '')); d.append(el('div', 'k', k), el('div', 'v', v)); if (sub) d.append(el('div', 's', sub)); kgrid.append(d); };
  ekpi('Player hails to us', fmt(s.direct_human_in || 0), 'private DMs or @CLTV mentions from real players', s.direct_human_in ? 'warn' : 'main pos');
  ekpi('Sent by our fleet', fmt(s.sent_by_us || 0), 'Rule F4 radio silence holds (Suggi-only outbound)', s.sent_by_us ? 'warn' : 'pos');
  ekpi('Local pilot radio', fmt(s.local_human || 0), 'unique human messages heard near our ships', '');
  ekpi('Comms firewall', 'CaMeL + Nonce', 'prompt-injection quarantine active (Rule F4) + contracts.log', 'pos');
  panel.append(kgrid);

  panel.append(el('h3', null, 'Direct diplomatic hails -- received from & sent to players'));
  if (!(c.direct_in || []).length && !(c.sent_out || []).length) {
    panel.append(el('p', 'empty', 'Zero human private hails received and zero outbound player messages sent so far (' + fmt(s.total_logged || 0) + ' total radio frames audited by inbox service). Any player DM or @CLTV mention will surface here immediately.'));
  } else {
    const drows = [];
    for (const m of (c.sent_out || [])) {
      drows.push([el('span', 'pill warn', 'SENT'), stampCet(m.t), (m.tag ? '[' + m.tag + '] ' : '') + m.sender, m.channel, m.text]);
    }
    for (const m of (c.direct_in || [])) {
      drows.push([el('span', 'pill good', 'RECEIVED'), stampCet(m.t), (m.tag ? '[' + m.tag + '] ' : '') + m.sender, m.channel, m.text]);
    }
    panel.append(fitTable(table(['Dir', 'When', 'Pilot', 'Channel', 'Message'], drows)));
  }

  panel.append(el('h3', null, 'Intercepted nearby pilot radio (' + (c.local_radio || []).length + ' newest)'));
  if (!(c.local_radio || []).length) {
    panel.append(el('p', 'empty', 'No nearby human local radio captured yet.'));
  } else {
    const feedWrap = el('div', 'icards');
    for (const m of (c.local_radio || []).slice(0, 25)) {
      const card = el('div', 'ibldg');
      const bh = el('div', 'ibhead');
      if (m.tag) bh.append(el('span', 'rtag', '[' + m.tag + ']'));
      bh.append(el('b', null, m.sender || 'Unknown'));
      if (m.system && sys.has(m.system)) bh.append(' in ', sysLink(m.system));
      else if (m.system) bh.append(el('span', 'rmeta-sub', ' in ' + m.system));
      bh.append(el('span', 'pill', (m.channel || 'local').toUpperCase()));
      card.append(bh);
      card.append(el('div', 'msg-body', m.text));
      card.append(el('div', 'rmeta-sub', stampCet(m.t) + (m.poi ? ' | ' + m.poi : '')));
      feedWrap.append(card);
    }
    panel.append(feedWrap);
  }

  if ((c.npc_notices || []).length) {
    panel.append(el('h3', null, 'Station & authority dispatches to our ships (' + c.npc_notices.length + ' newest)'));
    panel.append(fitTable(table(['When', 'Authority', 'Notice'],
      c.npc_notices.slice(0, 12).map((m) => [stampCet(m.t), m.sender, m.text]))));
  }
}

const TABS = { Selection: renderSelection, Empire: renderEmpire, Metrics: renderMetrics, Inventory: renderInventory, Docs: renderDocs };
let renderSeq = 0, viewKey = '';
function render() {
  const panel = $('panel'), mine = ++renderSeq, live = () => mine === renderSeq;
  const key = [tab, selShip, selShip ? '' : selected, pilotCard ? pilotCard.name : '', docView ? docView.path : '',
    tab === 'Inventory' ? invMode + '/' + (invItem || '') + '/' + invCat + '/' + invSort : '',
    tab === 'Empire' ? empSub + '/' + empSort + '/' + (rivalFocus ? rivalFocus.tag : '') : '',
    tab === 'Docs' && !docView ? docSub + '/' + docAuthor : ''].join('|');
  const same = key === viewKey, keep = same ? panel.scrollTop : 0;
  viewKey = key;
  document.querySelectorAll('nav button').forEach((b) => b.classList.toggle('on', b.textContent === tab));
  $('rail-right-label').textContent = tab;
  if (tab !== 'Docs') setWide(tab === 'Empire' || tab === 'Metrics' || tab === 'Inventory' ? 'metrics' : false);
  if (tab === 'Metrics' || tab === 'Empire') {
    const fn = TABS[tab];
    if (tab === 'Metrics') {
      metricsAt = Date.now();
      if (!same) routeOrder.key = '';              // the tab was opened anew: the routes are sorted afresh
    }
    if (same && panel.childElementCount) {         // a refresh of the open tab: built aside and swapped in whole, so the page keeps its height, its place and its order
      const aside = document.createDocumentFragment();
      Promise.resolve(fn(aside, live)).then(() => {
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
  if (OPS.data && OPS.data.freshness && OPS.data.freshness.ships) {
    const fr = OPS.data.freshness;
    const cls = fr.max_s <= 35 ? 'good' : fr.max_s <= 90 ? 'warn' : 'bad';
    item('Tick lag', fr.median_s + 's / ' + fr.max_s + 's', cls, cls === 'good' ? 'opt' : null);
    box.lastChild.title = 'Pilot state_at age across ' + fmt(fr.ships) + ' ships: median ' + fr.median_s + 's, p95 ' + fr.p95_s + 's, max ' + fr.max_s + 's';
  }
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
let chatTargets = new Set(['unity']);            // selected recipients when no explicit @Name is typed in chat-input

function markUnseen(n) {
  chat.unseen = n;
  for (const id of ['dock-unseen', 'pill-unseen']) {
    const u = $(id);
    if (u) { u.textContent = n ? n + ' new' : ''; u.hidden = !n; }
  }
}
const agentOf = (id) => ((S && S.roster) || []).find((a) => a.id === id) || { id, name: id, division: 'Command', rank: '' };

function applyChatMin() {
  const isMin = shut.has('chatmin');
  const dock = $('chat-dock'), pill = $('chat-pill');
  if (dock) dock.hidden = isMin;
  if (pill) pill.hidden = !isMin;
  const col = $('map-col');
  if (col && dock) col.style.setProperty('--dockh', isMin ? '42px' : dock.offsetHeight + 'px');
}

function setChatMin(min) {
  if (min) shut.add('chatmin'); else shut.delete('chatmin');
  saveShut();
  applyChatMin();
  if (!min) {
    markUnseen(0);
    const log = $('chat-log');
    if (log) log.scrollTop = log.scrollHeight;
  }
}

function openCommsFor(id) {                      // clicked from Top Bar or Fleet Outliner: unminimize Comms and focus this agent
  if (shut.has('chatmin')) setChatMin(false);
  chatTargets = new Set([id]);
  markWho();
  const inp = $('chat-input');
  if (inp) inp.focus();
}

function address(id) {                           // toggle 1, multiple, 5 Admirals, or All 6 recipients cleanly
  if (shut.has('chatmin')) setChatMin(false);
  const allIds = ((S && S.roster) || []).map((a) => a.id);
  const admIds = ((S && S.roster) || []).filter((a) => a.rank === 'Admiral').map((a) => a.id);
  if (id === 'all') {
    chatTargets = chatTargets.size === allIds.length ? new Set(['unity']) : new Set(allIds);
  } else if (id === 'admirals') {
    const allAdm = admIds.length > 0 && admIds.every((x) => chatTargets.has(x)) && chatTargets.size === admIds.length;
    chatTargets = allAdm ? new Set(['unity']) : new Set(admIds);
  } else {
    if (chatTargets.size === allIds.length) {
      chatTargets = new Set([id]);               // coming off All -> solo the clicked member
    } else if (chatTargets.has(id)) {
      chatTargets.delete(id);
      if (!chatTargets.size) chatTargets.add('unity');
    } else {
      chatTargets.add(id);
    }
  }
  markWho();
  const input = $('chat-input');
  if (input) input.focus();
}

function effectiveTargets(rawText) {             // explicit @mentions in text win; otherwise use selected chatTargets pills
  const roster = (S && S.roster) || [];
  const typed = (String(rawText || '').match(/@[A-Za-z]+/g) || []).map((s) => s.slice(1).toLowerCase());
  if (typed.length) {
    if (typed.some((n) => ['all', 'everyone', 'fleet'].includes(n))) return roster.map((a) => a.id);
    const out = [];
    for (const w of typed) {
      if (w === 'admirals') roster.filter((a) => a.rank === 'Admiral').forEach((a) => { if (!out.includes(a.id)) out.push(a.id); });
      else {
        const hit = roster.find((a) => a.id === w || a.name.toLowerCase() === w);
        if (hit && !out.includes(hit.id)) out.push(hit.id);
      }
    }
    if (out.length) return out;
  }
  return [...chatTargets];
}

function markWho() {
  const roster = (S && S.roster) || [];
  const input = $('chat-input');
  const activeIds = new Set(effectiveTargets(input ? input.value : ''));
  const allOn = roster.length > 0 && roster.every((a) => activeIds.has(a.id));
  const admIds = roster.filter((a) => a.rank === 'Admiral').map((a) => a.id);
  const admOn = !allOn && admIds.length > 0 && admIds.every((id) => activeIds.has(id)) && activeIds.size === admIds.length;
  const names = [];
  document.querySelectorAll('#chat-who button').forEach((b) => {
    const bid = b.dataset.id;
    if (bid === 'all') b.classList.toggle('on', allOn);
    else if (bid === 'admirals') b.classList.toggle('on', admOn);
    else {
      const on = activeIds.has(bid);
      b.classList.toggle('on', on);
      if (on) names.push(agentOf(bid).name);
    }
  });
  if (input) {
    const dest = allOn ? 'All 6 (Group)' : admOn ? 'All 5 Admirals' : names.join(' + ') || 'Unity';
    input.placeholder = 'Message -> ' + dest + '  (click portraits to toggle 1, several, Admirals or All; Enter sends)';
  }
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
  if (mine) head.append(el('b', null, 'Suggi'), el('span', 'to', ' -> ' + ((m.to || []).length >= 6 ? 'All 6' : (m.to || []).map((i) => agentOf(i).name).join(', ') || 'Unity')));
  else {
    const name = el('b', null, a.name), c = DIV[a.division] || DIV.Command;
    name.style.color = c; box.style.borderLeftColor = c;
    head.append(faceSvg(a.id, a.division, c, 18), name, el('span', null, ' ' + a.division));
  }
  head.append(el('span', 'when', clock((m.t || 0) * 1000)));
  box.append(head);
  const cleanTxt = mine ? String(m.text || '').replace(/^(?:@[A-Za-z]+\s+)+/, '') : m.text;
  if (mine || m.kind === 'error') box.append(el('div', 'msgtext', cleanTxt || m.text)); else box.append(markdown(m.text, '', false));
  log.append(box);
}

async function pollGroup() {
  clearTimeout(chat.timer);
  let d = null;
  try { d = await get('/api/group?after=' + chat.after); } catch (e) { d = null; }
  if (d && d.messages) {
    const log = $('chat-log'), stick = chat.first || log.scrollHeight - log.scrollTop - log.clientHeight < 80;
    d.messages.forEach((m) => { groupMessage(m); chat.after = Math.max(chat.after, m.n); });
    if (!chat.first && (shut.has('dock') || shut.has('chatmin'))) {
      markUnseen(chat.unseen + d.messages.filter((m) => m.who !== 'suggi').length);
    }
    if (chat.first && !log.children.length) {
      log.append(el('div', 'chathint', 'Direct & Group Command Channel. Toggle any combination of portraits below (1 agent, several, 5 Admirals, or All 6) and press Enter.'));
    }
    if (d.messages.length && stick) log.scrollTop = log.scrollHeight;
    chat.first = false;
    chat.busy = d.running.length > 0;
    const stateStr = d.running.map((r) => agentOf(r.agent).name + ' working (' + r.seconds + 's' + (r.tool ? ', ' + r.tool : '') + ')').join(' | ');
    $('chat-state').textContent = stateStr;
    const pSub = $('pill-sub');
    if (pSub) pSub.textContent = d.running.length ? d.running.length + ' answering...' : '6 agents';
    const pill = $('chat-pill');
    if (pill) pill.classList.toggle('busy', chat.busy);
    document.querySelectorAll('#chat-who button').forEach((b) => b.classList.toggle('busy', d.running.some((r) => r.agent === b.dataset.id)));
  }
  chat.timer = setTimeout(pollGroup, chat.busy ? 1500 : 5000);
}

async function sendGroup() {
  const input = $('chat-input'), raw = input.value.trim(), send = $('chat-send');
  if (!raw || send.disabled) return;
  const roster = (S && S.roster) || [];
  const hasExplicit = /@[A-Za-z]+/.test(raw);
  let payload = raw;
  if (!hasExplicit) {
    const ids = [...chatTargets];
    if (roster.length > 0 && ids.length === roster.length) payload = '@all ' + raw;
    else if (ids.length) payload = ids.map((i) => '@' + agentOf(i).name).join(' ') + ' ' + raw;
  }
  send.disabled = true;
  try {
    const d = await post('/api/group/send', { text: payload });
    input.value = '';
    markWho();
    if (shut.has('dock')) toggleShut('dock');     // pop open the message stream when sending so the reply is visible
    if (d.busy && d.busy.length) chatNote('Busy (still answering prior turn): ' + d.busy.map((i) => agentOf(i).name).join(', '));
  } catch (e) { chatNote('Not sent: ' + e.message); }
  send.disabled = false;
  pollGroup();
}

function initChat() {
  const who = $('chat-who');
  who.replaceChildren();
  const all = el('button', 'all', 'All 6');
  all.type = 'button'; all.dataset.id = 'all';
  all.title = 'Broadcast to Unity + all 5 Admirals (@all)';
  all.addEventListener('click', () => address('all'));
  who.append(all);

  const adms = el('button', 'all', '5 Adm');
  adms.type = 'button'; adms.dataset.id = 'admirals';
  adms.title = 'Message all 5 Division Admirals (@admirals)';
  adms.addEventListener('click', () => address('admirals'));
  who.append(adms);

  for (const a of S.roster) {
    const b = el('button', null), c = DIV[a.division] || DIV.Command;
    b.type = 'button'; b.dataset.id = a.id;
    b.style.setProperty('--c', c);
    b.append(faceSvg(a.id, a.division, c, 20), el('span', null, a.name));
    b.title = 'Toggle ' + a.name + ' (' + a.division + ') -- double-click to solo ' + a.name;
    b.addEventListener('click', () => address(a.id));
    b.addEventListener('dblclick', () => { chatTargets = new Set([a.id]); markWho(); $('chat-input').focus(); });
    who.append(b);
  }
  const minBtn = $('dock-min'), pillBtn = $('chat-pill');
  if (minBtn) minBtn.addEventListener('click', () => setChatMin(true));
  if (pillBtn) pillBtn.addEventListener('click', () => setChatMin(false));
  applyChatMin();

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
  realmNames = [...spaces].map(([name, list]) => ({ word: (name === 'outerrim' ? 'outer rim' : name).toUpperCase(), colour: color(list[0]), home: name === homeEmpire,
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
    if (name === homeEmpire) row(swatch(rgba(OURS, 0.9), rgba(OURS, 0.2)), name + ': our home, drawn in our green');
    else row(swatch(rgba(colour, 0.75), rgba(colour, 0.22)), name === 'outerrim' ? 'outer rim' : name);
  }
  const free = el('i'); free.style.background = LAWLESS;
  row(free, 'lawless');
  row(swatch(rgba(OURS, 0.9), rgba(OURS, 0.16)), 'our space: our home and the lines out along the lanes to our bases beyond the border', true);
  head('Our fleet');
  row(tokenSvg(), 'our ships: a slice per division, their number inside; outer ring: whose space', true);
  for (const kind of KINDS.slice(0, 6)) {            // the silhouette of each kind, as in the roster
    const span = el('span', 'lrow kind');
    span.append(shipSvg(kind === 'Command' ? 'Flagship' : kind, DIV[kind], 13), kind === 'Command' ? 'command group' : kind.toLowerCase());
    legend.append(span);
  }
  head('Ours');
  row(glyphSvg('outpost', BUILT, 13), 'outpost');
  row(glyphSvg('station', BUILT, 13), 'station');
  row(glyphSvg('storage', BUILT, 13), 'shared storage');
  row(glyphSvg('fuel', BUILT, 13), 'fuel bunker');
  row(glyphSvg('recruit', BUILT, 13), 'hiring office');
  row(glyphSvg('foundry', BUILT, 13), 'foundry / shipyard');
  row(glyphSvg('office', BUILT, 13), 'other office');
  row(glyphSvg('storage', RAISING, 13), 'amber: building / damaged');
  row(glyphSvg('flag', '#e8c35a', 13), 'next chosen build site');
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
    const infraAt = (px, py) => infraHits.find((h) => px >= h.x && px <= h.x + h.w && py >= h.y && py <= h.y + h.h);
    const tip = $('tip'), badge = S && badgeAt(mx, my), inf = !badge && S && infraAt(mx, my), grp = !badge && !inf && S && groupAt(mx, my), s = !badge && !inf && !grp && S && nearest(mx, my);
    hover = inf ? inf.system : s ? s.id : null; hoverBadge = badge || null;
    canvas.style.cursor = badge || inf || grp ? 'pointer' : '';
    const placeName = (b) => { const o = sys.get(b.system); return o ? o.name : b.system; };
    const placeTip = () => {
      tip.hidden = false;
      const tw = tip.offsetWidth || 250, th = tip.offsetHeight || 110;
      const left = mx + 16 + tw > W - 10 ? Math.max(8, mx - tw - 14) : mx + 16;
      const top = my + 14 + th > H - 10 ? Math.max(8, my - th - 12) : my + 14;
      tip.style.left = Math.round(left) + 'px';
      tip.style.top = Math.round(top) + 'px';
    };
    const tipKV = (grid, k, v) => { const c = el('div', 'tip-cell'); c.append(el('span', null, k), el('b', null, String(v))); grid.append(c); };
    if (badge) {
      const at = sys.get(badge.system) || {};
      tip.replaceChildren();
      const hd = el('div', 'tip-head'), bgs = el('div', 'tip-badges');
      bgs.append(el('span', 'pill good', badge.count + (badge.count === 1 ? ' ship' : ' ships')), el('span', 'pill info', at.empire || 'lawless'));
      hd.append(el('span', 'tip-title', placeName(badge)), bgs);
      tip.append(hd, el('div', 'tip-own', badge.parts), el('div', 'tip-foot', 'Click marker for live fleet card'));
      placeTip();
    } else if (inf) {
      tip.replaceChildren();
      const hd = el('div', 'tip-head');
      hd.append(el('span', 'tip-title', placeName(inf)), el('span', 'pill good', 'CLTV INFRA'));
      tip.append(hd);
      if (inf.own.length) {
        const lst = el('div', 'tip-list');
        inf.own.forEach((b) => lst.append(el('div', 'tip-own', b.name + (b.at && !b.part ? ' @ ' + b.at : '') + (stands(b) ? '' : ' [' + b.status + ']'))));
        tip.append(lst);
      }
      if (inf.site && inf.site.status !== 'built' && inf.site.status !== 'dropped') {
        const pctTxt = inf.siteInfo && inf.siteInfo.need_pct !== null ? ' -- ' + inf.siteInfo.need_pct + '% kit ready' : '';
        tip.append(el('div', 'tip-site', 'Planned site: ' + inf.site.status.toUpperCase() + pctTxt));
      }
      tip.append(el('div', 'tip-foot', 'Click to inspect buildings & stock'));
      placeTip();
    } else if (grp) {
      const g = grp.group;
      tip.replaceChildren();
      const hd = el('div', 'tip-head');
      hd.append(el('span', 'tip-title', '[' + g.tag + '] ' + (g.name || 'Foreign Group')),
        el('span', 'pill ' + (g.standing === 'hostile' ? 'bad' : g.standing === 'ally' ? 'good' : 'warn'), g.standing));
      const gr = el('div', 'tip-grid');
      tipKV(gr, 'System', placeName(grp));
      tipKV(gr, 'Pilots (1h)', g.count);
      tip.append(hd, gr, el('div', 'tip-foot', 'Click for pilot & hull intel'));
      placeTip();
    } else if (s) {
      const ours = shipsBy.get(s.id) || [], own = holdBy.get(s.id) || [], site = sitesBy.get(s.id), st = stationsBy.get(s.id) || [];
      tip.replaceChildren();
      const hd = el('div', 'tip-head'), bgs = el('div', 'tip-badges');
      if (s.stronghold) bgs.append(el('span', 'pill bad', 'stronghold'));
      bgs.append(el('span', 'pill ' + (s.empire ? 'info' : 'warn'), s.empire || 'lawless'));
      if (s.jumps >= 0) bgs.append(el('span', 'pill', s.jumps + 'j'));
      hd.append(el('span', 'tip-title', s.name), bgs);
      tip.append(hd);
      if (own.length) {
        tip.append(el('div', 'tip-own', 'CLTV: ' + own.map((b) => b.name + (stands(b) ? '' : ' (' + String(b.status).replace(/_/g, ' ') + ')')).join(', ')));
      }
      if (site && site.status !== 'dropped' && site.status !== 'built') {
        const sr = ((OPS.data && OPS.data.empire && OPS.data.empire.sites) || []).find((x) => x.system === s.id);
        tip.append(el('div', 'tip-site', 'Expansion site: ' + site.status.toUpperCase() + (sr && sr.need_pct != null ? ' (' + sr.need_pct + '%)' : '')));
      }
      const gr = el('div', 'tip-grid');
      tipKV(gr, 'Our ships', ours.length ? ours.length + ' active' : '0');
      tipKV(gr, 'Stations', st.length);
      tipKV(gr, 'Traffic 1h', (L.hour[s.id] || 0) + ' pilots');
      tipKV(gr, 'Traffic 24h', (L.day[s.id] || 0) + ' pilots');
      if (INVCACHE.value && st.length) {
        const sNames = new Set(st.map((t) => t.name));
        const stWorth = INVCACHE.value.stations.filter((x) => sNames.has(x.name)).reduce((a, x) => a + (x.worth || 0), 0);
        if (stWorth > 0) tipKV(gr, 'Our stock', fmtCompact(stWorth) + ' cr');
      }
      tip.append(gr);
      const ft = el('div', 'tip-foot');
      ft.append(el('span', null, 'Click to open Selection'));
      if (S.intel.systems[s.id] && S.intel.systems[s.id].threat && S.intel.systems[s.id].threat !== 'none') {
        ft.append(el('span', null, 'threat: ' + S.intel.systems[s.id].threat));
      }
      tip.append(ft);
      placeTip();
    } else tip.hidden = true;
    draw();
  });
  canvas.addEventListener('mouseleave', () => { $('tip').hidden = true; hover = null; hoverBadge = null; draw(); });
  canvas.addEventListener('click', (e) => {
    if (moved || !S) return;
    const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top, badge = badgeAt(mx, my);
    if (badge) { $('tip').hidden = true; select(badge.system, false); openPop(badge.system, badge.kind); return; }   // our ships stand in the system's own place: the system is picked and their card opens
    const inf = infraHits.find((h) => mx >= h.x && mx <= h.x + h.w && my >= h.y && my <= h.y + h.h);
    if (inf) { $('tip').hidden = true; if (pop) closePop(); select(inf.system, false); return; }
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
  if ($('btn-bases')) $('btn-bases').addEventListener('click', () => fitBases(false));
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
  document.querySelectorAll('#rfilters .rf').forEach((b) => b.addEventListener('click', () => setRosterMode(b.dataset.mode)));
  const rInp = $('roster-filter'), rSort = $('roster-sort'), bHelp = $('btn-help');
  if (rInp) rInp.addEventListener('input', () => { rosterQuery = rInp.value.trim().toLowerCase(); renderRoster(); });
  if (rSort) rSort.addEventListener('change', () => { rosterSort = rSort.value; renderRoster(); });
  if (bHelp) bHelp.addEventListener('click', (e) => { e.stopPropagation(); toggleHelp(); });
  document.addEventListener('click', (e) => { if (!e.target.closest('#helpcard') && !e.target.closest('#btn-help')) toggleHelp(false); });
  window.addEventListener('keydown', (e) => {
    const tag = (document.activeElement && document.activeElement.tagName) || '';
    if (e.key === 'Escape') {
      if (pop) closePop();
      toggleHelp(false);
      if (tag === 'INPUT' || tag === 'TEXTAREA') document.activeElement.blur();
      return;
    }
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || e.ctrlKey || e.metaKey || e.altKey) return;
    const k = e.key.toLowerCase();
    if (k === 'f') fitFleet(false);
    else if (k === 'b') fitBases(false);
    else if (k === 'e') { tab = 'Empire'; pilotCard = null; docView = null; render(); }
    else if (k === 'h' && S) fit(S.systems.filter((s) => s.jumps >= 0 && s.jumps <= 4), 500);
    else if (k === 'g' && S) fit(S.systems, 1200);
    else if (k === '1') { tab = 'Selection'; render(); }
    else if (k === '2') { tab = 'Empire'; pilotCard = null; docView = null; render(); }
    else if (k === '3') { tab = 'Metrics'; pilotCard = null; docView = null; render(); }
    else if (k === '4') { tab = 'Inventory'; pilotCard = null; docView = null; invItem = null; render(); }
    else if (k === '5') { tab = 'Docs'; pilotCard = null; render(); }
    else if (k === '[') toggleShut('left');
    else if (k === ']') toggleShut('right');
    else if (k === '/') { e.preventDefault(); const inp = $('search'); if (inp) inp.focus(); }
    else if (e.key === '?') toggleHelp();
  });
}

function fitFleet(jump) {
  const list = [...shipsBy.keys()].map((id) => sys.get(id)).filter(Boolean);
  if (!list.length) { fit(S.systems.filter((s) => s.jumps >= 0 && s.jumps <= 4), 500, jump); return; }
  fit(list.concat(list.flatMap((s) => s.lanes.map((id) => sys.get(id)).filter(Boolean))), 300, jump);
}

function fitBases(jump) {
  const ids = new Set([...holdBy.keys()]);
  for (const [id, st] of sitesBy) { if (st.status === 'chosen') ids.add(id); }
  const list = [...ids].map((id) => sys.get(id)).filter(Boolean);
  if (!list.length) { fitFleet(jump); return; }
  fit(list.concat(list.flatMap((s) => s.lanes.map((id) => sys.get(id)).filter(Boolean))), 420, jump);
}

(async function main() {
  init();
  await loadState();
  resize();
  await loadFleet();
  fitFleet(true);
  await loadLive();
  await loadOps();
  render();
  initChat();
  setInterval(loadLive, 5000);
  setInterval(loadFleet, 5000);
  setInterval(loadOps, 30000);
  setInterval(tickAges, 1000);
  setInterval(async () => { await loadState(); draw(); if (tab === 'Docs' && !docView) render(); }, 120000);
})().catch((e) => { $('panel').replaceChildren(el('p', 'empty', 'The station could not load its data: ' + e.message)); });
