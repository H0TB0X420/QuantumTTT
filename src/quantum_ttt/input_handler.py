"""Keyboard input processing for Tic-Tac-Toe."""

import curses
from enum import Enum


class Action(Enum):
    MOVE = "MOVE"
    PLACE = "PLACE"
    QUIT = "QUIT"
    RESTART = "RESTART"
    NONE = "NONE"


def handle_input(key: int, cursor_pos: int) -> tuple[Action, int]:
    """Process a keypress and return (action, new_cursor_pos).

    Arrow keys move the cursor with wrapping. Enter/Space places.
    q quits, r restarts.
    """
    assert 0 <= cursor_pos <= 8, f"Cursor out of range: {cursor_pos}"

    row = cursor_pos // 3
    col = cursor_pos % 3

    if key == curses.KEY_UP:
        row = (row - 1) % 3
        return Action.MOVE, row * 3 + col

    elif key == curses.KEY_DOWN:
        row = (row + 1) % 3
        return Action.MOVE, row * 3 + col

    elif key == curses.KEY_LEFT:
        col = (col - 1) % 3
        return Action.MOVE, row * 3 + col

    elif key == curses.KEY_RIGHT:
        col = (col + 1) % 3
        return Action.MOVE, row * 3 + col

    elif key in (curses.KEY_ENTER, ord("\n"), ord(" ")):
        return Action.PLACE, cursor_pos

    elif key == ord("q"):
        return Action.QUIT, cursor_pos

    elif key == ord("r"):
        return Action.RESTART, cursor_pos

    else:
        return Action.NONE, cursor_pos
