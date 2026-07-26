import pytest

from game_engine import BLUE, RED, InvalidGameStateError, group_at, groups_for_color


def test_group_at_returns_orthogonal_component_only() -> None:
    board = [[None for _ in range(6)] for _ in range(6)]
    board[1][1] = RED
    board[1][2] = RED
    board[2][2] = RED
    board[2][1] = BLUE
    board[0][0] = RED  # diagonal-only connection to (1,1)

    group = set(group_at(board, (1, 1)))
    assert group == {(1, 1), (1, 2), (2, 2)}


def test_diagonal_touch_does_not_merge_groups() -> None:
    board = [[None for _ in range(6)] for _ in range(6)]
    board[1][1] = BLUE
    board[2][2] = BLUE

    all_groups = [set(group) for group in groups_for_color(board, BLUE)]
    assert {frozenset(group) for group in all_groups} == {
        frozenset({(1, 1)}),
        frozenset({(2, 2)}),
    }


def test_group_at_rejects_out_of_bounds_coordinate() -> None:
    board = [[None for _ in range(6)] for _ in range(6)]
    with pytest.raises(InvalidGameStateError):
        group_at(board, (6, 0))


def test_groups_for_color_rejects_invalid_color() -> None:
    board = [[None for _ in range(6)] for _ in range(6)]
    with pytest.raises(InvalidGameStateError):
        groups_for_color(board, "GREEN")


def test_group_at_rejects_invalid_board_payloads() -> None:
    with pytest.raises(InvalidGameStateError):
        group_at(["......"] * 6, (0, 0))  # type: ignore[arg-type]

    board = [[None for _ in range(6)] for _ in range(6)]
    board[0][0] = "GREEN"  # type: ignore[assignment]
    with pytest.raises(InvalidGameStateError):
        group_at(board, (0, 0))


