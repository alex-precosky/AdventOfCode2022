# https://adventofcode.com/2022/day/3

from collections import namedtuple
import string
from typing import Dict, List


TwoCompartmentRucksack = namedtuple(
    "TwoCompartmentRucksack", ["first_compartment", "second_compartment"]
)


def build_rucksack_from_str(in_str: str) -> TwoCompartmentRucksack:
    """Parse a string into a two compartment rucksack object"""
    pivot_idx = int(len(in_str) / 2)

    first_compartment = in_str[:pivot_idx]
    second_compartment = in_str[pivot_idx:]

    return TwoCompartmentRucksack(
        first_compartment=first_compartment, second_compartment=second_compartment
    )


def build_priority_lut() -> Dict[str, int]:
    """Build a dictionary for looking up the priority of a character"""
    priority_lut = dict()

    for i in range(1, 26 + 1):
        priority_lut[string.ascii_lowercase[i - 1]] = i
        priority_lut[string.ascii_uppercase[i - 1]] = i + 26

    return priority_lut


def calc_rucksack_priority(rucksack: TwoCompartmentRucksack) -> int:
    """Given a TwoCompartmentRucksack, calculate its priority"""
    first_compartment_set = set(rucksack.first_compartment)
    second_compartment_set = set(rucksack.second_compartment)

    intersection = first_compartment_set.intersection(second_compartment_set)

    priority_lut = build_priority_lut()

    priority = priority_lut[list(intersection)[0]]

    return priority


def calc_rucksack_priority_sum(rucksacks: List[str]) -> int:
    """Given a list of rucksacks, calculate their total priority"""
    two_compartment_rucksacks = [
        build_rucksack_from_str(rucksack) for rucksack in rucksacks
    ]

    return sum(
        [calc_rucksack_priority(rucksack) for rucksack in two_compartment_rucksacks]
    )


def find_common_letter_in_rucksack_group(group: List[str]):
    """Given a group of rucksacks, find what letter they all contain
    Assumes that there is exactly one such letter"""
    sets = [set(contents) for contents in group]
    intersection = set.intersection(*sets)

    return list(intersection)[0]


def calc_groups_of_three_priority_sum(rucksacks: List[str]) -> int:
    """Given a list of rucksacks, calculate the sum of the priority of the
    rucksacks grouped into groups of three"""
    groups_of_three = []
    for i in range(0, len(rucksacks), 3):
        groups_of_three.append(rucksacks[i : i + 3])

    common_letters = [
        find_common_letter_in_rucksack_group(group) for group in groups_of_three
    ]

    priority_lut = build_priority_lut()
    priority_sum = sum(
        [priority_lut[common_letter] for common_letter in common_letters]
    )
    return priority_sum


if __name__ == "__main__":
    rucksacks = [line.strip() for line in open("input/day03.txt").readlines()]

    priority_sum = calc_rucksack_priority_sum(rucksacks)
    print(f"The sum of the rucksack priorities is: {priority_sum}")

    priority_sum = calc_groups_of_three_priority_sum(rucksacks)
    print(f"The sum of the rucksack priorities of groups of three is: {priority_sum}")
