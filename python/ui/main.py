"""Single-window desktop controller."""

from __future__ import annotations

import random
import tkinter as tk

from game_engine import GameState, StrategicReserveError, apply_placement, create_game, pass_turn, roll_dice

from .board_view import BoardView
from .controls import GameControls, GameOverView, MenuView


class QuitDialog(tk.Toplevel):
    """Explicit Yes/No confirmation whose Escape path is always No."""

    def __init__(self, parent: tk.Misc, on_yes, on_no):
        super().__init__(parent)
        self.title("Quit game?")
        self.resizable(False, False)
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", on_no)
        self.bind("<Escape>", lambda _event: on_no())
        tk.Label(self, text="Quit the unfinished game?", padx=24, pady=14).pack()
        buttons = tk.Frame(self, padx=12, pady=8)
        buttons.pack(fill="x")
        tk.Button(buttons, text="Yes", command=on_yes).pack(side="left", expand=True, fill="x")
        no = tk.Button(buttons, text="No", command=on_no)
        no.pack(side="right", expand=True, fill="x")
        no.focus_set()
        self.grab_set()


class GameController:
    """Owns a UI session while delegating all game decisions to game_engine."""

    def __init__(self, root: tk.Tk, rng=random.random, animation_steps: int = 8, animation_ms: int = 70):
        self.root = root
        self.rng = rng
        self.animation_steps = animation_steps
        self.animation_ms = animation_ms
        self.state: GameState | None = None
        self.generation = 0
        self.animating = False
        self.container: tk.Frame | None = None
        self.board: BoardView | None = None
        self.controls: GameControls | None = None
        self.game_over: GameOverView | None = None
        self.quit_dialog: QuitDialog | None = None
        self.root.title("Strategic Reserve")
        self.root.protocol("WM_DELETE_WINDOW", self.request_quit)
        self.show_menu()

    def _replace(self) -> tk.Frame:
        self.generation += 1
        self.animating = False
        self.game_over = None
        if self.quit_dialog is not None:
            self.quit_dialog.destroy()
            self.quit_dialog = None
        if self.container is not None:
            self.container.destroy()
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        return self.container

    def show_menu(self) -> None:
        self.state = None
        frame = self._replace()
        MenuView(frame, self.new_game, self.request_quit).pack(expand=True)

    def new_game(self) -> None:
        self.state = create_game()
        frame = self._replace()
        self.board = BoardView(frame, self.activate_square)
        self.board.pack(side="left", padx=12, pady=12)
        self.board.bind("<<BoardFocusChanged>>", lambda _event: self.refresh())
        self.controls = GameControls(frame, self.roll, self.pass_action, self.request_quit)
        self.controls.pack(side="right", fill="y", pady=12)
        self.refresh()

    def refresh(self, message: str = "") -> None:
        if self.state is None or self.board is None or self.controls is None:
            return
        self.board.render(self.state, enabled=not self.animating and self.state.winner is None)
        self.controls.render(self.state, message, self.animating)
        if self.state.winner is not None and self.game_over is None:
            self.game_over = GameOverView(
                self.container, self.state.winner, self.show_menu, self.request_quit
            )
            self.game_over.place(relx=.5, rely=.5, anchor="center")

    def roll(self) -> None:
        if (self.state is None or self.animating or self.state.winner is not None
                or self.state.turn_context.dice is not None):
            return
        self.animating = True
        token = self.generation
        self.refresh("Rolling…")
        self._animation_tick(token, self.animation_steps)

    def _animation_tick(self, token: int, remaining: int) -> None:
        if token != self.generation or not self.animating:
            return
        if remaining > 0:
            if self.controls:
                self.controls.dice.set(f"Purple column: {random.randint(1, 6)}   Green row: {random.randint(1, 6)}")
            self.root.after(self.animation_ms, lambda: self._animation_tick(token, remaining - 1))
            return
        try:
            assert self.state is not None
            self.state = roll_dice(self.state, self.rng)
            message = "Choose a green square." if self.state.turn_context.legal_moves else "No legal move; pass the turn."
        except StrategicReserveError as exc:
            message = str(exc)
        self.animating = False
        self.refresh(message)

    def activate_square(self, destination: tuple[int, int]) -> None:
        if self.state is None or self.animating or self.state.winner is not None:
            return
        try:
            self.state = apply_placement(self.state, destination)
            self.refresh()
        except StrategicReserveError as exc:
            self.refresh(f"Illegal or stale square: {exc}")

    def pass_action(self) -> None:
        if self.state is None or self.animating:
            return
        try:
            self.state = pass_turn(self.state)
            self.refresh()
        except StrategicReserveError as exc:
            self.refresh(str(exc))

    def request_quit(self) -> None:
        active = self.state is not None and self.state.winner is None
        if not active:
            self._confirm_quit()
        elif self.quit_dialog is None:
            self.quit_dialog = QuitDialog(self.root, self._confirm_quit, self.cancel_quit)

    def cancel_quit(self) -> None:
        """Dismiss confirmation without touching session state or animation."""
        if self.quit_dialog is not None:
            self.quit_dialog.grab_release()
            self.quit_dialog.destroy()
            self.quit_dialog = None

    def _confirm_quit(self) -> None:
        self.generation += 1
        self.animating = False
        self.root.destroy()


def run() -> None:
    root = tk.Tk()
    GameController(root)
    root.mainloop()
