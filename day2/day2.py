from typing import Iterator


def parse_id_ranges_file(file_path: str) -> Iterator[tuple[str, str]]:
    with open(file_path, "r") as file:
        input = file.readline().rstrip("\n")
    for item in input.split(","):
        interval = item.split("-")
        yield interval[0], interval[1]


def get_invalid_ids_in_range(start: str, stop: str) -> Iterator[int]:
    digits_start = len(start)
    digits_stop = len(stop)
    start_is_odd = digits_start % 2 != 0
    stop_is_odd = digits_stop % 2 != 0
    if start_is_odd and stop_is_odd:
        return
    if start_is_odd:
        start = "1" + "0" * digits_start
        digits_start += 1
    if stop_is_odd:
        stop = "9" * (digits_stop - 1)
        digits_stop -= 1

    if digits_start < digits_stop:
        # large intervals like these are not given in the input (but should be easy to handle if necessary)
        raise NotImplementedError()

    # at this point start and stop has the same number of even digits
    # we can thus split both numbers into two halves and work with that
    half_point = int(digits_start / 2)
    start0, start1 = int(start[:half_point]), int(start[half_point:])
    stop0, stop1 = int(stop[:half_point]), int(stop[half_point:])

    for i in range(start0 + 1, stop0):
        yield int(str(i) * 2)
    if start0 < stop0:
        if start1 <= start0:
            yield int(str(start0) * 2)
        if stop0 <= stop1:
            yield int(str(stop0) * 2)
    elif start1 <= start0 <= stop1:
        yield int(str(start0) * 2)


def solve_part1():
    invalid_ids: set[int] = set()
    for start, stop in parse_id_ranges_file("input.txt"):
        for invalid_id in get_invalid_ids_in_range(start, stop):
            invalid_ids.add(invalid_id)
    return sum(invalid_ids)


print(solve_part1())
