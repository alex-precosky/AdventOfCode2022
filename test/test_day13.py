from day13 import is_correct_order, OrderCorrectness, parse_packet


def test_parse_ex1():
    target = "[1,2,31,1,1]"

    expected = [1, 2, 31, 1, 1]
    actual = parse_packet(target)

    assert expected == actual


def test_parse_ex2():
    target = "[[1],[2,3,4]]"

    expected = [[1], [2, 3, 4]]
    actual = parse_packet(target)

    assert expected == actual


def test_parse_ex3():
    target = "[[1],4]"

    expected = [[1], 4]
    actual = parse_packet(target)

    assert expected == actual


def test_parse_ex4():
    target = "[1]"

    expected = [1]
    actual = parse_packet(target)

    assert expected == actual


def test_parse_ex5():
    target = "[[8,7,6]]"

    expected = [[8, 7, 6]]
    actual = parse_packet(target)

    assert expected == actual


def test_parse_ex6():
    target = "[]"

    expected = []
    actual = parse_packet(target)

    assert expected == actual


def test_parse_ex7():
    target = "[[[]]]"

    expected = [[[]]]
    actual = parse_packet(target)

    assert expected == actual


def test_parse_ex8():
    target = "[1,[2,[3,[4,[5,6,7]]]],8,9]"

    expected = [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
    actual = parse_packet(target)

    assert expected == actual


def test_compair_pair1():
    left = [1, 1, 3, 1, 1]
    right = [1, 1, 5, 1, 1]

    expected = OrderCorrectness.CORRECT
    actual = is_correct_order(left, right)

    assert expected == actual


def test_compair_pair2():
    left = [[1], [2, 3, 4]]
    right = [[1], 4]

    expected = OrderCorrectness.CORRECT
    actual = is_correct_order(left, right)

    assert expected == actual


def test_compair_pair3():
    left = [9]
    right = [[8, 7, 6]]

    expected = OrderCorrectness.INCORRECT
    actual = is_correct_order(left, right)

    assert expected == actual


def test_compair_pair4():
    left = [[4,4],4,4]
    right = [[4,4],4,4,4]

    expected = OrderCorrectness.CORRECT
    actual = is_correct_order(left, right)

    assert expected == actual


def test_compair_pair5():
    left = [7,7,7,7]
    right = [7,7,7]

    expected = OrderCorrectness.INCORRECT
    actual = is_correct_order(left, right)

    assert expected == actual

def test_compair_pair6():
    left = []
    right = [3]

    expected = OrderCorrectness.CORRECT
    actual = is_correct_order(left, right)

    assert expected == actual


def test_compair_pair7():
    left = [[[]]] 
    right = [[]]

    expected = OrderCorrectness.INCORRECT
    actual = is_correct_order(left, right)

    assert expected == actual


def test_compair_pair8():
    left = [1,[2,[3,[4,[5,6,7]]]],8,9]
    right = [1,[2,[3,[4,[5,6,0]]]],8,9]

    expected = OrderCorrectness.INCORRECT
    actual = is_correct_order(left, right)

    assert expected == actual
