def write_output(grid, entry, exit_point, path, filepath) -> None:
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
