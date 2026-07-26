"""Reusable Tk controls for menu, play, and game-over screens."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable

from game_engine import BLUE, RED, GameState


class MenuView(tk.Frame):
    def __init__(self, parent: tk.Misc, on_new: Callable[..., None], on_quit: Callable[[], None]):
        super().__init__(parent, padx=24, pady=24)
        tk.Label(self, text="Strategic Reserve", font=("TkDefaultFont", 20, "bold")).pack(pady=10)
        tk.Label(self, text="Choose a game mode").pack()
        tk.Button(self, text="Local two-player", command=lambda: on_new("pvp")).pack(fill="x", pady=4)
        tk.Button(self, text="Computer — Rudimentary", command=lambda: on_new("pvc", "rudimentary")).pack(fill="x", pady=4)
        tk.Button(self, text="Computer — Advanced", command=lambda: on_new("pvc", "advanced")).pack(fill="x", pady=4)
        tk.Button(self, text="Quit", command=on_quit).pack(fill="x", pady=4)


class GameControls(tk.Frame):
    def __init__(self, parent: tk.Misc, on_roll: Callable[[], None], on_quit: Callable[[], None]):
        super().__init__(parent, padx=12)
        self.status = tk.StringVar(value="")
        self.announcement = tk.StringVar(value="")
        self.dice = tk.StringVar(value="Purple column: –   Green row: –")
        self.reserves = tk.StringVar(value="")
        self.status_label = tk.Label(self, textvariable=self.status, font=("TkDefaultFont", 12, "bold"),
                                     takefocus=False, name="game_status")
        self.status_label.pack()
        tk.Label(self, textvariable=self.dice).pack()
        tk.Label(self, textvariable=self.reserves).pack()
        self.roll = tk.Button(self, text="Roll Dice", command=on_roll)
        self.roll.pack(fill="x", pady=2)
        tk.Button(self, text="Quit", command=on_quit).pack(fill="x", pady=2)

    def announce(self, text: str) -> None:
        """Publish the same concise message visibly and through a stable Tk variable.

        Named status text is exposed by native Tk accessibility bridges;
        changing the variable also gives adapters a deterministic notification hook.
        """
        self.announcement.set(text)
        self.status.set(text)

    def render(self, state: GameState, message: str = "", animating: bool = False,
               input_locked: bool = False) -> None:
        color = "Red" if state.current_player == RED else "Blue"
        visible = message or (f"{color} wins!" if state.winner else f"{color}'s turn")
        if message:
            self.announce(visible)
        else:
            self.status.set(visible)
        dice = state.turn_context.dice
        if dice:
            self.dice.set(f"Purple column: {dice.column}   Green row: {dice.row}")
        elif not animating:
            self.dice.set("Purple column: –   Green row: –")
        self.reserves.set(f"Red reserve: {state.reserves[RED]}   Blue reserve: {state.reserves[BLUE]}")
        can_roll = not input_locked and not animating and state.winner is None and dice is None
        self.roll.configure(state=tk.NORMAL if can_roll else tk.DISABLED)


class GameOverView(tk.Frame):
    def __init__(self, parent: tk.Misc, winner: str, on_new: Callable[[], None], on_quit: Callable[[], None]):
        super().__init__(parent, padx=24, pady=24)
        name = "Red" if winner == RED else "Blue"
        tk.Label(self, text=f"{name} wins!", font=("TkDefaultFont", 20, "bold")).pack(pady=8)
        self.new_game = tk.Button(self, text="New Game", command=on_new)
        self.new_game.pack(fill="x", pady=4)
        self.quit = tk.Button(self, text="Quit", command=on_quit)
        self.quit.pack(fill="x", pady=4)
