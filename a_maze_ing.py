from config_parser import parse_config
from output import write_output
from mazegen import MazeGenerator
from solver import solve
from menu import ui_menu
import sys


def main() -> None:
    if len(sys.argv) == 2:
        try:
            config = parse_config(sys.argv[1])
            if not config:
                return
            width = config["WIDTH"]
            height = config["HEIGHT"]
            entry = config["ENTRY"]
            exit_point = config["EXIT"]
            output_file = config["OUTPUT_FILE"]
            perfect = config["PERFECT"]
            start_x, start_y = entry
            seed = config.get("SEED")
            mg = MazeGenerator(width, height, start_x, start_y,perfect, seed)
            mg.generate()
            grid = mg.grid
            mg.generate()
            grid = mg.grid
            if tuple(entry) in mg.pattern_cell:
                print("Warning: entry lands on '42' pattern, defaulting to (0,0)")
                entry = [0, 0]
            if tuple(exit_point) in mg.pattern_cell:
                print("Warning: exit lands on '42' pattern, defaulting to (width-1, height-1)")
                exit_point = [width-1, height-1]
            path = solve(grid, entry, exit_point)
            path = solve(grid, entry, exit_point)
            write_output(grid, entry, exit_point, path, output_file)
            ui_menu(mg, height, width, entry, exit_point, output_file)
        except ValueError as e:
            print(f"{e}")
    else:
        print("Please provide a file path to construct the maze")


if __name__ == "__main__":
    main()
