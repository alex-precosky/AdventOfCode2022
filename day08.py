import numpy as np
from typing import List


# This is an exercise in iterating along rows or columns an array while getting
# your indexing right. It is good practice in array slicing.


def parse_input(in_str: str) -> np.ndarray:
    lines = in_str.strip().split("\n")

    height = len(lines)
    width = len(lines[0])

    arr = np.zeros((height, width))

    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            arr[row, col] = ch

    return arr


def count_externally_visible_trees(arr: np.ndarray) -> int:
    seen = set()  # holds tuples (row, col) of trees that have been externally
                  # seen

    # Scan from the left
    for row, row_data in enumerate(arr):
        highest = -1
        for col, value in enumerate(row_data):
            if value > highest:
                # We see the tree!
                highest = value
                seen.add((row, col))
            if value == 9:
                break

    # Scan from the right
    for row, row_data in enumerate(arr):
        highest = -1
        for col, value in reversed(list(enumerate(row_data))):
            if value > highest:
                # We see the tree!
                highest = value
                seen.add((row, col))
            if value == 9:
                break

    # Scan from the top
    for col, col_data in enumerate(arr.T):
        highest = -1
        for row, value in enumerate(col_data):
            if value > highest:
                # We see the tree!
                highest = value
                seen.add((row, col))
            if value == 9:
                break

    # Scan from the bottom
    for col, col_data in enumerate(arr.T):
        highest = -1
        for row, value in reversed(list(enumerate(col_data))):
            if value > highest:
                # We see the tree!
                highest = value
                seen.add((row, col))
            if value == 9:
                break

    return len(seen)


def get_viewing_distance(target_height, heights: List[int]):
    """Heights is a list of tree heights radiating away from the target tree"""
    viewing_distance = 0
    for value in heights:
        viewing_distance += 1
        if value >= target_height:
            break

    return viewing_distance


def get_scenic_score_for_tree(arr, row: int, col: int) -> int:

    target_height = arr[row][col]

    # For each scanning distance, use fancy slicing to get a list of tree
    # heights eminating outwards from the target tree

    left_viewing_distance = get_viewing_distance(
        target_height, list(reversed(arr[row][0:col]))
    )

    right_viewing_distance = get_viewing_distance(target_height, arr[row][col + 1 :])

    up_viewing_distance = get_viewing_distance(
        target_height, list(reversed(arr.T[col][0:row]))
    )

    down_viewing_distance = get_viewing_distance(target_height, arr.T[col][row + 1 :])

    return (
        left_viewing_distance
        * right_viewing_distance
        * up_viewing_distance
        * down_viewing_distance
    )


def find_highest_scenic_score(arr: np.ndarray) -> int:
    highest = 0

    height, width = arr.shape
    for row in range(height):
        for col in range(width):
            scenic_score = get_scenic_score_for_tree(arr, row, col)
            if scenic_score > highest:
                highest = scenic_score

    return highest


if __name__ == "__main__":
    arr = parse_input(open("input/day08.txt").read())

    visible_trees = count_externally_visible_trees(arr)
    print(f"Part 1: The number of externally visibile trees is: {visible_trees}")

    highest_scenic_score = find_highest_scenic_score(arr)
    print(f"Part 2: The highest scenic score is: {highest_scenic_score}")
