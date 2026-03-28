import random


class MazeGenerator:
    def __init__(self, width, height, start_x, start_y, seed=None):
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.seed = seed
        self.grid = []

    def generate(self):
        random.seed(self.seed)
        self.grid = [[15 for _ in range(self.width)] for _ in range(self.height)]
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        stack = [(self.start_x, self.start_y)]
        visited[self.start_y][self.start_x] = True

        while stack:
            cx, cy = stack[-1]
            neighbors = self._get_unvisited_neighbors(cx, cy, visited)
            if neighbors:
                nx, ny = random.choice(neighbors)
                self._carve_passage(cx, cy, nx, ny)
                visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

    def _get_unvisited_neighbors(self, cx, cy, visited):
        neighbors = []

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx = cx + dx
            ny = cy + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not visited[ny][nx]:
                    neighbors.append((nx, ny))

        return neighbors

    def _carve_passage(self, cx, cy, nx, ny):
        dx = nx - cx
        dy = ny - cy

        if dx == 1:
            self.grid[cy][cx] &= ~2
            self.grid[ny][nx] &= ~8
        elif dx == -1:
            self.grid[cy][cx] &= ~8
            self.grid[ny][nx] &= ~2
        elif dy == 1:
            self.grid[cy][cx] &= ~4
            self.grid[ny][nx] &= ~1
        elif dy == -1:
            self.grid[cy][cx] &= ~1
            self.grid[ny][nx] &= ~4
