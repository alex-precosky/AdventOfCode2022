from day04 import parse_input_range_pair, range_str_to_set


def test_range_str_to_set():
    target = "4-6"
    expected = {4, 5, 6}
    actual = range_str_to_set(target)

    assert expected == actual


def test_parse_input_range_pair():
    target = "1-2,4-6"
    expected = [{1, 2}, {4, 5, 6}]
    actual = parse_input_range_pair(target)

    assert expected == actual
