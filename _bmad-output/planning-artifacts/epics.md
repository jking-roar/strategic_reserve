---
stepsCompleted: ['step-01-validate-prerequisites', 'step-02-design-epics', 'step-03-create-stories', 'step-04-final-validation']
inputDocuments:
  - '_bmad-output/planning-artifacts/prds/prd-strategic_reserve-2026-07-25/prd.md'
  - '_bmad-output/planning-artifacts/architecture/architecture-strategic_reserve-2026-07-25/ARCHITECTURE-SPINE.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-strategic_reserve-2026-07-25/DESIGN.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-strategic_reserve-2026-07-25/EXPERIENCE.md'
---

# Strategic Reserve - Epic Breakdown

## Overview

This progression plan decomposes Strategic Reserve into independently deliverable, user-valued increments. Stories are ordered so each depends only on work in earlier stories.

## Requirements Inventory

### Functional Requirements

- **FR-1:** Display the initial 6×6 board, twelve starting checkers, six checkers in each reserve, and clear empty squares.
- **FR-2:** Display purple-column and green-row die values and highlight their target square.
- **FR-3:** Highlight every legal placement square for the resolved roll.
- **FR-4:** Display and update both reserve counts.
- **FR-5:** Roll two fair six-sided dice and map them to a target from the current player's perspective.
- **FR-6:** Identify maximal, orthogonally connected same-color groups.
- **FR-7:** Remove a rolled enemy group and return its checkers to its owner's reserve.
- **FR-8:** On a friendly-group hit, remove every adjacent enemy group and restrict placement to empty squares adjacent to the friendly group.
- **FR-9:** On an empty hit, allow placement on any empty square.
- **FR-10:** Declare the player whose reserve reaches zero the winner immediately after placement.
- **FR-11:** Provide a rudimentary AI that randomly selects a legal move.
- **FR-12:** Provide an advanced AI using minimax or stochastic simulation and considering all 36 roll outcomes.
- **FR-13:** Support local player-versus-computer play with selectable difficulty.
- **FR-14:** Support two humans alternating on the same computer.
- **FR-15:** Start a game from the main menu with mode and difficulty selection.
- **FR-16:** Quit an in-progress game only after confirmation.

### Non-Functional Requirements

- **NFR-1:** Advanced AI decisions complete within five seconds.
- **NFR-2:** AI does not crash or hang on any valid board state.
- **NFR-3:** Rudimentary AI decisions complete within one second.

### Additional Requirements

- Use Python 3 and Tkinter with `game_engine/`, `ai/`, and `ui/` layers; dependencies flow UI → AI → game engine.
- The game engine exclusively owns mutable game state; UI and AI consume state without becoming alternate authorities.
- Represent the board as a 6×6 structure and game state as dataclasses, using absolute zero-based coordinates internally.
- Perform perspective conversion only at the UI boundary and group discovery with orthogonal flood fill.
- AI implementations expose `get_move(game_state, player_color)` and return a coordinate or `None`.
- Reject domain violations with explicit errors such as `IllegalMoveError` and `InvalidGameStateError`.
- Follow snake_case functions/modules, PascalCase classes, and UPPER_CASE constants.
- Add automated unit tests around deterministic game-engine and AI behavior.

### UX Design Requirements

- **UX-DR1:** Provide a main menu for PvC/PvP mode, AI difficulty, New Game, and Quit.
- **UX-DR2:** Render the 6×6 board, outlined red/blue checkers, two dice, and reserve counters.
- **UX-DR3:** Render legal moves with light-green fill and a dark-green border.
- **UX-DR4:** Render the rolled target with gold fill and a dark-gold border.
- **UX-DR5:** Render an orange hover or keyboard-navigation outline.
- **UX-DR6:** Support arrow-key board navigation, Enter/Space selection, logical Tab order, and Escape cancellation.
- **UX-DR7:** Present a centered game-over announcement and New Game action.
- **UX-DR8:** Present a Yes/No confirmation before quitting an active game.
- **UX-DR9:** Animate and distinguish the purple column die and green row die.
- **UX-DR10:** Display the current player in concise language.
- **UX-DR11:** Provide visible focus, screen-reader announcements, keyboard parity, and WCAG AA contrast.
- **UX-DR12:** Update reserve counters immediately after placements and captures.

