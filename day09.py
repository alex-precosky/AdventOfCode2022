from dataclasses import dataclass
from enum import auto, Enum
import re
from typing import List, Set, Tuple


# RopeState is a list of KnotPositions
# 0th element is head, final element is tail
RopeState = list


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Move:
    dir: Direction
    dist: int


def do_move(rope_state: RopeState, move: Move, visited: Set[Tuple]):
    for _ in range(move.dist):
        if move.dir == Direction.UP:
            rope_state[0] = (rope_state[0][0], rope_state[0][1] + 1)
        elif move.dir == Direction.DOWN:
            rope_state[0] = (rope_state[0][0], rope_state[0][1] - 1)
        elif move.dir == Direction.LEFT:
            rope_state[0] = (rope_state[0][0] - 1, rope_state[0][1])
        elif move.dir == Direction.RIGHT:
            rope_state[0] = (rope_state[0][0] + 1, rope_state[0][1])

        # There are many tails. Catch them all up!
        for j in range(len(rope_state) - 1):
            head = rope_state[j]
            tail = rope_state[j + 1]

            head_x = head[0]
            head_y = head[1]
            tail_x = tail[0]
            tail_y = tail[1]

            # Catch up the tail vertical
            if head_x == tail_x:
                if (head_y - tail_y) > 1:
                    tail_y += 1
                elif (head_y - tail_y) < -1:
                    tail_y -= 1

            # Catch up the tail horizontal
            elif head_y == tail_y:
                if (head_x - tail_x) > 1:
                    tail_x += 1
                elif (head_x - tail_x) < -1:
                    tail_x -= 1

            # Catch up the tail diagonally
            elif abs(head_x - tail_x) + abs(head_y - tail_y) > 2:
                # Catch up tail to the up-right
                if (head_y > tail_y) and (head_x > tail_x):
                    tail_x += 1
                    tail_y += 1
                # Catch up tail to the up-left
                elif (head_y > tail_y) and (head_x < tail_x):
                    tail_x -= 1
                    tail_y += 1
                # Catch up tail to the down-right
                elif (head_y < tail_y) and (head_x > tail_x):
                    tail_x += 1
                    tail_y -= 1
                # Catch up tail to the down-left
                elif (head_y < tail_y) and (head_x < tail_x):
                    tail_x -= 1
                    tail_y -= 1

            # Put the updated tail position back into the rope state
            rope_state[j + 1] = (tail_x, tail_y)

        visited.add(rope_state[-1])

    return rope_state


def calc_positions_tail_visits(moves: List[Move], rope_length: int) -> int:
    rope_state = RopeState([(0, 0)] * rope_length)
    visited = {rope_state[-1]}

    for move in moves:
        do_move(rope_state, move, visited)

    return len(visited)


def parse_moves(input_str: str) -> List[Move]:
    input_lines = input_str.strip().split("\n")

    dir_lut = {
        "U": Direction.UP,
        "D": Direction.DOWN,
        "L": Direction.LEFT,
        "R": Direction.RIGHT,
    }

    moves = []
    for line in input_lines:
        dist = int(re.findall(r"\d+", line)[0])
        dir = dir_lut[line[0]]
        move = Move(dir=dir, dist=dist)
        moves.append(move)

    return moves


if __name__ == "__main__":
    input_str = open("input/day09.txt").read()
    moves = parse_moves(input_str)

    rope_length = 2
    tail_positions = calc_positions_tail_visits(moves, rope_length)
    print(
        f"Part 1: Number of tail positions visited for a length {rope_length} rope: {tail_positions}"
    )

    rope_length = 10
    tail_positions = calc_positions_tail_visits(moves, rope_length)
    print(
        f"Part 2: Number of tail positions visited for a length {rope_length} rope: {tail_positions}"
    )
