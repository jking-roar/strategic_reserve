# Strategic Reserve Python Core

Python gameplay foundation for Strategic Reserve.

## Run tests

```bash
python -m pytest
```

## Layout

- `game_engine/` core rules, state, validation, and group logic
- `ai/` AI integration boundary (depends on `game_engine` only)
- `ui/` UI integration boundary (depends on `ai`/`game_engine`)
- `tests/` Epic 2 foundation tests

