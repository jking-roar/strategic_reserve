"""UI integration boundary and Tk desktop client for Strategic Reserve."""

from ai import get_move
from game_engine import GameState
from .main import GameController, run

__all__ = ["GameState", "get_move", "GameController", "run"]
