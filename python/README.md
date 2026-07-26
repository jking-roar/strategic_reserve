# Strategic Reserve Python Desktop Game

Accessible local desktop edition of **Strategic Reserve**, a game by **Mark Steere**.

## Supported environment and installation

Python 3.11+ with Tk 8.6 is supported on graphical Windows, macOS, and Linux
desktops. From the repository root, run `python -m build python/`, install the
wheel from `python/dist/` in a virtual environment, then launch the installed
`strategic-reserve` command. There are no third-party runtime dependencies.
Linux Python installations may require the OS package `python3-tk`.

## Play locally

Tkinter is the only GUI dependency. From the repository root, launch with:

```bash
python python/main.py
```

Choose local two-player play or either computer difficulty. In computer mode,
the human plays Red and the computer plays Blue; Blue's strategic search runs
off the Tk event thread and human controls remain locked for its entire turn.
Roll explicitly, then choose a legal square:

- **Pointer:** select a green legal square.
- **Keyboard:** use Tab to reach the board, arrow keys to move, and Enter or
  Space to place.
- **Quit:** quitting or closing the window asks for confirmation; Escape or No
  leaves the game unchanged.

The gold marker is the dice target. Focused or hovered squares have a dark-orange
(`#C24100`) outline; legal squares have a labeled border treatment, and the dice
target has a dashed border and `T`. Escape clears the transient square
description without changing selection or game state. Visible status text
reports turns, dice and target coordinates, legal counts, captures, reserves,
invalid actions, and winners for assistive-technology access through
native Tk bridges.

## Capture and placement rules

The engine provides a copy-on-write turn lifecycle: roll the dice, inspect the
resolved target and legal destinations, then place on one of the always-available
legal squares. Enemy hits remove the complete orthogonally
connected enemy group and permit placement on any empty square. Friendly hits
capture each adjacent enemy group once and restrict placement to empty orthogonal
neighbors of the friendly group. Empty hits permit placement on every empty square.
A player whose reserve reaches zero wins immediately and cannot begin another turn.

Dice values must be built-in integers from 1 through 6, and placement coordinates
must be built-in integers using zero-based board coordinates. Every successful placement advances
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
- `ai/` rudimentary and bounded strategic opponents (depends on `game_engine` only)
- `ui/` replaceable Tk presentation/controller (depends on `ai` and `game_engine`)
- `tests/` engine, terminal lifecycle, headless UI-boundary, and architecture tests

The engine remains authoritative for board, reserves, player, turn context, and
winner. Automated tests import and exercise controller boundaries without opening
a window, so they do not require `$DISPLAY`; interactive smoke testing does.

## Known limitations

The application is desktop-only and requires a graphical display plus a Python
build containing Tk. Native screen-reader exposure varies by OS/Tk bridge and is
validated with the manual release checklist. Network play, mobile support,
save/load, replay, tutorials, audio, themes, and custom board sizes are not included.
