"""Deadline-bounded one-ply strategic computer opponent."""

import time
from math import isfinite
from collections.abc import Callable

from game_engine import BLUE, RED, GameState, apply_placement, roll_dice

from .rudimentary import _resolved_moves


def _score(state: GameState, player: str) -> float:
    opponent = BLUE if player == RED else RED
    if state.winner == player:
        return 1_000_000.0
    if state.winner == opponent:
        return -1_000_000.0
    own_board = sum(cell == player for row in state.board for cell in row)
    enemy_board = sum(cell == opponent for row in state.board for cell in row)
    return (state.reserves[opponent] - state.reserves[player]) * 100 + own_board - enemy_board


def get_move(
    game_state: GameState,
    player_color: str,
    *,
    budget: float = 4.5,
    clock: Callable[[], float] = time.monotonic,
    outcome_observer: Callable[[tuple[int, int], int, int], None] | None = None,
) -> tuple[int, int]:
    """Evaluate complete 36-roll opponent samples while retaining a legal fallback."""
    moves = _resolved_moves(game_state, player_color)
    if not isfinite(budget) or budget < 0:
        raise ValueError("AI budget must be a finite non-negative number.")

    best = moves[0]
    best_score = float("-inf")
    started = clock()
    if not isfinite(started):
        raise ValueError("AI clock must return finite values.")
    deadline = started + min(budget, 4.9)
    for move in moves:
        # Never publish a partially evaluated candidate.
        now = clock()
        if not isfinite(now):
            raise ValueError("AI clock must return finite values.")
        if now >= deadline:
            break
        after_move = apply_placement(game_state, move)
        if after_move.winner == player_color:
            candidate_score = _score(after_move, player_color)
        else:
            total = 0.0
            complete = True
            for column in range(1, 7):
                for row in range(1, 7):
                    now = clock()
                    if not isfinite(now):
                        raise ValueError("AI clock must return finite values.")
                    if now >= deadline:
                        complete = False
                        break
                    values = iter(((column - 0.5) / 6, (row - 0.5) / 6))
                    response = roll_dice(after_move, lambda: next(values))
                    total += _score(response, player_color)
                    if outcome_observer:
                        outcome_observer(move, column, row)
                if not complete:
                    break
            if not complete:
                break
            candidate_score = total / 36
        if candidate_score > best_score:
            best, best_score = move, candidate_score
    return best
