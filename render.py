from typing import Any


def render_maze(height: Any, width: Any, grid: Any, entry: Any,
                exit_point: Any, path_cells: Any,
                wall_color: str = "\033[37m",
                pattern_cells: Any = None) -> None:
    if path_cells is None:
        path_cells = []
    if pattern_cells is None:
        pattern_cells = []
    entry_x, entry_y = entry
    exit_x, exit_y = exit_point
    ENTRY = "\033[45m"   # magenta BACKGROUND
    EXIT = "\033[41m"   # red BACKGROUND
    RESET = "\033[0m"
    PATH = "\033[43m"   # yellow background
    PATTERN = "\033[45m"  # magenta background
    for char_y in range(height * 2 + 1):
        for char_x in range(width * 2 + 1):
            cell_x = char_x // 2
            cell_y = char_y // 2
            if char_x % 2 == 0 and char_y % 2 == 0:
                print(f'{wall_color}█{RESET}', end='')
            elif char_x % 2 != 0 and char_y % 2 == 0:  # horizontal wall
                if cell_y >= height or (grid[cell_y][cell_x] & 1):
                    print(f'{wall_color}██{RESET}', end='')
                else:
                    print('  ', end='')
            elif char_x % 2 == 0 and char_y % 2 != 0:  # vertical wall
                if cell_x >= width or (grid[cell_y][cell_x] & 8):
                    print(f'{wall_color}█{RESET}', end='')
                else:
                    print(' ', end='')
            else:  # interior
                if entry_x == cell_x and entry_y == cell_y:
                    print(f"{ENTRY}  {RESET}", end='')  # use EE to see it
                elif exit_x == cell_x and exit_y == cell_y:
                    print(f"{EXIT}  {RESET}", end='')   # use XX to see it
                elif (cell_x, cell_y) in path_cells:
                    print(f"{PATH}  {RESET}", end='')
                elif (cell_x, cell_y) in pattern_cells:
                    print(f'{PATTERN}  {RESET}', end='')
                else:
                    print('  ', end='')
        print()  # newline at end of each row
