---
title: 'Stabilize Board Square Dimensions'
type: 'bugfix'
created: '2026-07-25'
status: 'done'
route: 'one-shot'
---

# Stabilize Board Square Dimensions

## Intent

**Problem:** Board grid rows inherited content-driven implicit sizing, so rows containing checkers could render at different heights from empty rows.

**Approach:** Define six equal, shrinkable tracks on both grid axes and preserve that invariant with a focused stylesheet regression test.

## Suggested Review Order

**Layout invariant**

- Explicit row and column tracks keep every board square equally sized regardless of content.
  [`styles.css:27`](../../site/styles.css#L27)

**Regression coverage**

- Source-level assertions prevent either explicit six-track axis from being removed accidentally.
  [`static.test.js:8`](../../site/tests/static.test.js#L8)
