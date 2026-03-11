"""Tests for keyboard input processing."""

import curses

from quantum_ttt.input_handler import Action, handle_input


# --- Arrow key movement ---

def test_move_right_from_center():
    """Right arrow from center (4) moves to cell 5."""
    action, pos = handle_input(curses.KEY_RIGHT, 4)
    assert action == Action.MOVE
    assert pos == 5


def test_move_left_wraps_at_row_start():
    """Left arrow at start of middle row (3) wraps to end of row (5)."""
    action, pos = handle_input(curses.KEY_LEFT, 3)
    assert action == Action.MOVE
    assert pos == 5


def test_move_right_wraps_at_row_end():
    """Right arrow at end of top row (2) wraps to start of row (0)."""
    action, pos = handle_input(curses.KEY_RIGHT, 2)
    assert action == Action.MOVE
    assert pos == 0


def test_move_up_wraps_at_top():
    """Up arrow at top row (1) wraps to bottom row (7)."""
    action, pos = handle_input(curses.KEY_UP, 1)
    assert action == Action.MOVE
    assert pos == 7


def test_move_down_wraps_at_bottom():
    """Down arrow at bottom row (7) wraps to top row (1)."""
    action, pos = handle_input(curses.KEY_DOWN, 7)
    assert action == Action.MOVE
    assert pos == 1


# --- Action keys ---

def test_enter_triggers_place():
    """Enter key returns PLACE action."""
    action, pos = handle_input(ord("\n"), 4)
    assert action == Action.PLACE
    assert pos == 4


def test_space_triggers_place():
    """Space key returns PLACE action."""
    action, pos = handle_input(ord(" "), 0)
    assert action == Action.PLACE
    assert pos == 0


def test_q_triggers_quit():
    """q key returns QUIT action."""
    action, pos = handle_input(ord("q"), 4)
    assert action == Action.QUIT


def test_r_triggers_restart():
    """r key returns RESTART action."""
    action, pos = handle_input(ord("r"), 4)
    assert action == Action.RESTART


def test_unknown_key_returns_none_action():
    """An unrecognized key returns NONE action with unchanged position."""
    action, pos = handle_input(ord("z"), 4)
    assert action == Action.NONE
    assert pos == 4