### FR Coverage Map

| Requirement | Epic | Stories |
|---|---|---|
| FR-1, FR-4 | Epic 1 | 1.2, 1.4 |
| FR-5, FR-6 | Epic 1 | 1.2, 1.3 |
| FR-7, FR-8, FR-9 | Epic 2 | 2.1, 2.2, 2.3 |
| FR-2, FR-3 | Epic 3 | 3.2, 3.3 |
| FR-10 | Epic 3 | 3.4 |
| FR-14, FR-15, FR-16 | Epic 3 | 3.1, 3.5 |
| FR-11, FR-12 | Epic 4 | 4.1, 4.2 |
| FR-13 | Epic 4 | 4.3 |
| NFR-1, NFR-2, NFR-3 | Epic 4 | 4.1, 4.2, 4.4 |
| UX-DR1–UX-DR12 | Epics 3 and 5 | 3.1–3.5, 5.1–5.3 |

## Epic List

1. **Playable Rules Foundation** — establish a tested state model, board groups, turns, dice, and reserves.
2. **Complete Capture and Placement Rules** — make every roll outcome resolve according to the official rules.
3. **Local Desktop Game** — deliver a complete, visible two-player game loop.
4. **Computer Opponents** — add safe rudimentary and advanced AI play.
5. **Accessible Release Experience** — complete keyboard, assistive, visual, and release-quality validation.

## Epic 1: Playable Rules Foundation

Players can create a valid game, roll dice, inspect groups, and place pieces through a deterministic engine API.

### Story 1.1: Establish the Layered Application Skeleton

As a developer, I want enforceable package boundaries and test tooling, so that gameplay features grow on a reliable foundation.

**Acceptance Criteria:**

**Given** a clean checkout, **when** the documented test command runs, **then** the game-engine, AI, and UI packages import successfully and tests execute.

**Given** package dependency checks, **when** imports are inspected, **then** the engine imports neither AI nor UI and AI imports no UI code.

### Story 1.2: Create and Validate a Game State

As a player, I want every new game to begin in the official position, so that play starts fairly.

**Acceptance Criteria:**

**Given** a new game, **when** its state is inspected, **then** the 6×6 board contains the prescribed twelve checkers, each reserve contains six, and the starting player is recorded.

**Given** malformed dimensions, colors, counts, or coordinates, **when** state validation runs, **then** `InvalidGameStateError` is raised without mutating state.

### Story 1.3: Discover Orthogonal Groups

As a player, I want connected checker groups identified accurately, so that captures follow the rules.

**Acceptance Criteria:**

**Given** same-color pieces joined orthogonally, **when** group discovery starts from any member, **then** every and only orthogonally connected member is returned once.

**Given** pieces touching only diagonally, **when** groups are discovered, **then** they remain separate groups.

### Story 1.4: Roll Dice and Place a Reserve Checker

As a player, I want a roll and placement to update one authoritative state, so that turns can progress consistently.

**Acceptance Criteria:**

**Given** a current player, **when** dice are rolled, **then** two values from one through six are recorded and map to one absolute board coordinate.

**Given** a legal empty destination, **when** the player places, **then** one checker moves from their reserve to that square and the turn advances exactly once.

**Given** an illegal destination or empty reserve, **when** placement is attempted, **then** `IllegalMoveError` is raised and state remains unchanged.

## Epic 2: Complete Capture and Placement Rules

Players can resolve enemy, friendly, and empty targets with correct captures and legal destinations.

