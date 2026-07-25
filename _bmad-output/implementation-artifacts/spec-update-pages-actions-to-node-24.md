---
title: 'Update Pages actions to Node.js 24'
type: 'chore'
created: '2026-07-25'
status: 'done'
route: 'one-shot'
---

# Update Pages actions to Node.js 24

## Intent

**Problem:** Both GitHub Pages workflows reference action releases that use the deprecated Node.js 20 action runtime, causing deployment warnings and forced runtime upgrades.

**Approach:** Upgrade every Pages workflow action to its current Node.js 24-based major release while preserving the existing triggers, permissions, artifact paths, and deployment behavior.

## Suggested Review Order

1. [`.github/workflows/deploy-pages.yml`](../../../.github/workflows/deploy-pages.yml) — verify the `master` deployment uses current action majors.
2. [`.github/workflows/pages.yml`](../../../.github/workflows/pages.yml) — verify the parallel `main` deployment stays aligned.
