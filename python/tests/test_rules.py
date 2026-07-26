from copy import deepcopy

import pytest

from game_engine import (
    CHECKERS_PER_PLAYER,
    BLUE,
    DiceRoll,
    GameState,
    RED,
    TurnContext,
    IllegalMoveError,
    InvalidGameStateError,
    apply_placement,
    create_game,
    legal_destinations,
    pass_turn,
    roll_dice,
    target_from_roll,
    validate_game_state,
)


def test_target_from_roll_maps_by_player_perspective() -> None:
    assert target_from_roll(RED, 1, 1) == (5, 0)
    assert target_from_roll(RED, 6, 6) == (0, 5)
    assert target_from_roll(BLUE, 1, 1) == (0, 5)
    assert target_from_roll(BLUE, 6, 6) == (5, 0)


def test_target_from_roll_rejects_invalid_inputs_with_domain_error() -> None:
    for column, row in ((0, 2), (7, 2), (1.0, 2), (1, "2"), (True, 2), (1, False)):
        with pytest.raises(InvalidGameStateError):
            target_from_roll(RED, column, row)  # type: ignore[arg-type]

    with pytest.raises(InvalidGameStateError):
        target_from_roll("GREEN", 1, 1)


def _rng_for_dice(column: int, row: int):
    values = iter(((column - 1) / 6, (row - 1) / 6))
    return lambda: next(values)


def _state_from_rows(rows: list[str], current_player: str = RED, reserves: dict[str, int] | None = None) -> GameState:
    board = [
        [RED if token == "R" else BLUE if token == "B" else None for token in row]
        for row in rows
    ]
    if reserves is None:
        red_count = sum(cell == RED for row in board for cell in row)
        blue_count = sum(cell == BLUE for row in board for cell in row)
        reserves = {RED: CHECKERS_PER_PLAYER - red_count, BLUE: CHECKERS_PER_PLAYER - blue_count}
    state = GameState(board=board, reserves=reserves, current_player=current_player, turn_context=TurnContext())
    validate_game_state(state)
    return state


def test_roll_dice_persists_values_and_target() -> None:
    values = iter([0.0, 0.999999])
    state = create_game()

    rolled = roll_dice(state, rng=lambda: next(values))

    assert rolled.turn_context.dice is not None
    assert rolled.turn_context.dice.column == 1
    assert rolled.turn_context.dice.row == 6
    assert rolled.turn_context.target == target_from_roll(state.current_player, 1, 6)
    assert rolled.turn_context.legal_moves


def test_enemy_hit_removes_maximal_group_and_opens_all_empty_squares() -> None:
    state = _state_from_rows(
        [
            "......",
            "..B...",
            ".BB...",
            "...R..",
            "......",
            "......",
        ]
    )

    rolled = roll_dice(state, rng=_rng_for_dice(3, 4))

    assert rolled.board[1][2] is None
    assert rolled.board[2][1] is None
    assert rolled.board[2][2] is None
    assert rolled.reserves[BLUE] == 12

    legal = legal_destinations(rolled)
    assert len(legal) == 35
    assert all(rolled.board[row][col] is None for row, col in legal)
    assert rolled.board[3][3] == RED


def test_enemy_hit_preserves_diagonal_and_disconnected_enemy_checkers() -> None:
    state = _state_from_rows(
        [
            "B.....",
            ".BB...",
            ".B....",
            "...B..",
            "......",
            ".....B",
        ]
    )

    rolled = roll_dice(state, rng=_rng_for_dice(2, 5))

    assert rolled.board[1][1] is None
    assert rolled.board[1][2] is None
    assert rolled.board[2][1] is None
    assert rolled.board[0][0] == BLUE
    assert rolled.board[3][3] == BLUE
    assert rolled.board[5][5] == BLUE
    assert rolled.reserves[BLUE] == 9


