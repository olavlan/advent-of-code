from typing import Iterator, Iterable
import bisect


class DisjointIntervals:
    bounds: list[int]

    def __init__(self) -> None:
        self.bounds = []

    def __iter__(self) -> Iterator[tuple[int, int]]:
        for i in range(0, len(self.bounds) // 2 + 1, 2):
            yield self.bounds[i], self.bounds[i + 1]

    def __contains__(self, number: int) -> bool:
        return any(start <= number <= stop for start, stop in self)

    def __len__(self):
        return sum(stop - start + 1 for start, stop in self)

    def add(self, start: int, stop: int) -> None:
        if not self.bounds:
            self.bounds = [start, stop]
            return

        new_bounds = [b for b in self.bounds if b < start - 1 or stop + 1 < b]
        insertion_point = bisect.bisect_left(new_bounds, start)
        start_is_in_existing_interval = insertion_point % 2 == 1
        if not start_is_in_existing_interval:
            new_bounds.insert(insertion_point, start)
        if len(new_bounds) % 2 == 1:
            new_bounds.insert(insertion_point + 1, stop)
        print(start, stop)
        print(new_bounds)
        print()
        self.bounds = new_bounds


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
print(solve_part2("input.txt"))
