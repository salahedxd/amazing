from collections import deque

def solve_maze(maze, entry, exit):
    height = len(maze)
    width = len(maze[0])

    queue = deque([entry])
    visited = {entry: None}

    while queue:
        x, y = queue.popleft()

        if (x, y) == exit:
            break

        cell = maze[y][x]

        directions = [
            (0, -1, 1),  # North (bit 0)
            (1, 0, 2),   # East  (bit 1)
            (0, 1, 4),   # South (bit 2)
            (-1, 0, 8),  # West  (bit 3)
        ]

        for dx, dy, wall_bit in directions:
            # if wall is OPEN (bit not set)
            if not (cell & wall_bit):
                nx = x + dx
                ny = y + dy

                if 0 <= nx < width and 0 <= ny < height:
                    if (nx, ny) not in visited:
                        visited[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

    # reconstruct path
    path = []
    node = exit

    if node not in visited:
        return []  # no path

    while node:
        path.append(node)
        node = visited[node]

    path.reverse()

    # remove entry and exit from animation path
    if path and path[0] == entry:
        path = path[1:]
    if path and path[-1] == exit:
        path = path[:-1]

    return path