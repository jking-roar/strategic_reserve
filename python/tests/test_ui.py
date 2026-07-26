"""Display-independent checks for the Tk client boundary."""

from concurrent.futures import Future

from ui.board_view import BEIGE, LEGAL_DARK, LEGAL_LIGHT, PIECE, TARGET
from game_engine import BLUE, DiceRoll, RED, TurnContext, apply_placement, create_game, roll_dice
from ui.main import GameController


def test_palette_and_controller_import_without_a_display() -> None:
    assert BEIGE == "#F5F5DC"
    assert LEGAL_LIGHT == "#90EE90"
    assert LEGAL_DARK == "#006400"
    assert TARGET == "#FFD700"
    assert set(PIECE) == {"RED", "BLUE"}
    assert callable(GameController.activate_square)


def test_stale_animation_callback_is_harmless() -> None:
    controller = object.__new__(GameController)
    controller.generation = 4
    controller.animating = True
    controller._animation_tick(3, 1)
    assert controller.animating is True


class _Root:
    def __init__(self):
        self.destroyed = False
        self.after_calls = []

    def after(self, _ms, callback):
        self.after_calls.append(callback)

    def destroy(self):
        self.destroyed = True


class _Board:
    def __init__(self):
        self.renders = []

    def render(self, state, enabled=True):
        self.renders.append((state, enabled))


class _Value:
    def set(self, value):
        self.value = value


class _Controls:
    def __init__(self):
        self.renders = []
        self.dice = _Value()

    def render(self, state, message="", animating=False, input_locked=False):
        self.renders.append((state, message, animating, input_locked))


def _controller(state=None):
    controller = object.__new__(GameController)
    controller.root = _Root()
    controller.rng = lambda: 0.0
    controller.animation_steps = 0
    controller.animation_ms = 1
    controller.state = state or create_game()
    controller.generation = 2
    controller.animating = False
    controller.container = object()
    controller.board = _Board()
    controller.controls = _Controls()
    controller.game_over = None
    controller.quit_dialog = None
    return controller


def test_controller_roll_placement_and_illegal_activation_preserve_authority() -> None:
    controller = _controller()
    controller.roll()
    assert controller.state.turn_context.dice == DiceRoll(1, 1)
    assert not controller.animating
    original = controller.state
    controller.activate_square((1, 1))
    assert controller.state is original
    assert "Illegal or stale" in controller.controls.renders[-1][1]
    destination = controller.state.turn_context.legal_moves[0]
    controller.activate_square(destination)
    assert controller.state is not original
    assert controller.state.current_player == BLUE


def test_controller_pass_and_roll_guards() -> None:
    state = create_game()
    state.turn_context = TurnContext(dice=DiceRoll(1, 1), target=(5, 0), legal_moves=[])
    controller = _controller(state)
    controller.roll()
    assert controller.state is state and not controller.animating
    controller.pass_action()
    assert controller.state.current_player == BLUE

    controller.state.winner = BLUE
    controller.state.reserves[BLUE] = 0
    controller.roll()
    assert not controller.animating


def test_quit_no_escape_semantics_and_yes_invalidate_session() -> None:
    controller = _controller()
    class Dialog:
        def grab_release(self):
            pass

        def destroy(self):
            pass

    sentinel = Dialog()
    controller.quit_dialog = sentinel
    controller.animating = True
    state = controller.state
    generation = controller.generation

    # A small fake supplies the Toplevel methods used by cancel_quit.
    controller.cancel_quit()
    assert controller.state is state
    assert controller.animating is True
    assert controller.generation == generation

    controller._confirm_quit()
    assert controller.root.destroyed
    assert controller.generation == generation + 1
    assert not controller.animating


def test_refresh_creates_only_one_winner_overlay(monkeypatch) -> None:
    created = []

    class Overlay:
        def __init__(self, *args):
            created.append(args)

        def place(self, **_kwargs):
            pass

    monkeypatch.setattr("ui.main.GameOverView", Overlay)
    state = create_game()
    # Construct a validation-independent presentation state.
    state.winner = RED
    controller = _controller(state)
    controller.refresh()
    controller.refresh()
    assert len(created) == 1


class _ImmediateExecutor:
    def submit(self, function, *args):
        future = Future()
        future.set_result(function(*args))
        return future


class _FailingExecutor:
    def submit(self, *_args):
        raise RuntimeError("worker unavailable")


def test_pvc_blue_rolls_and_completes_turn_without_human_race() -> None:
    red_roll = roll_dice(create_game(), lambda: 0.0)
    blue_turn = apply_placement(red_roll, red_roll.turn_context.legal_moves[0])
    controller = _controller(blue_turn)
    controller.mode = "pvc"
    controller.difficulty = "rudimentary"
    controller.ai_busy = False
    controller._executor = _ImmediateExecutor()

    controller._start_ai_turn()
    assert controller.ai_busy and controller._human_locked()
    assert controller.state.current_player == BLUE
    controller.root.after_calls.pop()()
    assert not controller.ai_busy
    assert controller.state.current_player == RED


def test_stale_ai_result_cannot_mutate_replaced_session() -> None:
    controller = _controller()
    controller.ai_busy = True
    snapshot = controller.state
    future = Future()
    future.set_result((0, 0))
    controller._poll_ai(future, controller.generation - 1, snapshot)
    assert controller.state is snapshot
    assert controller.ai_busy


def test_submission_and_arbitrary_worker_failures_unlock_controller() -> None:
    red_roll = roll_dice(create_game(), lambda: 0.0)
    blue_turn = apply_placement(red_roll, red_roll.turn_context.legal_moves[0])
    controller = _controller(blue_turn)
    controller.mode = "pvc"
    controller.difficulty = "advanced"
    controller.ai_busy = False
    controller._executor = _FailingExecutor()
    controller._start_ai_turn()
    assert not controller.ai_busy
    assert controller.state.current_player == RED
    assert "safe fallback" in controller.controls.renders[-1][1]

    controller.state = roll_dice(blue_turn, lambda: 0.0)
    future = Future()
    future.set_exception(RuntimeError("strategy exploded"))
    controller.ai_busy = True
    snapshot = controller.state
    controller._poll_ai(future, controller.generation, snapshot)
    assert not controller.ai_busy
    assert controller.state.current_player == RED
    assert "strategy exploded" in controller.controls.renders[-1][1]
