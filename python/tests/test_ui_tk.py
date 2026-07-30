"""Display-backed checks for native Tk focus and event bindings."""

import tkinter as tk

import pytest

from game_engine import RED, create_game, roll_dice
from ui.board_view import BoardView, TARGET
from ui.controls import GameControls
from ui.main import GameController, QuitDialog


@pytest.fixture()
def root():
    try:
        window = tk.Tk()
    except tk.TclError as exc:
        pytest.skip(f"Tk display unavailable: {exc}")
    # Keep the window mapped inside Xvfb/desktop: native key and focus events are
    # intentionally ignored by Tk for an unmapped toplevel.
    window.geometry("800x600+0+0")
    window.update()
    yield window
    window.destroy()


def test_native_focus_cue_bindings_and_traversal(root) -> None:
    frame = tk.Frame(root)
    frame.pack()
    activated = []
    messages = []
    board = BoardView(frame, activated.append, messages.append)
    board.pack()
    controls = GameControls(frame, lambda: None, lambda: None, lambda: None)
    controls.pack()
    board.render(create_game())
    root.update_idletasks()

    board.focus_force()
    root.update()
    assert board.has_focus
    assert board.find_withtag("interaction-cue")
    board.event_generate("<KeyPress-Right>")
    board.event_generate("<KeyPress-space>")
    root.update()
    board.event_generate("<KeyPress-Return>")
    board.event_generate("<KeyPress-Left>")
    board.event_generate("<KeyPress-Up>")
    root.update()
    assert activated == [(0, 1), (0, 1)]
    assert board.focused == (5, 0)
    assert str(board.tk_focusNext()) == str(controls.roll)
    assert str(controls.roll.tk_focusPrev()) == str(board)
    board.focus_force()
    board.event_generate("<KeyPress-Tab>")
    root.update()
    assert root.focus_get() == controls.roll
    controls.roll.event_generate("<Shift-KeyPress-Tab>")
    root.update()
    assert root.focus_get() == board


def test_escape_is_non_destructive(root) -> None:
    cancelled = []
    board = BoardView(root, lambda _coordinate: None, on_cancel=lambda: cancelled.append(True))
    board.pack()
    state = create_game()
    board.render(state)
    root.update()
    board.focus_force()
    root.update()
    board.event_generate("<KeyPress-Escape>")
    root.update()
    assert cancelled == [True]
    assert board._state is state


def test_hover_describes_square_and_leave_restores_status(root) -> None:
    messages, restored = [], []
    board = BoardView(root, lambda _coordinate: None, messages.append,
                      on_restore=lambda: restored.append(True))
    board.pack()
    board.render(create_game())
    root.update()
    board.event_generate("<Motion>", x=65, y=3)
    root.update()
    assert board.hovered == (0, 1)
    assert "row 1, column 2" in messages[-1]
    assert board.find_withtag("interaction-cue")
    board.event_generate("<Leave>")
    root.update()
    assert board.hovered is None and restored


def test_disabled_legal_target_overlap_retains_each_non_color_cue(root) -> None:
    state = roll_dice(create_game(), lambda: 0.0)
    board = BoardView(root, lambda _coordinate: None)
    board.pack()
    board.render(state, enabled=False)
    root.update()
    assert len(board.find_withtag("disabled-cue")) == 36
    marker = board.find_withtag("target-marker")
    assert marker and board.itemcget(marker[0], "fill") == TARGET
    activated = []
    board.on_activate = activated.append
    board.focus_force()
    board.event_generate("<KeyPress-space>")
    root.update()
    assert not activated


def test_transition_frame_pulses_target_and_ghosts_all_removed_chips(root) -> None:
    board = BoardView(root, lambda _coordinate: None)
    board.pack()
    board.render(create_game())

    board.show_transition(((0, 0, RED), (1, 1, RED)), (2, 3), .5)
    root.update()

    assert len(board.find_withtag("target-pulse")) == 1
    assert len(board.find_withtag("removed-chip")) == 2
    assert len(board.find_withtag("transition-effect")) == 3


def test_quit_dialog_escape_is_no_and_terminal_restart_focus(root) -> None:
    decisions = []
    dialog = QuitDialog(root, lambda: decisions.append("yes"), lambda: decisions.append("no"))
    root.update()
    dialog.event_generate("<Escape>")
    root.update()
    assert decisions == ["no"]
    dialog.destroy()

    controller = GameController(root, animation_steps=0)
    controller.new_game()
    assert controller.state is not None
    controller.state.winner = RED
    controller.state.reserves[RED] = 0
    controller.refresh()
    root.update()
    assert controller.game_over is not None
    assert root.focus_get() == controller.game_over.new_game
    controller.game_over.new_game.invoke()
    root.update()
    assert controller.state is None
    controller._reset_executor()
