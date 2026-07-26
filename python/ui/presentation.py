"""Pure text presentation for game-state transitions."""

from game_engine import BLUE, RED, GameState


def player_name(player: str) -> str:
    """Return the user-facing name for a player domain value."""
    if player == RED:
        return "Red"
    if player == BLUE:
        return "Blue"
    raise ValueError(f"Unknown player: {player!r}")


def transition_summary(before: GameState, after: GameState, event: str) -> str:
    """Describe an authoritative transition without owning any game state."""
    actor = player_name(before.current_player)
    captured = {
        color: max(0, after.reserves[color] - before.reserves[color])
        for color in before.reserves
    }
    details: list[str] = []
    if event == "roll":
        if not after.turn_context.dice or not after.turn_context.target:
            raise ValueError("A roll summary requires dice and a target")
        dice, (row, col) = after.turn_context.dice, after.turn_context.target
        details.append(
            f"{actor}'s turn. Purple column {dice.column}, Green row {dice.row}. "
            f"Target row {row + 1}, column {col + 1}."
        )
        details.append(f"{len(after.turn_context.legal_moves)} legal placements.")
        for color, count in captured.items():
            if count:
                details.append(f"Captured {count} {player_name(color)} checker{'s' if count != 1 else ''}; returned to reserve.")
        if any(captured.values()):
            details.append(f"Reserves: Red {after.reserves[RED]}, Blue {after.reserves[BLUE]}.")
    elif event == "placement":
        details.append(f"{actor} placed a checker.")
        for color, count in captured.items():
            if count:
                details.append(f"Captured {count} {player_name(color)} checker{'s' if count != 1 else ''}; returned to reserve.")
        details.append(f"Reserves: Red {after.reserves[RED]}, Blue {after.reserves[BLUE]}.")
        details.append(
            f"{player_name(after.winner)} wins!" if after.winner else f"{player_name(after.current_player)}'s turn."
        )
    else:
        raise ValueError(f"Unknown transition event: {event!r}")
    return " ".join(details)
