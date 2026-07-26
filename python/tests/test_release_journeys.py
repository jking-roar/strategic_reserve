"""Controller-level release lifecycle coverage for every desktop mode."""

from concurrent.futures import Future

import pytest

from game_engine import BLUE, RED, GameState, apply_placement, create_game, roll_dice, validate_game_state
from ui.main import GameController


class _Root:
    def __init__(self):
        self.callbacks = []
        self.destroyed = False

    def after(self, _delay, callback):
        self.callbacks.append(callback)

    def destroy(self):
        self.destroyed = True


class _Board:
    hovered = None

    def render(self, _state, enabled=True):
        self.enabled = enabled


class _Controls:
    def __init__(self):
        self.messages = []

    def render(self, _state, message="", *_args, **_kwargs):
        self.messages.append(message)

    def announce(self, message):
        self.messages.append(message)


class _Executor:
    def submit(self, function, *args):
        future = Future()
        try:
            future.set_result(function(*args))
        except Exception as exc:  # the Future owns worker failures, like an executor
            future.set_exception(exc)
        return future

    def shutdown(self, **_kwargs):
        pass


def _controller(state: GameState, mode="pvp", difficulty="rudimentary") -> GameController:
    controller = object.__new__(GameController)
    controller.root = _Root()
    controller.rng = lambda: 0.0
    controller.animation_steps = 0
    controller.animation_ms = 0
    controller.state = state
    controller.generation = 1
    controller.animating = False
    controller.mode = mode
    controller.difficulty = difficulty
    controller.ai_busy = False
    controller._executor = _Executor()
    controller._ai_future = None
    controller.container = object()
    controller.board = _Board()
    controller.controls = _Controls()
    controller.game_over = object()  # keep refresh headless
    controller.quit_dialog = None
    controller._status_message = ""
    return controller


def _near_red_win() -> GameState:
    rows = ["RRRRRR", "RRRRR.", "B.....", "......", "......", "......"]
    board = [[RED if cell == "R" else BLUE if cell == "B" else None for cell in row] for row in rows]
    state = GameState(board, {RED: 1, BLUE: 11}, RED)
    validate_game_state(state)
    return state


def test_pvp_controller_roll_capture_place_win_and_quit() -> None:
    controller = _controller(_near_red_win())
    # A controller-owned deterministic roll and placement reaches a real terminal state.
    controller.rng = iter(((6 - .5) / 6, (1 - .5) / 6)).__next__
    controller.roll()
    assert controller.state.turn_context.target == (5, 5)
    controller.activate_square((5, 5))
    assert controller.state.winner == RED
    assert "Red wins" in controller.controls.messages[-1]
    controller.request_quit()
    assert controller.root.destroyed


@pytest.mark.parametrize("difficulty", ["rudimentary", "advanced"])
def test_blue_computer_controller_lifecycle_and_budget_contract(difficulty) -> None:
    red_roll = roll_dice(create_game(), lambda: 0.0)
    blue_turn = apply_placement(red_roll, red_roll.turn_context.legal_moves[0])
    controller = _controller(blue_turn, "pvc", difficulty)
    controller._start_ai_turn()
    assert controller.ai_busy and controller.state.current_player == BLUE
    assert "Purple column" in controller.controls.messages[-1]
    controller.root.callbacks.pop()()
    assert not controller.ai_busy
    assert controller.state.current_player == RED
    assert "Blue placed" in controller.controls.messages[-1]


def test_restart_and_quit_invalidate_stale_computer_work() -> None:
    controller = _controller(create_game(), "pvc", "advanced")
    snapshot = controller.state
    stale = Future()
    stale.set_result((0, 0))
    controller.ai_busy = True
    controller.generation += 1  # same invalidation used by replacement/restart
    controller._poll_ai(stale, controller.generation - 1, snapshot)
    assert controller.state is snapshot
    controller._confirm_quit()
    assert controller.root.destroyed and not controller.animating


def test_ai_recovery_announces_authoritative_fallback_transition() -> None:
    red_roll = roll_dice(create_game(), lambda: 0.0)
    blue_turn = apply_placement(red_roll, red_roll.turn_context.legal_moves[0])
    controller = _controller(roll_dice(blue_turn, lambda: 0.0), "pvc", "advanced")
    controller.ai_busy = True
    controller._recover_ai_turn(RuntimeError("failed"))
    message = controller.controls.messages[-1]
    assert "safe fallback" in message and "Blue placed" in message and "Reserves:" in message
