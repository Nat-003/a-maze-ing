import random
from typing import Any, LiteralString


class MazeGenerator:
    MANDATORY_KEYS = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE',
                      'PERFECT']

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.output_file: str = None
        self.width: int = None
        self.height: int = None
        self.start_x: int = None
        self.start_y: int = None
        self.seed: int = None
        self.entry = None
        self.grid: list[Any] = []
        self.pattern_cell: list[Any] = []
        self.perfect: bool = None
        self.exit_point = None

    def generate(self) -> None:
        random.seed(self.seed)
        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]
        visited = [[False for _ in range(self.width)]
                   for _ in range(self.height)]

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
        if not self.perfect:
            self._add_loops()

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

    def _add_loops(self):
        extra_passages = (self.width * self.height) // 10
        for _ in range(extra_passages):
            # pick a random cell
            cx = random.randint(0, self.width - 1)
            cy = random.randint(0, self.height - 1)
            # pick a random direction
            dx, dy = random.choice([(0, -1), (1, 0), (0, 1), (-1, 0)])
            nx, ny = cx + dx, cy + dy
            # check bounds
            if 0 <= nx < self.width and 0 <= ny < self.height \
                and (nx, ny) not in self.pattern_cell \
                    and (cx, cy) not in self.pattern_cell:
                self._carve_passage(cx, cy, nx, ny)

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

    def get_key(self, filepath: str) -> dict[str, Any]:
        config = {}
        upper_config = {}
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    clean_line = line.strip()
                    if not clean_line or clean_line.startswith('#'):
                        continue
                    tmp = clean_line.split('=', 1)
                    if len(tmp) == 1:
                        continue
                    key, value = tmp
                    config.update({key: value})
                upper_config = self.key_capitalize(config)
            for key in self.MANDATORY_KEYS:
                if key not in upper_config:
                    raise ValueError(f"Missing mandatory key: {key}")
        except FileNotFoundError:
            raise ValueError(f"File not found: {filepath}")
        return upper_config

    def key_capitalize(self, config: dict[Any, Any]) -> dict[str, Any]:
        new_config = {}
        for key, value in config.items():
            new = str(key).upper()
            new_config.update({new: value})
        return new_config

    def parse_config(self, filepath: str) -> dict[str, Any]:
        config = {}
        try:
            config = self.get_key(filepath)
            for key, value in config.items():
                if key in ("WIDTH", "HEIGHT"):
                    try:
                        new_value: Any = int(value)
                        config[key] = new_value
                    except ValueError:
                        raise ValueError(f"Error invalid height or width: {value}")
                elif key in ("ENTRY", "EXIT"):
                    try:
                        new_value = []
                        tmp = value.split(',')
                        for v in tmp:
                            casted = int(v)
                            new_value.append(casted)
                        config[key] = new_value
                    except ValueError:
                        raise ValueError(f"Error invalid entry or exit: {value}")
                elif key == "PERFECT":
                    if value == "True" or value == "False":
                        config[key] = (value == "True")
                    else:
                        raise ValueError(f"incorrect boolean value {value}")
                elif key == "SEED":
                    try:
                        config[key] = int(value)
                    except ValueError:
                        config[key] = None
                        print("Warning invalid SEED entered, using random seed")
            entry = config["ENTRY"]
            exit_point = config["EXIT"]
            width = config["WIDTH"]
            height = config["HEIGHT"]
            entry_x, entry_y = entry
            exit_x, exit_y = exit_point
            if entry_x < 0 or entry_x >= width or entry_y < 0 or entry_y >= height:
                print(f"Warning: Entry coordinates({entry_x},{entry_y}) out of "
                    f"bounds for maze ({width},{height}) defaulting to (0,0)")
                config["ENTRY"] = (0, 0)
            elif exit_x < 0 or exit_x >= width or exit_y < 0 or exit_y >= height:
                print(f"Warning: Exit coordinates({exit_x},{exit_y}) out of bounds"
                    f" for maze ({width},{height}) defaulting to "
                    f"({width-1},{height-1})")
                config["EXIT"] = (width-1, height-1)
            return config
        except ValueError as e:
            print(f"{e}")
            return config

    def set_config(self) -> None:
        config = self.parse_config(self.file_path)
        try:
            self.width = config["WIDTH"]
            self.height = config["HEIGHT"]
            self.entry = config["ENTRY"]
            self.exit_point = config["EXIT"]
            self.output_file = config["OUTPUT_FILE"]
            self.perfect = config["PERFECT"]
        except KeyError:
            raise ValueError
        try:
            self.seed = config["SEED"]
        except KeyError:
            self.seed = None
        self.start_x, self.start_y = self.entry
        self.generate()
        if tuple(self.entry) in self.pattern_cell:
            print("Warning: entry lands on '42' pattern, "
                  "defaulting to (0,0)")
            self.start_x, self.start_y = (0, 0)
        if tuple(self.exit_point) in self.pattern_cell:
            print("Warning: exit lands on '42' pattern, "
                  "defaulting to (width-1, height-1)")
            self.exit_point = [self.width-1, self.height-1]

    def solve(self) -> LiteralString:
        start_x = self.start_x
        start_y = self.start_y
        end_x, end_y = self.exit_point
        queue = [(start_x, start_y)]
        came_from: dict[tuple[int, int], Any] = {(start_x, start_y): None}
        solution_path: list[Any] = []
        while queue:
            cx, cy = queue.pop(0)
            if cx == end_x and cy == end_y:
                current = (end_x, end_y)
                while current is not None:
                    previous = came_from[current]
                    if previous is None:
                        break
                    current_x, current_y = current
                    previous_x, previous_y = previous
                    dx = current_x - previous_x
                    dy = current_y - previous_y
                    if dx == 1:
                        solution_path.append('E')
                    elif dx == -1:
                        solution_path.append('W')
                    elif dy == 1:
                        solution_path.append('S')
                    elif dy == -1:
                        solution_path.append('N')
                    current = previous
                break
            for dx, dy, wall in [(0, -1, 1), (1, 0, 2), (0, 1, 4), (-1, 0, 8)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):  # bounds
                    if (nx, ny) not in came_from:  # not visited
                        if not (self.grid[cy][cx] & wall):  # wall open
                            came_from[(nx, ny)] = (cx, cy)
                            queue.append((nx, ny))
        return "".join(reversed(solution_path))

    def path_to_cells(self, path: LiteralString, entry: Any) -> list[tuple[Any, Any]]:
        x = self.start_x
        y = self.start_y
        cells = [(x, y)]  # start with entry cell
        for direction in path:
            if direction == 'N':
                y -= 1
            elif direction == 'S':
                y += 1
            elif direction == 'E':
                x += 1
            elif direction == 'W':
                x -= 1
            cells.append((x, y))
        return cells

    def write_output(self, entry: Any, exit_point: Any, path: Any,
                     filepath: Any) -> None:
        with open(filepath, 'w') as f:
            for row in self.grid:
                f.write("".join(f"{cell:X}" for cell in row))
                f.write("\n")
            f.write("\n")
            x, y = entry
            ex, ey = exit_point
            f.write(f"{x},{y}\n")
            f.write(f"{ex},{ey}\n")
            f.write(f"{path}\n")
