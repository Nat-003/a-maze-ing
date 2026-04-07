from mazegen import MazeGenerator
from menu import ui_menu
import sys


def main() -> None:
    if len(sys.argv) == 2:
        try:
            mg = MazeGenerator(sys.argv[1])
            mg.set_config()
            path = mg.solve()
            mg.write_output(mg.entry, mg.exit_point, path, mg.output_file)
            ui_menu(mg, mg.height, mg.width, mg.entry,
                    mg.exit_point, mg.output_file)
        except ValueError as e:
            print(f"{e}")
            exit()
    else:
        print("Please provide a file path to construct the maze")


if __name__ == "__main__":
    main()
