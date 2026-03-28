from render import render_maze
from output import write_output
from solver import solve


def ui_menu(mg: object, height, width, entry, exit_point, output_file) -> None:
    grid = mg.grid
    render_maze(height, width, grid, entry, exit_point)
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
                path = solve(grid, entry, exit_point)
                write_output(grid, entry, exit_point, path, output_file)
                render_maze(height, width, grid, entry, exit_point)
            elif user_choice == 2:
                print("Showing path")
            elif user_choice == 3:
                print("changing color ")
            elif user_choice == 4:
                print("Exiting...")
                break
            else:
                print("Invalid choice, only number between 1-4 accepted")
        except ValueError:
            print("Please enter a number between 1 and 4")
