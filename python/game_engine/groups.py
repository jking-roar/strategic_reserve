from .models import BLUE, BOARD_SIZE, Coordinate, PLAYERS, RED
from .errors import InvalidGameStateError
from .validation import validate_coordinate


def _validate_board(board: list[list[str | None]]) -> None:
    if type(board) is not list or len(board) != BOARD_SIZE:
        raise InvalidGameStateError("Board must be a 6x6 matrix.")

    if any(type(row) is not list or len(row) != BOARD_SIZE for row in board):
        raise InvalidGameStateError("Board must be a 6x6 matrix.")

    for row in board:
        for cell in row:
            if cell not in (None, RED, BLUE):
                raise InvalidGameStateError("Board contains an invalid token.")


def _inside(row: int, col: int) -> bool:
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def _neighbors(point: Coordinate) -> list[Coordinate]:
    row, col = point
    return [
        (r, c)
        for r, c in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
        if _inside(r, c)
    ]


def group_at(board: list[list[str | None]], start: Coordinate) -> list[Coordinate]:
    _validate_board(board)
    validate_coordinate(start)
    row, col = start
    color = board[row][col]
    if color not in (RED, BLUE):
        return []

    found: list[Coordinate] = []
    pending = [start]
    seen = {start}

    while pending:
        point = pending.pop()
        found.append(point)
        for neighbor in _neighbors(point):
            n_row, n_col = neighbor
            if board[n_row][n_col] == color and neighbor not in seen:
                seen.add(neighbor)
                pending.append(neighbor)

    return found


def groups_for_color(board: list[list[str | None]], color: str) -> list[list[Coordinate]]:
    _validate_board(board)
    if color not in PLAYERS:
        raise InvalidGameStateError("Color must be RED or BLUE.")

    result: list[list[Coordinate]] = []
    seen: set[Coordinate] = set()

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            point = (row, col)
            if board[row][col] == color and point not in seen:
                group = group_at(board, point)
                seen.update(group)
                result.append(group)

    return result

