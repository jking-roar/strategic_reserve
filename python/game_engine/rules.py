from random import random
from math import isfinite
from typing import Callable

from .errors import IllegalMoveError, InvalidGameStateError
from .models import BLUE, BOARD_SIZE, RED, DiceRoll, GameState, TurnContext
from .groups import group_at
from .state import clone_state
from .validation import validate_game_state


def _other(player: str) -> str:
    return BLUE if player == RED else RED


def _roll_die(rng: Callable[[], float]) -> int:
    try:
        value = float(rng())
    except (TypeError, ValueError) as exc:
        raise InvalidGameStateError("RNG must produce a numeric value.") from exc

    if not isfinite(value):
        raise InvalidGameStateError("RNG must produce a finite numeric value.")

    normalized = max(0.0, min(value, 1.0 - 1e-12))
    return 1 + int(normalized * BOARD_SIZE)


def _inside(row: int, col: int) -> bool:
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def _neighbors(point: tuple[int, int]) -> list[tuple[int, int]]:
    row, col = point
    return [
        (r, c)
        for r, c in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
        if _inside(r, c)
    ]


def _empty_squares(board: list[list[str | None]]) -> list[tuple[int, int]]:
    return [
        (row, col)
        for row in range(BOARD_SIZE)
        for col in range(BOARD_SIZE)
        if board[row][col] is None
    ]


def _remove_group(state: GameState, group: list[tuple[int, int]], owner: str) -> None:
    for row, col in group:
        state.board[row][col] = None
    state.reserves[owner] += len(group)


def _resolve_legal_moves(state: GameState) -> list[tuple[int, int]]:
    target = state.turn_context.target
    if target is None:
        raise InvalidGameStateError("Roll target is required before resolution.")

    player = state.current_player
    enemy = _other(player)
    row, col = target
    occupant = state.board[row][col]

    if occupant == enemy:
        _remove_group(state, group_at(state.board, target), enemy)
        return _empty_squares(state.board)

    if occupant == player:
        friendly_group = group_at(state.board, target)
        captured_groups: dict[frozenset[tuple[int, int]], list[tuple[int, int]]] = {}
        for point in friendly_group:
            for neighbor in _neighbors(point):
                n_row, n_col = neighbor
                if state.board[n_row][n_col] == enemy:
                    enemy_group = group_at(state.board, neighbor)
                    captured_groups.setdefault(frozenset(enemy_group), enemy_group)

        for enemy_group in captured_groups.values():
            _remove_group(state, enemy_group, enemy)

        legal_moves = {
            neighbor
            for point in friendly_group
            for neighbor in _neighbors(point)
            if state.board[neighbor[0]][neighbor[1]] is None
        }
        return sorted(legal_moves)

    return _empty_squares(state.board)


def _advance_turn(state: GameState, player: str) -> None:
    state.current_player = _other(player)
    state.turn += 1
    state.turn_context = TurnContext()


def target_from_roll(player: str, column: int, row: int) -> tuple[int, int]:
    if (
        type(column) is not int
        or type(row) is not int
        or column not in range(1, BOARD_SIZE + 1)
        or row not in range(1, BOARD_SIZE + 1)
    ):
        raise InvalidGameStateError("Dice values must be integers from 1 through 6.")
    if player == RED:
        return (BOARD_SIZE - row, column - 1)
    if player == BLUE:
        return (row - 1, BOARD_SIZE - column)
    raise InvalidGameStateError("Invalid player color.")


def roll_dice(state: GameState, rng: Callable[[], float] = random) -> GameState:
    validate_game_state(state)
    if (
        state.turn_context.dice is not None
        or state.turn_context.target is not None
        or state.turn_context.legal_moves
    ):
        raise IllegalMoveError("Cannot re-roll after a roll has already been resolved.")

    column = _roll_die(rng)
    row = _roll_die(rng)
    target = target_from_roll(state.current_player, column, row)

    next_state = clone_state(state)
    next_state.turn_context = TurnContext(dice=DiceRoll(column=column, row=row), target=target)
    legal_moves = _resolve_legal_moves(next_state)
    if next_state.reserves[next_state.current_player] <= 0:
        legal_moves = []
    next_state.turn_context.legal_moves = legal_moves
    validate_game_state(next_state)
    return next_state


def legal_destinations(state: GameState) -> list[tuple[int, int]]:
    validate_game_state(state)
    if state.turn_context.dice is None or state.turn_context.target is None:
        raise IllegalMoveError("Roll must be resolved before requesting legal destinations.")
    return list(state.turn_context.legal_moves)


def pass_turn(state: GameState) -> GameState:
    validate_game_state(state)

    if state.turn_context.dice is None or state.turn_context.target is None:
        raise IllegalMoveError("Roll must be resolved before passing a turn.")

    if state.turn_context.legal_moves:
        raise IllegalMoveError("Cannot pass while legal placements are available.")

    player = state.current_player
    next_state = clone_state(state)
    _advance_turn(next_state, player)
    validate_game_state(next_state)
    return next_state


def apply_placement(state: GameState, destination: tuple[int, int]) -> GameState:
    validate_game_state(state)

    if state.turn_context.dice is None or state.turn_context.target is None:
        raise IllegalMoveError("Roll must be resolved before placing a checker.")

    if not state.turn_context.legal_moves:
        raise IllegalMoveError("No legal placements are available; pass the turn instead.")

    if (
        not isinstance(destination, tuple)
        or len(destination) != 2
        or not all(type(value) is int for value in destination)
    ):
        raise IllegalMoveError("Destination must be a (row, col) tuple.")

    row, col = destination
    player = state.current_player

    if not _inside(row, col):
        raise IllegalMoveError("Destination is out of board bounds.")

    if state.reserves[player] <= 0:
        raise IllegalMoveError("Active player has no reserve checkers left.")

    if destination not in state.turn_context.legal_moves:
        raise IllegalMoveError("Destination is not legal for the resolved roll.")

    if state.board[row][col] is not None:
        raise IllegalMoveError("Destination is already occupied.")

    next_state = clone_state(state)
    next_state.board[row][col] = player
    next_state.reserves[player] -= 1
    _advance_turn(next_state, player)
    validate_game_state(next_state)
    return next_state
