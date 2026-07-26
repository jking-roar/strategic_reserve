---
title: 'Epic 7: Remove Unreachable No-Legal-Move Flow'
type: 'refactor'
created: '2026-07-26T00:00:00Z'
status: 'done'
review_loop_iteration: 0
baseline_revision: 'd6ead2e05c6cdef92d1c18006e06bfdd9edaaf5b'
final_revision: 'c36b718cfe85cb23d5edfa964ac3b37e96325825'
followup_review_recommended: true
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-7-context.md'
warnings:
  - multiple-goals
---

<intent-contract>

## Intent

**Problem:** Both editions preserve pass controls, nullable AI behavior, and documentation for a no-legal-placement state that cannot occur in a valid active game. This expands state machines and allows fabricated invalid states to masquerade as normal turns.

**Approach:** Enforce the non-empty legal-placement invariant at each engine boundary, remove pass/no-move branches through engines, AI, and UI, and align tests and current documentation with direct roll-to-placement play.

## Boundaries & Constraints

**Always:** Preserve twelve-checker conservation per player, capture and target semantics, copy-on-write transitions, immediate victory, absolute engine/AI coordinates, UI→AI→engine dependency direction, AI immutability/deadlines, accessibility, and equivalent Python/browser outcomes. Every valid active resolved roll has a non-empty set of unique, empty, in-bounds destinations; malformed resolved states fail as domain errors.

**Block If:** Official rules contradict the proven invariant, or enforcing it requires changing checker conservation, capture semantics, target mapping, or victory timing.

**Never:** Add a replacement pass/recovery state, let UI or AI repair invalid engine output, weaken validation or deadlines, rewrite completed historical results as though they never occurred, or expand into unrelated gameplay/design work.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Valid roll | Valid active state; any dice pair | Captures resolve and at least one empty legal coordinate enters placement | No error expected |
| Friendly target | Maximal friendly group with empty/enemy boundary | Adjacent enemies are removed; empty boundary destinations remain | No error expected |
| Fabricated no-move | Active resolved state with empty legal list | State is rejected at engine boundary | Python/JS domain error; no pass flow |
| AI turn | Valid resolved active state | Each difficulty returns a legal coordinate without mutation and within its deadline | Invalid engine state propagates; UI does not pass |
| Terminal state | Winner or exhausted active reserve | Further roll/place is rejected | Existing terminal-state domain error |

</intent-contract>

## Code Map

- `python/game_engine/{validation.py,rules.py,__init__.py}` -- Python invariants, transitions, and public API.
- `site/js/game-engine.js` -- browser validation and roll/place state machine.
- `python/ai/*.py`, `site/js/ai.js` -- non-null legal-coordinate strategies.
- `python/ui/{controls.py,main.py,presentation.py}`, `site/{index.html,js/app.js}` -- pass controls, focus, announcements, and AI orchestration.
- `python/tests`, `site/tests` -- engine, parity, AI, UI, accessibility, architecture, static, and journey coverage.
- `README.md`, `site/README.md`, `python/README.md`, `docs/python`, `_bmad-output/planning-artifacts` -- current claims and superseded historical records.

## Tasks & Acceptance

**Execution:**
- [x] `python/game_engine/validation.py`, `python/game_engine/rules.py`, `python/game_engine/__init__.py` -- reject incoherent/resolved-empty states, assert non-empty computed moves, and remove `pass_turn` and pass guidance while preserving rules.
- [x] `site/js/game-engine.js` -- add authoritative conservation/phase/context/move validation, require placement after every valid roll, and remove `await-pass`/`pass`.
- [x] `python/ai/*.py`, `site/js/ai.js` -- make valid resolved input return a non-null legal coordinate while retaining immutability and time budgets.
- [x] `python/ui/controls.py`, `python/ui/main.py`, `python/ui/presentation.py`, `site/index.html`, `site/js/app.js` -- remove pass UI/orchestration/copy and retain coherent placement focus, fallback safety, and announcements.
- [x] `python/tests`, `site/tests` -- replace synthetic no-move/pass tests with exhaustive 36-roll invariant, malformed-state rejection, conservation, parity, non-null AI, absent-control, focus, and journey checks.
- [x] `README.md`, `site/README.md`, `python/README.md`, `docs/python/*`, `_bmad-output/planning-artifacts/**/*`, `_bmad-output/implementation-artifacts/*` -- replace current pass claims with the invariant and clearly mark completed contradictory artifacts as historical/superseded.

