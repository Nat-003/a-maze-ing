from render import render_maze
from output import write_output
from solver import solve, path_to_cells


def ui_menu(mg: object, height, width, entry, exit_point, output_file) -> None:
    grid = mg.grid
    cell = []
    path = solve(grid, entry, exit_point)
    render_maze(height, width, grid, entry, exit_point, cell)
    show_path = False
    while True:
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Change maze colors")
        print("4. Quit")
        choice = input("Choice? (1-4): ")
        try:
            user_choice = int(choice)
            if user_choice == 1:
                mg.generate()
                grid = mg.grid
                show_path = False  # ← reset toggle
                cell = []          # ← clear path cells
                path = solve(grid, entry, exit_point)
                write_output(grid, entry, exit_point, path, output_file)
                render_maze(height, width, grid, entry, exit_point, cell)
            elif user_choice == 2:
                show_path = not show_path
                if show_path:
                    cell = path_to_cells(path, entry)
                else:
                    cell = []
                render_maze(height, width, grid, entry, exit_point, cell)
            elif user_choice == 3:
                print("changing color ")
            elif user_choice == 4:
                print("Exiting...")
                break
            else:
                print("Invalid choice, only number between 1-4 accepted")
        except ValueError:
            print("Please enter a number between 1 and 4")
