from collections import Counter
from dataclasses import dataclass
from typing import Iterator


@dataclass
class TachyonLayer:
    splitters: set[int]

    def process_timelines(self, timelines: Counter[int]) -> Counter[int]:
        for s in self.splitters & set(timelines.keys()):
            timelines[s - 1] += timelines[s]
            timelines[s + 1] += timelines[s]
            timelines.pop(s)
        return timelines


class TachyonManifold:
    layers: list[TachyonLayer]

    def __init__(self, lines: list[str]) -> None:
        self.layers = []
        for layer in self.parse_lines(lines):
            self.layers.append(layer)

    def process_timelines(self, timelines: Counter[int]) -> Counter[int]:
        for layer in self.layers:
            timelines = layer.process_timelines(timelines)
        return timelines

    @staticmethod
    def parse_lines(lines: list[str]) -> Iterator[TachyonLayer]:
        for line in lines:
            splitters = {i for i, ch in enumerate(line) if ch == "^"}
            if not splitters:
                continue
            yield TachyonLayer(splitters)


def parse_tachyon_manifold_file(file_path: str) -> tuple[Counter[int], TachyonManifold]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]

    timelines = Counter()
    timelines[lines[0].index("S")] += 1

    return timelines, TachyonManifold(lines[1:])


def solve_part2(file_path: str) -> int:
    beams, tachyon_manifold = parse_tachyon_manifold_file(file_path)
    final_timelines = tachyon_manifold.process_timelines(beams)
    return sum(final_timelines.values())


print(solve_part2("input.txt"))
