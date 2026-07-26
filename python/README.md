# Strategic Reserve Python Core

Python gameplay foundation for Strategic Reserve.

## Capture and placement rules

The engine provides a copy-on-write turn lifecycle: roll the dice, inspect the
resolved target and legal destinations, then either place a checker or explicitly
pass when no placement is available. Enemy hits remove the complete orthogonally
connected enemy group and permit placement on any empty square. Friendly hits
capture each adjacent enemy group once and restrict placement to empty orthogonal
neighbors of the friendly group. Empty hits permit placement on every empty square.
When the active player has no reserve checker, resolution exposes no placement and
the caller completes the turn with the explicit pass operation.

Dice values must be built-in integers from 1 through 6, and placement coordinates
must be built-in integers using zero-based board coordinates. Every successful placement or legal pass advances
the turn exactly once, while rejected actions leave caller-owned state unchanged.
The scenario suite covers maximal groups, multi-contact capture de-duplication,
diagonal and disconnected survival, both player perspectives across all 36 dice
outcomes, defensive copies, atomic failures, conservation, and complete turns.

## Run tests

```bash
python -m pytest
```

## Layout

- `game_engine/` core rules, state, validation, and group logic
- `ai/` AI integration boundary (depends on `game_engine` only)
- `ui/` UI integration boundary (depends on `ai`/`game_engine`)
- `tests/` Epic 2 foundation and Epic 3 capture/placement scenario tests
