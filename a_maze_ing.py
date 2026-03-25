from config_parser import parse_config
from output import write_output
from maze_generator import MazeGenerator
from solver import solve
from render import render_maze
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
            start_x, start_y = entry
            seed = config.get("SEED")
            mg = MazeGenerator(width, height, start_x, start_y, seed)
            mg.generate()
            grid = mg.grid
            path = solve(grid, entry, exit_point)
            write_output(grid, entry, exit_point, path, output_file)
            render_maze(height, width, grid)
        except ValueError as e:
            print(f"{e}")
    else:
        print("Please provide a file path to construct the maze")


if __name__ == "__main__":
    main()
