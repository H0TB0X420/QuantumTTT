"""Tests for board state, move validation, and win detection."""

from quantum_ttt.board import Board, Player


def test_new_board_is_empty():
    """A fresh board has all cells empty."""
    board = Board()
    for i in range(9):
        assert board.is_cell_empty(i)


def test_new_board_starts_with_x():
    board = Board()
    assert board.current_player == Player.X


def test_place_mark_on_empty_cell():
    board = Board()
    assert board.place_mark(0, Player.X)
    assert board.cells[0] == Player.X


def test_place_mark_rejects_occupied_cell():
    board = Board()
    board.place_mark(0, Player.X)
    assert not board.place_mark(0, Player.O)
    assert board.cells[0] == Player.X


def test_toggle_player():
    board = Board()
    assert board.current_player == Player.X
    board.toggle_player()
    assert board.current_player == Player.O
    board.toggle_player()
    assert board.current_player == Player.X


def test_is_full():
    board = Board()
    assert not board.is_full()
    board.cells = [Player.X, Player.O, Player.X,
                   Player.X, Player.O, Player.O,
                   Player.O, Player.X, Player.X]
    assert board.is_full()


def test_check_winner_top_row():
    board = Board()
    for i in [0, 1, 2]:
        board.place_mark(i, Player.X)
    result = board.check_winner()
    assert result is not None
    winner, line = result
    assert winner == Player.X
    assert line == (0, 1, 2)


def test_check_winner_diagonal():
    board = Board()
    for i in [0, 4, 8]:
        board.place_mark(i, Player.O)
    result = board.check_winner()
    assert result is not None
    assert result[0] == Player.O


def test_check_winner_returns_none_on_empty_board():
    board = Board()
    assert board.check_winner() is None


def test_check_winner_column():
    board = Board()
    for i in [0, 3, 6]:
        board.place_mark(i, Player.X)
    result = board.check_winner()
    assert result is not None
    assert result[0] == Player.X
    assert result[1] == (0, 3, 6)


def test_is_draw():
    board = Board()
    board.cells = [Player.X, Player.O, Player.X,
                   Player.X, Player.O, Player.O,
                   Player.O, Player.X, Player.X]
    assert board.is_draw()


def test_is_draw_false_with_winner():
    board = Board()
    board.cells = [Player.X, Player.X, Player.X,
                   Player.O, Player.O, Player.X,
                   Player.O, Player.X, Player.O]
    assert not board.is_draw()


def test_reset():
    board = Board()
    board.place_mark(0, Player.X)
    board.toggle_player()
    board.reset()
    assert all(cell is None for cell in board.cells)
    assert board.current_player == Player.X
