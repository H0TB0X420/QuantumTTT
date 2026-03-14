"""All curses drawing logic for Tic-Tac-Toe."""

import curses

from quantum_ttt.board import Board
from quantum_ttt.quantum import Player

# Color pair IDs.
COLOR_X = 1
COLOR_O = 2
COLOR_CURSOR = 3
COLOR_GRID = 4
COLOR_WIN = 5

# Each cell is 5 wide x 3 tall. Grid = 3 cells + 2 separators per axis.
CELL_W = 5
CELL_H = 3
GRID_W = CELL_W * 3 + 2  # 17
GRID_H = CELL_H * 3 + 2  # 11


def init_colors() -> None:
    """Initialize curses color pairs."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(COLOR_X, curses.COLOR_CYAN, -1)
    curses.init_pair(COLOR_O, curses.COLOR_MAGENTA, -1)
    curses.init_pair(COLOR_CURSOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(COLOR_GRID, curses.COLOR_WHITE, -1)
    curses.init_pair(COLOR_WIN, curses.COLOR_GREEN, -1)


class Renderer:
    """Draws the board, marks, cursor, and status text."""

    def __init__(self, screen: curses.window) -> None:
        self.screen = screen

    def _grid_origin(self) -> tuple[int, int]:
        """Top-left corner to center the grid in the terminal."""
        max_y, max_x = self.screen.getmaxyx()
        y = max(0, (max_y - GRID_H - 4) // 2)
        x = max(0, (max_x - GRID_W) // 2)
        return y, x

    def _cell_origin(self, index: int, gy: int, gx: int) -> tuple[int, int]:
        """Top-left corner of a cell (0-8) relative to grid origin."""
        assert 0 <= index < 9, f"Cell index out of range: {index}"
        row, col = index // 3, index % 3
        return gy + row * (CELL_H + 1), gx + col * (CELL_W + 1)

    def _safe_addstr(self, y: int, x: int, text: str, attr: int = 0) -> None:
        """Write to screen, ignoring out-of-bounds errors from small terminals."""
        try:
            self.screen.addstr(y, x, text, attr)
        except curses.error:
            pass

    def _draw_grid(self, gy: int, gx: int) -> None:
        """Draw grid lines using box-drawing characters."""
        attr = curses.color_pair(COLOR_GRID)

        # Two horizontal separators.
        for sep in range(2):
            y = gy + (sep + 1) * CELL_H + sep
            for x_off in range(GRID_W):
                char = "┼" if x_off in (CELL_W, CELL_W * 2 + 1) else "─"
                self._safe_addstr(y, gx + x_off, char, attr)

        # Two vertical separators.
        for sep in range(2):
            x = gx + (sep + 1) * CELL_W + sep
            for row in range(3):
                for r_off in range(CELL_H):
                    self._safe_addstr(gy + row * (CELL_H + 1) + r_off, x, "│", attr)

    def _draw_marks(self, board: Board, gy: int, gx: int,
                    cursor_pos: int, winning_line: tuple[int, int, int] | None) -> None:
        """Draw X/O marks with cursor highlight and win highlight."""
        for i in range(9):
            cy, cx = self._cell_origin(i, gy, gx)
            center_y = cy + CELL_H // 2
            center_x = cx + CELL_W // 2

            cell = board.cells[i]
            mark = cell.collapsed
            is_cursor = (i == cursor_pos)
            is_winner = winning_line is not None and i in winning_line

            if mark is not None:
                char = mark.value
                if is_winner:
                    attr = curses.color_pair(COLOR_WIN) | curses.A_BOLD
                elif mark == Player.X:
                    attr = curses.color_pair(COLOR_X)
                else:
                    attr = curses.color_pair(COLOR_O)
            else:
                char = "·"
                attr = curses.color_pair(COLOR_GRID) | curses.A_DIM

            if is_cursor:
                attr = curses.color_pair(COLOR_CURSOR) | curses.A_BOLD

            self._safe_addstr(center_y, center_x, char, attr)

            # Bracket markers around the cursor cell.
            if is_cursor:
                b_attr = curses.color_pair(COLOR_CURSOR)
                self._safe_addstr(center_y, cx + 1, "[", b_attr)
                self._safe_addstr(center_y, cx + CELL_W - 2, "]", b_attr)

    def _draw_status(self, board: Board, gy: int, gx: int,
                     game_over: bool, message: str | None) -> None:
        """Draw turn indicator or game-over message below the grid."""
        y = gy + GRID_H + 1
        if game_over and message is not None:
            self._safe_addstr(y, gx, message, curses.A_BOLD)
            self._safe_addstr(y + 1, gx, "Press r to restart, q to quit")
        else:
            self._safe_addstr(y, gx, f"Turn: {board.current_player.value}")
            self._safe_addstr(y + 1, gx, "Arrows: move  Enter: place  q: quit")

    def render(self, board: Board, cursor_pos: int, game_over: bool,
               message: str | None, winning_line: tuple[int, int, int] | None) -> None:
        """Full render pass: clear, draw everything, refresh."""
        self.screen.erase()
        gy, gx = self._grid_origin()
        self._draw_grid(gy, gx)
        self._draw_marks(board, gy, gx, cursor_pos, winning_line)
        self._draw_status(board, gy, gx, game_over, message)
        self.screen.refresh()
