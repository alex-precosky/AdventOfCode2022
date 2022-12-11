from day11 import Monkey, Operation, OperandType, parse_monkey_str


def test_parse_monkey_str():
    target = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
"""

    expected = Monkey()
    expected.inspection_count = 0
    expected.items = [79, 98]
    expected.operation = Operation.MUL
    expected.operand_type = OperandType.INT
    expected.operand = 19
    expected.test_divisor = 23
    expected.true_dest = 2
    expected.false_dest = 3

    actual = parse_monkey_str(target)

    assert expected == actual
