# Epic 1 Context: Browser-Accessible Strategic Reserve

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Publish Strategic Reserve through GitHub Pages and deliver a complete, responsive, keyboard-accessible HTML edition that visitors can discover and play without installing the Python desktop application. The browser game must stand alone as a static release while preserving the Python/Tkinter edition as a separate supported edition.

## Stories

- Story 1.1: Publish the Project Site
- Story 1.2: Explore the Browser Game Shell
- Story 1.3: Play a Complete Local Browser Game
- Story 1.4: Play Against Browser AI
- Story 1.5: Validate the Static Browser Release

## Requirements & Constraints

- Publish a meaningful static entry point through the existing GitHub Pages workflow using only repository-hosted assets and no server-side runtime. All pages, navigation, scripts, styles, and media must resolve when hosted below a project subpath rather than at a domain root.
- Add a prominent playable-site link to the repository README and distinguish the HTML edition from the Python/Tkinter edition. Core title, edition status, and repository navigation must remain understandable even if enhanced assets fail.
- Provide a responsive shell with game title, PvP/PvC mode selection, rudimentary/advanced AI difficulty, New Game, a 6×6 board, purple-column and green-row dice, both reserve counters, concise turn/status text, and project attribution.
- Implement browser-owned state and the complete official game loop without network requests: fair six-sided dice; current-player perspective mapping; maximal orthogonal same-color groups; enemy-group, friendly-group, and empty-square hit resolution; legal placement enforcement; reserve updates; alternating turns; and immediate victory when the active player places their last reserve checker.
- Start with twelve checkers in the official pattern and six reserve checkers per player. Empty and occupied cells, the rolled target, and every legal destination must be clearly distinguishable.
- Support two humans sharing one browser and solo play at two difficulties. Rudimentary AI randomly chooses a legal move within one second. Advanced AI considers all 36 next-roll outcomes and returns its best-so-far legal move within five seconds. Either AI must safely return a legal move or no move for every valid state without corrupting state or indefinitely blocking browser input.
- Validate the production artifact from a non-root base path, full PvP and both PvC flows at desktop and mobile sizes, and setup, roll, capture, placement, win, and restart behavior. Accessibility validation must cover semantic names, announcements, keyboard parity, visible focus, and WCAG AA contrast.

## Technical Decisions

- The HTML edition is independently deployable and must not depend on the Python runtime or a backend. Keep its browser game state authoritative within the edition; rendering and AI move selection must not become competing state authorities.
- Use a 6×6 board and consistent absolute zero-based coordinates for internal rule evaluation. Convert purple-column and green-row rolls from the active player's perspective only at the presentation boundary.
- Discover groups with flood fill using up, down, left, and right neighbors only; diagonals never connect groups. Groups are maximal.
- Treat AI as move selection over game state: it returns a coordinate or no move, and the browser rules layer validates legality before applying it. AI evaluation must not mutate authoritative game state.
- Preserve static-host compatibility throughout: use subpath-safe relative asset references and avoid server rewrites, dynamic endpoints, or domain-root assumptions.

## UX & Interaction Patterns

- Favor a clean, flat, classic-board-game presentation with system fonts, a beige grid, outlined red and blue circular checkers, and high-contrast solid colors. Avoid gradients, shadows, decorative patterns, and custom web fonts.
- Mark legal destinations with light-green fill plus a dark-green border, the dice target with gold fill plus a dark-gold border, and pointer hover or keyboard navigation with an orange outline. Never rely on color alone; provide accessible labels and border/state distinctions.
- Keep the board prominent, with current player and dice near the top and reserves and controls nearby. Reserve counters update immediately after placements and captures. Dice are visually distinguished as purple for column and green for row, show values, and may animate without obscuring state.
- Provide pointer and keyboard parity: logical Tab/Shift+Tab order, visible focus, arrow-key movement among board cells, Enter or Space to place, and Escape to cancel or close. Announce turn, dice, target, state changes, and the winner to assistive technology.
- Use direct microcopy such as “Red's turn,” “Blue wins!,” and “New Game.” On victory, center the announcement, disable further board input, and expose New Game. Confirm quitting an active game with clear Yes/No actions.

## Cross-Story Dependencies

- The published shell and subpath-safe asset strategy established by Stories 1.1–1.2 are prerequisites for browser gameplay and release validation.
- Story 1.3 supplies authoritative rules, legal-move generation, and state transitions used by both AI difficulties in Story 1.4.
- Story 1.5 validates the integrated output of Stories 1.1–1.4 against static hosting, responsive play, gameplay, performance, and accessibility requirements.
