from day02 import (
    Move,
    Outcome,
    Part1Round,
    Part2Round,
    parse_input_line_part1,
    parse_input_line_part2,
    round_outcome
)


def test_parse_part1():
    actual_rounds = [parse_input_line_part1("A Y"),
                     parse_input_line_part1("B X"),
                     parse_input_line_part1("C Z")]

    expected_rounds = [Part1Round(player_move=Move.PAPER, opponent_move=Move.ROCK),
                       Part1Round(player_move=Move.ROCK, opponent_move=Move.PAPER),
                       Part1Round(player_move=Move.SCISSORS, opponent_move=Move.SCISSORS)]

    assert expected_rounds == actual_rounds



def test_parse_part2():
    actual_rounds = [parse_input_line_part2("A Y"),
                     parse_input_line_part2("B X"),
                     parse_input_line_part2("C Z")]

    expected_rounds = [Part2Round(player_outcome=Outcome.DRAW, opponent_move=Move.ROCK),
                       Part2Round(player_outcome=Outcome.LOSE, opponent_move=Move.PAPER),
                       Part2Round(player_outcome=Outcome.WIN, opponent_move=Move.SCISSORS)]

    assert expected_rounds == actual_rounds

def test_round_outcome():
    rounds = [
        Part1Round(player_move=Move.ROCK, opponent_move=Move.PAPER),
        Part1Round(player_move=Move.PAPER, opponent_move=Move.PAPER),
        Part1Round(player_move=Move.SCISSORS, opponent_move=Move.PAPER),
    ]

    expected_outcomes = [Outcome.LOSE, Outcome.DRAW, Outcome.WIN]

    actual_outcomes = [round_outcome(round) for round in rounds]

    assert expected_outcomes == actual_outcomes
