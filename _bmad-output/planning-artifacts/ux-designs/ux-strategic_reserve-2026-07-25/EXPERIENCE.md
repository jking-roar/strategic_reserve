---
title: Strategic Reserve UX Experience
status: final
created: 2026-07-25
updated: 2026-07-25
sources:
  - C:/code/games/strategic_reserve/_bmad-output/planning-artifacts/prds/prd-strategic_reserve-2026-07-25/prd.md
  - C:/code/games/strategic_reserve/_bmad-output/planning-artifacts/architecture/architecture-strategic_reserve-2026-07-25/ARCHITECTURE-SPINE.md
---

# Strategic Reserve — Experience Spine

## Foundation

Desktop application using Tkinter for UI rendering. `DESIGN.md` provides the visual identity reference with color tokens, typography, and component specifications. The application supports two game modes: Player vs Computer (PvC) and Player vs Player (PvP) on the same machine. Form factor is desktop-only with no responsive behavior required.

## Information Architecture

| Surface | Reached from | Purpose |
|---|---|---|
| Main Menu | Application launch | Game mode selection (PvC/PvP), AI difficulty selection, New Game initiation |
| Game Board | Main Menu → New Game | Active gameplay with board visualization, dice rolls, move selection |
| Game Over | Win condition met | Winner announcement, New Game option |

Single-window application. No navigation between multiple surfaces — the game board is the primary and only gameplay surface. Main Menu appears on launch and after game completion.

## Voice and Tone

Microcopy is functional and direct, matching the classic board game aesthetic.

| Do | Don't |
|---|---|
| "Red's turn" | "It is now the Red player's turn to make a move!" |
| "Blue wins!" | "Congratulations! The Blue player has emerged victorious!" |
| "New Game" | "Start a fresh new game session" |
| "Quit" | "Exit the application completely" |
| Clear, concise labels | Explanatory or enthusiastic text |

## Component Patterns

Behavioral specifications. Visual specs live in `DESIGN.md.Components`.

| Component | Use | Behavioral rules |
|---|---|---|
| Board grid | Game Board | 6×6 grid of clickable squares. Click to select placement square. Keyboard navigation with arrow keys. Hover shows `{DESIGN.md.components.hover_cell}` styling. |
| Checker | Board cells | Red/Blue circles rendered in occupied cells. Visual per `{DESIGN.md.components.checker_red}` and `{DESIGN.md.components.checker_blue}`. No interaction — selection is on the square, not the checker. |
| Dice display | Top bar | Shows Purple die (column) and Green die (row) values. Displays numerically and with dot patterns. Updates each turn. Highlights corresponding board square with `{DESIGN.md.components.target_cell}`. |
| Reserve counter | Bottom bar | Labels "Red Reserve: X" and "Blue Reserve: X". Updates in real-time as checkers are placed and returned. |
| Legal move highlight | Board cells | Highlights all legal placement squares with `{DESIGN.md.components.legal_move_cell}` after dice roll. Updates each turn. |
| Primary button | Main Menu, Game Over | "New Game" button using `{DESIGN.md.components.button_primary}`. Initiates new game with current mode/difficulty settings. |
| Secondary button | Main Menu, Game Over | "Quit" button using `{DESIGN.md.components.button_secondary}`. Exits application with confirmation if game in progress. |

## State Patterns

| State | Surface | Treatment |
|---|---|---|
| Application launch | Main Menu | Show game mode selection (PvC/PvP), AI difficulty dropdown (rudimentary/advanced), New Game and Quit buttons. |
| Playing - Dice roll | Game Board | Animate dice roll, display values, highlight target square on board, highlight all legal placement squares. |
| Playing - Move selection | Game Board | Player selects square via click or keyboard navigation. Selected square shows hover outline. |
| Playing - AI turn | Game Board | AI calculates move (rudimentary: <1s, advanced: <5s), places checker, board updates automatically. |
| Game Over | Game Board overlay | Display winner announcement "Red wins!" or "Blue wins!" centered on board. Show New Game button. |
| Quit confirmation | Dialog | If game in progress, show "Quit game?" dialog with Yes/No buttons. If no game in progress, quit immediately. |

## Interaction Primitives

**Mouse and keyboard parity.** Players can interact using either input method.

**Mouse:**
- Click on board square to select placement
- Hover over square shows `{DESIGN.md.components.hover_cell}` outline
- Click buttons to trigger actions

**Keyboard:**
- Arrow keys (↑↓←→) navigate board squares
- Enter or Space to select current square
- Tab to navigate between board and buttons
- Esc to cancel selection or close dialogs

**Banned everywhere:** drag-and-drop, right-click context menus, keyboard shortcuts beyond navigation keys.

## Accessibility Floor

Behavioral. Visual contrast lives in `DESIGN.md`.

- Full keyboard navigation for all game actions
- Focus indicators visible on all interactive elements
- Screen reader announces game state changes: "Red's turn. Purple die 3, Green die 4. Target square (2,3)."
- Tab order follows visual layout: top bar → board → bottom bar
- Color not used as sole indicator — legal moves have both color change and border styling
- High contrast colors meet WCAG AA standards for readability

## Key Flows

### Flow 1 — Player vs Computer game (Alex, solo player, evening practice)

1. Alex launches Strategic Reserve. Main Menu appears with PvC/PvP selection and AI difficulty dropdown.
2. He selects "Player vs Computer" and chooses "Advanced" difficulty.
3. He clicks "New Game". Game Board appears with starting position, Red Reserve: 6, Blue Reserve: 6.
4. **Climax:** Dice roll animation shows Purple 4, Green 2. Target square (3,1) highlights gold. Legal squares highlight green. Alex clicks a legal square, Red checker appears, Red Reserve decrements to 5.
5. AI turn: Blue checker appears after brief calculation, Blue Reserve decrements to 5.
6. Play continues turn-by-turn until one reserve reaches zero.
7. Game Over: "Blue wins!" appears on board. Alex clicks "New Game" to play again.

Failure: Alex tries to place on illegal square → visual feedback (no placement, square remains highlighted as illegal), no error message needed.

### Flow 2 — Player vs Player game (Jordan and Taylor, local multiplayer, afternoon)

1. Jordan launches Strategic Reserve. Main Menu appears.
2. He selects "Player vs Player" and clicks "New Game".
3. Game Board appears with starting position. "Red's turn" displayed in top bar.
4. Jordan (Red) rolls dice, places checker. "Blue's turn" appears.
5. Taylor (Blue) takes the keyboard, navigates with arrow keys, presses Enter to place checker.
6. Play continues alternating until Taylor's reserve reaches zero.
7. Game Over: "Red wins!" appears. Jordan clicks "New Game" for another round.

Failure: Player tries to quit mid-game → confirmation dialog "Quit game?" appears. Player selects "No" and game continues.
