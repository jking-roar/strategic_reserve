# Epic 7 Context: Remove Unreachable No-Legal-Move Flow

<!-- Generated from planning artifacts. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Ensure players and maintainers encounter only states permitted by the official rules by proving that every valid, non-terminal resolved roll has a legal placement, rejecting fabricated states that violate that invariant, and removing the pass/no-placement flow from both game editions, their AI and UI layers, tests, and current documentation. This keeps turn progression direct and makes the Python and browser implementations consistent without preserving defensive behavior for unreachable positions.

## Stories

- Story 7.1: Encode the Legal-Placement Invariant
- Story 7.2: Remove Pass Handling from Both Game Engines
- Story 7.3: Remove Pass Handling from AI, UI, and Documentation

## Requirements & Constraints

- Every valid, active state must resolve every one of the 36 dice outcomes to at least one legal, empty, in-bounds placement square. An empty or enemy target permits placement on an empty square; removing an enemy target group makes its target square empty; and a friendly target group has an orthogonal boundary square that is empty after adjacent enemy groups are removed.
- Checker conservation is part of the proof and validation boundary: each player owns twelve checkers across board and reserve, so at most 24 of the 36 squares can be occupied and at least twelve remain empty. A player whose reserve is empty has already won and cannot begin another active turn.
- A non-terminal resolved state with no legal placements is invalid and must be rejected at the engine boundary rather than represented as a passable turn.
- Remove Python pass operations, no-placement exceptions, and path-specific exports and tests. Remove browser `await-pass`/`pass` transitions, messages, and synthetic pass tests. Preserve dice mapping, group removal, reserve conservation, placement rules, turn alternation, and immediate victory detection.
- Equivalent valid positions and rolls in the Python and browser engines must yield non-empty legal sets with the same rules semantics.
- Both AI difficulties must return a legal absolute `(row, column)` coordinate for valid resolved active states. Removing nullable no-move recovery must not weaken state immutability or the rudimentary under-one-second and advanced under-five-second decision deadlines.
- Browser and desktop gameplay must proceed from roll resolution directly to placement. Remove pass controls, announcements, acknowledgement focus behavior, and automatic AI pass branches while retaining clear target and legal-placement feedback, mouse/keyboard parity, visible focus, and screen-reader state announcements.
- Current normative requirements, accessibility copy, READMEs, implementation specifications, and tests must describe the invariant rather than no-legal-play support. Historical completed artifacts may remain only when clearly identified as historical or must otherwise be updated consistently.
- Engine, AI, UI, static, architecture, and release-journey checks must remain green, with explicit invariant coverage replacing pass-flow coverage.

## Technical Decisions

- The game engine remains the sole owner and mutator of board, reserve, current-player, and winner state. It validates the legal-placement invariant and exposes legal coordinates; neither AI nor UI may compensate for invalid engine output.
- Dependencies continue downward only: UI depends on AI and engine, AI depends on engine, and the engine depends on neither. Keep the browser and Python state machines aligned while respecting their existing edition boundaries.
- Engine logic uses absolute zero-based coordinates on the 6×6 board. Perspective conversion remains a UI concern, and AI receives and returns absolute coordinates.
- Legal destinations must follow hit semantics: any empty square for empty and enemy hits, or an empty orthogonally adjacent boundary square for a friendly hit after capture resolution. Group membership is maximal and orthogonal; diagonal adjacency does not connect groups.
- Rule violations use the engine's invalid-state/domain-error mechanism. Impossible no-placement results are invariant failures, not ordinary control flow or user-facing recovery states.
- AI remains stateless, receives state as input, returns only a move coordinate, and never mutates engine state. The engine must still validate an AI-selected placement before applying it.

## UX & Interaction Patterns

After each roll, display both dice, highlight the target, and distinctly highlight every legal placement square; then accept placement by click or keyboard navigation. AI turns calculate and place automatically. Do not introduce an intermediate acknowledgement or pass action. Legal moves must remain identifiable by more than color, focus order must remain coherent without removed pass controls, and assistive announcements must describe the current turn, dice, target, and placement state without mentioning no-move or pass behavior.

## Cross-Story Dependencies

Story 7.1 establishes and tests the invariant that makes deletion safe. Story 7.2 then simplifies both engines and establishes cross-edition parity. Story 7.3 relies on those non-null engine contracts to remove AI and presentation fallbacks and to update normative documentation and end-to-end checks. The cleanup also depends on existing capture, reserve-conservation, victory, AI-deadline, accessibility, and release-journey behavior remaining intact.
