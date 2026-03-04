# maze_solver.py
from collections import deque
from typing import List, Tuple


def solve_maze(
    maze: List[List[int]], entry_pos: Tuple[int, int],
        exit_pos: Tuple[int, int]
) -> List[Tuple[int, int]]:
    """
    Solve a maze using BFS and return the path from entry to exit.

    Maze cells use bitmask:
      1 → North wall
      2 → East wall
      4 → South wall
      8 → West wall

    Args:
        maze: 2D list of integers representing maze walls.
        entry_pos: (x, y) tuple for maze entry.
        exit_pos: (x, y) tuple for maze exit.

    Returns:
        List of (x, y) tuples representing the path. Entry and exit are
        removed for animation purposes.
    """
    height = len(maze)
    width = len(maze[0])

    queue = deque([entry_pos])
    visited = {entry_pos: None}

    # BFS traversal
    while queue:
        x, y = queue.popleft()

        if (x, y) == exit_pos:
            break

        cell = maze[y][x]

        # Directions: (dx, dy, wall_bit)
        directions = [
            (0, -1, 1),  # North
            (1, 0, 2),   # East
            (0, 1, 4),   # South
            (-1, 0, 8),  # West
        ]

        for dx, dy, wall_bit in directions:
            if not (cell & wall_bit):  # Open wall
                nx, ny = x + dx, y + dy
                if (
                        0 <= nx < width
                        and 0 <= ny < height
                        and (nx, ny) not in visited):
                    visited[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

    # Reconstruct path from exit to entry
    path: List[Tuple[int, int]] = []
    node = exit_pos

    if node not in visited:
        return []  # No path found

    while node:
        path.append(node)
        node = visited[node]

    path.reverse()

    # Remove entry and exit for animation
    if path and path[0] == entry_pos:
        path = path[1:]
    if path and path[-1] == exit_pos:
        path = path[:-1]

    return path
