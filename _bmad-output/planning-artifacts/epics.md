---
stepsCompleted: ['step-01-validate-prerequisites', 'step-02-design-epics']
inputDocuments: ['C:/code/games/strategic_reserve/_bmad-output/planning-artifacts/prds/prd-strategic_reserve-2026-07-25/prd.md', 'C:/code/games/strategic_reserve/_bmad-output/planning-artifacts/architecture/architecture-strategic_reserve-2026-07-25/ARCHITECTURE-SPINE.md', 'C:/code/games/strategic_reserve/_bmad-output/planning-artifacts/ux-designs/ux-strategic_reserve-2026-07-25/DESIGN.md', 'C:/code/games/strategic_reserve/_bmad-output/planning-artifacts/ux-designs/ux-strategic_reserve-2026-07-25/EXPERIENCE.md']
---

# Strategic Reserve - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Strategic Reserve, decomposing the requirements from the PRD and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR-1: Display initial board state - System displays the starting position: 12 checkers arranged per rules (Red and Blue in specific pattern), 6 checkers in each player's reserve, and empty squares marked clearly.

FR-2: Visualize dice rolls - System displays Purple die (column) and Green die (row) values after each roll, highlighting the corresponding square on the board.

FR-3: Show legal placement options - System highlights all legal placement squares based on the current game state and dice roll (any empty square for enemy/empty hits, orthogonally adjacent squares for friendly hits).

FR-4: Display reserve counts - System shows current reserve count for each player, updating in real-time as checkers are placed and returned.

FR-5: Roll dice and determine target square - System generates random dice rolls (1-6 for each die) and maps Purple die to column, Green die to row from current player's perspective.

FR-6: Detect groups on board - System identifies all maximal orthogonally connected groups of same-colored checkers on the board.

FR-7: Resolve enemy group hits - When rolled square belongs to enemy group, system removes entire connected group and returns all checkers to opponent's reserve.

FR-8: Resolve friendly group hits - When rolled square belongs to player's own group, system removes all adjacent enemy groups and returns them to opponent's reserve. Player must place on empty orthogonally adjacent square to the friendly group.

FR-9: Resolve empty hits - When rolled square is empty, system allows placement on any empty square.

FR-10: Detect win condition - System detects when a player's reserve reaches zero and declares that player the winner immediately after placing their last checker.

FR-11: Implement rudimentary AI - System provides AI opponent that selects legal moves randomly from available options.

FR-12: Implement advanced AI - System provides AI opponent using minimax or stochastic simulation algorithm that considers all 36 possible dice roll combinations in game tree evaluation.

FR-13: Support Player vs Computer mode - System allows single player to play against AI opponent with selectable difficulty.

FR-14: Support Player vs Player mode - System allows two human players to alternate turns on the same machine.

FR-15: Start new game - System allows starting a new game from main menu with mode and difficulty selection.

FR-16: Quit game - System allows quitting the current game with confirmation if game is in progress.

### NonFunctional Requirements

NFR-1: AI decision time must not exceed 5 seconds for advanced difficulty (from FR-12 feature-specific NFRs).

NFR-2: AI must not crash or hang on any board state (from FR-12 feature-specific NFRs).

NFR-3: AI completes turns within reasonable time (< 1 second) for rudimentary difficulty (from FR-11 consequences).

### Additional Requirements

- Layered architecture with Game Engine, AI, and UI layers (from Architecture AD-1, AD-2)
- Game Engine owns all game state; UI and AI are stateless (from Architecture AD-1)
- Module dependencies flow downward only: UI → AI → Game Engine (from Architecture AD-2)
- Game Engine uses absolute internal coordinates (0-5, 0-5); UI handles player perspective mapping (from Architecture AD-3)
- AI modules implement get_move(game_state, player_color) interface returning (row, col) or None (from Architecture AD-4)
- Group detection uses flood fill with orthogonal connectivity only (from Architecture AD-5)
- Custom exceptions for domain errors (IllegalMoveError, InvalidGameStateError) (from Architecture AD-6)
- Naming conventions: snake_case for modules/functions, PascalCase for classes, UPPER_CASE for constants (from Architecture consistency conventions)
- Data structures: Board as 6x6 2D list, GameState as dataclass (from Architecture consistency conventions)
- Stack: Python 3.x with Tkinter (built-in) (from Architecture Stack)
- Project structure: game_engine/, ai/, ui/ modules with specific file organization (from Architecture Structural Seed)

### UX Design Requirements

UX-DR1: Implement Main Menu surface with game mode selection (PvC/PvP), AI difficulty dropdown (rudimentary/advanced), New Game and Quit buttons.

UX-DR2: Implement Game Board surface with 6×6 grid of clickable squares, checker rendering (Red/Blue circles with outlines), dice display (Purple/Green values with dot patterns), reserve counters (Red Reserve: X, Blue Reserve: X).

UX-DR3: Implement legal move highlighting using light green background (#90EE90) with dark green border on all legal placement squares after dice roll.

UX-DR4: Implement target square highlighting using gold background (#FFD700) with dark golden border on the square determined by dice roll.

UX-DR5: Implement hover state showing orange outline (#FF6600) on squares when hovering with mouse or navigating with keyboard.

UX-DR6: Implement keyboard navigation using arrow keys (↑↓←→) to navigate board squares, Enter/Space to select, Tab to navigate between board and buttons, Esc to cancel selection or close dialogs.

UX-DR7: Implement Game Over overlay with winner announcement ("Red wins!" or "Blue wins!") centered on board and New Game button.

UX-DR8: Implement quit confirmation dialog ("Quit game?" with Yes/No buttons) when game is in progress.

UX-DR9: Implement dice roll animation showing Purple die (column) and Green die (row) values with visual feedback.

UX-DR10: Implement current player indicator in top bar showing "Red's turn" or "Blue's turn".

UX-DR11: Implement accessibility features including full keyboard navigation, focus indicators, screen reader announcements, tab order following visual layout, high contrast colors meeting WCAG AA standards.

UX-DR12: Implement reserve counter real-time updates as checkers are placed and returned.

### FR Coverage Map

{{requirements_coverage_map}}

## Epic List

{{epics_list}}
