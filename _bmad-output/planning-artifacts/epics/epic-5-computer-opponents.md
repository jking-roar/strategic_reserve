---
epic: 5
title: Computer Opponents
status: done
source: _bmad-output/planning-artifacts/epics.md
lastReviewed: 2026-07-25
---

# Epic 5: Computer Opponents

A solo player can choose between fast random play and bounded strategic play without compromising engine integrity.

## Story Status

- 5.1 - Done
- 5.2 - Done
- 5.3 - Done
- 5.4 - Done

## Stories

### Story 5.1: Play Against a Rudimentary AI

As a solo player, I want a quick random opponent, so that I can practice casually.

**Acceptance Criteria:**

**Given** any valid state with legal moves, **when** rudimentary `get_move` runs, **then** it returns one of those moves without mutating input state and completes within one second.

**Given** no legal move, **when** it runs, **then** it returns `None` without crashing or hanging.

### Story 5.2: Play Against an Advanced AI

As a solo player, I want a strategic opponent, so that practice remains challenging.

**Acceptance Criteria:**

**Given** a valid state, **when** advanced `get_move` runs, **then** it evaluates candidate play using all 36 possible next-roll outcomes and returns a legal move.

**Given** a configured search budget, **when** the position is complex, **then** a best-so-far legal move returns within five seconds.

### Story 5.3: Configure and Run a PvC Game

As a solo player, I want to choose AI difficulty, so that opponent strength matches my preference.

**Acceptance Criteria:**

**Given** PvC mode, **when** rudimentary or advanced difficulty is selected and the game starts, **then** the matching AI controls its assigned color.

**Given** an AI turn, **when** its move completes, **then** the same roll, capture, placement, render, and win rules used for humans apply and human input cannot race the AI.

### Story 5.4: Verify AI Safety and Performance

As a player, I want dependable AI turns, so that unusual positions cannot freeze or corrupt my game.

**Acceptance Criteria:**

**Given** a corpus covering full, sparse, capture-heavy, no-move, and near-win states, **when** both AIs run, **then** every result is legal or `None`, input states remain unchanged, and no run crashes or hangs.

**Given** timed performance tests, **when** each difficulty runs under documented conditions, **then** rudimentary remains below one second and advanced remains below five seconds.
