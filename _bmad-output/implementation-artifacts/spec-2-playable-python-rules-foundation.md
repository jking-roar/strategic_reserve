---
title: 'Epic 2: Playable Python Rules Foundation'
type: 'feature'
created: '2026-07-25'
status: 'done'
review_loop_iteration: 0
followup_review_recommended: false
baseline_revision: '6cf9cdc3d9adafbe47ba8544fb9c085ccfe3ec5c'
final_revision: '9fed0bd7fe4f96a1a2f9c8953f3301388a18866e'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
warnings:
  - multiple-goals
---

<intent-contract>

## Intent

**Problem:** The repository has a complete browser rules implementation but no Python gameplay core, so Epic 2 cannot progress and later desktop/UI/AI work has no authoritative Python engine to build on.

**Approach:** Build a Python-first layered skeleton (`game_engine`, `ai`, `ui`) plus deterministic engine modules for state creation, validation, orthogonal group discovery, dice targeting, and legal reserve placement with invariant-preserving errors; back all of it with focused tests and a runnable test command.

## Boundaries & Constraints

**Always:** Preserve one-way dependency flow `ui -> ai -> game_engine`; keep mutable state authority inside `game_engine`; represent board/state with dataclasses and zero-based absolute coordinates; raise explicit domain errors (`IllegalMoveError`, `InvalidGameStateError`) on invalid operations without mutating state; enforce Epic 2 acceptance criteria for stories 2.1-2.4.

**Block If:** Existing repository constraints require a different Python runtime than what Epic 2 artifacts specify; import-boundary verification cannot be implemented without introducing heavyweight external tooling that conflicts with repo policy; acceptance criteria conflict with documented official rules.

**Never:** Modify browser game behavior to satisfy Python stories; introduce server/network dependencies; bypass validation by silently coercing invalid state; merge diagonal neighbors in group discovery; allow illegal placement side effects.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| NEW_GAME_INIT | Fresh engine call to create a game | 6x6 board with official 12 starting checkers, reserves `{red:6, blue:6}`, starting player recorded, pending turn state initialized | No error expected |
| INVALID_STATE_SHAPE | Board not 6x6, invalid token value, impossible reserve count, or out-of-range coordinate | Validation fails atomically and reports the first violated invariant | Raise `InvalidGameStateError`; do not mutate inspected state |
| ORTHOGONAL_GROUP | Start from a checker in a mixed board with orthogonal and diagonal touches | Return each same-color orthogonally connected coordinate exactly once; diagonal-only neighbors excluded | No error expected |
| ROLL_TARGET_MAPPING | Dice roll values (1..6,1..6) for active player | Persist roll values and computed absolute target coordinate | Raise `InvalidGameStateError` only for impossible internal state |
| LEGAL_PLACE_ADVANCE | Legal empty destination and reserve > 0 | Place one checker, decrement active reserve by one, clear transient turn fields, toggle current player once | No error expected |
| ILLEGAL_PLACE_OR_EMPTY_RESERVE | Occupied/out-of-bounds destination or reserve already zero | Reject placement and leave board, reserves, active player, and roll context unchanged | Raise `IllegalMoveError` |

</intent-contract>

## Code Map

- `site/js/game-engine.js` -- authoritative behavior reference for rules parity and flood-fill semantics.
- `_bmad-output/implementation-artifacts/epic-2-context.md` -- distilled Epic 2 requirements/constraints used for planning.
- `python/pyproject.toml` -- Python tooling entry point and pytest configuration.
- `python/game_engine/models.py` -- dataclasses and immutable constants for board/state payloads.
- `python/game_engine/errors.py` -- domain-specific exception taxonomy.
- `python/game_engine/state.py` -- canonical initial-state factory and deep-copy-safe helpers.
- `python/game_engine/validation.py` -- invariant checks and explicit invalid-state rejection.
- `python/game_engine/groups.py` -- orthogonal flood-fill group discovery utilities.
- `python/game_engine/rules.py` -- dice roll, target resolution, legal destinations, and placement transition logic.
- `python/ai/__init__.py` -- AI package boundary marker importing from engine only.
- `python/ui/__init__.py` -- UI package boundary marker importing from AI/engine only.
- `python/tests/test_architecture.py` -- package import boundary tests for story 2.1.
- `python/tests/test_state.py` -- initialization and validation tests for story 2.2.
- `python/tests/test_groups.py` -- orthogonal group tests for story 2.3.
- `python/tests/test_rules.py` -- dice and placement behavior tests for story 2.4.

## Tasks & Acceptance

**Execution:**
- [x] `python/pyproject.toml` -- add minimal Python project metadata and pytest command wiring -- enables clean-checkout test execution.
- [x] `python/game_engine/__init__.py` -- expose stable public engine API symbols -- provides import anchor for downstream layers.
- [x] `python/game_engine/errors.py` -- define `StrategicReserveError`, `InvalidGameStateError`, `IllegalMoveError` -- codifies explicit domain failures.
- [x] `python/game_engine/models.py` -- implement dataclasses (`DiceRoll`, `TurnContext`, `GameState`) and constants for tokens/dimensions -- establishes typed state model.
- [x] `python/game_engine/state.py` -- implement official initial board constructor and safe state-clone utility -- satisfies new-game baseline.
- [x] `python/game_engine/validation.py` -- implement invariant validation entry points for board shape, tokens, reserves, player, and coordinates -- enforces atomic rejection of malformed states.
- [x] `python/game_engine/groups.py` -- implement orthogonal-only flood-fill and derived maximal-group helper -- enables capture-era connectivity correctness.
- [x] `python/game_engine/rules.py` -- implement dice rolling, target-coordinate mapping from active player perspective, legal-empty placement, reserve decrement, and turn advance -- delivers playable turn foundation.
- [x] `python/ai/__init__.py` and `python/ui/__init__.py` -- scaffold layer packages with dependency-safe imports -- fulfills layered skeleton requirement.
- [x] `python/tests/test_architecture.py` -- verify imports reflect `ui -> ai -> game_engine` and forbid reverse dependencies -- guards architecture contract.
- [x] `python/tests/test_state.py` -- verify official initial setup and invalid-state rejection behavior -- covers story 2.2 AC.
- [x] `python/tests/test_groups.py` -- verify orthogonal connectivity and diagonal separation -- covers story 2.3 AC.
- [x] `python/tests/test_rules.py` -- verify roll ranges/target mapping, legal placement effects, and illegal atomic failures -- covers story 2.4 AC.
- [x] `python/README.md` -- document Python test command and module layout -- satisfies clean-checkout usability.

