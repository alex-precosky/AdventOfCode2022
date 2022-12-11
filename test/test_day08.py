from day08 import parse_input
import numpy as np


def test_parse_input():
    target = open("input/day08_test01.txt").read()

    expected = np.array(
        [
            [3, 0, 3, 7, 3],
            [2, 5, 5, 1, 2],
            [6, 5, 3, 3, 2],
            [3, 3, 5, 4, 9],
            [3, 5, 3, 9, 0],
        ]
    )

    actual = parse_input(target)

    assert (expected == actual).all()
