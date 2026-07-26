---
title: 'Epic 4: Local Desktop Game'
type: 'feature'
created: '2026-07-26'
status: 'done'
baseline_revision: '786dbe4601a9e6f11873a261abfc9217a6de7331'
final_revision: '81772879db510956e48543dbd4fe90197f9ae224'
review_loop_iteration: 0
followup_review_recommended: true
context:
  - '{project-root}/_bmad-output/planning-artifacts/epics/epic-4-local-desktop-game.md'
warnings: [multiple-goals]
---

<intent-contract>

## Intent

**Problem:** The Python rules engine is playable only through its API; there is no desktop interface in which two people can configure, play, finish, restart, and safely quit a local game.

**Approach:** Add a Tkinter desktop shell that remains a replaceable consumer of the authoritative engine, complete the engine-owned winner lifecycle, and cover controller behavior with headless tests and the widgets with import/smoke checks.

## Boundaries & Constraints

**Always:** Preserve UI -> AI -> engine dependency direction and copy-on-write engine transitions; keep board, reserves, current player, turn context, and winner authoritative in `game_engine`; use absolute `(row, column)` engine coordinates; use non-blocking `after` callbacks for dice animation; invalidate stale callbacks on restart/quit; expose explicit pass when no legal move exists; catch domain errors at the UI boundary; keep all interaction keyboard operable.

**Block If:** Existing engine semantics conflict with an acceptance criterion in a way that cannot be reconciled without changing completed Epic 2/3 behavior, or Tkinter is unavailable as a standard-library dependency.

**Never:** Add a third-party GUI dependency, duplicate game rules in the UI, mutate `GameState` in place, implement computer opponents or release packaging, silently treat PvC as PvP, sleep/block the Tk event loop, or depend on a display server for the automated suite.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| New local game | Main menu, PvP selected | Fresh official board replaces menu; Red and reserves are shown | Unsupported PvC remains unavailable with concise feedback |
| Resolved roll | Active game, Roll Dice | Animation completes, then values, gold target, and only legal green squares persist | Disable repeated roll during animation |
| Placement | Current legal destination | Engine applies placement/capture, refreshes board/reserves/player immediately | Illegal or stale activation preserves state and reports concise status |
| Forced pass | Resolved roll with no legal destinations | Pass control advances the turn via engine API | Pass is unavailable while legal moves exist |
| Winning placement | Placement reduces active reserve to zero | Engine records winner immediately; UI announces winner and disables game input | All later engine turn actions reject without mutation |
| Restart | Game-over New Game | Return to clean configured-game menu with no prior state/callbacks | Pending callbacks are invalidated |
| Quit request | Active unfinished game or window close | Yes exits; No/Escape closes confirmation and preserves play exactly | Menu/completed-game quit may exit directly |

</intent-contract>

## Code Map

- `python/game_engine/models.py` -- authoritative `GameState`, extended with winner.
- `python/game_engine/validation.py` -- winner consistency and terminal-state validation.
- `python/game_engine/rules.py` -- immutable winner detection and post-game action guards.
- `python/ui/board_view.py` -- Canvas-based 6x6 board, checker, target, legal, focus, and activation rendering.
- `python/ui/controls.py` -- menu, status/dice/reserve controls, and game-over presentation.
- `python/ui/main.py` -- screen/session controller, animation scheduling, engine orchestration, and quit flow.
- `python/main.py` -- executable desktop entry point.
- `python/tests/test_rules.py`, `python/tests/test_state.py` -- engine terminal-state coverage.
- `python/tests/test_ui.py` -- headless controller/presentation behavior using fakes.
- `python/tests/test_architecture.py` -- dependency-direction coverage for all Python UI/AI modules.
- `python/README.md`, `docs/python/README.md` -- run instructions and current capability documentation.
- `_bmad-output/planning-artifacts/epics/epic-4-local-desktop-game.md`, `_bmad-output/planning-artifacts/epics/README.md` -- completion tracking after verification.

## Tasks & Acceptance

**Execution:**
- [x] `python/game_engine/models.py`, `python/game_engine/state.py`, `python/game_engine/validation.py`, `python/game_engine/rules.py`, `python/game_engine/__init__.py` -- add an optional engine-owned winner, declare it on the last reserve placement without advancing away from the winner, and immutably reject roll/place/pass after completion.
- [x] `python/ui/board_view.py` -- render a fixed 6x6 beige grid with outlined red/blue checkers, layered gold target and light/dark-green legal treatments, keyboard focus, and absolute-coordinate activation callbacks.
- [x] `python/ui/controls.py` -- implement the PvP menu, disabled/unavailable PvC difficulty path, persistent numerical/dot dice, player/reserve/status controls, pass action, and centered game-over action.
- [x] `python/ui/main.py`, `python/ui/__init__.py`, `python/main.py` -- implement a single-window controller with explicit roll, non-blocking animation, legal/stale input handling, immediate refresh/win flow, restart cleanup, and a Yes/No/Escape active-game quit dialog shared by Quit and window close.
- [x] `python/tests/test_rules.py`, `python/tests/test_state.py`, `python/tests/test_ui.py`, `python/tests/test_architecture.py` -- test every matrix row, winner validation/copy semantics, stale animation/session callbacks, view-model rendering rules, and dependency boundaries without requiring `$DISPLAY`.
- [x] `python/README.md`, `docs/python/README.md` -- document desktop launch, controls, architecture boundary, and test/headless limitations accurately.
- [x] `_bmad-output/planning-artifacts/epics/epic-4-local-desktop-game.md`, `_bmad-output/planning-artifacts/epics/README.md` -- mark Epic 4 and stories 4.1-4.5 complete only after all automated verification passes.

