---
title: 'Epic 5: Computer Opponents'
type: 'feature'
created: '2026-07-26'
status: 'done'
baseline_revision: '752b1c29912b0f20c30422d455a44b8aeeaf22f3'
final_revision: 'f45b998'
review_loop_iteration: 0
followup_review_recommended: true
context:
  - '{project-root}/_bmad-output/planning-artifacts/epics/epic-5-computer-opponents.md'
warnings: [multiple-goals]
---

<intent-contract>

## Intent

**Problem:** The Python desktop game supports only local PvP and its AI package is a placeholder, so all four Epic 5 stories remain unavailable; earlier epic delivery tracking and public documentation are also inconsistent with completed code.

**Approach:** Add safe rudimentary and bounded strategic AI implementations, connect selectable PvC difficulties to the Tk controller through the authoritative engine, prove legality/immutability/performance with deterministic corpus tests, and synchronize all Epic 1-5 completion records after verification.

## Boundaries & Constraints

**Always:** Preserve `ui -> ai -> game_engine`; keep engine transitions copy-on-write and authoritative; accept only a resolved current-player turn; return a legal coordinate or `None`; leave caller state unchanged; make rudimentary selection injectable/deterministic; evaluate all 36 next-roll outcomes in advanced completed candidate analysis; keep a legal best-so-far fallback; use a monotonic configurable budget; assign the computer Blue; lock human input for every AI-owned phase; reuse `roll_dice`, `apply_placement`, `pass_turn`, rendering, and winner handling; invalidate stale callbacks on session change.

**Block If:** Epic 5 requires changing established capture, placement, pass, or winner semantics, or safe Tk result handoff cannot be implemented without a non-standard runtime dependency.

**Never:** Mutate caller-owned state; duplicate rules in AI/UI; return an unchecked move; let workers touch Tk widgets or controller state; block the Tk event loop for strategic search; allow human input to race an AI turn; add packaging or Epic 6 accessibility scope.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Rudimentary turn | Resolved state with legal moves | Random injected choice from the exact legal set in under one second | Input remains equal to its snapshot |
| No move | Resolved state with no legal moves | Both difficulties return `None` promptly | UI uses the engine pass lifecycle |
| Advanced turn | Resolved state and bounded budget | Legal best-so-far selected using 36 next-roll outcomes per completed candidate, under five seconds | Deadline retains a legal fallback |
| PvC lifecycle | Human Red completes a turn | Blue AI rolls, chooses/places or passes through engine APIs, then returns control | Human controls remain locked until completion |
| Stale result | Restart/quit/session change during AI work | Result is discarded without state/widget mutation | Generation token protects handoff |
| Safety corpus | Full, sparse, capture-heavy, no-move, near-win states | Every result is legal or `None`; no crash, hang, or mutation | Invalid phase/player requests fail explicitly |

</intent-contract>

## Code Map

- `python/ai/` -- difficulty implementations and stable selection API.
- `python/game_engine/rules.py` -- authoritative roll, placement, pass, and simulation primitives.
- `python/ui/controls.py` -- mode and difficulty selection plus turn controls.
- `python/ui/main.py` -- session configuration, AI scheduling, input locking, and safe result handoff.
- `python/tests/test_ai.py` -- AI outcome, corpus, immutability, budget, and timing contracts.
- `python/tests/test_ui.py` -- headless PvC lifecycle and stale-callback contracts.
- `README.md`, `python/README.md`, `docs/python/README.md` -- accurate edition capabilities and commands.
- `_bmad-output/planning-artifacts/epics*.md` -- synchronized earlier-epic audit and Epic 5 delivery status.

## Tasks & Acceptance

**Execution:**
- [x] `python/ai/` -- implement validated rudimentary selection and bounded 36-outcome strategic selection with injectable randomness/clock -- satisfies stories 5.1, 5.2, and safe testability.
- [x] `python/ui/controls.py`, `python/ui/main.py`, `python/ui/__init__.py` -- add PvP/PvC difficulty configuration, Blue AI lifecycle, complete input locking, and generation-safe nonblocking computation -- satisfies story 5.3.
- [x] `python/tests/test_ai.py`, `python/tests/test_ui.py`, `python/tests/test_architecture.py` -- cover the required state corpus, legality, immutability, 36 outcomes, time budgets, dispatch, pass/win, race prevention, and dependency direction -- satisfies story 5.4.
- [x] `README.md`, `python/README.md`, `docs/python/README.md` -- document completed Python PvC behavior and current limitations.
- [x] `_bmad-output/planning-artifacts/epics.md`, `_bmad-output/planning-artifacts/epics/*.md`, `_bmad-output/implementation-artifacts/spec-epic-4-local-desktop-game.md` -- reconcile Epics 1-4 status, record the Epic 4 follow-up audit, and mark Epic 5 complete only after verification.

