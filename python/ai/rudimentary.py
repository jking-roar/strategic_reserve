"""Fast random computer opponent."""

import random
from collections.abc import Callable, Sequence

from game_engine import GameState, IllegalMoveError, legal_destinations


def _resolved_moves(state: GameState, player_color: str) -> list[tuple[int, int]]:
    if state.current_player != player_color:
        raise IllegalMoveError("AI may only act for the current player.")
    return legal_destinations(state)


def get_move(
    game_state: GameState,
    player_color: str,
    *,
    chooser: Callable[[Sequence[tuple[int, int]]], tuple[int, int]] = random.choice,
) -> tuple[int, int]:
    """Choose directly from the engine's legal set without changing ``game_state``."""
    moves = _resolved_moves(game_state, player_color)
    move = chooser(tuple(moves))
    if move not in moves:
        raise IllegalMoveError("AI chooser returned a move outside the legal set.")
    return move
