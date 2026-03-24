from config_parser import parse_config
from output import write_output
from maze_generator import generate_maze
import sys


def main() -> None:
    if len(sys.argv) == 2:
        try:
            config = parse_config(sys.argv[1])
            if not config:
                return
            for key, value in config.items():
                if key == "WIDTH":
                    width = value
                elif key == "HEIGHT":
                    height = value
                elif key == "ENTRY":
                    entry = value
                elif key == "EXIT":
                    exit_point = value
                elif key == "OUTPUT_FILE":
                    output_file = value

            start_x, start_y = entry
            grid = generate_maze(width, height, start_x, start_y)
            write_output(grid, entry, exit_point, "test", output_file)
        except ValueError as e:
            print(f"{e}")
    else:
        print("Please provide a file path to constrcut the maze")


if __name__ == "__main__":
    main()
