---
title: Strategic Reserve UX Design
status: final
created: 2026-07-25
updated: 2026-07-25
colors:
  red_checker: '#CC0000'
  blue_checker: '#0000CC'
  board_background: '#F5F5DC'
  grid_lines: '#333333'
  legal_move_highlight: '#90EE90'
  target_square_highlight: '#FFD700'
  hover_outline: '#FF6600'
typography:
  body:
    fontFamily: 'system-ui, sans-serif'
    fontSize: '14px'
    fontWeight: '400'
  display:
    fontFamily: 'system-ui, sans-serif'
    fontSize: '18px'
    fontWeight: '600'
  label:
    fontFamily: 'system-ui, sans-serif'
    fontSize: '12px'
    fontWeight: '500'
rounded:
  checker: '50%'
  button: '4px'
  panel: '8px'
spacing:
  board_padding: '20px'
  cell_size: '60px'
  gap: '2px'
components:
  checker_red:
    background: '{colors.red_checker}'
    border: '2px solid #000000'
    radius: '{rounded.checker}'
  checker_blue:
    background: '{colors.blue_checker}'
    border: '2px solid #000000'
    radius: '{rounded.checker}'
  board_cell:
    background: '{colors.board_background}'
    border: '1px solid {colors.grid_lines}'
    width: '{spacing.cell_size}'
    height: '{spacing.cell_size}'
  legal_move_cell:
    background: '{colors.legal_move_highlight}'
    border: '2px solid #006400'
  target_cell:
    background: '{colors.target_square_highlight}'
    border: '2px solid #B8860B'
  hover_cell:
    border: '3px solid {colors.hover_outline}'
  button_primary:
    background: '#4CAF50'
    foreground: '#FFFFFF'
    radius: '{rounded.button}'
  button_secondary:
    background: '#F5F5F5'
    foreground: '#333333'
    border: '1px solid #CCCCCC'
    radius: '{rounded.button}'

## Brand & Style

Strategic Reserve is a desktop board game implementation focused on clarity and playability. The visual style is functional and clean, using solid colors with clear outlines to distinguish game elements. The design prioritizes game state visibility over decorative elements, ensuring players can quickly read the board, dice rolls, and legal moves. The aesthetic is that of a classic board game brought to digital form — straightforward, readable, and focused on the gameplay mechanics.

## Colors

The palette uses high-contrast colors for game elements with neutral backgrounds for the playing surface.

- **Red Checker (`#CC0000`)** — Red player's pieces. Solid fill with black outline for visibility against any background.
- **Blue Checker (`#0000CC`)** — Blue player's pieces. Solid fill with black outline for visibility against any background.
- **Board Background (`#F5F5DC`)** — Beige/tan background for the board, reminiscent of classic board game materials.
- **Grid Lines (`#333333`)** — Dark gray lines defining the 6×6 grid structure.
- **Legal Move Highlight (`#90EE90`)** — Light green highlighting squares where placement is legal.
- **Target Square Highlight (`#FFD700`)** — Gold highlighting the square determined by the dice roll.
- **Hover Outline (`#FF6600`)** — Orange outline when hovering over a square with mouse or keyboard focus.

Avoid: gradients, shadows, decorative patterns, low-contrast combinations. The discipline is high-contrast solid colors for maximum readability.

## Typography

System fonts are used throughout for desktop application consistency and performance.

- **Body text** — System sans-serif at 14px normal weight for general UI elements and labels.
- **Display text** — System sans-serif at 18px semi-bold for game state announcements, winner messages, and prominent labels.
- **Label text** — System sans-serif at 12px medium weight for reserve counters, dice labels, and secondary information.

All text is left-aligned except for centered game state announcements. No custom fonts are loaded; system defaults ensure fast rendering and native feel.

## Layout & Spacing

The layout is centered around the game board with supporting information in peripheral areas.

- **Board padding** — 20px of space around the board to separate it from window edges.
- **Cell size** — 60px × 60px squares for the 6×6 grid, providing adequate space for checkers and visual feedback.
- **Gap** — 2px spacing between grid cells for clear visual separation.
- **Window layout** — Top bar: current player and dice display. Center: game board. Bottom bar: reserve counters and control buttons.

The board is always centered horizontally and vertically in the main window area. No responsive behavior is required for this desktop-only application.

## Elevation & Depth

No elevation or shadow effects are used. The design is flat with depth created only through color contrast and borders. This maintains the classic board game aesthetic and ensures clarity.

## Shapes

- **Checkers** — Perfect circles (50% border radius) to represent game pieces.
- **Buttons** — 4px border radius for subtle rounding on control buttons.
- **Panels** — 8px border radius for any container panels or dialog boxes.

No pill shapes or complex geometric forms are used. The shape language is simple and geometric.

## Components

Core game components with their visual specifications:

- **Red Checker** — `{colors.red_checker}` fill, 2px black border, circular shape. Size fills most of the cell with small padding.
- **Blue Checker** — `{colors.blue_checker}` fill, 2px black border, circular shape. Size fills most of the cell with small padding.
- **Board Cell** — `{colors.board_background}` fill, 1px `{colors.grid_lines}` border, 60px × 60px square.
- **Legal Move Cell** — `{colors.legal_move_highlight}` fill, 2px dark green border, indicates placement is legal.
- **Target Cell** — `{colors.target_square_highlight}` fill, 2px dark golden border, indicates dice-determined square.
- **Hover Cell** — 3px `{colors.hover_outline}` border, indicates mouse hover or keyboard focus.
- **Primary Button** — `{button_primary}` styling for main actions (New Game).
- **Secondary Button** — `{button_secondary}` styling for secondary actions (Quit).

## Do's and Don'ts

| Do | Don't |
|---|---|
| Use high-contrast solid colors for game elements | Use gradients or shadows on game pieces |
| Maintain consistent cell sizing across the board | Vary cell sizes or spacing |
| Highlight legal moves and target squares clearly | Leave players guessing which squares are legal |
| Use system fonts for native desktop feel | Load custom web fonts |
| Keep the board centered and prominent | Clutter the board with decorative elements |
| Provide clear visual feedback for hover/focus states | Rely on color alone for state indication |
