# Epic 3 Context: Complete Python Capture and Placement Rules

<!-- Generated from planning artifacts. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Complete the Python game engine's roll-resolution behavior so every target category—enemy group, friendly group, or empty square—produces the official captures and legal placement destinations while preserving valid, authoritative game state. This closes the Python edition's core rules gap and provides dependable turn behavior for the later desktop UI and computer opponents.

## Stories

- Story 3.1: Resolve an Enemy-Group Hit
- Story 3.2: Resolve a Friendly-Group Hit
- Story 3.3: Resolve an Empty-Square Hit
- Story 3.4: Preserve Rule Invariants Across Full Turns

## Requirements & Constraints

- An enemy-group hit removes the entire maximal group containing the rolled target, returns every removed checker to the opponent's reserve, and then permits placement on every and only empty board square, including squares emptied by the capture.
- A friendly-group hit removes every enemy group orthogonally adjacent to any member of the targeted friendly group. Each adjacent enemy group must be removed exactly once even when it touches the friendly group at multiple positions, and all removed checkers return to their owner's reserve.
- After a friendly-group hit, legal destinations are every and only empty square orthogonally adjacent to at least one member of the resolved friendly group. Non-adjacent and occupied destinations must be rejected.
- If a friendly-group resolution leaves no adjacent empty destination, the engine must expose no placement and apply the documented no-move turn progression without hanging.
- An empty-square hit performs no capture and permits placement on every and only empty board square.
- A successful placement moves one checker from the active player's reserve to a legal empty destination and advances the turn exactly once. Capture reserve changes and placement reserve changes must remain consistent.
- Invalid destinations and other domain violations must raise an explicit domain error. A failed action must be atomic: no capture, placement, reserve adjustment, or turn transition may survive the failure.
- Automated scenarios must cover all target categories and board boundaries through complete turns. They must verify board occupancy, checker and reserve totals, active-player progression, maximal-group behavior, and unchanged state after rejected actions.
- Resolution must handle every valid board state and all 36 possible dice outcomes without crashing, hanging, or corrupting state.

## Technical Decisions

- The game engine is the sole owner of the board, reserves, current player, and winner. Capture resolution, legal-move calculation, placement validation, and mutation belong in the engine; UI and AI may inspect state but must not mutate it.
- Preserve the layered dependency direction: the engine imports neither AI nor UI, and AI imports no UI code. Epic 3 behavior must therefore be usable as a deterministic engine API independent of Tkinter.
- Represent the board as a 6×6 two-dimensional structure with `None` for empty cells and `RED`/`BLUE` checker values. Use absolute zero-based `(row, col)` coordinates throughout engine logic; the engine maps player-perspective dice values to those coordinates, while display conversion remains a UI concern.
- Discover groups by orthogonal flood fill only. Groups are maximal, diagonal contact never connects pieces, and group collections must not contain duplicate members or subset groups.
- Route all state changes through game-engine methods, use no global mutable state, and validate an action before committing its effects so errors cannot leave partial mutations.
- Signal illegal moves and invalid states with the established custom domain exceptions. Follow snake_case for modules and functions, PascalCase for classes, and UPPER_CASE for constants.
- Keep deterministic rule behavior covered by automated unit and scenario tests; randomness is limited to dice generation, while target resolution and legal-move derivation must be directly testable from known state and roll inputs.

## Cross-Story Dependencies

- This epic depends on the Python foundation for validated game state, absolute-coordinate dice mapping, orthogonal maximal-group discovery, reserve placement, and single turn advancement.
- Enemy, friendly, and empty resolution must share one consistent resolution/placement lifecycle so invariant tests can exercise the same public behavior rather than category-specific mutation paths.
- The desktop game loop and both AI implementations depend on Epic 3's legal-move results and no-move outcome; the API must support a coordinate choice or an explicit absence of legal placement without transferring state ownership to callers.