**Acceptance Criteria:**
- Given application launch, when the menu appears and PvP New Game is activated, then a correctly initialized 6x6 game replaces it and announces Red.
- Given an active game, when it renders or a roll resolves, then outlined pieces, empty squares, reserves, current player, purple-column and green-row dice, gold target, and exactly the legal green destinations are visible.
- Given a legal, illegal, or stale square activation, when it is processed, then only the legal current action changes authoritative state and all others preserve it with concise feedback.
- Given the final reserve placement, when it completes, then the engine and centered UI immediately declare that player winner, disable further board/turn input, and New Game returns to a clean menu flow.
- Given an active game, when Quit or window close is requested, then Yes exits while No or Escape resumes the identical game.

## Spec Change Log

## Review Triage Log

- 2026-07-26 follow-up audit: the complete Python engine and headless UI suite
  reconfirmed all Epic 4 behavior while integrating Epic 5; no regressions found.

### 2026-07-26 — Review pass
- intent_gap: 0
- bad_spec: 0
- patch: 9: (high 4, medium 5, low 0)
- defer: 0
- reject: 2: (high 0, medium 2, low 0)
- addressed_findings:
  - `[medium]` `[patch]` Drew the target treatment above occupied checkers so it remains visible.
  - `[medium]` `[patch]` Reused one game-over overlay and suppressed disabled-board key navigation.
  - `[high]` `[patch]` Enforced exactly one consistent winner whenever a reserve reaches zero.
  - `[medium]` `[patch]` Rejected ambiguous terminal states in which both reserves are zero.
  - `[medium]` `[patch]` Restored the existing `ui.GameState` and `ui.get_move` exports and package docstring.
  - `[high]` `[patch]` Expanded headless UI/controller and architecture tests across the promised lifecycle and stale-session paths.
  - `[high]` `[patch]` Replaced platform-dependent quit prompting with explicit Yes/No/Escape/close behavior that preserves canceled sessions.
  - `[medium]` `[patch]` Guarded completed and already-resolved turns before starting dice animation.
  - `[high]` `[patch]` Preserved in-flight animation and state exactly while quit confirmation is canceled.

## Design Notes

Use the established palette: red `#CC0000`, blue `#0000CC`, beige `#F5F5DC`, grid `#333333`, legal `#90EE90`/`#006400`, target `#FFD700`/`#B8860B`, and focus `#FF6600`. Target and legal treatments must layer rather than overwrite. A generation token must make callbacks from a prior screen/session harmless. Preserve the winning player as `current_player` when the winning placement ends the game.

## Verification

**Commands:**
- `python -m pytest -q` -- all Python engine, UI-controller, and architecture tests pass headlessly.
- `python -m compileall -q python` -- all Python sources compile.
- `npm test` -- browser regression suite passes.
- `npm run check` -- browser type/lint/build checks pass.
- `git diff --check` -- patch contains no whitespace errors.

**Manual checks (if no CLI):**
- With a display available, run `python python/main.py` and exercise menu, roll/placement/pass, game-over/restart, keyboard traversal, and Yes/No/Escape quit behavior.


## Auto Run Result

### Summary
Completed Epic 4 with an engine-owned terminal lifecycle and a local two-player Tkinter desktop game covering configuration, play, pass, victory, restart, and protected quitting.

### Files Changed
- `python/game_engine/models.py`, `python/game_engine/rules.py`, `python/game_engine/validation.py` — winner state, declaration, invariants, and terminal guards.
- `python/ui/board_view.py`, `python/ui/controls.py`, `python/ui/main.py`, `python/ui/__init__.py`, `python/main.py` — desktop presentation, orchestration, entry point, and compatibility exports.
- `python/tests/test_rules.py`, `python/tests/test_state.py`, `python/tests/test_ui.py`, `python/tests/test_architecture.py` — engine, controller, interaction, stale-session, and dependency coverage.
- `python/README.md`, `docs/python/README.md` — launch, controls, capability, and headless-testing documentation.
- `_bmad-output/planning-artifacts/epics/README.md`, `_bmad-output/planning-artifacts/epics/epic-4-local-desktop-game.md` — completed Epic 4 tracking.

### Review Findings
Applied nine review-driven patches: four high-consequence lifecycle/verification/quit fixes and five medium-consequence rendering, validation, compatibility, and guard fixes. Deferred no items and rejected two findings that misread the permitted downward dependency direction or treated an explicitly disabled, labeled future mode as missing feedback.

### Follow-up Review Recommendation
`true` — the final pass made broad, behaviorally significant fixes to terminal invariants, quit semantics, rendering, and test coverage.

### Verification
- `python -m pytest -q` — 51 passed.
- `python -m compileall -q python` — passed.
- `npm test` — 22 passed.
- `npm run check` — passed.
- `git diff --check` — passed.

### Residual Risks
The automated suite is headless; interactive widget appearance and native window-manager behavior still require a graphical desktop smoke check.
