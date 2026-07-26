# Epic 2 Context: Playable Python Rules Foundation

<!-- Generated from planning artifacts. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Establish the Python gameplay core so developers can create a valid game state, roll and resolve target coordinates, discover orthogonal checker groups, and apply legal reserve placements through a deterministic engine API. This epic creates the reliability and rule integrity that later capture logic, desktop UI flows, and AI opponents depend on.

## Stories

- Story 2.1: Establish the Layered Application Skeleton
- Story 2.2: Create and Validate a Game State
- Story 2.3: Discover Orthogonal Groups
- Story 2.4: Roll Dice and Place a Reserve Checker

## Requirements & Constraints

- The foundation must satisfy the baseline rules/data requirements needed for Python gameplay: initial 6×6 board setup, reserve tracking, dice rolling, and group discovery.
- New game state must initialize to the official starting position with 12 on-board checkers, 6 reserve checkers per player, and a recorded starting player.
- State validation must reject malformed board dimensions, invalid colors/coordinates/counts, or other domain-invalid states without mutating existing state.
- Dice logic must generate fair values from 1–6 for both dice and map them to one absolute board coordinate per turn.
- Group discovery must return maximal same-color groups connected orthogonally only; diagonal adjacency must not merge groups.
- Placement must only allow legal empty destinations, decrement the current player reserve by one, and advance turn exactly once.
- Illegal placements and empty-reserve placements must fail atomically with explicit domain errors (for example, `IllegalMoveError` or `InvalidGameStateError`).
- Tests must cover deterministic game-engine behavior, package import integrity, and rule-invariant preservation for failed actions.

## Technical Decisions

- Use a strict layered structure: `game_engine/` (rules/state), `ai/` (move selection), `ui/` (Tkinter presentation) with one-way dependencies UI → AI → game engine.
- Treat the game engine as the single authority over mutable state; UI and AI consume state and request actions but do not mutate state directly.
- Model board/state with Python dataclasses and a 6×6 internal structure using zero-based absolute coordinates.
- Keep perspective conversion outside engine logic; only UI-facing code should translate player perspective.
- Implement group detection using orthogonal flood fill and ensure each checker belongs to exactly one maximal group.
- Standardize AI integration with `get_move(game_state, player_color)` returning a coordinate or `None`; engine remains responsible for legality enforcement.
- Enforce naming and consistency conventions: snake_case modules/functions, PascalCase classes, UPPER_CASE constants.

## Cross-Story Dependencies

- Story 2.1 underpins Stories 2.2–2.4 by enforcing package boundaries and test scaffolding.
- Story 2.2 (validated canonical game state) is a prerequisite for Story 2.3 group discovery and Story 2.4 roll/place transitions.
- Story 2.3 is required by Epic 3 capture rules, which depend on correct maximal-group identification.
- Story 2.4 establishes turn progression and legal placement flow used directly by Epic 3 rule completion, Epic 4 desktop interaction, and Epic 5 AI turn execution.

