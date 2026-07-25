---
title: 'Animate turn events'
type: 'feature'
created: '2026-07-25'
status: 'done'
review_loop_iteration: 0
baseline_commit: '4629b3f6963210d93d7473208dbde5c39242c501'
context:
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-strategic_reserve-2026-07-25/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Dice outcomes and their board effects appear immediately, making turns difficult to follow.

**Approach:** Add a short, ordered visual treatment for rolling dice, identifying the targeted square, and removing captured checkers while preserving the current rules and accessible status announcements.

## Boundaries & Constraints

**Always:** Keep gameplay responsive, preserve keyboard/focus behavior, use the existing purple/green/target/player colors, and disable all added motion under `prefers-reduced-motion`.

**Ask First:** Any change to game rules, turn timing beyond brief presentation delays, or introduction of a runtime dependency.

**Never:** Change engine outcomes, block screen-reader announcements until animations finish, depend on animation completion events for game correctness, or make color the only indication of the targeted square.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Human roll | Player activates Roll Dice | Both dice visibly tumble, settle, and the target square pulses | Roll control remains disabled during the sequence |
| Capture | Roll removes one or more checkers | Removed checker ghosts shrink/fade from their former squares | Multiple removals animate together without changing the resolved state |
| Reduced motion | OS requests reduced motion | Final dice, target, and board state appear without motion | No presentation delay is required |

</frozen-after-approval>

## Code Map

- `site/js/app.js` -- Browser controller and render lifecycle for dice, target, and checker state.
- `site/styles.css` -- Visual presentation, keyframes, and reduced-motion override.
- `site/tests/static.test.js` -- Static accessibility and interaction-contract coverage.

## Tasks & Acceptance

**Execution:**
- [x] `site/js/app.js` -- Stage roll presentation and derive captured locations from before/after states without changing the engine.
- [x] `site/styles.css` -- Add concise dice, target, and checker-removal animations with reduced-motion behavior.
- [x] `site/tests/static.test.js` -- Assert the animation hooks and reduced-motion contracts remain present.

**Acceptance Criteria:**
- Given an active human or computer turn, when dice are rolled, then the dice animate before settling on the resolved values.
- Given the resolved roll targets a square, when the board updates, then that square receives a noticeable pulse in addition to its Target label.
- Given resolution captures checkers, when the board updates, then representations of those checkers animate out from their previous cells.
- Given reduced motion is enabled, when any turn resolves, then all state changes remain legible without animation.

## Verification

**Commands:**
- `npm test` -- expected: all engine, AI, and static contract tests pass.
- `npm run check` -- expected: JavaScript syntax and static page checks pass.

## Suggested Review Order

**Turn sequencing**

- Stages dice settlement and preserves removed checkers as transient presentation state.
  [`app.js:21`](../../../site/js/app.js#L21)

- Cancels stale asynchronous animations safely across new, quit, and AI flows.
  [`app.js:9`](../../../site/js/app.js#L9)

**Motion design**

- Defines dice, target, and checker-removal treatments with reduced-motion fallback.
  [`styles.css:26`](../../../site/styles.css#L26)

- Keeps native hidden states authoritative over component display declarations.
  [`styles.css:3`](../../../site/styles.css#L3)

**Contracts**

- Protects animation hooks, hidden states, and reduced-motion behavior from regression.
  [`static.test.js:7`](../../../site/tests/static.test.js#L7)
