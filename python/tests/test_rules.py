from copy import deepcopy

import pytest

from game_engine import (
    BLUE,
    RED,
    IllegalMoveError,
    InvalidGameStateError,
    apply_placement,
    create_game,
    roll_dice,
    target_from_roll,
)


def test_target_from_roll_maps_by_player_perspective() -> None:
    assert target_from_roll(RED, 1, 1) == (5, 0)
    assert target_from_roll(RED, 6, 6) == (0, 5)
    assert target_from_roll(BLUE, 1, 1) == (0, 5)
    assert target_from_roll(BLUE, 6, 6) == (5, 0)


def test_target_from_roll_rejects_invalid_inputs_with_domain_error() -> None:
    with pytest.raises(InvalidGameStateError):
        target_from_roll(RED, 0, 2)

    with pytest.raises(InvalidGameStateError):
        target_from_roll("GREEN", 1, 1)


def test_roll_dice_persists_values_and_target() -> None:
    values = iter([0.0, 0.999999])
    state = create_game()

    rolled = roll_dice(state, rng=lambda: next(values))

    assert rolled.turn_context.dice is not None
    assert rolled.turn_context.dice.column == 1
    assert rolled.turn_context.dice.row == 6
    assert rolled.turn_context.target == target_from_roll(state.current_player, 1, 6)


def test_roll_dice_rejects_reroll_in_same_turn() -> None:
    state = create_game()
    rolled = roll_dice(state, rng=lambda: 0.2)
    with pytest.raises(IllegalMoveError):
        roll_dice(rolled, rng=lambda: 0.3)


def test_roll_dice_rejects_non_finite_or_non_numeric_rng() -> None:
    state = create_game()
    with pytest.raises(InvalidGameStateError):
        roll_dice(state, rng=lambda: float("nan"))

    with pytest.raises(InvalidGameStateError):
        roll_dice(state, rng=lambda: "oops")


def test_apply_placement_advances_turn_and_decrements_reserve() -> None:
    state = create_game()
    state.turn_context = deepcopy(roll_dice(state, rng=lambda: 0.2).turn_context)

    next_state = apply_placement(state, (0, 0))
    assert next_state.board[0][0] == RED
    assert next_state.reserves[RED] == 5
    assert next_state.current_player == BLUE
    assert next_state.turn == state.turn + 1
    assert next_state.turn_context.dice is None
    assert next_state.turn_context.target is None


def test_apply_placement_rejects_illegal_and_keeps_state_unchanged() -> None:
    state = create_game()
    original = deepcopy(state)
    with pytest.raises(IllegalMoveError):
        apply_placement(state, (1, 1))  # occupied
    assert state == original

    with pytest.raises(IllegalMoveError):
        apply_placement(state, (-1, 0))

    state = create_game()
    original = deepcopy(state)
    with pytest.raises(IllegalMoveError):
        apply_placement(state, (0, 0))
    assert state == original

    state = create_game()
    for row, col in ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)):
        state.board[row][col] = RED
    state.reserves[RED] = 0
    state.turn_context = deepcopy(roll_dice(state, rng=lambda: 0.2).turn_context)
    original = deepcopy(state)
    with pytest.raises(IllegalMoveError):
        apply_placement(state, (5, 5))
    assert state == original

