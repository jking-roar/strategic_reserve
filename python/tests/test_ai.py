"""Safety, dispatch, and bounded-lookahead contracts for both opponents."""

from copy import deepcopy
from time import monotonic

import pytest

from ai import get_advanced_move, get_move, get_rudimentary_move
from game_engine import (
    BLUE, RED, GameState, IllegalMoveError, InvalidGameStateError, TurnContext, create_game,
    legal_destinations, roll_dice, validate_game_state,
)


def _resolved(column=1, row=1):
    values = iter(((column - .5) / 6, (row - .5) / 6))
    return roll_dice(create_game(), lambda: next(values))


def _resolved_rows(rows, column=6, row=6):
    board = [[RED if cell == "R" else BLUE if cell == "B" else None for cell in line] for line in rows]
    counts = {color: sum(cell == color for line in board for cell in line) for color in (RED, BLUE)}
    state = GameState(board, {color: 12 - counts[color] for color in counts}, RED)
    validate_game_state(state)
    values = iter(((column - .5) / 6, (row - .5) / 6))
    return roll_dice(state, lambda: next(values))


@pytest.mark.parametrize("strategy", [get_rudimentary_move, get_advanced_move])
@pytest.mark.parametrize("roll", [(1, 1), (3, 4), (6, 6)])
def test_ai_is_legal_prompt_and_immutable(strategy, roll):
    state = _resolved(*roll)
    before = deepcopy(state)
    started = monotonic()
    move = strategy(state, RED)
    assert move in legal_destinations(state)
    assert state == before
    assert monotonic() - started < (1 if strategy is get_rudimentary_move else 5)


@pytest.mark.parametrize("strategy", [get_rudimentary_move, get_advanced_move])
def test_invalid_resolved_state_without_moves_is_rejected(strategy):
    state = _resolved()
    state.turn_context.legal_moves = []
    with pytest.raises(InvalidGameStateError, match="legal placement"):
        strategy(state, RED)


@pytest.mark.parametrize("strategy", [get_rudimentary_move, get_advanced_move])
@pytest.mark.parametrize(
    "state",
    [
        pytest.param(_resolved_rows(["RBRBRB", "BRBRBR", "RBRBRB", "BR....", "......", "......"]), id="dense"),
        pytest.param(_resolved_rows(["R.....", "......", "......", "......", "......", ".....B"]), id="sparse"),
        pytest.param(_resolved_rows([".BBB..", ".BRB..", ".RRR..", "..R...", "......", "......"], 2, 5), id="capture-heavy"),
        pytest.param(_resolved_rows(["RRRRRR", "RRRRR.", "......", "......", "......", ".....B"]), id="near-win"),
    ],
)
def test_required_safety_corpus_is_legal_and_immutable(strategy, state):
    before = deepcopy(state)
    move = strategy(state, RED)
    assert move in legal_destinations(state)
    assert state == before


def test_rudimentary_chooser_is_injectable_and_checked():
    state = _resolved()
    expected = state.turn_context.legal_moves[-1]
    assert get_rudimentary_move(state, RED, chooser=lambda moves: moves[-1]) == expected
    with pytest.raises(IllegalMoveError):
        get_rudimentary_move(state, RED, chooser=lambda _moves: (99, 99))


def test_advanced_completed_candidate_observes_all_36_rolls():
    state = _resolved()
    seen = []
    move = get_advanced_move(state, RED, outcome_observer=lambda *event: seen.append(event))
    candidate_events = [event for event in seen if event[0] == move]
    assert {(column, row) for _, column, row in candidate_events} == {
        (column, row) for column in range(1, 7) for row in range(1, 7)
    }


def test_advanced_deadline_keeps_legal_fallback():
    state = _resolved()
    ticks = iter([0.0, 10.0])
    move = get_advanced_move(state, RED, budget=0.1, clock=lambda: next(ticks))
    assert move in legal_destinations(state)


def test_dispatch_and_invalid_turn_requests():
    state = _resolved()
    assert get_move(state, RED, "rudimentary", chooser=lambda moves: moves[0]) in legal_destinations(state)
    with pytest.raises(ValueError):
        get_move(state, RED, "legendary")
    with pytest.raises(IllegalMoveError):
        get_move(state, BLUE)


def test_unresolved_request_fails_explicitly():
    state = create_game()
    assert state.turn_context == TurnContext()
    with pytest.raises(IllegalMoveError):
        get_move(state, RED)


@pytest.mark.parametrize("budget", [float("inf"), float("nan"), -1])
def test_advanced_rejects_invalid_budgets(budget):
    with pytest.raises(ValueError):
        get_advanced_move(_resolved(), RED, budget=budget)


def test_advanced_rejects_non_finite_clock():
    with pytest.raises(ValueError):
        get_advanced_move(_resolved(), RED, clock=lambda: float("nan"))
