import itertools
import math
from typing import Iterable, Iterator, TypeAlias

Point: TypeAlias = tuple[int, int, int]
Edge: TypeAlias = tuple[
    int, int, float
]  # references indices of two points + distance between them


class Space:
    points: list[Point]
    sorted_edges: list[Edge]
    connected_sets: list[set[int]]

    def __init__(self, lines: Iterable[str]) -> None:
        self.points = [p for p in self.parse_lines(lines)]
        edges = [e for e in self.calculate_distances(self.points)]
        edges.sort(key=lambda edge: edge[2])
        self.sorted_edges = edges
        self.connected_sets = []

    @staticmethod
    def calculate_distances(points: list[Point]) -> Iterator[Edge]:
        n_points = len(points)
        for i, j in itertools.combinations(range(n_points), 2):
            yield (i, j, math.dist(points[i], points[j]))

    @staticmethod
    def parse_lines(lines: Iterable[str]) -> Iterator[Point]:
        for line in lines:
            x, y, z = line.split(",")
            yield (int(x), int(y), int(z))

    def connect_next(self) -> None:
        i, j, _ = self.sorted_edges.pop(0)
        print(i, self.points[i], j, self.points[j])
        i_membership = None
        j_membership = None
        for z, connected_set in enumerate(self.connected_sets):
            if i in connected_set:
                i_membership = z
            if j in connected_set:
                j_membership = z
            if i_membership and j_membership:
                break

        if i_membership and not j_membership:
            self.connected_sets[i_membership] |= {i, j}
            return
        if j_membership and not i_membership:
            self.connected_sets[j_membership] |= {i, j}
            return
        if not j_membership and not i_membership:
            self.connected_sets.append({i, j})
            return
        assert i_membership
        assert j_membership
        self.connected_sets[i_membership] |= {i, j} | self.connected_sets[j_membership]
        self.connected_sets.pop(j_membership)
        print(self.connected_sets)
        print()

    def make_connections(self, repetitions: int) -> None:
        for i in range(repetitions):
            print(i)
            self.connect_next()

    def get_sorted_connected_sets(self) -> Iterator[set[int]]:
        self.connected_sets.sort(
            key=lambda connected_set: len(connected_set),
            reverse=True,
        )
        connected_points: set[int] = set()
        for connected_set in self.connected_sets:
            connected_points |= connected_set
            yield connected_set
        missing_points = set(range(len(self.points))) - connected_points
        for p in missing_points:
            yield {p}


def parse_junction_box_file(file_path: str) -> Space:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]

    return Space(lines)


def solve_part1(file_path: str) -> int:
    playground_space = parse_junction_box_file(file_path)
    playground_space.make_connections(1000)
    sorted_sets = playground_space.get_sorted_connected_sets()
    print(playground_space.connected_sets)
    return math.prod(
        len(connected_set) for connected_set in itertools.islice(sorted_sets, 3)
    )


print(solve_part1("input.txt"))
