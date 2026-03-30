import random


class MazeGenerator:
    def __init__(self, width, height, start_x, start_y, seed=None):
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.seed = seed
        self.grid = []
        self.pattern_cell = []

    def generate(self):
        random.seed(self.seed)
        self.grid = [[15 for _ in range(self.width)] for _ in range(self.height)]
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        stack = [(self.start_x, self.start_y)]
        visited[self.start_y][self.start_x] = True
        self.pattern_cell = self._pattern(visited)
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

    def _pattern(self, visited) -> list:
        cell_pat = []
        PATTERN_42 = [
                        [1, 0, 0, 1, 0, 1, 1, 1],
                        [1, 0, 0, 1, 0, 0, 0, 1],
                        [1, 1, 1, 1, 0, 1, 1, 1],
                        [0, 0, 0, 1, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0, 1, 1, 1],
                    ]
        pattern_height = len(PATTERN_42)
        pattern_width = len(PATTERN_42[0])
        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            print("Maze too small to display '42' pattern")
            # skip placing the pattern
        else:
            start_x = (self.width - pattern_width) // 2
            start_y = (self.height - pattern_height) // 2
            for row in range(len(PATTERN_42)):
                for col in range(len(PATTERN_42[row])):
                    if PATTERN_42[row][col] == 1:
                        self.grid[start_y + row][start_x + col] = 15
                        visited[start_y + row][start_x + col] = True
                        cell_pat.append((start_x + col, start_y + row))
        return cell_pat
