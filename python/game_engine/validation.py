from .errors import InvalidGameStateError
from .models import BLUE, BOARD_SIZE, CHECKERS_PER_PLAYER, PLAYERS, RED, GameState, TurnContext


def _fail(message: str) -> None:
    raise InvalidGameStateError(message)


def validate_coordinate(coordinate: tuple[int, int]) -> None:
    if (
        not isinstance(coordinate, tuple)
        or len(coordinate) != 2
        or not all(type(value) is int for value in coordinate)
    ):
        _fail("Coordinates must be (row, col) integer tuples.")

    row, col = coordinate
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        _fail("Coordinate out of board bounds.")


def validate_game_state(state: GameState) -> None:
    if not isinstance(state, GameState):
        _fail("State must be a GameState instance.")

    if len(state.board) != BOARD_SIZE:
        _fail("Board must have exactly 6 rows.")

    for row in state.board:
        if len(row) != BOARD_SIZE:
            _fail("Board rows must have exactly 6 columns.")
        for cell in row:
            if cell not in (None, RED, BLUE):
                _fail("Board contains an invalid token.")

    if set(state.reserves.keys()) != set(PLAYERS):
        _fail("Reserves must contain RED and BLUE keys.")

    for player in PLAYERS:
        value = state.reserves[player]
        if type(value) is not int or value < 0 or value > CHECKERS_PER_PLAYER:
            _fail("Reserve counts must be integers between 0 and 12.")

    board_counts = {
        RED: sum(cell == RED for row in state.board for cell in row),
        BLUE: sum(cell == BLUE for row in state.board for cell in row),
    }
    for player in PLAYERS:
        if board_counts[player] + state.reserves[player] != CHECKERS_PER_PLAYER:
            _fail("Board and reserve totals must conserve each player's 12 checkers.")

    empty_reserves = [player for player in PLAYERS if state.reserves[player] == 0]
    if len(empty_reserves) > 1:
        _fail("Both players cannot have empty reserves.")
    if empty_reserves and state.winner != empty_reserves[0]:
        _fail("A player with no reserve checkers must be the winner.")
    if not empty_reserves and state.winner is not None:
        _fail("Winner must have no reserve checkers.")

    if state.current_player not in PLAYERS:
        _fail("Current player must be RED or BLUE.")

    if state.winner is not None:
        if state.winner not in PLAYERS:
            _fail("Winner must be RED, BLUE, or None.")
        if state.current_player != state.winner:
            _fail("Current player must remain the winner after game completion.")
        if state.turn_context != TurnContext():
            _fail("Completed games cannot retain a turn context.")

    if not isinstance(state.turn, int) or state.turn < 1:
        _fail("Turn counter must be a positive integer.")

    if not isinstance(state.turn_context, TurnContext):
        _fail("Turn context must be a TurnContext instance.")

    if state.turn_context.dice is not None:
        dice = state.turn_context.dice
        if not hasattr(dice, "column") or not hasattr(dice, "row"):
            _fail("Turn-context dice must expose column and row values.")

        if type(dice.column) is not int or type(dice.row) is not int:
            _fail("Dice values must be integers between 1 and 6.")

        if dice.column not in range(1, BOARD_SIZE + 1):
            _fail("Dice column value must be between 1 and 6.")
        if dice.row not in range(1, BOARD_SIZE + 1):
            _fail("Dice row value must be between 1 and 6.")

    if state.turn_context.dice is None and state.turn_context.target is not None:
        _fail("Turn target requires dice values.")

    if state.turn_context.dice is not None and state.turn_context.target is None:
        _fail("Resolved dice require a turn target.")

    if state.turn_context.dice is None and state.turn_context.legal_moves:
        _fail("Legal moves require a resolved roll.")

    if state.turn_context.target is not None:
        validate_coordinate(state.turn_context.target)
        dice = state.turn_context.dice
        assert dice is not None
        expected_target = (
            (BOARD_SIZE - dice.row, dice.column - 1)
            if state.current_player == RED
            else (dice.row - 1, BOARD_SIZE - dice.column)
        )
        if state.turn_context.target != expected_target:
            _fail("Turn target must match the dice and current-player perspective.")

    if type(state.turn_context.legal_moves) is not list:
        _fail("Turn legal moves must be a list of coordinates.")

    seen: set[tuple[int, int]] = set()
    for move in state.turn_context.legal_moves:
        validate_coordinate(move)
        if move in seen:
            _fail("Turn legal moves must not contain duplicates.")
        seen.add(move)
        row, col = move
        if state.board[row][col] is not None:
            _fail("Turn legal moves must identify empty squares.")

    if state.winner is None and state.turn_context.dice is not None and not seen:
        _fail("A resolved active turn must contain a legal placement.")