def test_friendly_hit_captures_adjacent_enemy_groups_once_and_constrains_placement() -> None:
    state = _state_from_rows(
        [
            "......",
            ".BB...",
            "..RR..",
            "..B...",
            "......",
            "......",
        ]
    )

    rolled = roll_dice(state, rng=_rng_for_dice(3, 4))

    assert rolled.reserves[BLUE] == 12
    assert rolled.board[1][1] is None
    assert rolled.board[1][2] is None
    assert rolled.board[3][2] is None

    assert set(legal_destinations(rolled)) == {
        (1, 2),
        (3, 2),
        (2, 1),
        (1, 3),
        (3, 3),
        (2, 4),
    }
    assert len(legal_destinations(rolled)) == len(set(legal_destinations(rolled)))


def test_empty_hit_allows_free_placement_without_capture_side_effects() -> None:
    state = _state_from_rows(
        [
            ".R....",
            "......",
            "..B...",
            "......",
            "......",
            "......",
        ]
    )

    rolled = roll_dice(state, rng=_rng_for_dice(6, 1))
    legal = legal_destinations(rolled)

    assert rolled.turn_context.target == (5, 5)
    assert set(legal) == {
        (row, col)
        for row in range(6)
        for col in range(6)
        if rolled.board[row][col] is None
    }

    next_state = apply_placement(rolled, legal[0])
    assert next_state.reserves[BLUE] == rolled.reserves[BLUE]
    assert next_state.current_player == BLUE


def test_roll_dice_rejects_reroll_in_same_turn() -> None:
    state = create_game()
    rolled = roll_dice(state, rng=lambda: 0.2)
    original = deepcopy(rolled)
    with pytest.raises(IllegalMoveError):
        roll_dice(rolled, rng=lambda: 0.3)
    assert rolled == original


def test_roll_dice_rejects_non_finite_or_non_numeric_rng() -> None:
    state = create_game()
    with pytest.raises(InvalidGameStateError):
        roll_dice(state, rng=lambda: float("nan"))

    with pytest.raises(InvalidGameStateError):
        roll_dice(state, rng=lambda: "oops")


def test_apply_placement_advances_turn_and_decrements_reserve() -> None:
    state = roll_dice(create_game(), rng=lambda: 0.2)

    next_state = apply_placement(state, (0, 0))
    assert next_state.board[0][0] == RED
    assert next_state.reserves[RED] == 5
    assert next_state.current_player == BLUE
    assert next_state.turn == state.turn + 1
    assert next_state.turn_context.dice is None
    assert next_state.turn_context.target is None
    assert next_state.turn_context.legal_moves == []


@pytest.mark.parametrize("player", [RED, BLUE])
def test_every_dice_outcome_maps_resolves_and_preserves_conservation(player: str) -> None:
    state = _state_from_rows(
        ["R.....", "......", "..B...", "......", "....R.", ".....B"],
        current_player=player,
    )

    targets = set()
    board_size = len(state.board)
    for column in range(1, board_size + 1):
        for row in range(1, board_size + 1):
            rolled = roll_dice(state, rng=_rng_for_dice(column, row))
            expected = target_from_roll(player, column, row)
            targets.add(expected)
            assert rolled.turn_context.target == expected
            validate_game_state(rolled)
            legal = legal_destinations(rolled)
            assert len(legal) == len(set(legal))
            assert all(0 <= r < board_size and 0 <= c < board_size for r, c in legal)
            assert all(rolled.board[r][c] is None for r, c in legal)
            for owner in (RED, BLUE):
                on_board = sum(cell == owner for board_row in rolled.board for cell in board_row)
                assert on_board + rolled.reserves[owner] == CHECKERS_PER_PLAYER

            completed = apply_placement(rolled, legal[0]) if legal else pass_turn(rolled)
            validate_game_state(completed)
            assert completed.current_player != player
            assert completed.turn == state.turn + 1
            assert completed.turn_context == TurnContext()
            for owner in (RED, BLUE):
                on_board = sum(cell == owner for board_row in completed.board for cell in board_row)
                assert on_board + completed.reserves[owner] == CHECKERS_PER_PLAYER

    assert targets == {(row, col) for row in range(board_size) for col in range(board_size)}


