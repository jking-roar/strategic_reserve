# Python Edition Notes

Last reviewed: 2026-07-26

## Scope in repository

The Python tree includes the authoritative copy-on-write rules engine and a local
two-player/PvC Tk desktop client.

## Structure

- `python/game_engine/` - datamodels, validation, state creation, group discovery, dice roll mapping, and basic placement transition.
- `python/ai/` - checked rudimentary and deadline-bounded advanced strategies.
- `python/ui/` - replaceable board, controls, and single-window controller.
- `python/tests/` - architecture and engine foundation tests.

## Implemented behaviors

- Official initial board and reserve setup via `create_game`.
- Game-state invariants via `validate_game_state`.
- Orthogonal group detection via `group_at` and `groups_for_color`.
- Dice roll generation and player-perspective target mapping via `roll_dice` and `target_from_roll`.
- Complete capture/placement/pass flow and engine-owned terminal winner lifecycle.
- Non-blocking dice animation, legal-square activation, restart, and protected quit.
- PvC configuration with Blue computer turns, generation-safe result handoff,
  and all 36 opponent dice outcomes in each completed advanced candidate.

## Not implemented yet

- Desktop release packaging and accessibility polish beyond keyboard operation.

## Commands

From `python/`:

```bash
python -m pytest
```

From repo root:

```bash
python -m pytest python/tests
python python/main.py
```

Tests are headless and do not need a display server. Launching the application
does require Tkinter and a graphical display.
