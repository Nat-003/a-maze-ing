from typing import Any


def write_output(grid: Any, entry: Any, exit_point: Any, path: Any,
                 filepath: Any) -> None:
    with open(filepath, 'w') as f:
        for row in grid:
            f.write("".join(f"{cell:X}" for cell in row))
            f.write("\n")
        f.write("\n")
        x, y = entry
        ex, ey = exit_point
        f.write(f"{x},{y}\n")
        f.write(f"{ex},{ey}\n")
        f.write(f"{path}\n")
