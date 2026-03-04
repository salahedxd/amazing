# maze_draw.py
import curses
from typing import Any, List, Optional, Tuple

# ---------- Characters ----------
WALL_CHAR = '█'
PATH_CHAR = ' '
ENTRY_CHAR = 'E'
EXIT_CHAR = 'X'
SOLUTION_CHAR = '☀'

# ---------- Header ----------
HEADER_TEXT = "★ THE AMAZING MAZE ENGINE ★"

# ---------- Color Themes ----------
# ---------- Color Themes ----------
# Format: (walls, entry, exit, solution, highlight)
COLOR_THEMES: List[Tuple[int, int, int, int, int]] = [
    (
        curses.COLOR_WHITE,
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_CYAN,
        curses.COLOR_MAGENTA,
    ),
    (
        curses.COLOR_GREEN,
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_CYAN,
        curses.COLOR_MAGENTA,
    ),
    (
        curses.COLOR_YELLOW,
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_CYAN,
        curses.COLOR_MAGENTA,
    ),
    (
        curses.COLOR_RED,
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_CYAN,
        curses.COLOR_MAGENTA,
    ),
    (
        curses.COLOR_CYAN,
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_CYAN,
        curses.COLOR_MAGENTA,
    ),
]

current_theme: int = 0  # Keep track of current theme

# ---------- Safe Draw Helper ----------


def safe_addstr(stdscr: Any, y: int, x: int, text: str, attr: int = 0) -> None:
    """
    Draw text safely inside terminal bounds to avoid curses errors.

    Args:
        stdscr: curses window object
        y: row position
        x: column position
        text: string to display
        attr: curses attributes (color, bold, etc.)
    """
    term_h, term_w = stdscr.getmaxyx()
    if 0 <= y < term_h and 0 <= x < term_w:
        try:
            stdscr.addstr(y, x, text, attr)
        except curses.error:
            pass

# ---------- Theme Functions ----------


def apply_theme() -> None:
    """
    Initialize curses color pairs based on the current theme.

    Color pair numbers:
        1 → Wall
        2 → Entry
        3 → Exit
        4 → Solution
        5 → Highlight / special blocks
    """
    wall, entry, exitc, solution, highlight = COLOR_THEMES[current_theme]
    curses.init_pair(1, wall, -1)
    curses.init_pair(2, entry, -1)
    curses.init_pair(3, exitc, -1)
    curses.init_pair(4, solution, -1)
    curses.init_pair(5, highlight, -1)


def rotate_theme() -> None:
    """Rotate to the next theme and apply it."""
    global current_theme
    current_theme = (current_theme + 1) % len(COLOR_THEMES)
    apply_theme()


# ---------- Maze Drawing ----------
def draw_cell(stdscr: Any, maze: List[List[int]], y: int, x: int) -> None:
    """
    Draw a single maze cell and carve open walls.

    Args:
        stdscr: curses window object
        maze: 2D list of maze cells
        y: row index in maze
        x: column index in maze
    """
    cell = maze[y][x]
    screen_y = 2 * y + 1
    screen_x = 2 * x + 1

    # Empty path
    safe_addstr(stdscr, screen_y, screen_x, PATH_CHAR)

    # Highlight special blocked cell
    if cell == 15:
        safe_addstr(stdscr, screen_y, screen_x, WALL_CHAR,
                    curses.color_pair(5) | curses.A_BOLD)
        return

    # Carve walls if open
    if not (cell & 1):  # North
        safe_addstr(stdscr, screen_y - 1, screen_x, PATH_CHAR)
    if not (cell & 2):  # East
        safe_addstr(stdscr, screen_y, screen_x + 1, PATH_CHAR)
    if not (cell & 4):  # South
        safe_addstr(stdscr, screen_y + 1, screen_x, PATH_CHAR)
    if not (cell & 8):  # West
        safe_addstr(stdscr, screen_y, screen_x - 1, PATH_CHAR)


def draw_maze(
    stdscr: Any,
    maze: List[List[int]],
    entry_pos: Tuple[int, int],
    exit_pos: Tuple[int, int],
    solution: Optional[List[Tuple[int, int]]] = None,
    animate_solution: bool = False,
    animate_maze: bool = False,
) -> None:
    """
    Draw the full maze, entry/exit, header, and optionally the solution.

    Args:
        stdscr: curses window object
        maze: 2D maze grid
        entry_pos: (x, y) entry coordinates
        exit_pos: (x, y) exit coordinates
        solution: list of (x, y) coordinates for solution path
        animate_solution: whether to animate solution drawing
        animate_maze: whether to animate maze build
    """
    stdscr.clear()
    height = len(maze)
    width = len(maze[0])
    canvas_height = 2 * height + 1
    canvas_width = 2 * width + 1

    # Animate full wall background
    for y in range(canvas_height):
        for x in range(canvas_width):
            safe_addstr(stdscr, y, x, WALL_CHAR, curses.color_pair(1))
        if animate_maze:
            stdscr.refresh()
            curses.napms(40)

    # Draw all cells
    for y in range(height):
        for x in range(width):
            draw_cell(stdscr, maze, y, x)
            if animate_maze:
                stdscr.refresh()
                curses.napms(10)

    # Draw entry/exit
    entry_y, entry_x = 2 * entry_pos[1] + 1, 2 * entry_pos[0] + 1
    exit_y, exit_x = 2 * exit_pos[1] + 1, 2 * exit_pos[0] + 1
    safe_addstr(stdscr, entry_y, entry_x, ENTRY_CHAR,
                curses.color_pair(2) | curses.A_BOLD)
    safe_addstr(stdscr, exit_y, exit_x, EXIT_CHAR,
                curses.color_pair(3) | curses.A_BOLD)

    # Draw header
    header_y = canvas_height + 1
    header_x = max(0, (canvas_width - len(HEADER_TEXT)) // 2)
    safe_addstr(stdscr, header_y, header_x, HEADER_TEXT,
                curses.color_pair(1) | curses.A_BOLD)

    # Draw solution path
    if solution:
        for x, y in solution:
            sol_y, sol_x = 2 * y + 1, 2 * x + 1
            safe_addstr(stdscr, sol_y, sol_x, SOLUTION_CHAR,
                        curses.color_pair(4) | curses.A_BOLD)
            if animate_solution:
                stdscr.refresh()
                curses.napms(50)

    stdscr.refresh()


# ---------- Menu ----------
MENU_ITEMS = [
    "1 - Re-generate maze",
    "2 - Show / Animate solution path",
    "3 - Rotate maze colors",
    "4 - Quit"
]


def draw_menu(stdscr: Any, maze_height: int) -> None:
    """
    Draw the menu under the maze.

    Args:
        stdscr: curses window object
        maze_height: number of rows in the maze
    """
    canvas_height = 2 * maze_height + 1
    start_y = canvas_height + 3
    start_x = 2

    for i, item in enumerate(MENU_ITEMS):
        safe_addstr(stdscr, start_y + i, start_x, item)

    safe_addstr(stdscr, start_y + len(MENU_ITEMS) + 1,
                start_x, "Choice (1-4): ")
    stdscr.refresh()
