# https://adventofcode.com/2022/day/2

from collections import namedtuple
from enum import auto, Enum
from typing import List


class Move(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()


class Outcome(Enum):
    WIN = auto()
    LOSE = auto()
    DRAW = auto()


outcome_score_lut = {Outcome.WIN: 6, Outcome.LOSE: 0, Outcome.DRAW: 3}


Part1Round = namedtuple("Part1Round", ["player_move", "opponent_move"])
Part2Round = namedtuple("Part2Round", ["player_outcome", "opponent_move"])


player_move_lut = {"X": Move.ROCK, "Y": Move.PAPER, "Z": Move.SCISSORS}
opponent_move_lut = {"A": Move.ROCK, "B": Move.PAPER, "C": Move.SCISSORS}
player_outcome_lut = {"X": Outcome.LOSE, "Y": Outcome.DRAW, "Z": Outcome.WIN}

# Key: Opponent move. Value: What to play to win against that
winning_move_lut = {
    Move.ROCK: Move.PAPER,
    Move.PAPER: Move.SCISSORS,
    Move.SCISSORS: Move.ROCK,
}

# Key: Opponent move. Value: What to play to lose against that
losing_move_lut = {
    Move.ROCK: Move.SCISSORS,
    Move.PAPER: Move.ROCK,
    Move.SCISSORS: Move.PAPER,
}

# Player moves are scored thusly regardless of game outcome
score_lut = {Move.ROCK: 1, Move.PAPER: 2, Move.SCISSORS: 3}


def parse_input_line_part1(input_line: str) -> Part1Round:
    opponent_move = opponent_move_lut[input_line[0]]
    player_move = player_move_lut[input_line[2]]

    return Part1Round(player_move, opponent_move)


def parse_input_line_part2(input_line: str) -> Part2Round:
    opponent_move = opponent_move_lut[input_line[0]]
    player_outcome = player_outcome_lut[input_line[2]]

    return Part2Round(player_outcome, opponent_move)


def round_outcome(round: Part1Round) -> Outcome:
    """Determines who won a round"""
    if winning_move_lut[round.opponent_move] == round.player_move:
        outcome = Outcome.WIN
    elif losing_move_lut[round.opponent_move] == round.player_move:
        outcome = Outcome.LOSE
    else:
        outcome = Outcome.DRAW

    return outcome


def outcome_part1_rules(round: Part1Round) -> int:
    """Calculate the player score from a round using the rules for part 1"""
    score = score_lut[round.player_move]
    outcome = round_outcome(round)
    score += outcome_score_lut[outcome]

    return score


def outcome_part2_rules(round: Part2Round) -> int:
    """Calculate the player score from a round using the rules for part 2"""

    if round.player_outcome == Outcome.WIN:
        player_move = winning_move_lut[round.opponent_move]
    elif round.player_outcome == Outcome.DRAW:
        player_move = round.opponent_move
    else:
        player_move = losing_move_lut[round.opponent_move]

    score = score_lut[player_move]
    score += outcome_score_lut[round.player_outcome]

    return score


def play_tournament_part1_rules(rounds: List[Part1Round]):
    player_score = sum([outcome_part1_rules(round) for round in rounds])
    print(f"Part 1: Final player score: {player_score}")


def play_tournament_part2_rules(rounds: List[Part2Round]):
    player_score = sum([outcome_part2_rules(round) for round in rounds])
    print(f"Part 2: Final player score: {player_score}")


if __name__ == "__main__":

    # Parse Input
    in_lines = [line.strip() for line in open("input/day02.txt").readlines()]
    part1_rounds = [parse_input_line_part1(line) for line in in_lines]
    part2_rounds = [parse_input_line_part2(line) for line in in_lines]

    play_tournament_part1_rules(part1_rounds)
    play_tournament_part2_rules(part2_rounds)
