from dataclasses import dataclass
from enum import auto, IntEnum
import functools
from io import StringIO
from typing import List, Tuple


def parse_input(input_str: str) -> Tuple[List, List]:
    """Parse the problem input into packet lists

    Returns a tuple of two lists - the left_packets and the right_packets
    """
    pair_strs = input_str.split('\n\n')

    pair_strs = [pair_str.split('\n') for pair_str in pair_strs]
    left_strs, right_strs = zip(*pair_strs)

    left_packets = [parse_packet(left_str) for left_str in left_strs]
    right_packets = [parse_packet(right_str) for right_str in right_strs]

    return left_packets, right_packets


def parse_list(sio: StringIO) -> List:
    """
    Parse a Python List from a string. Can parse lists inside of lists recursively.

    Parameters:
        sio: A StringIO where the opening [ has been removed from the stream already
    """
    return_list = []

    int_str = ""

    while True:
        ch = sio.read(1)
        if ch.isnumeric():
            int_str = int_str + ch
        elif ch == ",":
            if int_str != "":
                return_list.append(int(int_str))
                int_str = ""  # reset int_str
        elif ch == "[":
            return_list.append(parse_list(sio))
        elif ch == "]":
            if int_str != "":
                return_list.append(int(int_str))
            return return_list


def parse_packet(in_str: str) -> List[int]:
    """Parse an entire packet from string form to Python List form"""
    sio = StringIO(in_str)
    ch = sio.read(1)
    if ch != '[':
        print(f"First character in a packet must be [ but it was {ch}")
        exit()

    return_lists = []
    return_lists.append(parse_list(sio))

    return return_lists[0]


def compare_lists(left, right):
    for i in range(min((len(left), len(right)))):
        is_correct = is_correct_order(left[i], right[i])
        if is_correct is OrderCorrectness.CORRECT:
            return OrderCorrectness.CORRECT
        elif is_correct is OrderCorrectness.INCORRECT:
            return OrderCorrectness.INCORRECT

    if len(left) < len(right):
        return OrderCorrectness.CORRECT
    elif len(right) < len(left):
        return OrderCorrectness.INCORRECT
    else:
        return OrderCorrectness.UNKNOWN

class OrderCorrectness(IntEnum):
    CORRECT = 0
    INCORRECT = -1
    UNKNOWN = 2


def is_correct_order(left, right):
    if (type(left) is int) and (type(right) is int):
        if left < right:
            correctness = OrderCorrectness.CORRECT
        elif left > right:
            correctness = OrderCorrectness.INCORRECT
        else:
            correctness = OrderCorrectness.UNKNOWN

    elif (type(left) is list) and (type(right) is list):
        correctness = compare_lists(left, right)

    else:
        # Must be one integer and one list
        if type(left) is int:
            correctness = compare_lists([left], right)
        else:
            correctness = compare_lists(left, [right])

    return correctness


def calc_sum_pkt_nums_already_in_order(left_packets: List[str], right_packets: List[str]) -> int:
    """Sums the packet numbers of packets already in the right order

    Packets come in pairs - a left packet and a right packet. Which are in order already?"""
    sum_pkts_already_in_order = 0

    for i in range(len(left_packets)):
        pkt_num = 1 + i

        left_packet = left_packets[i]
        right_packet = right_packets[i]

        if is_correct_order(left_packet, right_packet) is OrderCorrectness.CORRECT:
            sum_pkts_already_in_order += pkt_num

    return sum_pkts_already_in_order


def sort_and_find_divider_pkt_prod_in_pkt_list(packets: List, div1: int, div2: int) -> int:
    """For part 2. Add some divider packets, sort the packet list, then find the product of the divider pkts' numbers"""

    # Add the divider packets
    packets.extend([ [[div1]], [[div2]] ])

    cmp = functools.cmp_to_key(is_correct_order)
    packets = sorted(packets, key=cmp, reverse=True)

    div1_pkt_num = 0
    div2_pkt_num = 0

    for i, packet in enumerate(packets):
        if packet == [[div1]]:
            div1_pkt_num = i + 1
        if packet == [[div2]]:
            div2_pkt_num = i + 1

    div_prod = div1_pkt_num * div2_pkt_num

    return div_prod


if __name__ == "__main__":
    input_str = open('input/day13.txt').read().strip()
    left_packets, right_packets = parse_input(input_str)

    sum_pkt_nums_already_in_order = calc_sum_pkt_nums_already_in_order(left_packets, right_packets)
    print(f"Part 1: The sum of the packet numbers already in the right order is: {sum_pkt_nums_already_in_order}")

    # Part 2 has us sort all the packets along with some extra "divider packets"
    all_packets = left_packets.copy()
    all_packets.extend(right_packets)
    
    div1 = 2
    div2 = 6
    div_prod = sort_and_find_divider_pkt_prod_in_pkt_list(all_packets, div1, div2)
    print(f"Part 2: The product of the divider packet numbers after sorting is: {div_prod}")
