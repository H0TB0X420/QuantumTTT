"""Entry point for Quantum Tic-Tac-Toe. Curses wrapper and game loop."""

import curses

from quantum_ttt.board import Board
from quantum_ttt.input_handler import Action, handle_input
from quantum_ttt.renderer import Renderer, init_colors


def init_screen(screen: curses.window) -> None:
    """Configure the curses screen for gameplay."""
    curses.curs_set(0)
    curses.noecho()
    screen.keypad(True)
    screen.nodelay(False)
    init_colors()


def game_loop(screen: curses.window) -> None:
    """Main game loop: input -> update -> render -> check end.

    Unbounded event loop by design — runs until the player quits.
    """
    init_screen(screen)

    board = Board()
    renderer = Renderer(screen)
    cursor_pos = 4
    game_over = False
    message: str | None = None
    winning_line: tuple[int, int, int] | None = None

    # Unbounded event loop — exits only on quit.
    while True:
        renderer.render(board, cursor_pos, game_over, message, winning_line)

        key = screen.getch()
        action, cursor_pos = handle_input(key, cursor_pos)

        if action == Action.QUIT:
            break

        elif action == Action.RESTART:
            board.reset()
            cursor_pos = 4
            game_over = False
            message = None
            winning_line = None

        elif action == Action.PLACE and not game_over:
            placed = board.place_mark(cursor_pos, board.current_player)
            if placed:
                result = board.check_winner()
                if result is not None:
                    winner, winning_line = result
                    message = f"{winner.value} wins!"
                    game_over = True
                elif board.is_draw():
                    message = "Draw!"
                    game_over = True
                else:
                    board.toggle_player()


def main() -> None:
    """Entry point. curses.wrapper handles clean terminal teardown."""
    curses.wrapper(game_loop)


if __name__ == "__main__":
    main()
