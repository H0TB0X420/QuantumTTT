"""Tests for quantum data model: QuantumMove, Cell, and Board quantum operations."""

import pytest

from quantum_ttt.board import Board
from quantum_ttt.quantum import Cell, Player, QuantumMove


# --- QuantumMove ---

def test_quantum_move_stores_fields():
    """QuantumMove records player, move number, and both cells."""
    move = QuantumMove(player=Player.X, move_number=1, cell_a=0, cell_b=1)
    assert move.player == Player.X
    assert move.move_number == 1
    assert move.cell_a == 0
    assert move.cell_b == 1


def test_quantum_move_is_frozen():
    """Frozen dataclass — fields cannot be reassigned after creation."""
    move = QuantumMove(player=Player.X, move_number=1, cell_a=0, cell_b=1)
    with pytest.raises(AttributeError):
        move.player = Player.O  # type: ignore[misc]


def test_quantum_move_is_hashable():
    """Frozen dataclass is hashable — can be used in sets and as dict keys."""
    move = QuantumMove(player=Player.X, move_number=1, cell_a=0, cell_b=1)
    assert hash(move) is not None
    assert move in {move}


def test_quantum_move_rejects_same_cell():
    """A quantum move must span two different cells."""
    with pytest.raises(AssertionError, match="two different cells"):
        QuantumMove(player=Player.X, move_number=1, cell_a=3, cell_b=3)


def test_quantum_move_rejects_out_of_range():
    """Cell indices must be 0-8."""
    with pytest.raises(AssertionError):
        QuantumMove(player=Player.X, move_number=1, cell_a=0, cell_b=9)


# --- Cell ---

def test_cell_starts_empty():
    """A fresh cell has no spooky marks and is not collapsed."""
    cell = Cell()
    assert cell.is_empty
    assert not cell.is_collapsed
    assert not cell.is_quantum


def test_cell_becomes_quantum_with_spooky_mark():
    """Adding a spooky mark transitions the cell from empty to quantum."""
    cell = Cell()
    move = QuantumMove(player=Player.X, move_number=1, cell_a=0, cell_b=1)
    cell.spooky_marks.append(move)
    assert cell.is_quantum
    assert not cell.is_empty
    assert not cell.is_collapsed


def test_cell_collapsed_state():
    """A collapsed cell is not empty and not quantum."""
    cell = Cell(collapsed=Player.X)
    assert cell.is_collapsed
    assert not cell.is_empty
    assert not cell.is_quantum


# --- Board quantum operations ---

def test_place_quantum_move_adds_to_both_cells():
    """A quantum move appears in both target cells' spooky marks."""
    board = Board()
    move = board.place_quantum_move(0, 8, Player.X)
    assert move in board.cells[0].spooky_marks
    assert move in board.cells[8].spooky_marks


def test_place_quantum_move_increments_counter():
    """Each quantum move gets a unique, incrementing move number."""
    board = Board()
    move1 = board.place_quantum_move(0, 1, Player.X)
    move2 = board.place_quantum_move(2, 3, Player.O)
    assert move1.move_number == 1
    assert move2.move_number == 2


def test_place_quantum_move_rejects_collapsed_cell():
    """Cannot place a quantum move in a cell that has already collapsed."""
    board = Board()
    board.place_mark(0, Player.X)
    with pytest.raises(AssertionError, match="already collapsed"):
        board.place_quantum_move(0, 1, Player.O)


def test_move_counter_resets():
    """Move counter returns to zero on board reset."""
    board = Board()
    board.place_quantum_move(0, 1, Player.X)
    board.reset()
    assert board.move_counter == 0
