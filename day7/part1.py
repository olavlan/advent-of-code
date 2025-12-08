from dataclasses import dataclass
from typing import Iterator


@dataclass
class TachyonLayer:
    splitters: set[int]
    n_used_splitters: int = 0

    def process_beams(self, beams: set[int]) -> set[int]:
        beams_stopped = beams & self.splitters
        self.n_used_splitters = len(beams_stopped)

        split_left = {b - 1 for b in beams_stopped}
        split_right = {b + 1 for b in beams_stopped}
        new_beams = split_left | split_right

        return (beams - beams_stopped) | new_beams


class TachyonManifold:
    layers: list[TachyonLayer]
    n_used_splitters: int

    def __init__(self, lines: list[str]) -> None:
        self.layers = []
        for layer in self.parse_lines(lines):
            self.layers.append(layer)
        self.n_used_splitters = 0

    def process_beams(self, beam: set[int]) -> set[int]:
        self.n_used_splitters = 0
        for layer in self.layers:
            beam = layer.process_beams(beam)
            self.n_used_splitters += layer.n_used_splitters
        return beam

    @staticmethod
    def parse_lines(lines: list[str]) -> Iterator[TachyonLayer]:
        for line in lines:
            splitters = {i for i, ch in enumerate(line) if ch == "^"}
            if not splitters:
                continue
            yield TachyonLayer(splitters)


def parse_tachyon_manifold_file(file_path: str) -> tuple[set[int], TachyonManifold]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]

    beams = {i for i, ch in enumerate(lines[0]) if ch == "S"}

    return beams, TachyonManifold(lines[1:])


def solve_part1(file_path: str) -> int:
    beams, tachyon_manifold = parse_tachyon_manifold_file(file_path)
    tachyon_manifold.process_beams(beams)
    return tachyon_manifold.n_used_splitters


print(solve_part1("input.txt"))
