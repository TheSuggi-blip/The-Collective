---
name: routes-templates-military
id: 20261117T001510Z
tier: intel
author: Unity
---

# templates-military.md -- The Templates of the Military Division

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `templates/military.json`:
the named lists of routes of the military division. A ship's row in the division's plan
file (`game/fleet/plan.py`) names one as `@<template>` among its own routes, and the ship
tries its routes in this order; a change of a template moves every ship that names it
within the minute. Kept with `plan.py template`; ships are put on one with `plan.py use`.
Up: [master-index.md](master-index.md).

Kept by Apophis. Templates: 2. Ships on them: 0.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| hunter | Hunt where a herd holds, one hunter a herd; sell stored curd where a bid stands; gather iron only when no herd is open | gunnery, weapons, tactics, xenobiology | [sell-curd-central-nexus](sell-curd-central-nexus.json) > [sell-curd-node-beta](sell-curd-node-beta.json) > [sell-curd-experiment](sell-curd-experiment.json) > [hunt-felis-frost-ring-hollow-pilgrim](hunt-felis-frost-ring-hollow-pilgrim.json) > [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) > [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) > [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) > [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) > [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) > [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) > [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) > [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) > [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) > [hunt-home-drift-ray](hunt-home-drift-ray.json) > [hunt-keid-belt-carapace](hunt-keid-belt-carapace.json) > [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) > [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) > [mine-pherkad-rift](mine-pherkad-rift.json) > [mine-acubens](mine-acubens.json) | 0 | Fit: the starter Pulse Laser I (reach 3) and Mining Laser I. Each hunt takes one ship (rule F9); the veil-ray, drift-ray and carapace hunts are standing work that store curd, carapace and biogas for the station list; the sell-curd routes open only while a bid stands and the pilot stores curd. Gathering is the fallback (rule F23). |
| guard | Guard where our ships mine beyond the border; read the guarded systems when no guard post is open | piloting, navigation | [guard-ironhollow-fading-signal](guard-ironhollow-fading-signal.json) > [guard-marfik-emission-nebula](guard-marfik-emission-nebula.json) > [census-guard-ice](census-guard-ice.json) | 0 | A guard route opens only while a pilot of ours flies the route it guards; it never fires, leaves under 60 percent hull or in a fight, and docks at the station named. Put it before @hunter in a ship's cell. |
