# main.py
import sys
import curses
from typing import Any

from maze_io import read_maze_file
from maze_solver import solve_maze
from maze_draw import draw_maze, draw_menu, apply_theme, rotate_theme


def main(stdscr: Any, filename: str) -> None:
    """
    Main entry point for the Amazing Maze Engine using curses.

    Args:
        stdscr: curses window object.
        filename: path to the maze file to load.
    """
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    apply_theme()

    maze, entry_pos, exit_pos = read_maze_file(filename)

    solution = solve_maze(maze, entry_pos, exit_pos)

    show_solution = False
    animate_solution = False

    # Initial maze build animation
    draw_maze(stdscr, maze, entry_pos, exit_pos, animate_maze=True)

    while True:
        # Draw maze with or without solution
        draw_maze(
            stdscr,
            maze,
            entry_pos,
            exit_pos,
            solution if show_solution else None,
            animate_solution=animate_solution,
        )
        draw_menu(stdscr, len(maze))

        # Reset animation flag after first run
        animate_solution = False

        # Wait for user input
        key = stdscr.getch()

        if key == ord('1'):
            # Re-generate maze
            maze, entry_pos, exit_pos = read_maze_file(filename)
            solution = solve_maze(maze, entry_pos, exit_pos)

        elif key == ord('2'):
            # Toggle solution animation
            show_solution = not show_solution
            animate_solution = show_solution

        elif key == ord('3'):
            # Rotate color theme
            rotate_theme()

        elif key == ord('4'):
            # Quit program
            break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <maze_file.txt>")
        sys.exit(1)

    maze, entry_pos, exit_pos = read_maze_file(sys.argv[1])
    if maze is None:
        print("Malformed maze detected. Exiting.")
        sys.exit(1)

    curses.wrapper(main, sys.argv[1])
