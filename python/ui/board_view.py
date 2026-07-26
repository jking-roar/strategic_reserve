"""Tk canvas presentation for the authoritative engine board."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable

from game_engine import BLUE, BOARD_SIZE, RED, GameState

BEIGE = "#F5F5DC"
GRID = "#333333"
LEGAL_LIGHT = "#90EE90"
LEGAL_DARK = "#006400"
TARGET = "#FFD700"
TARGET_OUTLINE = "#B8860B"
FOCUS = "#FF6600"
PIECE = {RED: "#CC0000", BLUE: "#0000CC"}


class BoardView(tk.Canvas):
    """A keyboard-operable, fixed 6x6 view using absolute coordinates."""

    def __init__(self, parent: tk.Misc, on_activate: Callable[[tuple[int, int]], None], cell_size: int = 64):
        super().__init__(parent, width=cell_size * BOARD_SIZE, height=cell_size * BOARD_SIZE,
                         background=BEIGE, highlightthickness=2, takefocus=True)
        self.cell_size = cell_size
        self.on_activate = on_activate
        self.focused = (0, 0)
        self.enabled = True
        self.bind("<Button-1>", self._click)
        self.bind("<Key>", self._key)

    def render(self, state: GameState, enabled: bool = True) -> None:
        self.delete("all")
        self.enabled = enabled
        legal = set(state.turn_context.legal_moves)
        target = state.turn_context.target
        size = self.cell_size
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x0, y0, x1, y1 = col * size, row * size, (col + 1) * size, (row + 1) * size
                fill = LEGAL_LIGHT if (row, col) in legal else BEIGE
                width, outline = (3, LEGAL_DARK) if (row, col) in legal else (1, GRID)
                self.create_rectangle(x0, y0, x1, y1, fill=fill, outline=outline, width=width)
                owner = state.board[row][col]
                if owner:
                    self.create_oval(x0 + 11, y0 + 11, x1 - 11, y1 - 11,
                                     fill=BEIGE, outline=PIECE[owner], width=6)
                # Target is deliberately drawn last so it remains visible on a checker.
                if (row, col) == target:
                    inset = 7
                    self.create_rectangle(x0 + inset, y0 + inset, x1 - inset, y1 - inset,
                                          outline=TARGET_OUTLINE, fill="", width=4)
                    self.create_oval(x0 + 22, y0 + 22, x1 - 22, y1 - 22,
                                     fill=TARGET, outline=TARGET_OUTLINE, width=2)
        row, col = self.focused
        self.create_rectangle(col * size + 3, row * size + 3, (col + 1) * size - 3,
                              (row + 1) * size - 3, outline=FOCUS, width=2)

    def _click(self, event: tk.Event) -> None:
        col, row = int(event.x) // self.cell_size, int(event.y) // self.cell_size
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            self.focused = (row, col)
            self.focus_set()
            if self.enabled:
                self.on_activate(self.focused)

    def _key(self, event: tk.Event) -> str | None:
        if not self.enabled:
            return "break"
        row, col = self.focused
        moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        if event.keysym in moves:
            dr, dc = moves[event.keysym]
            self.focused = ((row + dr) % BOARD_SIZE, (col + dc) % BOARD_SIZE)
            self.event_generate("<<BoardFocusChanged>>")
            return "break"
        if event.keysym in ("Return", "space") and self.enabled:
            self.on_activate(self.focused)
            return "break"
        return None
