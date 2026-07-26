---
title: 'Epic 3: Complete Python Capture and Placement Rules'
type: 'feature'
created: '2026-07-26'
status: 'done'
baseline_revision: '211543f4848a5fab8256609a038dc2837f07eebd'
final_revision: '5533a375bb0152aaf7d74655d58ec1ede4a4a56b'
review_loop_iteration: 0
followup_review_recommended: false
context: []
warnings: [multiple-goals]
---

> **Historical record — superseded by Epic 7:** Pass/no-placement behavior documented below described the implementation at completion time. Epic 7 proves every valid active roll has a legal placement and removes that behavior from the current product.

<intent-contract>

## Intent

**Problem:** The Python engine already contains the core enemy-hit, friendly-hit, empty-hit, placement, and explicit no-move pass lifecycle, but Epic 3 is not complete because its boundary, de-duplication, conservation, exhaustive dice-outcome, and atomic-failure guarantees are not fully hardened or demonstrated.

**Approach:** Preserve the existing copy-on-write rules API, close strict domain-validation gaps, and add deterministic scenario coverage proving all four Epic 3 stories across complete turns and all dice targets.

## Boundaries & Constraints

**Always:** Keep the engine authoritative and independent of UI/AI; use absolute zero-based board coordinates; discover maximal groups orthogonally; capture each group once; return all captured checkers to their owner; expose only empty legal destinations; conserve 12 checkers per player; validate before committing; advance exactly once on placement or an explicit legal pass; keep caller-owned input state unchanged.

**Block If:** A required behavior conflicts with the published Epic 3 acceptance criteria or would require winner/game-over semantics owned by a later epic.

**Never:** Change browser code, add UI/AI behavior, introduce global mutable state, auto-advance a no-move roll before callers can observe its resolution, weaken domain exceptions, or expand into winner detection.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Enemy hit | Roll targets an enemy maximal group | Remove only that group, restore its reserve, offer every empty square including captured squares | Input state remains unchanged |
| Friendly hit | Friendly group touches the same enemy group multiple times and other enemy groups | Capture each adjacent enemy group once; offer exactly empty orthogonal neighbors of the friendly group | Non-adjacent/occupied placement raises `IllegalMoveError` atomically |
| Empty hit | Roll targets any empty square | No capture; offer all and only empty squares; placement updates reserve and turn once | Invalid placement leaves resolved state unchanged |
| No move | Resolved roll has no legal placement | Expose an empty list; explicit `pass_turn` advances and clears context once | Passing when moves exist or before a roll is atomic and illegal |
| Dice boundaries | Either player, every column/row pair from 1 through 6 | Map to each board square and resolve a valid observable turn state | Non-integral, boolean, or out-of-range dice values raise a domain error |

</intent-contract>

## Code Map

- `python/game_engine/rules.py` -- dice mapping, capture resolution, legal destinations, placement, and pass lifecycle.
- `python/tests/test_rules.py` -- deterministic rule, atomicity, boundary, and full-turn invariant scenarios.
- `python/README.md` -- Python-edition capability and test-suite documentation.
- `_bmad-output/planning-artifacts/epics/epic-3-complete-python-capture-and-placement-rules.md` -- Epic/story delivery status.
- `_bmad-output/planning-artifacts/epics/README.md` -- epic index delivery status.

## Tasks & Acceptance

**Execution:**
- [x] `python/game_engine/rules.py` -- reject boolean and non-integer coordinate/dice values consistently while preserving the established resolution and copy-on-write lifecycle.
- [x] `python/tests/test_rules.py` -- add exact-set, maximal-group, multi-contact de-duplication, diagonal/disconnected survival, both-player boundary, all-36-outcome, conservation, turn-progression, defensive-copy, and atomic rejection coverage.
- [x] `python/README.md` -- describe the completed capture/placement behavior and Epic 3 scenario coverage.
- [x] `_bmad-output/planning-artifacts/epics/epic-3-complete-python-capture-and-placement-rules.md` and `_bmad-output/planning-artifacts/epics/README.md` -- mark Epic 3 and all four stories complete after verification.

**Acceptance Criteria:**
- Given any enemy, friendly, or empty target category, when a roll resolves and a legal placement completes, then captures, exact legal destinations, reserves, occupancy, active player, turn number, and cleared turn context match the rules.
- Given a friendly group with an enemy maximal group touching multiple members, when it resolves, then every member is removed once and the enemy reserve increases by exactly the group size.
- Given either player and each of the 36 dice pairs, when a representative valid state resolves, then the target is correct, the resolved state validates, legal moves are unique/in-bounds/empty, and checker conservation holds.
- Given any rejected roll, placement, or pass action, when input state is compared afterward, then no board, reserve, context, or turn mutation remains.
- Given a resolved state without legal destinations, when it is observed and explicitly passed, then no hang occurs and the turn advances exactly once.

## Spec Change Log

## Review Triage Log

### 2026-07-26 — Review pass
- intent_gap: 0
- bad_spec: 0
- patch: 5: (high 1, medium 2, low 2)
- defer: 0
- reject: 10: (high 0, medium 4, low 6)
- addressed_findings:
  - `[high]` `[patch]` Extended exhaustive dice coverage through placement/pass, validation, turn/context assertions, and post-turn conservation.
  - `[medium]` `[patch]` Corrected epic context to distinguish engine-owned dice perspective mapping from UI-owned display conversion.
  - `[medium]` `[patch]` Clarified the one-based built-in-integer dice contract versus zero-based built-in-integer board destinations.
  - `[low]` `[patch]` Derived exhaustive test bounds from the board rather than duplicating its size.
  - `[low]` `[patch]` Documented reserve-exhausted resolution and explicit-pass behavior.

## Design Notes

The explicit `roll_dice` → inspect `legal_destinations` → `apply_placement` or `pass_turn` lifecycle is retained. It makes capture results observable, supports future UI/AI choice, and avoids importing later-epic winner semantics into no-move handling.

## Verification

**Commands:**
- `python -m pytest -q` -- expected: all Python engine tests pass.
- `python -m compileall -q python` -- expected: all Python modules compile.
- `git diff --check` -- expected: no whitespace errors.

## Auto Run Result

- Summary: Completed and hardened all Epic 3 capture and placement rules while preserving the engine's copy-on-write resolution lifecycle.
- Files changed: `python/game_engine/rules.py` tightens dice and destination types; `python/tests/test_rules.py` proves capture, exact legal-move, exhaustive outcome, conservation, progression, and atomicity behavior; `python/README.md` documents the API; Epic 3 planning and implementation artifacts record delivery and review.
- Review findings: 5 patches applied, 0 items deferred, and 10 findings rejected as duplicates, transient workflow state, already-covered behavior, or unsupported scope expansion.
- Follow-up review recommendation: false; review-driven changes were localized to tests and documentation and introduced no new runtime behavior.
- Verification: `python -m pytest -q` passed with 41 tests; `python -m compileall -q python` passed; `git diff --check` passed.
- Residual risks: Winner/game-over semantics remain intentionally assigned to a later epic; callers must explicitly pass a resolved turn with no legal placement.
