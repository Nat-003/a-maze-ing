import random


def get_unvisited_neighbors(grid, visited, cx, cy, width, height):
    neighbors = []

    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # N, E, S, W
        nx = cx + dx
        ny = cy + dy
        if 0 <= nx < width and 0 <= ny < height:  # inside bounds
            if not visited[ny][nx]:  # not visited
                neighbors.append((nx, ny))

    return neighbors


def carve_passage(grid, cx, cy, nx, ny):
    dx = nx - cx
    dy = ny - cy

    if dx == 1:
        grid[cy][cx] &= ~2
        grid[ny][nx] &= ~8
    elif dx == -1:
        grid[cy][cx] &= ~8
        grid[ny][nx] &= ~2
    elif dy == 1:
        grid[cy][cx] &= ~4
        grid[ny][nx] &= ~1
    elif dy == -1:
        grid[cy][cx] &= ~1
        grid[ny][nx] &= ~4


def generate_maze(width, height, start_x, start_y):
    grid = [[15 for _ in range(width)] for _ in range(height)]
    visited = [[False for _ in range(width)] for _ in range(height)]

    stack = [(start_x, start_y)]
    visited[start_y][start_x] = True

    while stack:
        cx, cy = stack[-1]
        neighbors = get_unvisited_neighbors(grid,
                                            visited, cx, cy, width, height)
        if neighbors:
            nx, ny = random.choice(neighbors)
            carve_passage(grid, cx, cy, nx, ny)
            visited[ny][nx] = True
            stack.append((nx, ny))
        else:
            stack.pop()

    return grid

