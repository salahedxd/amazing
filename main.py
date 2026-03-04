# main.py
import sys
import curses
from maze_io import read_maze_file
from maze_solver import solve_maze
from maze_draw import draw_maze, draw_menu, apply_theme, current_theme, rotate_theme

def main(stdscr, filename):
    global current_theme
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    apply_theme()

    maze, entry, exit = read_maze_file(filename)
    solution = solve_maze(maze, entry, exit)
    show_solution = False
    animate_solution = False

    draw_maze(stdscr, maze, entry, exit, animate_maze=True)

    while True:
        draw_maze(stdscr, maze, entry, exit,
          solution if show_solution else None,
          animate_solution=animate_solution)
        draw_menu(stdscr, len(maze))
        animate_solution = False

        key = stdscr.getch()
        if key == ord('1'):
            maze, entry, exit = read_maze_file(filename)
            solution = solve_maze(maze, entry, exit)
        # Press 2 → toggle solution animation
        elif key == ord('2'):
            if not show_solution:
                show_solution = True
                animate_solution = True
            else:
                show_solution = False
                animate_solution = False
        # # Press 5 → animate maze building
        # elif key == ord('5'):
        #     draw_maze(stdscr, maze, entry, exit,
        #             solution=None, animate_maze=True)
        elif key == ord('3'):
            rotate_theme()
            apply_theme()
        elif key == ord('4'):
            break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missed file expected : python3 main.py <maze_file.txt>")
        sys.exit(1)
    curses.wrapper(main, sys.argv[1])