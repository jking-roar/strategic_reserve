---
title: 'Animate Python turn events'
type: 'feature'
created: '2026-07-27'
status: 'done'
review_loop_iteration: 0
baseline_commit: '76c218b'
context:
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-strategic_reserve-2026-07-25/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Computer turns in the Python desktop game resolve abruptly, so players cannot easily connect the dice result to its target and resulting captures.

**Approach:** Present every human and computer state transition as a short ordered sequence: tumble and settle the dice, pulse the targeted square, then visibly fade and shrink any removed checkers.

## Boundaries & Constraints

**Always:** Keep the engine state authoritative, lock conflicting input while presentation is in progress, preserve keyboard/focus behavior and visible text announcements, and make animations cancellable when the session changes.

**Ask First:** Any game-rule change, runtime dependency, or delay long enough to materially slow play.

**Never:** Run Tk operations on the AI worker thread, rely on animation callbacks for game correctness, hide the target's existing non-color “T” cue, or leave a computer turn input-locked after an AI error.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Computer roll | Blue begins a computer turn | Dice visibly cycle before settling; the resolved target then pulses before strategy selection completes | Stale callbacks cannot mutate a replaced session |
| Capture | A roll or placement removes one or more checkers | Ghosts of all removed checkers shrink and fade together over the resolved board | The final authoritative board remains visible if animation is skipped |
| Test/instant mode | Controller has zero animation steps | Transition resolves synchronously with no queued presentation work | Callbacks and AI progression still complete |

</frozen-after-approval>

## Code Map

- `python/ui/main.py` -- Tk controller sequencing for human and computer rolls, AI work, and transient presentation.
- `python/ui/board_view.py` -- Canvas rendering and transient target/removal overlays.
- `python/tests/test_ui.py` -- Display-independent controller sequencing contracts.
- `python/tests/test_ui_tk.py` -- Canvas-backed visual overlay checks.

## Tasks & Acceptance

**Execution:**
- [x] `python/ui/main.py` -- unify human/computer roll presentation and stage target/removal effects without changing engine outcomes.
- [x] `python/ui/board_view.py` -- draw progress-based target pulse and removed-checker ghosts.
- [x] `python/tests/test_ui.py` and `python/tests/test_ui_tk.py` -- cover AI dice animation, stale callbacks, target pulse, and simultaneous removal overlays.

**Acceptance Criteria:**
- Given a computer turn, when Blue rolls and moves, then the dice roll, targeted square, and any removed chips are visually sequenced before control returns to Red.
- Given a human roll or placement, when it removes checkers, then every removed location receives a transient visual ghost while the engine's resolved state remains authoritative.
- Given a new game or quit invalidates a sequence, when a queued callback runs, then it exits without mutating the new session.

## Spec Change Log

## Design Notes

The controller owns timing and generation-token cancellation. The canvas only renders a supplied progress value, keeping game decisions and completion independent from paint behavior. Zero animation steps is the deterministic instant mode used by unit tests.

## Verification

**Commands:**
- `cd python && pytest` -- expected: all Python engine, AI, UI, architecture, launcher, and release tests pass.
- `cd python && python -m compileall -q .` -- expected: Python sources compile successfully.

## Suggested Review Order

**Turn sequencing**

- Unifies human and computer dice rolls behind cancellable Tk event-loop sequencing.
  [`main.py:150`](../../../python/ui/main.py#L150)

- Publishes authoritative outcomes before drawing disposable target and capture effects.
  [`main.py:181`](../../../python/ui/main.py#L181)

- Delays strategy selection and animates normal and fallback computer placements consistently.
  [`main.py:266`](../../../python/ui/main.py#L266)

**Canvas effects**

- Retains transient frames across focus-driven rerenders without owning game state.
  [`board_view.py:77`](../../../python/ui/board_view.py#L77)

- Scales target pulses and removed-chip ghosts with animation progress and cell size.
  [`board_view.py:117`](../../../python/ui/board_view.py#L117)

**Regression contracts**

- Verifies computer dice cycling and stale callback cancellation independently of a display.
  [`test_ui.py:229`](../../../python/tests/test_ui.py#L229)

- Verifies target and simultaneous removal overlays on a real Tk canvas.
  [`test_ui_tk.py:112`](../../../python/tests/test_ui_tk.py#L112)
