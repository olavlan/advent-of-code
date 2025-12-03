from typing import Iterator


def parse_battery_bank_file(file_path: str) -> Iterator[str]:
    with open(file_path, "r") as file:
        for line in file:
            yield line.rstrip("\n")


def find_or_none(sequence: str, target: str, start: int | None = None) -> int | None:
    occurence = sequence.find(target, start)
    return None if occurence < 0 else occurence


def find_at_most_two_occurences(
    sequence: str, target: str
) -> tuple[int, int | None] | tuple[None, None]:
    first_occurence = find_or_none(sequence, target)
    if first_occurence is None:
        return None, None
    second_occurence = find_or_none(sequence, target, first_occurence + 1)
    return first_occurence, second_occurence


def max_digit_in_sequence(number_sequence: str) -> str:
    max_number = max(int(digit) for digit in number_sequence)
    return str(max_number)


def get_largest_joltage(battery_bank: str) -> int:
    battery_bank_length = len(battery_bank)
    second_digit: str | None = None
    for i in range(9, 0, -1):
        first_occurence, second_occurence = find_at_most_two_occurences(
            battery_bank, str(i)
        )
        if first_occurence is None:
            continue
        if first_occurence == battery_bank_length - 1:
            second_digit = str(i)
            continue
        if second_occurence is None:
            second_digit = max_digit_in_sequence(battery_bank[first_occurence + 1 :])
            return int(str(i) + second_digit)
        if second_digit is None:
            return int(str(i) * 2)
        return int(str(i) + second_digit)

    raise ValueError("Not a valid battery")


def solve_part1(file_path: str) -> int:
    sum = 0
    for battery_bank in parse_battery_bank_file(file_path):
        print("----------------")
        print(f"{battery_bank=}")
        joltage = get_largest_joltage(battery_bank)
        print(f"{joltage=}")
        sum += joltage
    return sum


# print(solve_part1("input.txt"))


def get_largest_subsequence(sequence: str, subsequence_size: int) -> str:
    if subsequence_size == 0:
        return ""
    sequence_length = len(sequence)
    for i in range(9, 0, -1):
        occurence = find_or_none(sequence, str(i))
        if occurence is None or sequence_length - occurence < subsequence_size:
            continue
        return str(i) + get_largest_subsequence(
            sequence[occurence + 1 :], subsequence_size - 1
        )
    raise ValueError("Not a valid sequence.")


def solve_part2(file_path: str) -> int:
    sum = 0
    for battery_bank in parse_battery_bank_file(file_path):
        print("----------------")
        print(f"{battery_bank=}")
        joltage = get_largest_subsequence(battery_bank, 12)
        print(f"{joltage=}")
        sum += int(joltage)
    return sum


print(solve_part2("input.txt"))
