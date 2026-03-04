# # maze_io.py
# def read_maze_file(filename):
#     maze = []
#     entry = (0, 0)
#     exit = (0, 0)
#     with open(filename, 'r', encoding='utf-8') as f:
#         lines = [line.strip() for line in f if line.strip()]

#     # Maze grid lines (only 0 and F)
#     grid_lines = [line for line in lines if all(c in '0F' for c in line.upper())]
#     for line in grid_lines:
#         maze.append([1 if c.upper() == 'F' else 0 for c in line])

#     # Entry/Exit coordinates
#     coords = [line for line in lines if ',' in line]
#     if len(coords) >= 2:
#         entry = tuple(map(int, coords[0].split(',')))
#         exit = tuple(map(int, coords[1].split(',')))
#     return maze, entry, exit

def read_maze_file(filename):
    maze = []
    entry = (0, 0)
    exit = (0, 0)

    with open(filename, 'r', encoding='utf-8') as f:
        raw_lines = [line.strip() for line in f.readlines()]

    # Separate grid from metadata
    grid_lines = []
    metadata = []
    empty_line_found = False

    for line in raw_lines:
        if line == "":
            empty_line_found = True
            continue
        if not empty_line_found:
            grid_lines.append(line)
        else:
            metadata.append(line)

    # Parse hex grid
    for line in grid_lines:
        row = [int(c, 16) for c in line]
        maze.append(row)

    # Parse entry / exit
    if len(metadata) >= 2:
        entry = tuple(map(int, metadata[0].split(',')))
        exit = tuple(map(int, metadata[1].split(',')))

    return maze, entry, exit