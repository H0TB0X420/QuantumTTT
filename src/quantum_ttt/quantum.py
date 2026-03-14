"""Quantum moves, cell state, and player enum for Quantum Tic-Tac-Toe."""

from dataclasses import dataclass, field
from enum import Enum


class Player(Enum):
    X = "X"
    O = "O"


@dataclass(frozen=True)
class QuantumMove:
    """A single quantum move: one mark superposed across two cells.

    Frozen so it's hashable and immutable — once placed, a move never changes.
    """
    player: Player
    move_number: int
    cell_a: int
    cell_b: int

    def __post_init__(self) -> None:
        assert 0 <= self.cell_a < 9, f"cell_a out of range: {self.cell_a}"
        assert 0 <= self.cell_b < 9, f"cell_b out of range: {self.cell_b}"
        assert self.cell_a != self.cell_b, "Quantum move must span two different cells"
        assert isinstance(self.player, Player), f"Invalid player: {self.player}"
        assert self.move_number >= 1, f"Move number must be positive: {self.move_number}"


@dataclass
class Cell:
    """A single board cell that can be empty, hold spooky marks, or be collapsed.

    States:
    - Empty: no spooky marks and not collapsed.
    - Quantum: has spooky marks but not yet collapsed.
    - Collapsed: has a definite classical mark.
    """
    spooky_marks: list[QuantumMove] = field(default_factory=list)
    collapsed: Player | None = None

    @property
    def is_empty(self) -> bool:
        """True when the cell has no spooky marks and is not collapsed."""
        return len(self.spooky_marks) == 0 and self.collapsed is None

    @property
    def is_collapsed(self) -> bool:
        return self.collapsed is not None

    @property
    def is_quantum(self) -> bool:
        """True when the cell has spooky marks but hasn't collapsed."""
        return len(self.spooky_marks) > 0 and self.collapsed is None
