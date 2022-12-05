# https://adventofcode.com/2022/day/5

from collections import deque, namedtuple
import re
from typing import List, Tuple


# This is a problem in crate stacking. We'll use Stacks to represent the stacked conainers
# We'll move crates from stack to stack based on a set of moves given in the input

Move = namedtuple("Move", ["num_to_move", "source_idx", "dest_idx"])


class Stack(deque):
    def push(self, item):
        self.append(item)


def parse_move(in_str: str) -> Move:
    """Parse a string like 'move 1 from 2 to 1' into a Move object"""
    m = re.findall(r"\d+", in_str)

    num_to_move = int(m[0])
    source_idx = int(m[1])
    dest_idx = int(m[2])

    return Move(num_to_move=num_to_move, source_idx=source_idx, dest_idx=dest_idx)


def parse_stacks(stacks_str: str):
    """Parse the part of the input that shows the graphical representation of the stacks
    into a list of stacks"""

    # The last line in the stacks string contains a numbering of the stacks. The final of such numbers
    # tells us how many stacks there are
    stack_number_str = stacks_str.split("\n")[-1]
    m = re.findall(r"\d+", stack_number_str)[-1]
    num_stacks = int(m[0])

    # Initialize a list of stacks that we'll pop items into
    stacks = list()
    for i in range(num_stacks):
        stacks.append(Stack())

    # Read the stack string representation one line at a time. Check in the columns
    # that could contain a letter, representing a crate label, to see if there is indeed
    # a crate there
    #
    # Iterates in reverse order so that the items at the bottom of the string end up at
    # the bottom of the stacks
    for stack_str in reversed(stacks_str.split("\n")[:-1]):
        for stack_num in range(num_stacks):
            label_idx = (stack_num * 4) + 1
            ch = stack_str[label_idx]
            if ch.isalpha():
                stacks[stack_num].push(ch)

    return stacks


def run_move(stacks: List[Stack], move: Move, retain_order: bool) -> None:
    """Runs one move on the stacks

    retain_order: Set to True if this is the 9001 model stacker which grabs
    multiple boxes at once.  False for the 9000 model stacker which moves on box
    at once, so their order gets reversed during the move
    """
    popped_items = list()
    for i in range(move.num_to_move):
        popped_items.append(stacks[move.source_idx - 1].pop())

    if retain_order:
        popped_items.reverse()

    for i in range(move.num_to_move):
        stacks[move.dest_idx - 1].push(popped_items[i])


def run_moves(stacks, moves, retain_order: bool):
    for move in moves:
        run_move(stacks, move, retain_order)


def get_tops_of_stacks(stacks) -> str:
    """Get a string representing the top of the stacks from first stack to last stack"""
    top_of_stacks = list()

    for i in range(len(stacks)):
        item = stacks[i][-1]
        top_of_stacks.append(item)

    return "".join(top_of_stacks)


def parse_input(in_str: str) -> Tuple:
    """Returns tuple: List[Stack], List[Move]"""
    in_str_components = in_str.split("\n\n")
    stacks_str = in_str_components[0]
    moves_str = in_str_components[1]

    stacks = parse_stacks(stacks_str)
    moves = [parse_move(move_str) for move_str in moves_str.split("\n")]

    run_moves(stacks, moves, retain_order=False)
    print(f'Part 1: {get_tops_of_stacks(stacks)}')

    # Reinit stacks for part 2
    stacks = parse_stacks(stacks_str)
    run_moves(stacks, moves, retain_order=True)
    print(f'Part 2: {get_tops_of_stacks(stacks)}')

if __name__ == "__main__":
    in_str = open("input/day05.txt").read()
    parse_input(in_str)
