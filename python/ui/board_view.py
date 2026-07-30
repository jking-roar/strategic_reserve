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
TARGET_OUTLINE = "#765400"
FOCUS = "#C24100"  # 3.66:1 against the light legal highlight.
DISABLED = "#767676"
PIECE = {RED: "#CC0000", BLUE: "#0000CC"}
CELL_SIZE = 60
CELL_GAP = 2


def move_focus(coordinate: tuple[int, int], keysym: str) -> tuple[int, int]:
    """Return deterministic, wrapping board navigation without touching state."""
    row, col = coordinate
    delta = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
    if keysym not in delta:
        return coordinate
    dr, dc = delta[keysym]
    return ((row + dr) % BOARD_SIZE, (col + dc) % BOARD_SIZE)


def square_description(state: GameState, coordinate: tuple[int, int]) -> str:
    """Describe a square using non-color names suitable for visible/AT status."""
    row, col = coordinate
    owner = state.board[row][col]
    parts = [f"Square row {row + 1}, column {col + 1}", "empty" if owner is None else f"{owner.title()} checker"]
    if coordinate == state.turn_context.target:
        parts.append("dice target")
    if coordinate in state.turn_context.legal_moves:
        parts.append("legal placement")
    return "; ".join(parts) + "."


class BoardView(tk.Canvas):
    """A keyboard-operable, fixed 6x6 view using absolute coordinates."""

    def __init__(self, parent: tk.Misc, on_activate: Callable[[tuple[int, int]], None],
                 on_describe: Callable[[str], None] | None = None,
                 on_cancel: Callable[[], None] | None = None,
                 on_restore: Callable[[], None] | None = None, cell_size: int = CELL_SIZE):
        extent = cell_size * BOARD_SIZE + CELL_GAP * (BOARD_SIZE - 1)
        super().__init__(parent, width=extent, height=extent, background=BEIGE,
                         highlightthickness=0, takefocus=True, cursor="hand2")
        self.cell_size = cell_size
        self.on_activate = on_activate
        self.on_describe = on_describe or (lambda _text: None)
        self.on_cancel = on_cancel or (lambda: None)
        self.on_restore = on_restore or (lambda: None)
        self.focused = (0, 0)
        self.hovered: tuple[int, int] | None = None
        self.has_focus = False
        self.enabled = True
        self._state: GameState | None = None
        self._transition_frame: tuple[tuple[tuple[int, int, str], ...], tuple[int, int] | None, float] | None = None
        self.bind("<Button-1>", self._click)
        self.bind("<Motion>", self._motion)
        self.bind("<Leave>", self._leave)
        self.bind("<FocusIn>", self._focus_in)
        self.bind("<FocusOut>", self._focus_out)
        self.bind("<Key>", self._key)

    @property
    def pitch(self) -> int:
        return self.cell_size + CELL_GAP

    def render(self, state: GameState, enabled: bool = True) -> None:
        self.delete("all")
        self._state = state
        self.enabled = enabled
        legal = set(state.turn_context.legal_moves)
        target = state.turn_context.target
        size, pitch = self.cell_size, self.pitch
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x0, y0 = col * pitch, row * pitch
                x1, y1 = x0 + size, y0 + size
                fill = LEGAL_LIGHT if (row, col) in legal else BEIGE
                width, outline = (2, LEGAL_DARK) if (row, col) in legal else (1, GRID)
                self.create_rectangle(x0, y0, x1, y1, fill=fill, outline=outline, width=width)
                owner = state.board[row][col]
                if owner:
                    self.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10,
                                     fill=PIECE[owner], outline="#000000", width=2)
                if (row, col) == target:
                    self.create_rectangle(x0 + 6, y0 + 6, x1 - 6, y1 - 6,
                                          outline=TARGET_OUTLINE, width=3, dash=(6, 3))
                    self.create_oval(x0 + 20, y0 + 20, x1 - 20, y1 - 20,
                                     fill=TARGET, outline=TARGET_OUTLINE, width=2,
                                     tags=("target-marker",))
                    self.create_text(x0 + size / 2, y0 + size / 2, text="T",
                                     fill="#000000", font=("TkDefaultFont", 11, "bold"))
                if not enabled:
                    self.create_rectangle(x0 + 10, y0 + 10, x1 - 10, y1 - 10,
                                          outline=DISABLED, width=2, dash=(3, 3),
                                          tags=("disabled-cue",))
        cue = self.focused if self.has_focus else self.hovered
        if cue is not None:
            row, col = cue
            x0, y0 = col * pitch, row * pitch
            self.create_rectangle(x0 + 2, y0 + 2, x0 + size - 2, y0 + size - 2,
                                  outline=FOCUS, width=3, tags=("interaction-cue",))
        if self._transition_frame is not None:
            self._draw_transition(*self._transition_frame)


    def show_transition(self, removed: tuple[tuple[int, int, str], ...],
                        target: tuple[int, int] | None, progress: float) -> None:
        """Draw one transient animation frame over the authoritative board."""
        self._transition_frame = (removed, target, progress)
        self._draw_transition(removed, target, progress)

    def clear_transition(self) -> None:
        """Remove transient effects without disturbing the rendered game state."""
        self._transition_frame = None
        self.delete("transition-effect")

    def _draw_transition(self, removed: tuple[tuple[int, int, str], ...],
                         target: tuple[int, int] | None, progress: float) -> None:
        self.delete("transition-effect")
        progress = max(0.0, min(1.0, progress))
        size, pitch = self.cell_size, self.pitch
        if target is not None:
            row, col = target
            x0, y0 = col * pitch, row * pitch
            inset = 3 + int(9 * progress)
            width = max(1, 6 - int(4 * progress))
            self.create_rectangle(
                x0 + inset, y0 + inset, x0 + size - inset, y0 + size - inset,
                outline=TARGET_OUTLINE, width=width, dash=(5, 3),
                tags=("target-pulse", "transition-effect"),
            )
        shrink = int(size * (1 / 6 + progress / 4))
        stipple = "gray25" if progress < .5 else "gray75"
        for row, col, owner in removed:
            x0, y0 = col * pitch, row * pitch
            self.create_oval(
                x0 + shrink, y0 + shrink, x0 + size - shrink, y0 + size - shrink,
                fill=PIECE[owner], outline="#000000", width=1, stipple=stipple,
                tags=("removed-chip", "transition-effect"),
            )

    def _coordinate_at(self, x: int, y: int) -> tuple[int, int] | None:
        col, row = x // self.pitch, y // self.pitch
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return None
        if x % self.pitch >= self.cell_size or y % self.pitch >= self.cell_size:
            return None
        return row, col

    def _describe(self, coordinate: tuple[int, int] | None = None) -> None:
        if self._state is not None:
            self.on_describe(square_description(self._state, coordinate or self.focused))

    def _click(self, event: tk.Event) -> None:
        coordinate = self._coordinate_at(int(event.x), int(event.y))
        if coordinate is not None:
            self.focused = coordinate
            self.focus_set()
            self._describe()
            if self.enabled:
                self.on_activate(coordinate)

    def _motion(self, event: tk.Event) -> None:
        coordinate = self._coordinate_at(int(event.x), int(event.y))
        if coordinate != self.hovered:
            self.hovered = coordinate
            if self._state is not None:
                self.render(self._state, self.enabled)
            if coordinate is not None:
                self._describe(coordinate)
            else:
                self.on_restore()

    def _leave(self, _event: tk.Event) -> None:
        self.hovered = None
        if self._state is not None:
            self.render(self._state, self.enabled)
        self.on_restore()

    def _focus_in(self, _event: tk.Event) -> None:
        self.has_focus = True
        if self._state is not None:
            self.render(self._state, self.enabled)
        self._describe()

    def _focus_out(self, _event: tk.Event) -> None:
        self.has_focus = False
        if self._state is not None:
            self.render(self._state, self.enabled)

    def _key(self, event: tk.Event) -> str | None:
        if event.keysym in ("Up", "Down", "Left", "Right"):
            self.focused = move_focus(self.focused, event.keysym)
            if self._state is not None:
                self.render(self._state, self.enabled)
            self._describe()
            return "break"
        if event.keysym in ("Return", "space"):
            if self.enabled:
                self.on_activate(self.focused)
            return "break"
        if event.keysym == "Escape":
            self.on_cancel()
            return "break"
        return None
