"""Board state, move validation, and win detection for Tic-Tac-Toe."""

from quantum_ttt.quantum import Cell, Player, QuantumMove


# All eight winning lines: rows, columns, diagonals.
WIN_LINES: list[tuple[int, int, int]] = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


class Board:
    """9-cell Tic-Tac-Toe board with move validation and win detection."""

    def __init__(self) -> None:
        self.cells: list[Cell] = [Cell() for _ in range(9)]
        self.current_player: Player = Player.X
        self.move_counter: int = 0

    def toggle_player(self) -> None:
        if self.current_player == Player.X:
            self.current_player = Player.O
        else:
            assert self.current_player == Player.O
            self.current_player = Player.X

    def is_cell_empty(self, index: int) -> bool:
        """True when the cell has no marks at all — no spooky marks, not collapsed."""
        assert 0 <= index < 9, f"Cell index out of range: {index}"
        return self.cells[index].is_empty

    def place_mark(self, index: int, player: Player) -> bool:
        """Place a classical mark at the given cell. Returns False if not empty."""
        assert 0 <= index < 9, f"Cell index out of range: {index}"
        assert isinstance(player, Player), f"Invalid player: {player}"

        if self.cells[index].is_collapsed:
            return False

        self.cells[index].collapsed = player
        assert self.cells[index].collapsed == player
        return True

    def place_quantum_move(self, cell_a: int, cell_b: int, player: Player) -> QuantumMove:
        """Place a quantum move spanning two cells. Returns the created move."""
        assert 0 <= cell_a < 9, f"cell_a out of range: {cell_a}"
        assert 0 <= cell_b < 9, f"cell_b out of range: {cell_b}"
        assert cell_a != cell_b, "Quantum move must span two different cells"
        assert not self.cells[cell_a].is_collapsed, f"Cell {cell_a} is already collapsed"
        assert not self.cells[cell_b].is_collapsed, f"Cell {cell_b} is already collapsed"

        self.move_counter += 1
        move = QuantumMove(
            player=player,
            move_number=self.move_counter,
            cell_a=cell_a,
            cell_b=cell_b,
        )

        self.cells[cell_a].spooky_marks.append(move)
        self.cells[cell_b].spooky_marks.append(move)

        assert move in self.cells[cell_a].spooky_marks
        assert move in self.cells[cell_b].spooky_marks
        return move

    def is_full(self) -> bool:
        """Board is full when all cells have collapsed to classical marks."""
        return all(cell.is_collapsed for cell in self.cells)

    def check_winner(self) -> tuple[Player, tuple[int, int, int]] | None:
        """Return (winner, winning_line) or None. Only checks collapsed cells."""
        for line in WIN_LINES:
            a, b, c = line
            collapsed_a = self.cells[a].collapsed
            if collapsed_a is not None and collapsed_a == self.cells[b].collapsed == self.cells[c].collapsed:
                return collapsed_a, line
        return None

    def is_draw(self) -> bool:
        return self.is_full() and self.check_winner() is None

    def reset(self) -> None:
        self.cells = [Cell() for _ in range(9)]
        self.current_player = Player.X
        self.move_counter = 0