**Acceptance Criteria:**
- Given a clean checkout, when `python -m pytest` runs from `python/`, then tests execute and `game_engine`, `ai`, and `ui` import successfully.
- Given dependency-boundary tests, when modules are inspected, then `game_engine` imports neither `ai` nor `ui`, and `ai` imports no `ui` code.
- Given a new game state, when inspected, then the board contains exactly the official twelve starting checkers, each reserve is six, and a starting player is recorded.
- Given malformed dimensions/colors/reserve counts/coordinates, when validation runs, then `InvalidGameStateError` is raised with no state mutation.
- Given same-color orthogonal adjacency, when group discovery starts at any member, then every and only orthogonally connected member is returned once.
- Given diagonal-only contact, when group discovery runs, then pieces remain in separate groups.
- Given an active player, when dice roll, then two values in `[1,6]` are recorded and mapped to one absolute board coordinate.
- Given a legal empty destination, when placement occurs, then one reserve checker is placed and turn advances exactly once.
- Given illegal destination or empty reserve, when placement is attempted, then `IllegalMoveError` is raised and state remains unchanged.

## Spec Change Log

## Review Triage Log

### 2026-07-25 — Review pass
- intent_gap: 0
- bad_spec: 0
- patch: 7: (high 1, medium 4, low 2)
- defer: 0
- reject: 0
- addressed_findings:
  - `[high]` `[patch]` Blocked re-roll within the same turn in `python/game_engine/rules.py` to preserve turn integrity.
  - `[medium]` `[patch]` Added dice payload shape/type validation in `python/game_engine/validation.py` to avoid non-domain exceptions.
  - `[medium]` `[patch]` Hardened group APIs in `python/game_engine/groups.py` to reject invalid color and invalid board payload/token inputs.
  - `[medium]` `[patch]` Enforced finite/numeric RNG outputs in `python/game_engine/rules.py` for robust die generation.
  - `[medium]` `[patch]` Enforced no-placement-before-roll guard in `python/game_engine/rules.py`.
  - `[low]` `[patch]` Rejected bool-valued reserves in `python/game_engine/validation.py`.
  - `[low]` `[patch]` Rejected bool-valued coordinates in `python/game_engine/validation.py`.

## Design Notes

- Use coordinate tuples `(row, col)` internally for zero-based absolute board math and maintain player-perspective conversion only in `target_from_roll`.
- Keep `apply_placement` pure by copying state before mutation and committing only after all guards pass; this preserves atomic failure semantics required by acceptance criteria.

## Verification

**Commands:**
- `cd python; python -m pytest` -- expected: all Epic 2 foundation tests pass.
- `cd python; python -m pytest -k architecture` -- expected: package boundary tests pass.

## Auto Run Result

- Summary: Delivered Epic 2 Python rules foundation with layered package skeleton, deterministic game-state/validation/group/rules modules, and edge-case hardened behavior validated by automated tests.
- Files changed:
  - `python/pyproject.toml` -- Python project metadata and pytest configuration.
  - `python/README.md` -- Python module layout and test instructions.
  - `python/game_engine/__init__.py` -- public engine API exports.
  - `python/game_engine/errors.py` -- domain exception hierarchy.
  - `python/game_engine/models.py` -- constants and dataclasses for core state.
  - `python/game_engine/state.py` -- canonical game initialization and cloning.
  - `python/game_engine/validation.py` -- comprehensive state and coordinate validation.
  - `python/game_engine/groups.py` -- orthogonal group discovery with input hardening.
  - `python/game_engine/rules.py` -- dice rolling, target mapping, and placement transitions.
  - `python/ai/__init__.py` -- AI package scaffold.
  - `python/ui/__init__.py` -- UI package scaffold.
  - `python/tests/test_architecture.py` -- layer dependency checks.
  - `python/tests/test_state.py` -- state initialization and validation tests.
  - `python/tests/test_groups.py` -- group and edge-case tests.
  - `python/tests/test_rules.py` -- dice/placement and edge-case tests.
  - `.gitignore` -- Python cache artifact ignores.
  - `_bmad-output/implementation-artifacts/epic-2-context.md` -- compiled planning context for Epic 2.
  - `_bmad-output/implementation-artifacts/spec-2-playable-python-rules-foundation.md` -- implementation spec, review log, and completion record.
- Review findings breakdown: patches applied 7, deferred 0, rejected 0.
- Follow-up review recommendation: false.
- Verification performed:
  - `cd python; python -m pytest` -> `24 passed, 1 warning`.
- Residual risks: pytest emits an external `pytest-asyncio` deprecation/config warning unrelated to Epic 2 logic; no functional failures observed.
