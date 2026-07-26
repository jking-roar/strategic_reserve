---
epic: 2
title: Playable Python Rules Foundation
status: done
source: _bmad-output/planning-artifacts/epics.md
lastReviewed: 2026-07-25
---

# Epic 2: Playable Python Rules Foundation

Players can create a valid game, roll dice, inspect groups, and place pieces through a deterministic engine API.

## Story Status

- 2.1 - Done
- 2.2 - Done
- 2.3 - Done
- 2.4 - Done

## Stories

### Story 2.1: Establish the Layered Application Skeleton

As a developer, I want enforceable package boundaries and test tooling, so that gameplay features grow on a reliable foundation.

**Acceptance Criteria:**

**Given** a clean checkout, **when** the documented test command runs, **then** the game-engine, AI, and UI packages import successfully and tests execute.

**Given** package dependency checks, **when** imports are inspected, **then** the engine imports neither AI nor UI and AI imports no UI code.

### Story 2.2: Create and Validate a Game State

As a player, I want every new game to begin in the official position, so that play starts fairly.

**Acceptance Criteria:**

**Given** a new game, **when** its state is inspected, **then** the 6x6 board contains the prescribed twelve checkers, each reserve contains six, and the starting player is recorded.

**Given** malformed dimensions, colors, counts, or coordinates, **when** state validation runs, **then** `InvalidGameStateError` is raised without mutating state.

### Story 2.3: Discover Orthogonal Groups

As a player, I want connected checker groups identified accurately, so that captures follow the rules.

**Acceptance Criteria:**

**Given** same-color pieces joined orthogonally, **when** group discovery starts from any member, **then** every and only orthogonally connected member is returned once.

**Given** pieces touching only diagonally, **when** groups are discovered, **then** they remain separate groups.

### Story 2.4: Roll Dice and Place a Reserve Checker

As a player, I want a roll and placement to update one authoritative state, so that turns can progress consistently.

**Acceptance Criteria:**

**Given** a current player, **when** dice are rolled, **then** two values from one through six are recorded and map to one absolute board coordinate.

**Given** a legal empty destination, **when** the player places, **then** one checker moves from their reserve to that square and the turn advances exactly once.

**Given** an illegal destination or empty reserve, **when** placement is attempted, **then** `IllegalMoveError` is raised and state remains unchanged.
