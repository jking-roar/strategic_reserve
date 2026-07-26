from copy import deepcopy

from .errors import InvalidGameStateError
from .models import BLUE, RED, STARTING_RESERVE, Board, GameState, PLAYERS
from .validation import validate_game_state

_INITIAL_ROWS = [
    "......",
    ".RBRB.",
    ".B..R.",
    ".R..B.",
    ".BRBR.",
    "......",
]


def _board_from_rows(rows: list[str]) -> Board:
    return [
        [RED if token == "R" else BLUE if token == "B" else None for token in row]
        for row in rows
    ]


def create_game(starting_player: str = RED) -> GameState:
    if starting_player not in PLAYERS:
        raise InvalidGameStateError("Starting player must be RED or BLUE.")

    state = GameState(
        board=_board_from_rows(_INITIAL_ROWS),
        reserves={RED: STARTING_RESERVE, BLUE: STARTING_RESERVE},
        current_player=starting_player,
    )
    validate_game_state(state)
    return state


def clone_state(state: GameState) -> GameState:
    return deepcopy(state)

