# maze_draw.py
import curses

# ---------- Characters ----------
WALL_CHAR = '█'
PATH_CHAR = ' '
ENTRY_CHAR = 'E'
EXIT_CHAR = 'X'
SOLUTION_CHAR = '☀'

# ---------- Color Themes ----------
# COLOR_THEMES = (walls, entry, exit, solution)
COLOR_THEMES = [
    (curses.COLOR_WHITE, curses.COLOR_GREEN, curses.COLOR_RED, curses.COLOR_CYAN, curses.COLOR_MAGENTA),
    (curses.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_RED, curses.COLOR_CYAN, curses.COLOR_MAGENTA),
    (curses.COLOR_YELLOW, curses.COLOR_GREEN, curses.COLOR_RED, curses.COLOR_CYAN, curses.COLOR_MAGENTA),
    (curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_RED, curses.COLOR_CYAN, curses.COLOR_MAGENTA),
    (curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_RED, curses.COLOR_CYAN, curses.COLOR_MAGENTA),
]

current_theme = 0  # start with first theme (white walls)

current_theme = 0  # start with first theme (white walls)

current_theme = 0  # keep track of current theme

# ---------- Theme Functions ----------
def apply_theme():
    global current_theme
    wall, entry, exitc, solution, highlight = COLOR_THEMES[current_theme]
    curses.init_pair(1, wall, -1)
    curses.init_pair(2, entry, -1)
    curses.init_pair(3, exitc, -1)
    curses.init_pair(4, solution, -1)
    curses.init_pair(5, highlight, -1)   # <-- NEW

def rotate_theme():
    """Rotate to the next theme and apply it"""
    global current_theme
    current_theme = (current_theme + 1) % len(COLOR_THEMES)
    apply_theme()

# maze_draw.py (update)

def draw_header(stdscr, text="★ THE AMAZING MAZE ENGINE ★"):
    """Draw header message under maze, using the same color theme"""
    height, width = stdscr.getmaxyx()
    # Put header 2 lines below the maze
    header_y = len(stdscr.getyx()[0])  # or len of maze
    header_x = max(2, (width - len(text)) // 2)  # center horizontally
    stdscr.addstr(header_y, header_x, text, curses.color_pair(1)|curses.A_BOLD)  # use wall color pair
    stdscr.refresh()


def draw_maze(stdscr, maze, entry, exit,
              solution=None,
              animate_solution=False,
              animate_maze=False):
    stdscr.clear()
    
    height = len(maze)
    width = len(maze[0])
    canvas_height = 2 * height + 1
    canvas_width  = 2 * width + 1

    # ---- Draw full wall background first ----
    for y in range(canvas_height):
        for x in range(canvas_width):
            stdscr.addstr(y, x, WALL_CHAR, curses.color_pair(1))
            if animate_maze:
                stdscr.refresh()
                curses.napms(5)

    # ---- Draw the maze ----
    cell_coords = [(y, x) for y in range(height) for x in range(width)]
    
    # Shuffle if you want a "growing maze" effect (optional)
    # import random; random.shuffle(cell_coords)

    for y, x in cell_coords:
        cell = maze[y][x]
        screen_y = 2*y + 1
        screen_x = 2*x + 1

        # carve cell interior
        stdscr.addstr(screen_y, screen_x, PATH_CHAR)

        # If this is a 42 pattern cell (blocked), highlight it
        # Highlight full-block cells (the 42 pattern)
        if cell == 15:  # F in hex
            stdscr.addstr(screen_y, screen_x,
                        WALL_CHAR,
                        curses.color_pair(5) | curses.A_BOLD)
            continue
        # carve open walls
        if not (cell & 1):  # North
            stdscr.addstr(screen_y - 1, screen_x, PATH_CHAR)
        if not (cell & 2):  # East
            stdscr.addstr(screen_y, screen_x + 1, PATH_CHAR)
        if not (cell & 4):  # South
            stdscr.addstr(screen_y + 1, screen_x, PATH_CHAR)
        if not (cell & 8):  # West
            stdscr.addstr(screen_y, screen_x - 1, PATH_CHAR)

        # Animate maze build if requested
        if animate_maze:
            stdscr.refresh()
            curses.napms(20)  # adjust speed here

    # ---- Draw entry ----
    entry_y = 2 * entry[1] + 1
    entry_x = 2 * entry[0] + 1
    stdscr.addstr(entry_y, entry_x, ENTRY_CHAR,
                  curses.color_pair(2) | curses.A_BOLD)

    # ---- Draw exit ----
    exit_y = 2 * exit[1] + 1
    exit_x = 2 * exit[0] + 1
    stdscr.addstr(exit_y, exit_x, EXIT_CHAR,
                  curses.color_pair(3) | curses.A_BOLD)

    # ---- Draw header under maze ----
    header_text = "★ THE AMAZING MAZE ENGINE BY SALAH ★"
    header_y = canvas_height + 1
    header_x = max(0, (canvas_width - len(header_text)) // 2)
    stdscr.addstr(header_y, header_x,
                  header_text,
                  curses.color_pair(1) | curses.A_BOLD)

    # ---- Draw solution ----
    if animate_solution and solution:
        for x, y in solution:
            sol_y = 2*y + 1
            sol_x = 2*x + 1
            stdscr.addstr(sol_y, sol_x, SOLUTION_CHAR,
                          curses.color_pair(4) | curses.A_BOLD)
            stdscr.refresh()
            curses.napms(80)  # speed of solution animation
    elif solution:
        # static solution if just showing
        for x, y in solution:
            sol_y = 2*y + 1
            sol_x = 2*x + 1
            stdscr.addstr(sol_y, sol_x, SOLUTION_CHAR,
                          curses.color_pair(4) | curses.A_BOLD)

    stdscr.refresh()

# Menu function
def draw_menu(stdscr, maze_height):
    height, width = stdscr.getmaxyx()

    # real canvas height
    canvas_height = 2 * maze_height + 1

    menu_items = [
        "1 - Re-generate maze",
        "2 - Show / Animate solution path",
        "3 - Rotate maze colors",
        "4 - Quit"
    ]

    start_y = canvas_height + 3
    start_x = 2  # left aligned (clean look)

    for i, item in enumerate(menu_items):
        stdscr.addstr(start_y + i, start_x, item)

    stdscr.addstr(start_y + len(menu_items),
                  start_x,
                  "\nChoice (1-4): ")

    stdscr.refresh()