from copy import deepcopy

import pytest

from game_engine import (
    BLUE,
    RED,
    GameState,
    InvalidGameStateError,
    TurnContext,
    create_game,
    validate_game_state,
)


def test_create_game_has_official_setup() -> None:
    state = create_game()
    assert len(state.board) == 6
    assert all(len(row) == 6 for row in state.board)

    red_count = sum(cell == RED for row in state.board for cell in row)
    blue_count = sum(cell == BLUE for row in state.board for cell in row)
    assert red_count + blue_count == 12
    assert red_count == 6
    assert blue_count == 6

    assert state.reserves == {RED: 6, BLUE: 6}
    assert state.current_player in (RED, BLUE)


def test_validate_rejects_bad_board_shape_without_mutation() -> None:
    state = create_game()
    state.board = state.board[:-1]
    original = deepcopy(state)

    with pytest.raises(InvalidGameStateError):
        validate_game_state(state)

    assert state == original


def test_validate_rejects_bad_token_and_coordinate() -> None:
    state = create_game()
    state.board[0][0] = "GREEN"
    with pytest.raises(InvalidGameStateError):
        validate_game_state(state)

    state = create_game()
    state.turn_context = TurnContext(target=(6, 0))
    with pytest.raises(InvalidGameStateError):
        validate_game_state(state)

    state = create_game()
    state.turn_context = TurnContext(target=(True, 0))
    with pytest.raises(InvalidGameStateError):
        validate_game_state(state)


def test_validate_rejects_negative_reserve() -> None:
    state = create_game()
    state.reserves[RED] = -1
    with pytest.raises(InvalidGameStateError):
        validate_game_state(state)


def test_validate_rejects_bool_reserve_counts() -> None:
    state = create_game()
    state.reserves[RED] = True
    with pytest.raises(InvalidGameStateError):
        validate_game_state(state)


def test_validate_rejects_malformed_dice_payload() -> None:
    state = create_game()
    state.turn_context = TurnContext(dice=(1, 2))  # type: ignore[assignment]
    with pytest.raises(InvalidGameStateError):
        validate_game_state(state)


def test_create_game_rejects_invalid_starting_player() -> None:
    with pytest.raises(InvalidGameStateError):
        create_game("GREEN")


def test_validate_rejects_reserve_above_player_total() -> None:
    state = create_game()
    state.reserves[RED] = 13
    with pytest.raises(InvalidGameStateError):
        validate_game_state(state)


def test_validate_rejects_material_non_conservation() -> None:
    state = create_game()
    state.board[0][0] = RED
    with pytest.raises(InvalidGameStateError):
        validate_game_state(state)


