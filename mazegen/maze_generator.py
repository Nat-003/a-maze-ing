import random
from typing import Any, LiteralString


class MazeGenerator:
    """Generate a maze using a recursive backtracker (DFS) algorithm.

    This class reads a configuration, generates a perfect or imperfect maze,
    embeds a '42' pattern, solves it using BFS, and writes the output to a
    hex-encoded text file.
    """

    MANDATORY_KEYS = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE',
                      'PERFECT']

    def __init__(self, file_path: str):
        """Initialize a new MazeGenerator instance.

        Args:
            file_path (str): The path to the configuration file
            (e.g., 'config.txt').
        """
        self.file_path = file_path
        self.output_file: str = ''
        self.width: int
        self.height: int
        self.start_x: int
        self.start_y: int
        self.seed: int | None
        self.entry: tuple[Any, Any]
        self.grid: list[Any] = []
        self.pattern_cell: list[Any] = []
        self.perfect: bool
        self.exit_point: list[Any]

    def generate(self) -> None:
        """Generate the maze using the recursive backtracker algorithm.

        Uses an explicit stack to prevent recursion depth limits. Handles the
        insertion of the '42' pattern and optional loops if the maze is set
        to be imperfect (PERFECT=False).
        """
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

    def _get_unvisited_neighbors(self, cx: int, cy: int,
                                 visited: list[list[bool]]) -> list[Any]:
        """Return a list of unvisited neighboring cells.

        Args:
            cx (int): X coordinate of the current cell.
            cy (int): Y coordinate of the current cell.
            visited (list[list[bool]]): Grid tracking visited cells.

        Returns:
            list[Any]: List of (x, y) tuples for unvisited neighbors.
        """
        neighbors = []

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx = cx + dx
            ny = cy + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not visited[ny][nx]:
                    neighbors.append((nx, ny))

        return neighbors

    def _carve_passage(self, cx: int, cy: int, nx: Any, ny: Any) -> None:
        """Carve a passage between the current cell and a target cell.

        Modifies the 4-bit wall encoding (North=1, East=2, South=4, West=8)
        to remove walls between the given cells.

        Args:
            cx (int): X coordinate of the current cell.
            cy (int): Y coordinate of the current cell.
            nx (Any): X coordinate of the target cell.
            ny (Any): Y coordinate of the target cell.
        """
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

    def _add_loops(self) -> None:
        """Open random extra passages to create an imperfect maze.

        These extra loops are randomly carved and do not intersect or modify
        the cells forming the central '42' pattern.
        """
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

    def _pattern(self, visited: list[Any]) -> list[Any]:
        """Insert the '42' pattern into the center of the maze.

        Args:
            visited (list[Any]): Grid tracking visited cells
            (will be modified).

        Returns:
            list[Any]: List of (x, y) coordinates making up the '42' pattern.
        """
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
        """Parse raw key-value pairs from the configuration file.

        Args:
            filepath (str): The path to the configuration file.

        Raises:
            ValueError: If a mandatory key is missing or the file is not found.

        Returns:
            dict[str, Any]: Dictionary containing uppercase keys
            and string values.
        """
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
        """Convert all keys in a configuration dictionary to uppercase.

        Args:
            config (dict[Any, Any]): The original configuration dictionary.

        Returns:
            dict[str, Any]: A new dictionary with uppercase keys.
        """
        new_config = {}
        for key, value in config.items():
            new = str(key).upper()
            new_config.update({new: value})
        return new_config

    def parse_config(self, filepath: str) -> dict[str, Any] | None:
        """Validate and format the configuration values.

        Casts values to integers, booleans, or lists as appropriate. Warns and
        provides defaults for invalid seeds or out-of-bounds coordinates.

        Args:
            filepath (str): Path to the configuration file.

        Returns:
            dict[str, Any] | None: Validated configuration dictionary, or None
                                   if validation fails.
        """
        config = {}
        try:
            config = self.get_key(filepath)
            for key, value in config.items():
                if key in ("WIDTH", "HEIGHT"):
                    try:
                        new_value: Any = int(value)
                        if new_value > 0:
                            config[key] = new_value
                        else:
                            raise ValueError
                    except ValueError:
                        raise ValueError("Error invalid height or "
                                         f"width: {value}")
                elif key in ("ENTRY", "EXIT"):
                    try:
                        new_value = []
                        tmp = value.split(',')
                        if len(tmp) != 2:
                            raise ValueError
                        for v in tmp:
                            casted = int(v)
                            new_value.append(casted)
                        config[key] = new_value
                    except ValueError:
                        raise ValueError("Error invalid entry or "
                                         f"exit: {value}")
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
                        print("Warning invalid SEED entered, "
                              "using random seed")
            entry = config["ENTRY"]
            exit_point = config["EXIT"]
            width = config["WIDTH"]
            height = config["HEIGHT"]
            entry_x, entry_y = entry
            exit_x, exit_y = exit_point
            if (entry_x < 0 or entry_x >= width or entry_y < 0
                    or entry_y >= height):
                raise ValueError("Warning: Entry coordinates"
                                 f"({entry_x},{entry_y}) ")
            elif (exit_x < 0 or exit_x >= width or exit_y < 0
                  or exit_y >= height):
                raise ValueError("Warning: Exit coordinates"
                                 f"({exit_x},{exit_y})"
                      "out of bounds")
            return config
        except ValueError as e:
            print(f"{e}")
            return None

    def set_config(self) -> None:
        """Apply the parsed configuration and trigger the maze generation.

        Handles boundary and pattern collision checks for the entry and exit
        points, applying safe defaults if collisions occur.

        Raises:
            ValueError: If the configuration parsing fails or keys are missing.
        """
        config = self.parse_config(self.file_path)
        if config is not None:
            try:
                self.width = config["WIDTH"]
                self.height = config["HEIGHT"]
                self.entry = config["ENTRY"]
                self.exit_point = config["EXIT"]
                self.output_file = config["OUTPUT_FILE"]
                self.perfect = config["PERFECT"]
            except KeyError:
                raise ValueError
            self.seed = config.get("SEED", None)
            self.start_x, self.start_y = self.entry
            if self.entry == self.exit_point:
                raise ValueError("Warning: entry and exit can't be "
                                 "on the same cell")
            self.generate()
            if tuple(self.entry) in self.pattern_cell:
                raise ValueError("Warning: entry lands on '42' pattern")
            if tuple(self.exit_point) in self.pattern_cell:
                raise ValueError("Warning: exit lands on '42' pattern")
        else:
            raise ValueError

    def solve(self) -> LiteralString:
        """Find the shortest path from entry to exit using a BFS algorithm.

        Returns:
            LiteralString: The solution path as a string of cardinal directions
                           (e.g., 'NNESWW'). Returns an empty string if
                           no path is found.
        """
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
                if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                    if (nx, ny) not in came_from:
                        if not (self.grid[cy][cx] & wall):
                            came_from[(nx, ny)] = (cx, cy)
                            queue.append((nx, ny))
        return "".join(reversed(solution_path))

    def path_to_cells(self, path: LiteralString,
                      entry: Any) -> list[tuple[Any, Any]]:
        """Convert a directional path string into a list of cell coordinates.

        Args:
            path (LiteralString): The directional path string
            (e.g., 'N', 'S', 'E', 'W').
            entry (Any): Tuple containing the (x, y) starting coordinates.

        Returns:
            list[tuple[Any, Any]]: List of (x, y) cells traversed by the path.
        """
        x = self.start_x
        y = self.start_y
        cells = [(x, y)]
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
        """Save the maze grid, entry/exit points, and solution path to a file.

        The grid is saved using a hexadecimal representation for the walls.

        Args:
            entry (Any): Tuple of entry coordinates.
            exit_point (Any): Tuple of exit coordinates.
            path (Any): The solution path string.
            filepath (Any): The path to the output text file.

        Raises:
            ValueError: If the file path is invalid or missing.
        """
        try:
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
        except FileNotFoundError:
            raise ValueError("No file provided")