### Story 2.1: Resolve an Enemy-Group Hit

As a player, I want a rolled enemy group removed, so that the enemy-hit rule changes board control correctly.

**Acceptance Criteria:**

**Given** the target belongs to an enemy group, **when** the roll resolves, **then** the whole maximal group is removed and its size is added to the enemy reserve.

**Given** the capture resolves, **when** legal moves are requested, **then** every empty square is offered and occupied squares are excluded.

### Story 2.2: Resolve a Friendly-Group Hit

As a player, I want adjacent enemy groups captured and placement constrained, so that friendly hits follow the tactical rule.

**Acceptance Criteria:**

**Given** a friendly target group adjacent to one or more enemy groups, **when** the roll resolves, **then** every orthogonally adjacent enemy group is removed once and returned to its owner’s reserve.

**Given** the resolved friendly group, **when** legal moves are requested, **then** only empty squares orthogonally adjacent to any group member are returned.

**Given** no adjacent empty square, **when** resolution completes, **then** the engine exposes no placement and advances according to the documented no-move rule without hanging.

### Story 2.3: Resolve an Empty-Square Hit

As a player, I want an empty target to allow free placement, so that I can choose any available square.

**Acceptance Criteria:**

**Given** an empty target, **when** legal moves are calculated, **then** all and only empty board squares are returned.

**Given** any returned destination, **when** placement occurs, **then** no checker is captured and normal reserve and turn updates apply.

### Story 2.4: Preserve Rule Invariants Across Full Turns

As a player, I want every full turn to remain valid, so that long games cannot corrupt themselves.

**Acceptance Criteria:**

**Given** each target category and boundary location, **when** automated scenario tests execute a full turn, **then** checker totals, reserve totals, occupancy, and active-player invariants hold.

**Given** a failed action, **when** state is compared before and after, **then** no partial capture, placement, or turn transition remains.

## Epic 3: Local Desktop Game

Two people can start, play, finish, restart, and safely quit a complete game on one desktop.

### Story 3.1: Start a Configured Local Game

As a player, I want to choose local multiplayer and start a game, so that two people can play on one machine.

**Acceptance Criteria:**

**Given** application launch, **when** the main menu appears, **then** it shows mode, difficulty where applicable, New Game, and Quit controls.

**Given** PvP is selected, **when** New Game is activated, **then** a correctly initialized board replaces the menu and the current player is announced.

### Story 3.2: See the Board, Dice, and Reserves

As a player, I want the complete state rendered clearly, so that I can understand the game at a glance.

**Acceptance Criteria:**

**Given** an active game, **when** it renders, **then** it shows a 6×6 grid, outlined red/blue checkers, empty squares, both reserve counts, and the current player.

**Given** a roll, **when** dice animation completes, **then** the purple column and green row values remain visible and their target has a gold treatment.

### Story 3.3: Select Only a Legal Move

As a player, I want legal destinations highlighted and clickable, so that I can complete a valid turn without memorizing constraints.

**Acceptance Criteria:**

**Given** a resolved roll, **when** legal moves render, **then** each legal square has the specified light-green/dark-green treatment and no illegal square does.

**Given** a legal square, **when** it is selected, **then** the engine accepts it and the board, reserve counters, and current player refresh immediately.

**Given** an illegal or stale square, **when** it is activated, **then** no state changes and concise feedback is presented.

### Story 3.4: Finish and Restart a Game

As a player, I want an immediate winner announcement and restart action, so that a completed game has a clear conclusion.

**Acceptance Criteria:**

**Given** a player places their last reserve checker, **when** placement completes, **then** that player is declared the winner immediately and further board input is disabled.

**Given** the centered game-over view, **when** New Game is activated, **then** the user returns to a fresh configured game flow with no prior state retained.

### Story 3.5: Confirm Quitting an Active Game

As a player, I want accidental quitting prevented, so that I do not lose a game unintentionally.

**Acceptance Criteria:**

