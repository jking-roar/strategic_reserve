---
epic: 4
title: Local Desktop Game
status: not-started
source: _bmad-output/planning-artifacts/epics.md
lastReviewed: 2026-07-25
---

# Epic 4: Local Desktop Game

Two people can start, play, finish, restart, and safely quit a complete game on one desktop.

## Story Status

- 4.1 - Not started
- 4.2 - Not started
- 4.3 - Not started
- 4.4 - Not started
- 4.5 - Not started

## Stories

### Story 4.1: Start a Configured Local Game

As a player, I want to choose local multiplayer and start a game, so that two people can play on one machine.

**Acceptance Criteria:**

**Given** application launch, **when** the main menu appears, **then** it shows mode, difficulty where applicable, New Game, and Quit controls.

**Given** PvP is selected, **when** New Game is activated, **then** a correctly initialized board replaces the menu and the current player is announced.

### Story 4.2: See the Board, Dice, and Reserves

As a player, I want the complete state rendered clearly, so that I can understand the game at a glance.

**Acceptance Criteria:**

**Given** an active game, **when** it renders, **then** it shows a 6x6 grid, outlined red/blue checkers, empty squares, both reserve counts, and the current player.

**Given** a roll, **when** dice animation completes, **then** the purple column and green row values remain visible and their target has a gold treatment.

### Story 4.3: Select Only a Legal Move

As a player, I want legal destinations highlighted and clickable, so that I can complete a valid turn without memorizing constraints.

**Acceptance Criteria:**

**Given** a resolved roll, **when** legal moves render, **then** each legal square has the specified light-green/dark-green treatment and no illegal square does.

**Given** a legal square, **when** it is selected, **then** the engine accepts it and the board, reserve counters, and current player refresh immediately.

**Given** an illegal or stale square, **when** it is activated, **then** no state changes and concise feedback is presented.

### Story 4.4: Finish and Restart a Game

As a player, I want an immediate winner announcement and restart action, so that a completed game has a clear conclusion.

**Acceptance Criteria:**

**Given** a player places their last reserve checker, **when** placement completes, **then** that player is declared the winner immediately and further board input is disabled.

**Given** the centered game-over view, **when** New Game is activated, **then** the user returns to a fresh configured game flow with no prior state retained.

### Story 4.5: Confirm Quitting an Active Game

As a player, I want accidental quitting prevented, so that I do not lose a game unintentionally.

**Acceptance Criteria:**

**Given** a game is active, **when** Quit or window close is requested, **then** a Yes/No confirmation appears.

**Given** the confirmation, **when** No or Escape is selected, **then** play resumes unchanged; **when** Yes is selected, **then** the application exits cleanly.

