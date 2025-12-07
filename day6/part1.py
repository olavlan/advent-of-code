import math
from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass
class MathProblem:
    numbers: list[int]
    operator: Callable[[Iterable[int]], int]

    def solve(self) -> int:
        return self.operator(self.numbers)


@dataclass
class Worksheet:
    problems: list[MathProblem]

    def solve(self) -> int:
        return sum(p.solve() for p in self.problems)


def parse_operator(operator: str) -> Callable[[Iterable[int]], int]:
    match operator:
        case "+":
            return sum
        case "*":
            return math.prod
        case _:
            raise ValueError("Operator not parsable.")


def parse_worksheet_file(file_path: str) -> Worksheet:
    lines: list[list[str]] = []
    with open(file_path, "r") as file:
        for line in file:
            lines.append(line.split())

    n_numbers_per_problem = len(lines) - 1
    n_problems = len(lines[0])
    problem_numbers = [
        [0 for i in range(n_numbers_per_problem)] for i in range(n_problems)
    ]
    for i_number, line in enumerate(lines[:-1]):
        for i_problem, number in enumerate(line):
            problem_numbers[i_problem][i_number] = int(number)

    problems: list[MathProblem] = []
    for i_problem, operator in enumerate(lines[-1]):
        problem = MathProblem(
            numbers=problem_numbers[i_problem],
            operator=parse_operator(operator),
        )
        problems.append(problem)

    return Worksheet(problems)


def solve_part1(file_path: str):
    worksheet = parse_worksheet_file(file_path)
    return worksheet.solve()


print(solve_part1("input-test.txt"))
