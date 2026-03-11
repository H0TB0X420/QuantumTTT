"""Board state, move validation, and win detection for Tic-Tac-Toe."""

from enum import Enum


class Player(Enum):
    X = "X"
    O = "O"


# All eight winning lines: rows, columns, diagonals.
WIN_LINES: list[tuple[int, int, int]] = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


class Board:
    """9-cell Tic-Tac-Toe board with move validation and win detection."""

    def __init__(self) -> None:
        self.cells: list[Player | None] = [None] * 9
        self.current_player: Player = Player.X

    def toggle_player(self) -> None:
        if self.current_player == Player.X:
            self.current_player = Player.O
        else:
            assert self.current_player == Player.O
            self.current_player = Player.X

    def is_cell_empty(self, index: int) -> bool:
        assert 0 <= index < 9, f"Cell index out of range: {index}"
        return self.cells[index] is None

    def place_mark(self, index: int, player: Player) -> bool:
        """Place a mark at the given cell. Returns False if occupied."""
        assert 0 <= index < 9, f"Cell index out of range: {index}"
        assert isinstance(player, Player), f"Invalid player: {player}"

        if not self.is_cell_empty(index):
            return False

        self.cells[index] = player
        assert self.cells[index] == player
        return True

    def is_full(self) -> bool:
        return all(cell is not None for cell in self.cells)

    def check_winner(self) -> tuple[Player, tuple[int, int, int]] | None:
        """Return (winner, winning_line) or None."""
        for line in WIN_LINES:
            a, b, c = line
            if self.cells[a] is not None and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a], line
        return None

    def is_draw(self) -> bool:
        return self.is_full() and self.check_winner() is None

    def reset(self) -> None:
        self.cells = [None] * 9
        self.current_player = Player.X
