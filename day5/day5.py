from typing import Iterator, Iterable
from dataclasses import dataclass


@dataclass
class Interval:
    start: int
    stop: int

    def __contains__(self, number: int) -> bool:
        return self.start <= number <= self.stop

    def __len__(self):
        return self.stop - self.start + 1


class DisjointIntervals:
    intervals: list[Interval]

    def print(self):
        for i in self.intervals:
            print(i.start, i.stop)

    def __init__(self) -> None:
        self.intervals = []

    def __contains__(self, number: int) -> bool:
        return any(number in interval for interval in self.intervals)

    def __len__(self):
        return sum(len(interval) for interval in self.intervals)

    def add(self, new: Interval) -> None:
        i = 0
        for i, existing in enumerate(self.intervals):
            if new.stop < existing.start:
                break
            if new.start in existing:
                #go forwards and remove intervals 
                #existing.stop = max(existing.stop, new.stop)
                return
            if new.stop in existing:
                #go backwards and remove intervals
                #existing.start = min(existing.start, new.start)
                return
        self.intervals.insert(i + 1, new)
        for i in 
        return


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
        intervals.add(Interval(start, stop))
        intervals.print()
        print()

    return intervals, parse_numbers(lines[i + 1 :])


def solve_part1(file_path: str) -> int:
    intervals, numbers = parse_id_file(file_path)
    return sum(1 for i in numbers if i in intervals)


def solve_part2(file_path: str) -> int:
    intervals, _ = parse_id_file(file_path)
    return len(intervals)


print(solve_part1("input-test.txt"))
# print(solve_part2("input-test.txt"))
