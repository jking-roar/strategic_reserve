# Python Edition Notes

Last reviewed: 2026-07-25

## Scope in repository

The Python tree is currently a core engine foundation with package boundaries and unit tests.
It is not yet a complete desktop UI application.

## Structure

- `python/game_engine/` - datamodels, validation, state creation, group discovery, dice roll mapping, and basic placement transition.
- `python/ai/` - AI package boundary placeholder.
- `python/ui/` - UI package boundary placeholder.
- `python/tests/` - architecture and engine foundation tests.

## Implemented behaviors

- Official initial board and reserve setup via `create_game`.
- Game-state invariants via `validate_game_state`.
- Orthogonal group detection via `group_at` and `groups_for_color`.
- Dice roll generation and player-perspective target mapping via `roll_dice` and `target_from_roll`.
- Basic placement action via `apply_placement` (bounds/occupancy/reserve checks, turn advance).

## Not implemented yet

- Enemy/friendly/empty hit capture-resolution flow in Python engine.
- Python AI opponents.
- Python UI gameplay loop.

## Commands

From `python/`:

```bash
python -m pytest
```

From repo root:

```bash
python -m pytest python/tests
```

