# Grid: TypeAlias = list[list[Literal[0,1]]]
# parse_paper_roll_grid(file_path: str) -> Grid
# adjacent_ones(Grid, position: tuple[int, int]) -> int
# solve_part1(file_path: str) -> int
# get_accesible_grid_positions(grid: Grid) -> Iterator[tuple[int, int]]

from typing import TypeAlias, Iterator
import itertools

Row: TypeAlias = list[int]
Grid: TypeAlias = list[Row]


def get_zeros_list(length):
    return [0] * length


def parse_paper_roll_grid_file(file_path: str) -> Grid:
    grid: Grid = []
    with open(file_path, "r") as file:
        first = file.readline().rstrip("\n")
        length = len(first) + 2
        grid.append([0] * length)
        file.seek(0)
        for line in file:
            row: Row = [0] * length
            for i, character in enumerate(line):
                if character == "@":
                    row[i + 1] = 1
            grid.append(row)
        grid.append([0] * length)
    return grid


def sum_grid(grid: Grid):
    return sum(sum(col for col in row) for row in grid)


def count_adjacent_ones(grid: Grid, row: int, col: int) -> int:
    subgrid = [row[col - 1 : col + 2] for row in grid[row - 1 : row + 2]]
    return sum_grid(subgrid) - 1


def create_grid_of_zeros(row_size: int, col_size: int) -> Grid:
    return [[0] * row_size for i in range(col_size)]


def print_grid(grid):
    for row in grid:
        print(row)


def solve_part1(file_path: str) -> int:
    grid = parse_paper_roll_grid_file(file_path)
    col_size = len(grid)
    row_size = len(grid[0])
    grid_with_counts = create_grid_of_zeros(row_size, col_size)
    grid_of_accessible_rolls = create_grid_of_zeros(row_size, col_size)
    for row, col in itertools.product(range(1, col_size - 1), range(1, row_size - 1)):
        if grid[row][col] == 1:
            n = count_adjacent_ones(grid, row, col)
            grid_with_counts[row][col] = n
            if n < 4:
                grid_of_accessible_rolls[row][col] = 1
    return sum_grid(grid_of_accessible_rolls)


print(solve_part1("input.txt"))


def get_accessible_grid_positions(grid: Grid) -> Iterator[tuple[int, int]]:
    col_size = len(grid)
    row_size = len(grid[0])
    for row, col in itertools.product(range(1, col_size - 1), range(1, row_size - 1)):
        if grid[row][col] == 1:
            if count_adjacent_ones(grid, row, col) < 4:
                yield row, col


def solve_part2(file_path: str) -> int:
    grid = parse_paper_roll_grid_file(file_path)
    n_removed = 0
    while True:
        accessible_grid_positions = list(get_accessible_grid_positions(grid))
        if not accessible_grid_positions:
            break
        for row, col in accessible_grid_positions:
            grid[row][col] = 0
            n_removed += 1
    return n_removed


print(solve_part2("input.txt"))