**Acceptance Criteria:**
- Given any representative valid active state for either player, when all 36 rolls resolve in either engine, then each produces a non-empty set containing only unique empty in-bounds squares with equivalent rule semantics and conserved checkers.
- Given a fabricated active resolved state with no legal moves, when an engine API validates or consumes it, then it is rejected rather than advanced.
- Given either AI difficulty and valid resolved state, when a move is selected, then a legal coordinate is returned within the existing deadline without mutating input.
- Given browser or desktop play, when a roll resolves, then focus and announcements proceed directly to legal placement and no pass control, pass copy, or automatic pass branch exists.
- Given current normative docs and historical implementation artifacts, when searched, then current guidance states the invariant and any retained contradictory completion record is explicitly labeled superseded.

## Spec Change Log

## Review Triage Log

### 2026-07-26 — Review pass
- intent_gap: 0
- bad_spec: 0
- patch: 5: (high 2, medium 2, low 1)
- defer: 3: (medium 3)
- reject: 7: (medium 3, low 4)
- addressed_findings:
  - `[high]` `[patch]` Added browser async engine/AI error boundaries that clear busy state and return safely to setup instead of leaving controls locked.
  - `[high]` `[patch]` Made desktop AI recovery handle an unexpectedly empty fallback list without leaking `IndexError` or leaving the interface locked.
  - `[medium]` `[patch]` Validated browser AI budgets and clock results as finite, non-negative, and capped below five seconds.
  - `[medium]` `[patch]` Rejected non-integer browser target coordinates rather than accepting numeric strings through key coercion.
  - `[low]` `[patch]` Removed two remaining current Python README references to obsolete pass behavior and strengthened the AI domain-error assertion.

## Design Notes

Validation is the deletion boundary: public transitions validate input and output, so AI and UI may rely on a non-empty legal list. Python should reuse its domain validation; browser validation should mirror the same conservation, terminal, turn-context, and coordinate constraints. Historical `done` specs remain auditable by adding a prominent Epic 7 supersession note instead of altering their original contracts/results.

## Verification

**Commands:**
- `python -m pytest -q python/tests` -- expected: all engine, AI, UI, accessibility, architecture, and journey tests pass.
- `python -m compileall -q python` -- expected: Python sources compile.
- `npm test` -- expected: browser engine, AI, DOM, static, and invariant suites pass.
- `npm run check` -- expected: browser syntax/static checks pass.
- `python -m build python/` -- expected: desktop release artifacts build.
- `git diff --check` -- expected: no whitespace errors.
- `rg -n -i 'await-pass|pass_turn|Pass — No Legal Play|no-move pass|No legal placement|explicit pass|forced pass' README.md site python docs _bmad-output` -- expected: only Epic 7 and explicitly superseded historical records remain.

## Auto Run Result

Implemented the legal-placement invariant across both engines and removed the unreachable pass lifecycle from engine APIs, AI contracts, browser and desktop interfaces, tests, and current documentation. Python now rejects incoherent resolved state and browser transitions validate conservation, phase, turn context, and legal coordinates. Both AIs return coordinates for valid resolved turns, and presentation flows proceed directly from roll to placement.

Changed engine, AI, UI, test, README, release-checklist, PRD, epic/context, and historical-spec files described in the Code Map and completed task list above. Historical completion records retain their original contracts under explicit Epic 7 supersession notices.

Review triage applied five patches, deferred three broader validation/parity/property-test hardening opportunities to `deferred-work.md`, and rejected seven findings that were redundant, pre-existing, unsupported by the intent, or adequately covered by existing tests. Because review patches affected failure recovery and AI deadline enforcement across both editions, an independent follow-up review is recommended.

Verification passed: `python -m pytest -q python/tests` (87 passed, 5 display-dependent skipped), `python -m compileall -q python`, `npm test` (23 passed), `npm run check`, `python -m build python/`, and `git diff --check`. Residual risk is limited to the explicitly deferred canonical-state authenticity, direct cross-edition comparison, and generated trajectory coverage; current engines independently cover every initial-board dice outcome and the required rule categories.
