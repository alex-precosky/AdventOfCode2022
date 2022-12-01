# https://adventofcode.com/2022/day/1

from typing import Dict


def tabulate_elf_calories(in_str: str) -> Dict[int, int]:
    """Take problem input string, and produce a dict of calories consumed by
    each elf

    :returns: Key: Elf number, starting at 0
              Value: Total calories consumed by that elf
    """

    groups = in_str.split("\n\n")

    return_dict = dict()

    for i, group in enumerate(groups):
        calories = [int(x) for x in group.strip().split("\n")]
        return_dict[i] = sum(calories)

    return return_dict


def max_calories_of_elf_with_most_calories(in_str: str) -> int:
    """Given the problem input string, return the most calories any elf consumed"""
    elf_calories = tabulate_elf_calories(in_str)

    max_calories = max(elf_calories.values())
    return max_calories


def calorie_sum_of_top_three_elves(in_str: str) -> int:
    """Given the problem input string, return the total calories consumed by the
    top three calorie consuming elves"""
    elf_calories = tabulate_elf_calories(in_str)

    calories_sorted = sorted(elf_calories.values(), reverse=True)
    top_three_sum = sum(calories_sorted[:3])

    return top_three_sum


if __name__ == "__main__":
    in_filename = "input/day01.txt"
    in_str = open(in_filename).read()

    # part 1
    max_calories = max_calories_of_elf_with_most_calories(in_str)
    print(f"The elf with the most calories had {max_calories} calories")

    # part 2
    top_three_sum = calorie_sum_of_top_three_elves(in_str)
    print(f"The top three elves with the most calories had {top_three_sum} calories")
