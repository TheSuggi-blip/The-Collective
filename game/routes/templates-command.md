---
name: routes-templates-command
id: 20261116T204515Z
tier: intel
author: Unity
---

# templates-command.md -- The Templates of the Command Division

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `templates/command.json`:
the named lists of routes of the command division. A ship's row in the division's plan
file (`game/fleet/plan.py`) names one as `@<template>` among its own routes, and the ship
tries its routes in this order; a change of a template moves every ship that names it
within the minute. Kept with `plan.py template`; ships are put on one with `plan.py use`.
Up: [master-index.md](master-index.md).

Kept by Unity. Templates: 1. Ships on them: 0.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| ice-and-hunt | Veil-ray hunts and two missions | weapons | [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) > [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) > [voidborn-network-expansion](voidborn-network-expansion.json) > [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | 0 | the flagships hunt and fly missions; ice is the miners' (rule F23, 2026-11-18) |
