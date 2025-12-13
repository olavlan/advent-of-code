from typing import Iterator

DIAL_SIZE = 100


def parse_rotations_file(file_path: str) -> Iterator[int]:
    # R48 -> 48, L31 -> -31
    with open(file_path, "r") as file:
        for line in file:
            value = int(line[1:])
            if line[0] == "L":
                value = -value
            yield value


position = 50
times_at_zero = 0
for rotation in parse_rotations_file("input.txt"):
    position = (position + rotation) % DIAL_SIZE
    if position == 0:
        times_at_zero += 1

print(times_at_zero)
