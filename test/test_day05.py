from day05 import Move, get_tops_of_stacks, parse_move, parse_stacks, Stack


def test_parse_move():
    expected = Move(num_to_move=1, source_idx=2, dest_idx=3)
    actual = parse_move("move 1 from 2 to 3")

    assert expected == actual


def test_parse_stacks():
    stacks_str = r"""    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 """

    actual = parse_stacks(stacks_str)
    assert list(actual[0]) == ["Z", "N"]
    assert list(actual[1]) == ["M", "C", "D"]
    assert list(actual[2]) == ["P"]


def test_get_tops_of_stacks():
    stack1 = Stack()
    stack2 = Stack()
    stack3 = Stack()

    stack1.push("A")
    stack1.push("B")
    stack2.push("C")
    stack3.push("D")
    stack3.push("E")
    stack3.push("F")

    expected = "BCF"
    actual = get_tops_of_stacks([stack1, stack2, stack3])

    assert expected == actual
