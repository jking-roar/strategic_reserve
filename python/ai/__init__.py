"""Computer-player strategies with a small, stable dispatch API."""

from .advanced import get_move as get_advanced_move
from .rudimentary import get_move as get_rudimentary_move


def get_move(game_state, player_color, difficulty="rudimentary", **kwargs):
    """Return a checked move for ``difficulty`` from an already-resolved turn."""
    strategies = {"rudimentary": get_rudimentary_move, "advanced": get_advanced_move}
    try:
        strategy = strategies[difficulty.lower()]
    except (AttributeError, KeyError) as exc:
        raise ValueError(f"Unknown AI difficulty: {difficulty!r}") from exc
    return strategy(game_state, player_color, **kwargs)


__all__ = ["get_move", "get_rudimentary_move", "get_advanced_move"]
