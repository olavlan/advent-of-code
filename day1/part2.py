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


def get_total_rotation(position_after_first_rotation: int, second_rotation: int):
    # we sum two rotation in the same direction
    # we assume first rotation is between -99 and 99, but we only know the resulting position
    # if the second rotation is negative, we assume the first rotation was also negative (i.e. if position is 75, the first rotation was -25)
    # we return the absolute total rotation
    first_rotation = position_after_first_rotation
    if position_after_first_rotation > 0 and second_rotation < 0:
        first_rotation -= DIAL_SIZE
    return abs(first_rotation + second_rotation)


position = 50
n_passing_zero = 0
for rotation in parse_rotations_file("input.txt"):
    total_rotation = get_total_rotation(position, rotation)
    n_passing_zero += total_rotation // DIAL_SIZE
    position = (position + rotation) % DIAL_SIZE

print(n_passing_zero)
