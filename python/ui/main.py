"""Single-window desktop controller."""

from __future__ import annotations

import random
import tkinter as tk
from concurrent.futures import Future, ThreadPoolExecutor

from ai import get_move
from game_engine import BLUE, GameState, StrategicReserveError, apply_placement, create_game, pass_turn, roll_dice

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
        self.mode = "pvp"
        self.difficulty = "rudimentary"
        self.ai_busy = False
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="strategic-reserve-ai")
        self._ai_future: Future | None = None
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
        self._reset_executor()
        self.animating = False
        self.ai_busy = False
        self.game_over = None
        if self.quit_dialog is not None:
            self.quit_dialog.destroy()
            self.quit_dialog = None
        if self.container is not None:
            self.container.destroy()
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        return self.container

    def _reset_executor(self) -> None:
        future = getattr(self, "_ai_future", None)
        if future is not None:
            future.cancel()
        executor = getattr(self, "_executor", None)
        if executor is not None:
            executor.shutdown(wait=False, cancel_futures=True)
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="strategic-reserve-ai")
        self._ai_future = None

    def show_menu(self) -> None:
        self.state = None
        frame = self._replace()
        MenuView(frame, self.new_game, self.request_quit).pack(expand=True)

    def new_game(self, mode: str = "pvp", difficulty: str = "rudimentary") -> None:
        self.mode = mode
        self.difficulty = difficulty
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
        locked = self._human_locked()
        self.board.render(self.state, enabled=not locked and not self.animating and self.state.winner is None)
        self.controls.render(self.state, message, self.animating or locked)
        if self.state.winner is not None and self.game_over is None:
            self.game_over = GameOverView(
                self.container, self.state.winner, self.show_menu, self.request_quit
            )
            self.game_over.place(relx=.5, rely=.5, anchor="center")

    def roll(self) -> None:
        if (self.state is None or self.animating or self._human_locked() or self.state.winner is not None
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
        if self.state is None or self.animating or self._human_locked() or self.state.winner is not None:
            return
        try:
            self.state = apply_placement(self.state, destination)
            self.refresh()
            self._start_ai_turn()
        except StrategicReserveError as exc:
            self.refresh(f"Illegal or stale square: {exc}")

    def pass_action(self) -> None:
        if self.state is None or self.animating or self._human_locked():
            return
        try:
            self.state = pass_turn(self.state)
            self.refresh()
            self._start_ai_turn()
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
        future = getattr(self, "_ai_future", None)
        if future is not None:
            future.cancel()
        executor = getattr(self, "_executor", None)
        if executor is not None:
            executor.shutdown(wait=False, cancel_futures=True)
        self.root.destroy()

    def _human_locked(self) -> bool:
        return bool(getattr(self, "ai_busy", False) or (
            getattr(self, "mode", "pvp") == "pvc"
            and self.state is not None and self.state.current_player == BLUE
        ))

    def _start_ai_turn(self) -> None:
        """Resolve Blue's roll on Tk, then compute only move selection off-thread."""
        if (getattr(self, "mode", "pvp") != "pvc" or self.state is None
                or self.state.winner is not None or self.state.current_player != BLUE
                or getattr(self, "ai_busy", False)):
            return
        self.ai_busy = True
        token = self.generation
        try:
            self.state = roll_dice(self.state, self.rng)
        except StrategicReserveError as exc:
            self.ai_busy = False
            self.refresh(str(exc))
            return
        self.refresh("Blue is thinking…")
        if not self.state.turn_context.legal_moves:
            self.state = pass_turn(self.state)
            self.ai_busy = False
            self.refresh()
            return
        snapshot = self.state
        try:
            future = self._executor.submit(get_move, snapshot, BLUE, self.difficulty)
        except Exception as exc:
            self._recover_ai_turn(exc)
            return
        self._ai_future = future
        self.root.after(10, lambda: self._poll_ai(future, token, snapshot))

    def _poll_ai(self, future: Future, token: int, snapshot: GameState) -> None:
        if token != self.generation:
            return
        if not future.done():
            self.root.after(10, lambda: self._poll_ai(future, token, snapshot))
            return
        if self.state is not snapshot or not self.ai_busy:
            return
        try:
            move = future.result()
            if move is None and self.state.turn_context.legal_moves:
                raise ValueError("computer returned no move while legal moves exist")
            self.state = pass_turn(self.state) if move is None else apply_placement(self.state, move)
            message = ""
        except Exception as exc:
            self._ai_future = None
            self._recover_ai_turn(exc)
            return
        self._ai_future = None
        self.ai_busy = False
        self.refresh(message)

    def _recover_ai_turn(self, error: Exception) -> None:
        """Finish a failed computer turn with a validated deterministic fallback."""
        assert self.state is not None
        try:
            legal = self.state.turn_context.legal_moves
            self.state = apply_placement(self.state, legal[0]) if legal else pass_turn(self.state)
            message = f"Computer strategy failed; a safe fallback was used: {error}"
        except StrategicReserveError as recovery_error:
            # A corrupt engine state is not safely recoverable; return to configuration
            # rather than leave an input-locked Blue turn on screen.
            self.ai_busy = False
            self.show_menu()
            return
        self.ai_busy = False
        self.refresh(message)


def run() -> None:
    root = tk.Tk()
    GameController(root)
    root.mainloop()
