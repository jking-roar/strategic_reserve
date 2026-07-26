---
epic: 7
title: Remove Unreachable No-Legal-Move Flow
status: backlog
source: _bmad-output/planning-artifacts/epics.md
lastReviewed: 2026-07-26
---

# Epic 7: Remove Unreachable No-Legal-Move Flow

Players and maintainers encounter only states permitted by the official rules, without pass controls or defensive AI branches for an unreachable no-placement condition.

## Rules Determination

A valid, non-terminal Strategic Reserve turn cannot resolve with zero legal placements:

1. Each player owns twelve checkers across the board and reserve. The board therefore contains at most 24 checkers and always has at least 12 empty squares.
2. An empty target permits placement on any empty square.
3. An enemy target removes at least the target's group, so the target square itself becomes an available empty square.
4. A friendly target belongs to a maximal friendly group. Because the board is not full, that group is a proper subset of the connected 6×6 grid and has an orthogonal boundary. A boundary square cannot contain a friendly checker (otherwise it would be in the maximal group); it is either already empty or belongs to an adjacent enemy group removed before placement. It is therefore empty when legal destinations are calculated.
5. A player with an empty reserve has already won, so reserve exhaustion cannot create an active no-placement turn.

The existing no-legal-move/pass behavior handles invalid or manually fabricated states rather than a position reachable under the official rules.

## Story Status

- 7.1 - Backlog
- 7.2 - Backlog
- 7.3 - Backlog

## Stories

### Story 7.1: Encode the Legal-Placement Invariant

As a maintainer, I want every active resolved roll to contain at least one legal destination, so that impossible states fail at the engine boundary instead of entering a pass flow.

**Acceptance Criteria:**

**Given** a valid non-terminal state and any of the 36 rolls, **when** the roll resolves, **then** at least one legal placement is produced.

**Given** conservation of twelve checkers per player on a 36-square board, **when** any valid state is inspected, **then** the invariant is documented and tested that at most 24 squares are occupied and at least 12 are empty.

**Given** an empty or enemy target, **when** the rules resolve the target, **then** an existing or newly emptied square is available; **given** a friendly target, **then** the maximal friendly group has an orthogonal boundary containing an empty square or an enemy checker that is removed.

**Given** a non-terminal resolved state with an empty legal-move list, **when** it is validated, **then** it is rejected as invalid rather than accepted as passable.

### Story 7.2: Remove Pass Handling from Both Game Engines

As a maintainer, I want the Python and browser engines to model only reachable turn transitions, so that their APIs and state machines remain small and consistent.

**Acceptance Criteria:**

**Given** the Python engine, **when** cleanup is complete, **then** `pass_turn`, no-placement exceptions, and exports/tests used solely by that path are removed while roll, placement, capture, conservation, and victory behavior remain unchanged.

**Given** the browser engine, **when** cleanup is complete, **then** `await-pass`, `pass`, no-placement messages, and synthetic pass tests are removed, and every resolved active roll enters placement.

**Given** any active player, valid state, and dice pair, **when** the Python and browser engines resolve equivalent positions, **then** both produce a non-empty legal set containing only empty in-bounds squares.

### Story 7.3: Remove Pass Handling from AI, UI, and Documentation

As a player, I want every turn to proceed directly from rolling to placing, so that the interface does not describe or expose an impossible action.

**Acceptance Criteria:**

**Given** either AI difficulty, **when** it receives a valid resolved active state, **then** it returns a legal coordinate; nullable no-move branches and related recovery behavior are removed without weakening deadline or immutability guarantees.

**Given** either browser or desktop UI, **when** a roll resolves, **then** no pass control, pass announcement, acknowledgment focus path, or automatic AI pass branch exists.

**Given** project requirements, READMEs, accessibility text, implementation specs, and tests, **when** the cleanup is reviewed, **then** normative claims that no-legal-play is supported are removed or replaced by the proven invariant, while historical completed artifacts are clearly retained as historical or updated consistently.

**Given** the complete automated suites, **when** they run after cleanup, **then** all engine, AI, UI, static, architecture, and release-journey checks pass with new invariant coverage in place.
