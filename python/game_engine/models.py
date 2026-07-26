from dataclasses import dataclass, field

BOARD_SIZE = 6
RED = "RED"
BLUE = "BLUE"
PLAYERS = (RED, BLUE)
STARTING_RESERVE = 6
CHECKERS_PER_PLAYER = 12

Coordinate = tuple[int, int]
Cell = str | None
Board = list[list[Cell]]


@dataclass(slots=True)
class DiceRoll:
    column: int
    row: int


@dataclass(slots=True)
class TurnContext:
    dice: DiceRoll | None = None
    target: Coordinate | None = None
    legal_moves: list[Coordinate] = field(default_factory=list)


@dataclass(slots=True)
class GameState:
    board: Board
    reserves: dict[str, int]
    current_player: str
    turn: int = 1
    turn_context: TurnContext = field(default_factory=TurnContext)

