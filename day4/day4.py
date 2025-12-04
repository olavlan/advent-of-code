# Grid: TypeAlias = list[list[Literal[0,1]]]
# parse_paper_roll_grid(file_path: str) -> Grid
# adjacent_ones(Grid, position: tuple[int, int]) -> int
# solve_part1(file_path: str) -> int

from typing import TypeAlias, Literal

Row: TypeAlias = list[Literal[0, 1]]
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


print(parse_paper_roll_grid_file("input-test.txt"))
