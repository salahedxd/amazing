# maze_io.py
from typing import List, Tuple


def read_maze_file(
    filename: str,
) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
    """
    Read a maze file and return the maze grid, entry, and exit positions.

    Maze file format:
      - Grid of hex characters (0-F) representing wall bits
      - Empty line
      - Entry coordinates: x,y
      - Exit coordinates: x,y

    Returns:
      maze: 2D list of integers
      entry_pos: (x, y)
      exit_pos: (x, y)
    """
    maze: List[List[int]] = []
    entry_pos: Tuple[int, int] = (0, 0)
    exit_pos: Tuple[int, int] = (0, 0)

    # Read all lines and strip whitespace
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f]

    # Separate grid and metadata
    grid_lines = []
    metadata_lines = []
    empty_line_found = False

    for line in lines:
        if not line:
            empty_line_found = True
            continue
        if not empty_line_found:
            grid_lines.append(line)
        else:
            metadata_lines.append(line)

    # Parse grid lines as hex numbers
    for line in grid_lines:
        row = [int(c, 16) for c in line]
        maze.append(row)

    # --- Sanity check: all rows same length ---
    row_lengths = [len(row) for row in maze]
    if min(row_lengths) != max(row_lengths):
        return None, None, None

    # Parse entry / exit from metadata
    if len(metadata_lines) >= 2:
        entry_pos = tuple(map(int, metadata_lines[0].split(',')))
        exit_pos = tuple(map(int, metadata_lines[1].split(',')))

    return maze, entry_pos, exit_pos
