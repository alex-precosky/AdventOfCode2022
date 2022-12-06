# https://adventofcode.com/2022/day/6

from collections import deque


def find_nonrepeating_substring_of_length_n(in_str: str, substring_n: int) -> int:
    recent_chars = deque()

    for i, ch in enumerate(in_str):
        recent_chars.appendleft(ch)

        # Make sure we have enough chars first before seeing if we've found what
        # we're looking for
        if len(recent_chars) < substring_n:
            continue

        if len(set(recent_chars)) == substring_n:
            return i + 1  # +1 because problem uses 1-based indexing

        recent_chars.pop()

    # Nothing found!
    return -1


if __name__ == "__main__":

    input_str = open("input/day06.txt").read()
    part1 = find_nonrepeating_substring_of_length_n(input_str, 4)
    part2 = find_nonrepeating_substring_of_length_n(input_str, 14)

    print(f'Solution - Part1: {part1} Part2: {part2}')
