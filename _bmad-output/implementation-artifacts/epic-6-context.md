# Epic 6 Context: Accessible Desktop Release Experience

<!-- Generated from planning artifacts. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Deliver a desktop release in which keyboard and assistive-technology users can complete every supported PvP and PvC journey with information equivalent to pointer and visual interaction, while ensuring the distributable application satisfies the documented visual, dependency, quality, and attribution contract.

## Stories

- Story 6.1: Play the Board Entirely by Keyboard
- Story 6.2: Announce State and Meet Contrast Standards
- Story 6.3: Validate the Release Journey

## Requirements & Constraints

- Every available game action must have keyboard parity. Arrow keys move focus predictably within the 6×6 board; Enter and Space activate a legal focused square; Tab and Shift+Tab traverse interactive surfaces in visual order; Escape cancels selection or closes a non-destructive dialog.
- Turn changes, dice values and target, captures, reserve changes, invalid actions, and the winner must be communicated with concise accessible text. Gameplay information must never depend on color alone, and no further board input is accepted after a win.
- Normal, hover, focus, legal, target, and disabled states must preserve visible focus and meet WCAG AA contrast for text and essential indicators. Legal destinations, the rolled target, and pointer or keyboard focus must remain mutually distinguishable.
- A clean supported Python environment must launch the desktop application using the documented instructions and only declared dependencies. Tkinter is the desktop UI framework and is supplied with Python; the product is desktop-only and does not require responsive behavior.
- Release validation must cover complete PvP games and both rudimentary and advanced PvC difficulties, including setup, dice rolls, captures, placement, win, restart, and quit. Automated and manual checks must satisfy the requirements coverage map with no critical defects.
- The release artifact must document game attribution, controls, launch and test commands, supported environment, and known limitations.
- The desktop release remains local-only: online multiplayer, mobile support, save/load, replay, tutorial, audio, and custom themes are outside MVP scope. In-progress quit and restart actions require confirmation; quitting outside an active game may be immediate.

## Technical Decisions

- Preserve the layered dependency direction: UI may depend on AI and Game Engine, AI may depend only on Game Engine, and Game Engine depends on neither. The Game Engine exclusively owns and mutates board, reserve, turn, and winner state; the UI renders current state and translates user intent into engine operations.
- Engine and AI coordinates are absolute zero-indexed `(row, col)` values on the 6×6 board. Player-perspective conversion belongs only in the UI and must have unit coverage for both perspectives, including keyboard movement and announced coordinates.
- The UI catches domain rule errors and turns them into user-friendly feedback; rule violations use custom engine exceptions. AI failures return `None` rather than raising into the UI, and all moves remain subject to engine legality validation. Do not use bare exception handlers.
- Keep assistive output synchronized from authoritative engine state rather than maintaining a second mutable accessibility state. UI interaction logic must not bypass the same legal-move and terminal-state enforcement used by pointer input.
- Use system fonts and native Tkinter behavior without custom font or web dependencies. Maintain the existing module conventions: snake_case functions/modules, PascalCase classes, uppercase constants, and no global mutable state.
- Release checks must retain the AI response budgets: rudimentary moves complete in under one second and advanced moves in under five seconds without hanging or crashing.

## UX & Interaction Patterns

- The single-window flow moves from Main Menu to Game Board, with a centered game-over announcement and New Game action. Tab order follows the visual hierarchy: top bar, board, then bottom bar and controls.
- Board focus and mouse hover use a 3px orange (`#FF6600`) outline. Legal squares use light green with a dark-green 2px border; the dice target uses gold with a dark-golden 2px border. Preserve borders or another non-color cue whenever states overlap.
- Board cells remain consistent 60px squares with 2px gaps. Red and blue checkers use solid fills with black outlines; grid lines are dark gray on a beige board. Avoid gradients, shadows, decorative patterns, and low-contrast combinations.
- Use concise, direct status language such as turn and winner announcements. A state announcement should combine the active player, purple and green die values, and target location when relevant, without verbose or celebratory copy.
- The quit confirmation is keyboard operable and dismissible with Escape when doing so is non-destructive. Selection applies to the square rather than the checker; drag-and-drop, context menus, and unrelated keyboard shortcuts are not supported.

## Cross-Story Dependencies

- Keyboard navigation and focus semantics from Story 6.1 provide the interaction targets whose announcements, contrast, and state differentiation are audited in Story 6.2.
- Story 6.3 validates the combined accessible interaction contract from Stories 6.1 and 6.2 across the complete game journeys, and depends on the desktop game loop and both AI difficulties delivered by earlier epics.
