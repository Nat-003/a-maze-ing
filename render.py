def render_maze(height, width, grid) -> None:
    for char_y in range(height * 2 + 1):
        for char_x in range(width* 2 + 1):
            if char_x % 2 == 0 and char_y % 2 == 0:
                print('█', end='')
            elif char_x % 2 != 0 and char_y % 2 == 0 :  # horizontal wall
                cell_x = char_x // 2
                cell_y = char_y // 2
                if cell_y >= height or (grid[cell_y][cell_x] & 1):
                    print('██', end='')
                else:
                    print('  ', end='')
            elif char_x % 2 == 0 and char_y % 2 != 0:  # vertical wall
                cell_x = char_x // 2
                cell_y = char_y // 2
                if cell_x >= width or (grid[cell_y][cell_x] & 8):
                    print('█', end='')
                else:
                    print(' ', end='')
            else:  # interior
                print('  ', end='')
        print()  # newline at end of each row