---
title: 'Epic 6: Accessible Desktop Release Experience'
type: 'feature'
created: '2026-07-26'
status: 'done'
baseline_revision: '883048d2ad8a3bd399fc3d29b908a554457eb02a'
final_revision: 'cac3f89'
review_loop_iteration: 0
followup_review_recommended: true
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-6-context.md'
warnings: [multiple-goals, oversized]
---

<intent-contract>

## Intent

**Problem:** The desktop game has partial keyboard input but lacks complete focus semantics, equivalent accessible state announcements, audited contrast, and a validated distributable release journey, leaving all three Epic 6 stories incomplete.

**Approach:** Harden the Tk interaction and presentation layer around authoritative engine state, add deterministic accessibility and journey coverage, package the Python application with a supported entry point, and publish a repeatable release/coverage checklist plus accurate documentation.

## Boundaries & Constraints

**Always:** Preserve `ui -> ai -> game_engine`; keep engine state authoritative and derive announcements from it; provide pointer/keyboard parity; keep arrows predictable on the 6x6 board, Enter/Space equivalent, Tab order aligned to visual order, and Escape non-destructive; expose turn, dice, target, capture, reserve, invalid-action, and winner information without color alone; preserve mutually distinguishable 3px orange focus/hover, legal, target, and disabled states meeting WCAG AA; retain 60px cells with 2px gaps and solid outlined checkers; use standard-library Tkinter and system fonts; declare every install dependency; validate PvP and both PvC modes; retain AI response budgets.

**Block If:** A supported release cannot be installed/launched from a clean Python environment without adding a non-standard runtime dependency, or the platform cannot expose equivalent accessible information through Tk without changing the established desktop framework.

**Never:** Duplicate or mutate game rules/state in accessibility code; let UI shortcuts bypass legality or terminal locking; rely on color alone; accept a manual-only claim where deterministic automation is possible; add online play, mobile, save/load, replay, tutorial, audio, themes, or unrelated browser scope.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Board navigation | Focused corner/edge/interior plus arrows | Deterministic in-grid focused square; 3px orange cue only while focused/hovered | No illegal coordinate or engine mutation |
| Activation/cancel | Enter/Space on focused square; Escape during selection/dialog | Same legal action as click; selection clears or non-destructive dialog closes | Invalid actions are announced and state stays valid |
| Overlapping states | Square is focus/hover plus legal or target | Orange cue and non-color legal/target cue remain distinguishable | Disabled/terminal board cannot activate |
| State transition | Roll, placement, capture, reserve, pass/turn, error, or win | Concise visible accessible text reflects authoritative state, including coordinates/dice where relevant | No stale announcement becomes mutable game state |
| Clean install | Supported Python/Tk desktop environment and built artifact | Install and console launch use only declared requirements | Missing display/Tk produces documented actionable behavior |
| Complete journey | PvP, rudimentary PvC, advanced PvC | Start, roll, captures, placement, win, restart, and quit satisfy coverage map | No critical defect; stale AI work cannot affect restart/quit |

</intent-contract>

## Code Map

- `python/ui/board_view.py` -- Canvas navigation, activation, focus/hover rendering, square descriptions, and cancel binding.
- `python/ui/controls.py` -- menu/control traversal and visible accessible status surface.
- `python/ui/main.py` -- authoritative transition announcements, focus restoration, lifecycle, restart, and quit orchestration.
- `python/tests/test_ui.py` -- headless controller, navigation, announcement, locking, and lifecycle contracts.
- `python/tests/test_ui_tk.py` -- display-backed Tk focus, traversal, bindings, rendering, and dialog checks.
- `python/tests/test_release_journeys.py` -- deterministic complete PvP/PvC release journeys.
- `python/pyproject.toml` -- build backend, package metadata, and installed launch entry point.
- `README.md`, `python/README.md`, `docs/python/README.md` -- release usage, attribution, support, controls, tests, and limitations.
- `docs/python/release-checklist.md` -- Epic 6 coverage map, contrast evidence, automated/manual release gate.
- `_bmad-output/planning-artifacts/epics*.md` -- synchronized Epic 6 completion records after verification.

## Tasks & Acceptance

**Execution:**
- [x] `python/ui/board_view.py` -- separate actual focus and hover ownership, render compliant overlapping cues and checker/grid geometry, support deterministic arrows/activation/Escape, and expose square/state descriptions.
- [x] `python/ui/controls.py`, `python/ui/main.py`, `python/ui/__init__.py` -- establish visual-order traversal/focus restoration and concise non-color announcements for every required authoritative state transition without weakening AI/session safety.
- [x] `python/tests/test_ui.py`, `python/tests/test_ui_tk.py` -- prove keyboard boundaries, Tab/Shift+Tab, Enter/Space, Escape, focus/hover/disabled overlap, announcement content, terminal locking, dialogs, and restart focus; skip display-backed tests only when no display exists.
- [x] `python/tests/test_release_journeys.py` -- exercise deterministic complete PvP and both PvC lifecycles including setup, rolls, captures, placement, win, restart, quit, and stale-work safety.
- [x] `python/pyproject.toml`, packaging modules -- create a standards-compliant wheel/sdist and console entry point that installs and imports from a clean environment without undeclared Python dependencies.
- [x] `docs/python/release-checklist.md` -- map every Epic 6 criterion to repeatable automated/manual evidence, calculate contrast for all specified states, specify keyboard/screen-reader journeys, and require zero critical defects.
- [x] `README.md`, `python/README.md`, `docs/python/README.md` -- document artifact installation/launch/test commands, keyboard controls, attribution, supported Python/Tk desktop/display requirements, accessibility behavior, and known limitations.
- [x] `_bmad-output/planning-artifacts/epics.md`, `_bmad-output/planning-artifacts/epics/*.md` -- mark Epic 6 stories complete only after all automated gates and checklist evidence pass.

