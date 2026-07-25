---
title: Strategic Reserve PRD
status: draft
created: 2026-07-25
updated: 2026-07-25
---

# PRD: Strategic Reserve

## 0. Document Purpose
This PRD defines requirements for a desktop Python implementation of Strategic Reserve, a two-player dice-based board game designed by Mark Steere. The document is structured with a Glossary-anchored vocabulary, features grouped with nested functional requirements, and inline assumptions tagged for explicit confirmation. This PRD serves as the foundation for architecture design and epic/story creation.

## 1. Vision
Strategic Reserve is a desktop application that brings the dice-based strategy game to life with visual board representation, game simulation, and AI opponents. The application enables players to experience the game's unique mechanics where dice rolls determine board positions and strategic checker placement determines victory. For the builder, this project provides an opportunity to implement game logic, AI algorithms (random and minimax-based), and a lightweight Python UI framework.

## 2. Target User

### 2.1 Jobs To Be Done
- Play a complete game of Strategic Reserve following the official rules
- Visualize the 6×6 board, checker positions, and dice rolls in real-time
- Practice against AI opponents of varying difficulty levels
- Play locally against another human on the same machine
- Understand game state and legal moves through clear UI feedback

### 2.2 Non-Users (v1)
- Online multiplayer players (no network play in v1)
- Mobile users (desktop-only in v1)
- Tournament organizers (no tournament features in v1)

### 2.3 Key User Journeys

- **UJ-1. Player starts a new game against AI.**
  - Persona + context: A player wanting to practice against the computer.
  - Entry state: Application launched, main menu visible.
  - Path: Select "New Game" → Choose opponent type (AI) → Select difficulty level → Game board initializes with starting position.
  - Climax: First dice roll appears, player can place a checker.
  - Resolution: Game proceeds turn-by-turn until reserve is emptied.
  - Edge case: If player quits mid-game, application asks to save or discard.

- **UJ-2. Player plays local multiplayer game.**
  - Persona + context: Two players sharing the same computer.
  - Entry state: Application launched, main menu visible.
  - Path: Select "New Game" → Choose opponent type (Human) → Game board initializes with starting position.
  - Climax: Players alternate turns, dice rolls determine positions.
  - Resolution: Game ends when one player empties their reserve.
  - Edge case: If players want to restart, application confirms discarding current game.

## 3. Glossary
- **Board** — 6×6 grid where checkers are placed. Coordinates are (column, row) with columns 1-6 left-to-right and rows 1-6 near-to-far from the current player's perspective.
- **Checker** — Game piece belonging to either Red or Blue player.
- **Reserve** — Off-board supply of 6 checkers per player. New checkers placed on the board come from reserve.
- **Group** — One or more orthogonally connected (up, down, left, right) checkers of the same color. Diagonal connections do not count. Groups are maximal (cannot be subset of larger connected group).
- **Dice** — Two six-sided dice: Purple die determines horizontal coordinate (column), Green die determines vertical coordinate (row).
- **Hit** — When rolled square belongs to a group, triggering removal rules.
- **Enemy group hit** — Rolled square belongs to opponent's group. Entire connected group is removed and returned to opponent's reserve. Player places checker on any empty square.
- **Friendly group hit** — Rolled square belongs to player's own group. All adjacent enemy groups are removed and returned to opponent's reserve. Player places checker on empty orthogonally adjacent square to the friendly group.
- **Empty hit** — Rolled square is empty. Player places checker on any empty square.

## 4. Features

### 4.1 Game Board Visualization
**Description:** Renders the 6×6 game board with checkers, reserve counts, and dice roll visualization. Shows current player turn, legal placement options, and game state updates in real-time. Realizes UJ-1, UJ-2.

**Functional Requirements:**

#### FR-1: Display initial board state
System displays the starting position: 12 checkers arranged per rules (Red and Blue in specific pattern), 6 checkers in each player's reserve, and empty squares marked clearly. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- Board shows 6×6 grid with correct checker positions
- Reserve counters display 6 for each player
- Empty squares are visually distinct from occupied squares

**Out of Scope:**
- Custom board themes or skins
- Board animations beyond basic piece placement

#### FR-2: Visualize dice rolls
System displays Purple die (column) and Green die (row) values after each roll, highlighting the corresponding square on the board. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- Dice values are shown numerically (1-6 each)
- Target square is highlighted on the board
- Dice visualization updates each turn

#### FR-3: Show legal placement options
System highlights all legal placement squares based on the current game state and dice roll (any empty square for enemy/empty hits, orthogonally adjacent squares for friendly hits). Realizes UJ-1, UJ-2.

**Consequences (testable):**
- Legal squares are visually distinct from illegal squares
- Highlighting updates correctly after each dice roll
- Placement restrictions are enforced (cannot place on occupied squares)

#### FR-4: Display reserve counts
System shows current reserve count for each player, updating in real-time as checkers are placed and returned. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- Reserve counts decrement when player places checker
- Reserve counts increment when opponent's checkers are returned
- Reserve counts display prominently in UI

### 4.2 Game Simulation Engine
**Description:** Implements core game logic including dice rolling, hit resolution, group detection, checker placement, and win condition checking. Enforces all game rules precisely. Realizes UJ-1, UJ-2.

**Functional Requirements:**

#### FR-5: Roll dice and determine target square
System generates random dice rolls (1-6 for each die) and maps Purple die to column, Green die to row from current player's perspective. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- Each die produces uniform random value 1-6
- Column/row mapping is correct for current player's perspective
- Target square coordinates are calculated correctly

