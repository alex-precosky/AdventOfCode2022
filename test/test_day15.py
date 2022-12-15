from day15 import Point, Sensor, manhattan_distance, parse_sensor


def test_manhattan_distance():
    point_1 = Point(13, 2)
    point_2 = Point(15, -4)

    expected = 8
    actual = manhattan_distance(point_1, point_2)

    assert expected == actual


def test_parse_sensor():
    target = "Sensor at x=2, y=-18: closest beacon is at x=-2, y=15"

    expected_point = Point(2, -18)
    expected_distance = 2 + 2 + 18 + 15

    actual = parse_sensor(target)

    assert expected_point == actual.point
    assert expected_distance == actual.dist_to_beacon