**Acceptance Criteria:**
- Given board or pointer focus, when arrows, Enter/Space, Tab/Shift+Tab, or Escape are used, then every supported action has pointer parity, traversal follows visual order, cancellation is non-destructive, and a visible 3px orange cue remains distinct from legal/target/disabled cues.
- Given any required gameplay transition, when it occurs, then concise visible accessible text communicates the active player, dice/target and capture/reserve/outcome details as applicable without relying only on color or accepting input after a win.
- Given all normal, hover, focus, legal, target, overlap, and disabled states, when the documented audit is executed, then text and essential indicators meet WCAG AA and visible-focus requirements with recorded ratios/evidence.
- Given a clean supported environment, when the built artifact is installed and its documented entry point invoked, then the Tk game opens without undeclared dependencies and documentation contains attribution, controls, test commands, support constraints, and limitations.
- Given automated tests and the manual checklist, when complete PvP and both PvC journeys cover start, rolls, captures, placement, win, restart, and quit, then every coverage-map item passes with no critical defect and AI budgets remain under one/five seconds.

## Spec Change Log

## Review Triage Log

### 2026-07-26 — Review pass
- intent_gap: 0
- bad_spec: 0
- patch: 17: (high 7, medium 7, low 3)
- defer: 0
- reject: 1: (high 1, medium 0, low 0)
- addressed_findings:
  - `[high]` `[patch]` Preserved keyboard square descriptions and made pointer hover announce its actual square without generic refreshes erasing either result.
  - `[high]` `[patch]` Preserved independent legal, target, disabled, and interaction cues in overlapping states and aligned the rendered gold target with audited contrast evidence.
  - `[medium]` `[patch]` Synchronized the compliant dark-orange focus token and clarified Escape as a non-destructive status-restoration action rather than a fictitious mutable selection.
  - `[high]` `[patch]` Replaced engine-only near-win claims with controller-level PvP and real Blue rudimentary/advanced lifecycle, restart, quit, stale-work, and recovery coverage.
  - `[high]` `[patch]` Expanded native Tk coverage for both activation keys, wrapping, forward/backward traversal, hover, overlap/disabled locking, dialog Escape, terminal focus, and restart behavior.
  - `[medium]` `[patch]` Added a dependency-light launcher that reports a missing Tk module or display without an import traceback.
  - `[high]` `[patch]` Included authoritative placement/pass/capture/reserve/turn/winner details in AI recovery announcements and rejected unknown player tokens.
  - `[medium]` `[patch]` Removed the read-only status label from Tab traversal while retaining its stable native name and made Board-to-Roll traversal explicit.
  - `[medium]` `[patch]` Corrected Windows installation guidance, expanded actual overlap contrast evidence, and stopped release documentation from implying unexecuted platform sign-off.

## Design Notes

Keep announcements as rendered text derived at transition boundaries from pre/post engine snapshots rather than a second accessibility state machine. Unit-test pure navigation, description, transition-summary, and contrast helpers; reserve display-backed tests for actual Tk traversal/focus/binding behavior. Package the existing layered modules rather than relocating rule ownership.

## Verification

**Commands:**
- `python -m pytest -q python/tests` -- expected: engine, AI, headless UI, Tk (when display is available), accessibility, journey, timing, and architecture tests pass.
- `python -m compileall -q python` -- expected: every Python module compiles.
- `python -m build python/` -- expected: wheel and sdist build from declared metadata.
- `python -m venv /tmp/strategic-reserve-venv && /tmp/strategic-reserve-venv/bin/pip install python/dist/*.whl` -- expected: clean installation succeeds without undeclared Python dependencies.
- `xvfb-run -a /tmp/strategic-reserve-venv/bin/strategic-reserve` -- expected: installed desktop entry point smoke-launches on a virtual display.
- `npm test && npm run check` -- expected: prior browser implementation remains green.
- `git diff --check` -- expected: no whitespace errors.

**Manual checks (if no CLI):**
- Complete the release checklist on every declared supported desktop using keyboard-only and a platform screen reader; verify focus, announcements, contrast evidence, all three game-mode journeys, restart, and quit with no critical defect.


## Auto Run Result

- Summary: Completed Epic 6 with full keyboard board control, authoritative non-color state announcements, audited visual cues, standards-based packaging, and repeatable desktop release validation.
- Files changed: `python/ui/` implements focus/hover/cancel semantics and transition announcements; `python/tests/` covers headless, native Tk, launcher, and complete controller journeys; packaging and public documentation define the supported artifact; planning artifacts record Epic 6 completion.
- Review findings: 17 patches applied, 0 items deferred, and 1 finding rejected because native screen-reader announcement behavior is platform-owned and explicitly covered by the delivered per-platform manual release gate rather than safely solvable through an undeclared bridge.
- Follow-up review recommendation: true; review-driven changes substantially expanded controller lifecycle coverage, overlap rendering, accessibility messaging, and launcher behavior.
- Verification: `xvfb-run -a python -m pytest -q python/tests` passed with 93 tests; `python -m compileall -q python` passed; wheel/sdist build, fresh-wheel install/import, and Xvfb installed-entry smoke passed; `npm test` passed with 22 tests; `npm run check` and `git diff --check` passed.
- Residual risks: Screen-reader exposure depends on each operating system's Tk accessibility bridge, so every release still requires the documented Windows, macOS, and Linux manual sign-off; no unexecuted platform result is claimed by this implementation run.
