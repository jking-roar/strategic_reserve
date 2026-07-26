---
epic: 3
title: Complete Python Capture and Placement Rules
status: done
source: _bmad-output/planning-artifacts/epics.md
lastReviewed: 2026-07-26
---

> **Historical acceptance criteria — superseded by Epic 7:** References below to no-move or nullable AI behavior record the earlier contract. Current engines prove every valid active roll has a legal placement.


# Epic 3: Complete Python Capture and Placement Rules

Players can resolve enemy, friendly, and empty targets with correct captures and legal destinations.

## Story Status

- 3.1 - Done
- 3.2 - Done
- 3.3 - Done
- 3.4 - Done

## Stories

### Story 3.1: Resolve an Enemy-Group Hit

As a player, I want a rolled enemy group removed, so that the enemy-hit rule changes board control correctly.

**Acceptance Criteria:**

**Given** the target belongs to an enemy group, **when** the roll resolves, **then** the whole maximal group is removed and its size is added to the enemy reserve.

**Given** the capture resolves, **when** legal moves are requested, **then** every empty square is offered and occupied squares are excluded.

### Story 3.2: Resolve a Friendly-Group Hit

As a player, I want adjacent enemy groups captured and placement constrained, so that friendly hits follow the tactical rule.

**Acceptance Criteria:**

**Given** a friendly target group adjacent to one or more enemy groups, **when** the roll resolves, **then** every orthogonally adjacent enemy group is removed once and returned to its owner's reserve.

**Given** the resolved friendly group, **when** legal moves are requested, **then** only empty squares orthogonally adjacent to any group member are returned.

**Given** no adjacent empty square, **when** resolution completes, **then** the engine exposes no placement and advances according to the documented no-move rule without hanging.

### Story 3.3: Resolve an Empty-Square Hit

As a player, I want an empty target to allow free placement, so that I can choose any available square.

**Acceptance Criteria:**

**Given** an empty target, **when** legal moves are calculated, **then** all and only empty board squares are returned.

**Given** any returned destination, **when** placement occurs, **then** no checker is captured and normal reserve and turn updates apply.

### Story 3.4: Preserve Rule Invariants Across Full Turns

As a player, I want every full turn to remain valid, so that long games cannot corrupt themselves.

**Acceptance Criteria:**

**Given** each target category and boundary location, **when** automated scenario tests execute a full turn, **then** checker totals, reserve totals, occupancy, and active-player invariants hold.

**Given** a failed action, **when** state is compared before and after, **then** no partial capture, placement, or turn transition remains.
