from enum import auto, Enum
import math
from os import abort
import re
from typing import List


class Operation(Enum):
    MUL = auto()
    ADD = auto()
    UNKNOWN = auto()


class OperandType(Enum):
    INT = auto()
    SELF = auto()
    UNKNOWN = auto()


class Monkey:
    def __init__(self) -> None:
        self.inspection_count = 0
        self.items = []  # List of integers representing the worry of an item
        self.operation = Operation.UNKNOWN
        self.operand_type = OperandType.UNKNOWN
        self.operand = 0
        self.test_divisor = 0
        self.true_dest = 0
        self.false_dest = 0

    def __eq__(self, other) -> bool:
        return (
            (self.inspection_count == other.inspection_count)
            and (self.items == other.items)
            and (self.operation == other.operation)
            and (self.operand_type == other.operand_type)
            and (self.operand == other.operand)
            and (self.test_divisor == other.test_divisor)
            and (self.true_dest == other.true_dest)
            and (self.false_dest == other.false_dest)
        )


def parse_monkey_str(monkey_str: str) -> Monkey:
    lines = monkey_str.split("\n")

    starting_items_str = lines[1]
    starting_items = [int(match) for match in re.findall(r"\d+", starting_items_str)]

    operation_line_str = lines[2]
    operation_char = re.findall(r"\+|\*", operation_line_str)[0]
    if operation_char == "+":
        operation = Operation.ADD
    elif operation_char == "*":
        operation = Operation.MUL
    else:
        print(f"Invalid operation_char: {operation_char}")
        abort()

    # The operand is either an integer, or the word 'old'.
    # If it's not an integer, then assume it's old
    operand = re.findall(r"\d+", operation_line_str)
    if len(operand) == 0:
        operand_type = OperandType.SELF
        operand = 0
    else:
        operand_type = OperandType.INT
        operand = int(operand[0])

    divisor_str = lines[3]
    divisor = int(re.findall(r"\d+", divisor_str)[0])

    true_str = lines[4]
    true_dest = int(re.findall(r"\d+", true_str)[0])

    false_str = lines[5]
    false_dest = int(re.findall(r"\d+", false_str)[0])

    return_monkey = Monkey()
    return_monkey.items = starting_items
    return_monkey.operation = operation
    return_monkey.operand = operand
    return_monkey.operand_type = operand_type
    return_monkey.test_divisor = divisor
    return_monkey.true_dest = true_dest
    return_monkey.false_dest = false_dest

    return return_monkey


def parse_monkeys_from_input(input_str: str) -> List[Monkey]:
    monkey_strs = input_str.strip().split("\n\n")
    monkeys = [parse_monkey_str(monkey_str) for monkey_str in monkey_strs]

    return monkeys


def tick_monkeys(
    monkeys: List[Monkey], lcm_of_divisors: int, div_3_reduction: bool
) -> None:
    """Tick all of the monkeys once, throwing items to other monkeys, updating the
    worries of those items. Optionally divides worries by three each throw, otherwise,
    takes the mod of the LCM of the test divisors for reducing worry"""
    for monkey in monkeys:
        for item in monkey.items:
            monkey.inspection_count += 1

            if monkey.operand_type == OperandType.INT:
                operand = monkey.operand
                if monkey.operation == Operation.ADD:
                    new_worry = item + operand
                elif monkey.operation == Operation.MUL:
                    new_worry = item * operand
                else:
                    print(f"Invalid operation: {monkey.operation}")
                    exit()
            elif monkey.operand_type == OperandType.SELF:
                if monkey.operation == Operation.ADD:
                    new_worry = item + item
                elif monkey.operation == Operation.MUL:
                    new_worry = item * item
                else:
                    print(f"Invalid operation: {monkey.operation}")
                    exit()
            else:
                print(f"Invalid operand type: {monkey.operand_type}")
                exit()

            if div_3_reduction is True:
                new_worry = math.floor(new_worry / 3.0)
            else:
                new_worry %= lcm_of_divisors

            if new_worry % monkey.test_divisor == 0:
                monkeys[monkey.true_dest].items.append(new_worry)
            else:
                monkeys[monkey.false_dest].items.append(new_worry)

        monkey.items = []


def calc_monkey_business_after_n_rounds(
    monkeys: List[Monkey], num_rounds: int, div_3_reduction: bool
) -> int:
    """Calculate the monkey business after n rounds of monkey action.
    A divide-by-three reduction in worry per round is optionally applied"""

    # If the div_3 reduction is not used, instead, by dividing worry by the LCM
    # of the test divisors each round, we operate on much smaller integers
    # without changing the result
    divisors = [monkey.test_divisor for monkey in monkeys]
    lcm_of_divisors = math.lcm(*divisors)

    for _ in range(num_rounds):
        tick_monkeys(monkeys, lcm_of_divisors, div_3_reduction)

    inspection_counts = [monkey.inspection_count for monkey in monkeys]
    inspection_counts.sort()

    monkey_business = inspection_counts[-1] * inspection_counts[-2]

    return monkey_business


if __name__ == "__main__":
    input_str = open("input/day11.txt").read()

    monkeys = parse_monkeys_from_input(input_str)

    num_rounds = 20
    monkey_business = calc_monkey_business_after_n_rounds(
        monkeys, num_rounds, div_3_reduction=True
    )
    print(f"Part 1: Monkey business: {monkey_business}")

    num_rounds = 10000
    monkeys = parse_monkeys_from_input(input_str)  # Reset the monkeys!
    monkey_business = calc_monkey_business_after_n_rounds(
        monkeys, num_rounds, div_3_reduction=False
    )
    print(f"Part 2: Monkey business: {monkey_business}")
