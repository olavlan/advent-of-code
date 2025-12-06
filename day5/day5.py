from typing import Iterator, Iterable
from dataclasses import dataclass


@dataclass
class Interval:
    start: int
    stop: int

    def __sub__(self, other: Interval) -> Interval | None:
        start = min(self.start, other.stop)
        stop = max(self.stop, other.start)
        if start > stop:
            return None
        return Interval(start, stop)

    def __str__(self) -> str:
        return f"({self.start}, {self.stop})"


class DisjointIntervals:
    bounds: list[int]
    intervals: list[Interval]

    def __init__(self) -> None:
        self.intervals = []

    def __iter__(self) -> Iterator[Interval]:
        for i in self.intervals:
            yield i

    def __contains__(self, number: int) -> bool:
        return any(i.start <= number <= i.stop for i in self)

    def __len__(self):
        return sum(i.stop - i.start + 1 for i in self)

    def __str__(self) -> str:
        return ", ".join(str(i) for i in self)

    def add(self, start: int, stop: int):
        new = Interval(start, stop)
        print(self)
        print(new)
        for existing in self.intervals:
            new -= existing
            if new is None:
                return
        print(new)
        self.intervals.append(new)
        print()


def parse_numbers(lines: Iterable[str]) -> Iterator[int]:
    for line in lines:
        yield int(line)


def parse_id_file(file_path: str) -> tuple[DisjointIntervals, Iterator[int]]:
    with open(file_path, "r") as file:
        lines = file.readlines()

    intervals = DisjointIntervals()
    i = 0
    for i, line in enumerate(lines):
        line = line.rstrip("\n")
        if not line:
            break
        line = line.split("-")
        start, stop = int(line[0]), int(line[1])
        intervals.add(start, stop)

    return intervals, parse_numbers(lines[i + 1 :])


def solve_part1(file_path: str) -> int:
    intervals, numbers = parse_id_file(file_path)
    return sum(1 for i in numbers if i in intervals)


def solve_part2(file_path: str) -> int:
    intervals, _ = parse_id_file(file_path)
    return len(intervals)


# print(solve_part1("input.txt"))
print(solve_part2("input-test.txt"))