**Acceptance Criteria:**
- Given any valid resolved state from the required corpus, when either AI runs, then its result is in the exact legal set or is `None` only when that set is empty, input is unchanged, and the documented one/five-second limits hold.
- Given an advanced search that completes candidate evaluation, when its lookahead is observed, then every one of the 36 possible opponent rolls contributed and the selected result remains legal even when the budget interrupts later work.
- Given PvC at either difficulty, when Red ends a turn, then Blue alone performs the matching AI roll and legal placement/pass through engine APIs while human actions cannot race it.
- Given a new session or quit during an outstanding AI turn, when a stale callback arrives, then it cannot mutate the new/current state or UI.
- Given the full repository suite passes, when delivery artifacts are inspected, then Epics 1-5 and their stories consistently reflect completed implementation while Epic 6 remains pending.

## Spec Change Log

## Review Triage Log

### 2026-07-26 — Review pass
- intent_gap: 0
- bad_spec: 0
- patch: 9: (high 4, medium 4, low 1)
- defer: 0
- reject: 4: (high 0, medium 3, low 1)
- addressed_findings:
  - `[high]` `[patch]` Recovered submission, worker, illegal-result, and unexpected AI failures with an engine-validated deterministic move/pass rather than leaving Blue's turn input-locked.
  - `[high]` `[patch]` Tracked and cancelled pending futures, replaced executors between sessions, and shut executor intake down without blocking the Tk thread on quit.
  - `[high]` `[patch]` Prevented obsolete work from queueing a new session's search behind the old generation.
  - `[high]` `[patch]` Added headless coverage for strategy dispatch, pass/win paths, failure recovery, input locking, and stale results.
  - `[medium]` `[patch]` Rejected negative and non-finite budgets and non-finite clock samples so the bounded-search contract cannot be disabled by NaN or infinity.
  - `[medium]` `[patch]` Kept observer callbacks within deadline measurement and preserved a legal fallback when observation exhausts the budget.
  - `[medium]` `[patch]` Strengthened safety/timing tests across representative resolved states and explicit invalid timing inputs.
  - `[medium]` `[patch]` Corrected the epic delivery audit date to match the completed review.
  - `[low]` `[patch]` Removed the unused alternate dice-RNG encoding.

## Design Notes

Advanced evaluation should favor immediate wins and reserve/board advantage, examine independent post-placement copies for opponent rolls, and avoid starting work it cannot safely finish. Tk work may run off-thread, but only the UI thread applies a generation-checked result.

## Verification

**Commands:**
- `python -m pytest -q` -- expected: all engine, AI, UI, timing, and architecture tests pass.
- `python -m compileall -q python` -- expected: every Python module compiles.
- `npm test` -- expected: earlier browser epic remains green.
- `npm run check` -- expected: browser syntax/static contracts remain green.
- `git diff --check` -- expected: no whitespace errors.

## Auto Run Result

- Summary: Completed Epic 5 with safe random and bounded strategic Python opponents, selectable desktop PvC play, nonblocking and generation-safe AI turns, and reconciled delivery records for all earlier epics.
- Files changed: `python/ai/` implements both strategies and dispatch; `python/ui/` adds difficulty selection and the Blue AI lifecycle; `python/tests/` covers strategy safety, performance, corpus, and controller races; project documentation and epic artifacts now reflect Epics 1-5 accurately.
- Review findings: 9 patches applied, 0 items deferred, and 4 findings rejected as unsupported scope expansion, impossible literal full-board state, or already-safe stale/terminal semantics.
- Follow-up review recommendation: true; review-driven controller recovery, executor lifecycle, timing validation, and expanded cross-layer tests changed several high-consequence asynchronous paths.
- Verification: `python -m pytest -q python/tests` passed with 79 tests; `python -m compileall -q python` passed; `npm test` passed with 22 tests; `npm run check` passed; `git diff --check` passed.
- Residual risks: Running Python worker code cannot be forcibly stopped once executing, but obsolete results are discarded, new sessions receive a fresh executor, and strategic work remains capped below five seconds; graphical Tk behavior still requires a display for manual smoke testing.
