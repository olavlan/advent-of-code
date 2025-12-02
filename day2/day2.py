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


def get_divisors(n) -> Iterator[int]:
    yield 1
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            yield i


def generate_numbers_with_repetitions(
    n_digits: int, start: str | None = None, stop: str | None = None
) -> Iterator[int]:
    if n_digits == 1:
        return
    if start is None:
        start = "1" + "0" * (n_digits - 1)
    if stop is None:
        stop = "9" * n_digits
    for repetition_length in get_divisors(n_digits):
        n_repetitions = int(n_digits / repetition_length)
        first_repeated_number = int(start[:repetition_length])
        last_repeated_number = int(stop[:repetition_length])
        first_number = int(str(first_repeated_number) * n_repetitions)
        last_number = int(str(last_repeated_number) * n_repetitions)
        if int(start) <= first_number <= int(stop):
            yield int(first_number)
        for number in range(first_repeated_number + 1, last_repeated_number):
            yield int(str(number) * n_repetitions)
        if int(start) <= last_number <= int(stop):
            yield int(last_number)


def generate_numbers_with_repetitions_in_range(start: str, stop: str) -> Iterator[int]:
    n_digits_start = len(start)
    n_digits_stop = len(stop)

    if n_digits_start == n_digits_stop:
        yield from generate_numbers_with_repetitions(
            n_digits_start, start=start, stop=stop
        )
        return
    yield from generate_numbers_with_repetitions(n_digits_start, start=start)
    for n_digits in range(n_digits_start + 1, n_digits_stop):
        yield from generate_numbers_with_repetitions(n_digits)
    yield from generate_numbers_with_repetitions(n_digits_stop, stop=stop)


def solve_part2():
    invalid_ids: set[int] = set()
    for start, stop in parse_id_ranges_file("input.txt"):
        for invalid_id in generate_numbers_with_repetitions_in_range(start, stop):
            invalid_ids.add(invalid_id)
    return sum(invalid_ids)


print(solve_part2())
