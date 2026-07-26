# Strategic Reserve Python Desktop Game

Python gameplay foundation for Strategic Reserve.

## Play locally

Tkinter is the only GUI dependency. From the repository root, launch with:

```bash
python python/main.py
```

Choose local two-player play or either computer difficulty. In computer mode,
the human plays Red and the computer plays Blue; Blue's strategic search runs
off the Tk event thread and human controls remain locked for its entire turn.
Roll explicitly, then select a
green legal square with the mouse or use Tab, arrow keys, and Enter/Space. The
gold marker is the dice target. When no green square exists, use **Pass**. Quit
or window close confirms before abandoning an unfinished game; Escape/No leaves
the game unchanged.

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
- `ai/` random and bounded strategic opponents (depends on `game_engine` only)
- `ui/` replaceable Tk presentation/controller (depends on `ai` and `game_engine`)
- `tests/` engine, terminal lifecycle, headless UI-boundary, and architecture tests

The engine remains authoritative for board, reserves, player, turn context, and
winner. Automated tests import and exercise controller boundaries without opening
a window, so they do not require `$DISPLAY`; interactive smoke testing does.
