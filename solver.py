from typing import LiteralString, Any


def solve(grid: list[list[int]], entry: list[int],
          exit_point: list[int] | Any) -> LiteralString:
    start_x, start_y = entry
    end_x, end_y = exit_point
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
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):  # bounds
                if (nx, ny) not in came_from:  # not visited
                    if not (grid[cy][cx] & wall):  # wall open
                        came_from[(nx, ny)] = (cx, cy)
                        queue.append((nx, ny))
    return "".join(reversed(solution_path))


def path_to_cells(path: LiteralString, entry: Any) -> list[tuple[Any, Any]]:
    cells = [tuple(entry)]  # start with entry cell
    x, y = entry
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
