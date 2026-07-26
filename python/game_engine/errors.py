class StrategicReserveError(Exception):
    """Base domain error for the Strategic Reserve engine."""


class InvalidGameStateError(StrategicReserveError):
    """Raised when a game state breaks engine invariants."""


class IllegalMoveError(StrategicReserveError):
    """Raised when a move request is illegal for the current state."""