**Given** a game is active, **when** Quit or window close is requested, **then** a Yes/No confirmation appears.

**Given** the confirmation, **when** No or Escape is selected, **then** play resumes unchanged; **when** Yes is selected, **then** the application exits cleanly.

## Epic 4: Computer Opponents

A solo player can choose between fast random play and bounded strategic play without compromising engine integrity.

### Story 4.1: Play Against a Rudimentary AI

As a solo player, I want a quick random opponent, so that I can practice casually.

**Acceptance Criteria:**

**Given** any valid state with legal moves, **when** rudimentary `get_move` runs, **then** it returns one of those moves without mutating input state and completes within one second.

**Given** no legal move, **when** it runs, **then** it returns `None` without crashing or hanging.

### Story 4.2: Play Against an Advanced AI

As a solo player, I want a strategic opponent, so that practice remains challenging.

**Acceptance Criteria:**

**Given** a valid state, **when** advanced `get_move` runs, **then** it evaluates candidate play using all 36 possible next-roll outcomes and returns a legal move.

**Given** a configured search budget, **when** the position is complex, **then** a best-so-far legal move returns within five seconds.

### Story 4.3: Configure and Run a PvC Game

As a solo player, I want to choose AI difficulty, so that opponent strength matches my preference.

**Acceptance Criteria:**

**Given** PvC mode, **when** rudimentary or advanced difficulty is selected and the game starts, **then** the matching AI controls its assigned color.

**Given** an AI turn, **when** its move completes, **then** the same roll, capture, placement, render, and win rules used for humans apply and human input cannot race the AI.

### Story 4.4: Verify AI Safety and Performance

As a player, I want dependable AI turns, so that unusual positions cannot freeze or corrupt my game.

**Acceptance Criteria:**

**Given** a corpus covering full, sparse, capture-heavy, no-move, and near-win states, **when** both AIs run, **then** every result is legal or `None`, input states remain unchanged, and no run crashes or hangs.

**Given** timed performance tests, **when** each difficulty runs under documented conditions, **then** rudimentary remains below one second and advanced remains below five seconds.

## Epic 5: Accessible Release Experience

Keyboard and assistive-technology users can complete every journey, and the packaged application meets the visual and quality contract.

### Story 5.1: Play the Board Entirely by Keyboard

As a keyboard user, I want parity with pointer interaction, so that I can complete a game without a mouse.

**Acceptance Criteria:**

**Given** board focus, **when** arrow keys are pressed, **then** focus moves predictably within the grid; Enter or Space activates a legal square.

**Given** any surface, **when** Tab and Shift+Tab are used, **then** focus follows visual order; Escape cancels selection or closes a non-destructive dialog.

**Given** pointer or keyboard focus, **when** a board square is targeted, **then** the orange outline is visible and distinguishable from target and legal-move states.

### Story 5.2: Announce State and Meet Contrast Standards

As an assistive-technology user, I want state changes announced and visible, so that I receive equivalent gameplay information.

**Acceptance Criteria:**

**Given** turn, roll, capture, reserve, invalid-action, or winner changes, **when** they occur, **then** concise accessible text communicates the change without relying only on color.

**Given** every normal, hover, focus, legal, target, and disabled state, **when** audited, **then** text and essential indicators meet WCAG AA contrast and visible-focus requirements.

### Story 5.3: Validate the Release Journey

As a player, I want a stable distributable game, so that installation and complete play work on a supported desktop.

**Acceptance Criteria:**

**Given** a clean supported Python environment, **when** documented launch instructions are followed, **then** the application opens without undeclared dependencies.

**Given** automated and manual release checks, **when** PvP and both PvC difficulties are played through start, captures, win, restart, and quit, **then** all requirements in the coverage map pass with no critical defects.

**Given** the release artifact, **when** source and documentation are inspected, **then** game attribution, controls, test commands, supported environment, and known limitations are present.