def test_no_legal_move_after_resolution_can_be_passed_without_hanging() -> None:
    state = create_game()
    state.turn_context = TurnContext(
        dice=DiceRoll(column=1, row=1), target=target_from_roll(RED, 1, 1), legal_moves=[]
    )
    rolled = state
    assert legal_destinations(rolled) == []

    passed = pass_turn(rolled)
    assert passed.current_player == BLUE
    assert passed.turn == rolled.turn + 1
    assert passed.turn_context == TurnContext()


@pytest.mark.parametrize(
    ("rows", "dice", "placement"),
    [
        (["B.....", "......", "..R...", "......", "......", "......"], (1, 6), (5, 5)),
        (["RR....", "B.....", "..B...", "......", "......", "......"], (1, 6), (0, 2)),
        ([".R....", "......", "..B...", "......", "......", "......"], (6, 1), (4, 4)),
    ],
)
def test_full_turn_preserves_invariants_across_target_categories_and_boundaries(
    rows: list[str], dice: tuple[int, int], placement: tuple[int, int]
) -> None:
    state = _state_from_rows(rows)
    rolled = roll_dice(state, rng=_rng_for_dice(*dice))
    completed = apply_placement(rolled, placement)

    validate_game_state(completed)
    assert completed.turn == state.turn + 1
    assert completed.current_player == BLUE
    assert completed.turn_context == TurnContext()

    for player in (RED, BLUE):
        on_board = sum(cell == player for row in completed.board for cell in row)
        assert on_board + completed.reserves[player] == CHECKERS_PER_PLAYER


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

    state = roll_dice(
        _state_from_rows(["RR....", "B.....", "..B...", "......", "......", "......"]),
        rng=_rng_for_dice(1, 6),
    )
    original = deepcopy(state)
    with pytest.raises(IllegalMoveError):
        apply_placement(state, (5, 5))  # empty but not legal for this friendly-hit turn
    assert state == original

    with pytest.raises(IllegalMoveError):
        pass_turn(state)
    assert state == original


@pytest.mark.parametrize("destination", [(True, 0), (0, False), [0, 0], (0.0, 0), (0, "0")])
def test_apply_placement_rejects_non_integral_coordinates_atomically(destination: object) -> None:
    rolled = roll_dice(create_game(), rng=_rng_for_dice(1, 1))
    original = deepcopy(rolled)

    with pytest.raises(IllegalMoveError):
        apply_placement(rolled, destination)  # type: ignore[arg-type]

    assert rolled == original


def test_legal_destinations_returns_a_defensive_copy() -> None:
    rolled = roll_dice(create_game(), rng=_rng_for_dice(1, 1))
    returned = legal_destinations(rolled)
    expected = list(returned)

    returned.clear()

    assert legal_destinations(rolled) == expected


def test_rejected_roll_and_pass_leave_input_state_unchanged() -> None:
    state = create_game()
    original = deepcopy(state)
    with pytest.raises(InvalidGameStateError):
        roll_dice(state, rng=lambda: object())
    assert state == original
    with pytest.raises(IllegalMoveError):
        pass_turn(state)
    assert state == original


def test_last_reserve_placement_declares_winner_and_guards_actions() -> None:
    state = _state_from_rows(
        ["RRRRRR", "RRRRR.", "B.....", "......", "......", "......"],
        reserves={RED: 1, BLUE: 11},
    )
    rolled = roll_dice(state, rng=_rng_for_dice(6, 1))
    won = apply_placement(rolled, (5, 5))

    assert won.winner == RED
    assert won.current_player == RED
    assert won.reserves[RED] == 0
    assert won.turn == state.turn
    assert won.turn_context == TurnContext()
    for action in (roll_dice, pass_turn):
        with pytest.raises(IllegalMoveError):
            action(won)
    with pytest.raises(IllegalMoveError):
        apply_placement(won, (4, 4))
