import math
from typing import Callable, Iterable


class MathProblem:
    numbers: list[int]
    operator: Callable[[Iterable[int]], int]

    def __init__(self, column: list[str]) -> None:
        self.numbers = self.parse_numbers(column[:-1])
        self.operator = self.parse_operator(column[-1])

    @staticmethod
    def parse_numbers(column: list[str]):
        column_width = len(column[0])
        numbers = []
        for i in range(column_width):
            number = "".join(row[i] for row in column if row[i])
            numbers.append(int(number))
        return numbers

    @staticmethod
    def parse_operator(operator: str) -> Callable[[Iterable[int]], int]:
        match operator.strip():
            case "+":
                return sum
            case "*":
                return math.prod
            case _:
                raise ValueError("Operator not parsable.")

    def solve(self) -> int:
        return self.operator(self.numbers)


class Worksheet:
    problems: list[MathProblem]

    def __init__(self, lines: list[str]):
        self.problems = self.parse_lines(lines)

    def solve(self) -> int:
        return sum(p.solve() for p in self.problems)

    @staticmethod
    def parse_lines(lines: list[str]) -> list[MathProblem]:
        max_line_length = max(len(line) for line in lines)
        columns = []
        column_start = 0
        for i in range(max_line_length):
            if all(line[i] == " " for line in lines):
                column = [line[column_start:i] for line in lines]
                columns.append(column)
                column_start = i + 1
        last_column = [line[column_start:].rstrip("\n") for line in lines]
        columns.append(last_column)

        problems = []
        for c in columns:
            problems.append(MathProblem(c))
        return problems


def parse_worksheet_file(file_path: str) -> Worksheet:
    lines = []
    with open(file_path, "r") as file:
        for line in file:
            lines.append(line)

    return Worksheet(lines)


def solve_part2(file_path: str):
    worksheet = parse_worksheet_file(file_path)
    return worksheet.solve()


print(solve_part2("input.txt"))
