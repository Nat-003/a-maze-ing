*This project has been created as part of the 42 curriculum by nappasam, inaciri.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator and solver written in Python 3. It takes a configuration file as input, generates a maze using the recursive backtracker algorithm, solves it using BFS, and outputs both a hex-encoded file and an interactive terminal visualization. The maze always contains a visible "42" pixel art pattern and supports perfect maze generation (exactly one path between entry and exit).

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
# Install the mazegen package
make install

# Or install dependencies manually
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Running

```bash
make run
# or
python3 a_maze_ing.py config.txt
```

### Other commands

```bash
make debug    		# run with Python debugger
make lint     		# run flake8 and mypy
make lint-strict	# run flake8 and mypy --strict
make clean    		# remove cache and build artifacts
make build    		# rebuild the mazegen package from sources
```

### Interactive menu

Once the maze is displayed, you can:

1. Re-generate a new maze
2. Show/Hide the shortest path from entry to exit
3. Cycle wall colours
4. Quit

## Configuration file

The configuration file uses one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored. Keys are case-insensitive.

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells (integer) | `WIDTH=20` |
| `HEIGHT` | Maze height in cells (integer) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates x,y | `ENTRY=0,0` |
| `EXIT` | Exit coordinates x,y | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Perfect maze? (`True` or `False`) | `PERFECT=True` |
| `SEED` | Optional integer seed for reproducibility | `SEED=42` |

Example config file:

```
# A-Maze-ing configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Maze generation algorithm

This project uses the **recursive backtracker** (also known as depth-first search maze generation).

### How it works

1. Start at a given cell, mark it as visited
2. Pick a random unvisited neighbour, carve a passage to it, mark it visited
3. Repeat from the new cell
4. When a cell has no unvisited neighbours, backtrack to the previous cell
5. Continue until all cells are visited

An explicit stack is used instead of Python recursion to avoid hitting the recursion limit on large mazes.

### Why we chose this algorithm

The recursive backtracker produces mazes with long winding corridors and few dead ends, which makes them visually interesting and satisfying to solve. It also naturally guarantees full connectivity (every cell is reachable) and wall coherence (both sides of every wall are always carved together). When `PERFECT=False`, a small number of extra passages are added via `_add_loops()` to create additional paths.

## Reusable module — mazegen

The maze generator is packaged as a standalone pip-installable module.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen import MazeGenerator

# Create a 20x15 perfect maze starting at (0, 0) with a fixed seed
mg = MazeGenerator(width=20, height=15, start_x=0, start_y=0, perfect=True, seed=42)
mg.generate()

# Access the grid — list of lists of integers (hex wall encoding)
grid = mg.grid

# Access the "42" pattern cells — list of (x, y) tuples
pattern_cells = mg.pattern_cell
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | int | Maze width in cells |
| `height` | int | Maze height in cells |
| `start_x` | int | Starting cell x coordinate |
| `start_y` | int | Starting cell y coordinate |
| `perfect` | bool | If True, generates a perfect maze (no loops) |
| `seed` | int or None | Random seed for reproducibility |

### Accessing the grid

`mg.grid` is a list of lists where each value is a 4-bit integer encoding the walls of that cell:

| Bit | Direction | Value |
|-----|-----------|-------|
| 0 (LSB) | North | 1 |
| 1 | East | 2 |
| 2 | South | 4 |
| 3 | West | 8 |

A bit set to `1` means the wall is closed, `0` means open. Example: `0xF` (15) means all 4 walls are closed.

### Rebuilding the package

```bash
# In a virtual environment
python -m pip install build
python -m build
# Output will be in dist/
```

## Team and project management

### Roles

- **nappasam** — maze generator (`maze_generator.py`), solver (`solver.py`), output writer (`output.py`)
- **inaciri** — config parser (`config_parser.py`), interactive menu (`menu.py`)

Both team members helped each other across modules when needed — roles were a guide, not a strict boundary.

### Planning

We approached the project logically by building it layer by layer: first the config parser to establish a solid foundation, then the maze generator, then the output writer to verify results visually, then the solver, and finally the terminal UI. This incremental approach made it easy to test each piece before moving on.

### What worked well

The incremental layer-by-layer approach worked very well — having a working foundation at each step made debugging much easier. Communication via Discord when we couldn't meet in person kept things moving smoothly.

### What could be improved

Getting a solid understanding of BFS and DFS took more time than expected. In hindsight, spending more time upfront studying the algorithms before starting to code would have saved time overall.

### Tools used

- **Editor**: VS Code
- **Communication**: Discord and in-person meetings
- **Version control**: Git

## Resources

- [W3Schools Python](https://www.w3schools.com) — quick reference for Python syntax
- [GeeksForGeeks](https://www.geeksforgeeks.org) — algorithm explanations and examples
- YouTube — video explanations of BFS, DFS, and maze generation algorithms
- Python official documentation — `random` module, type hints, packaging

### AI usage

Claude (Anthropic) was used to:
- Work out the logic behind BFS (solver) and DFS (recursive backtracker generator)
- Help debug and reason through error handling in the config parser
- Guide the structure of the pip package (`pyproject.toml`, package layout)
- Review code for correctness and edge cases

All AI-generated explanations and suggestions were reviewed, understood, and implemented by the team members themselves.