#### FR-6: Detect groups on board
System identifies all maximal orthogonally connected groups of same-colored checkers on the board. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- Groups are correctly identified using orthogonal connectivity only
- Diagonal connections are not considered part of same group
- Each checker belongs to exactly one group
- Groups are maximal (no subset of larger connected group)

#### FR-7: Resolve enemy group hits
When rolled square belongs to enemy group, system removes entire connected group and returns all checkers to opponent's reserve. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- Enemy group containing target square is completely removed
- All removed checkers increment opponent's reserve count
- Target square becomes empty after removal
- Placement can occur on any empty square after removal

#### FR-8: Resolve friendly group hits
When rolled square belongs to player's own group, system removes all adjacent enemy groups and returns them to opponent's reserve. Player must place on empty orthogonally adjacent square to the friendly group. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- All enemy groups orthogonally adjacent to the friendly group are removed
- Removed checkers increment opponent's reserve count
- Placement is restricted to empty orthogonally adjacent squares
- System rejects placement on non-adjacent squares

#### FR-9: Resolve empty hits
When rolled square is empty, system allows placement on any empty square. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- Any empty square is legal for placement
- No placement restrictions beyond square being empty
- System rejects placement on occupied squares

#### FR-10: Detect win condition
System detects when a player's reserve reaches zero and declares that player the winner immediately after placing their last checker. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- Win is detected immediately when reserve count reaches 0
- Game ends and winner is announced
- No further moves are allowed after win condition

### 4.3 AI Opponents
**Description:** Provides computer opponents with two difficulty levels: rudimentary (random/legal moves) and advanced (minimax or stochastic simulation considering all 36 dice roll combinations). Realizes UJ-1.

**Functional Requirements:**

#### FR-11: Implement rudimentary AI
System provides AI opponent that selects legal moves randomly from available options. Realizes UJ-1.

**Consequences (testable):**
- AI always selects a legal placement square
- Selection is uniformly random among legal options
- AI completes turns within reasonable time (< 1 second)

#### FR-12: Implement advanced AI
System provides AI opponent using minimax or stochastic simulation algorithm that considers all 36 possible dice roll combinations in game tree evaluation. Realizes UJ-1.

**Consequences (testable):**
- AI evaluates game states considering dice roll probability distribution
- AI selects moves that maximize expected outcome
- AI search depth is configurable `[ASSUMPTION: depth 3-5 ply appropriate for hobby project]`
- AI completes turns within reasonable time (< 5 seconds)

**Feature-specific NFRs:**
- AI decision time must not exceed 5 seconds for advanced difficulty
- AI must not crash or hang on any board state

### 4.4 Game Modes
**Description:** Supports Player vs Computer (PvC) and Player vs Player (PvP) local multiplayer modes. Realizes UJ-1, UJ-2.

**Functional Requirements:**

#### FR-13: Support Player vs Computer mode
System allows single player to play against AI opponent with selectable difficulty. Realizes UJ-1.

**Consequences (testable):**
- Player can choose AI difficulty level before game starts
- AI takes turns automatically after player moves
- Game proceeds until win condition

#### FR-14: Support Player vs Player mode
System allows two human players to alternate turns on the same machine. Realizes UJ-2.

**Consequences (testable):**
- Players alternate turns after each move
- Current player indicator is clearly displayed
- Dice roll perspective switches between players

### 4.5 Game Controls
**Description:** Provides game setup, pause/resume, restart, and quit functionality. Realizes UJ-1, UJ-2.

**Functional Requirements:**

#### FR-15: Start new game
System allows starting a new game from main menu with mode and difficulty selection. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- New game initializes with correct starting position
- Previous game state is discarded (or saved with confirmation)
- Mode and difficulty settings are applied

#### FR-16: Quit game
System allows quitting the current game with confirmation if game is in progress. Realizes UJ-1, UJ-2.

**Consequences (testable):**
- Quitting mid-game prompts for confirmation
- Application closes cleanly after confirmation
- No game state corruption on quit

## 5. Non-Goals (Explicit)
- Online multiplayer or network play
- Mobile or web platform support
- Tournament or league features
- Game replay or analysis tools
- Custom board sizes or rule variants
- Save/load game to disk
- Leaderboards or statistics tracking
- Sound effects or music
- Tutorial or rule explanations beyond basic UI

## 6. MVP Scope

### 6.1 In Scope
- Complete game board visualization (6×6 grid, checkers, dice, reserves)
- Full game simulation engine (all rules implemented correctly)
- Two AI difficulty levels (random and minimax/stochastic)
- PvC and PvP local multiplayer modes
- Basic game controls (new game, quit)
- Legal move highlighting and game state display

### 6.2 Out of Scope for MVP
- Online multiplayer (deferred indefinitely - personal project scope)
- Save/load functionality (deferred to v2 if needed)
- Custom themes or visual polish beyond basic clarity (deferred to v2)
- Tutorial or help system (deferred to v2 - rules document suffices)

## 7. Success Metrics
- **SM-1**: Complete game can be played from start to finish without crashes or rule violations. Validates FR-5 through FR-10.
- **SM-2**: AI completes moves within specified time limits (rudimentary < 1s, advanced < 5s). Validates FR-11, FR-12.
- **SM-3**: All 36 dice roll combinations are correctly handled by game engine. Validates FR-5.

**Counter-metrics (do not optimize)**
- **SM-C1**: AI win rate - this is a strategy game, AI should be challenging but not unbeatable. Counterbalances SM-2.

## 8. Open Questions
- None at this time.

## 9. Assumptions Index
- Inline assumption from FR-12: AI search depth of 3-5 ply is appropriate for hobby project performance.
- Inline assumption from §4.1: Tkinter or similar lightweight framework will be used for UI (user specified "lightweight, easily accessible via pip").
