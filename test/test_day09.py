from day09 import Direction, Move, parse_moves


def test_parse_moves():
    target = open("input/day09_test01.txt").read()
    expected = [
        Move(Direction.RIGHT, 4),
        Move(Direction.UP, 4),
        Move(Direction.LEFT, 3),
        Move(Direction.DOWN, 1),
        Move(Direction.RIGHT, 4),
        Move(Direction.DOWN, 1),
        Move(Direction.LEFT, 5),
        Move(Direction.RIGHT, 2),
    ]

    actual = parse_moves(target)

    assert expected == actual
