# https://adventofcode.com/2022/day/4

from typing import List


"""Day 4 is an exercise in basic set theory - we check for intersections and subsets"""


def range_str_to_set(in_str: str):
    """Convert a string representing a range to a set
    For example, inputting 4-6 would return {4, 5, 6}"""
    return_set = set()

    start_end_pair = in_str.split("-")

    start = int(start_end_pair[0])
    end = int(start_end_pair[1])

    for i in range(start, end + 1):
        return_set.add(i)

    return return_set


def parse_input_range_pair(in_str: str) -> List[set]:
    """Given a pair of integer ranges, like 1-3,4-6 return a list of two sets
    representing those two ranges"""
    split_input = in_str.split(",")
    range1 = split_input[0]
    range2 = split_input[1]

    set1 = range_str_to_set(range1)
    set2 = range_str_to_set(range2)

    return [set1, set2]


def does_assignment_pair_contain_a_subset(pair1: set, pair2: set) -> bool:
    """Returns true if set pair1 is a subset of set pair2, or vice-versa"""
    if pair1.issubset(pair2) or pair2.issubset(pair1):
        return True
    else:
        return False


def does_assignment_pair_contain_an_intersection(pair1: set, pair2: set) -> bool:
    """Returns true if sets pair1 and pair2 have any intersectoin"""
    if len(pair1.intersection(pair2)) != 0:
        return True
    else:
        return False


def count_range_pair_sets_that_have_a_subset(range_pair_sets: List[List[set]]) -> int:
    sum = 0

    for range_pair_set in range_pair_sets:
        has_subset = does_assignment_pair_contain_a_subset(
            range_pair_set[0], range_pair_set[1]
        )
        if has_subset is True:
            sum += 1

    return sum


def count_range_pair_sets_that_have_an_intersection(
    range_pair_sets: List[List[set]],
) -> int:
    sum = 0

    for range_pair_set in range_pair_sets:
        has_union = does_assignment_pair_contain_an_intersection(
            range_pair_set[0], range_pair_set[1]
        )
        if has_union is True:
            sum += 1

    return sum


if __name__ == "__main__":
    in_lines = [line.strip() for line in open("input/day04.txt").readlines()]
    range_pair_sets = [parse_input_range_pair(in_line) for in_line in in_lines]

    subset_count = count_range_pair_sets_that_have_a_subset(range_pair_sets)
    print(f"Sets with a subset: {subset_count}")

    intersection_count = count_range_pair_sets_that_have_an_intersection(
        range_pair_sets
    )
    print(f"Sets with a intersection: {intersection_count}")
