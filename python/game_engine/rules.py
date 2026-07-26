from random import random
from math import isfinite
from typing import Callable

from .errors import IllegalMoveError, InvalidGameStateError
from .models import BLUE, BOARD_SIZE, RED, DiceRoll, GameState, TurnContext
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


def target_from_roll(player: str, column: int, row: int) -> tuple[int, int]:
    if column not in range(1, BOARD_SIZE + 1) or row not in range(1, BOARD_SIZE + 1):
        raise InvalidGameStateError("Dice values must be integers from 1 through 6.")
    if player == RED:
        return (BOARD_SIZE - row, column - 1)
    if player == BLUE:
        return (row - 1, BOARD_SIZE - column)
    raise InvalidGameStateError("Invalid player color.")


def roll_dice(state: GameState, rng: Callable[[], float] = random) -> GameState:
    validate_game_state(state)
    if state.turn_context.dice is not None or state.turn_context.target is not None:
        raise IllegalMoveError("Cannot re-roll after a roll has already been resolved.")

    column = _roll_die(rng)
    row = _roll_die(rng)
    target = target_from_roll(state.current_player, column, row)

    next_state = clone_state(state)
    next_state.turn_context = TurnContext(dice=DiceRoll(column=column, row=row), target=target)
    validate_game_state(next_state)
    return next_state


def apply_placement(state: GameState, destination: tuple[int, int]) -> GameState:
    validate_game_state(state)

    if state.turn_context.dice is None or state.turn_context.target is None:
        raise IllegalMoveError("Roll must be resolved before placing a checker.")

    if (
        not isinstance(destination, tuple)
        or len(destination) != 2
        or not all(isinstance(value, int) for value in destination)
    ):
        raise IllegalMoveError("Destination must be a (row, col) tuple.")

    row, col = destination
    player = state.current_player

    if not _inside(row, col):
        raise IllegalMoveError("Destination is out of board bounds.")

    if state.reserves[player] <= 0:
        raise IllegalMoveError("Active player has no reserve checkers left.")

    if state.board[row][col] is not None:
        raise IllegalMoveError("Destination is already occupied.")

    next_state = clone_state(state)
    next_state.board[row][col] = player
    next_state.reserves[player] -= 1
    next_state.current_player = _other(player)
    next_state.turn += 1
    next_state.turn_context = TurnContext()
    validate_game_state(next_state)
    return next_state

