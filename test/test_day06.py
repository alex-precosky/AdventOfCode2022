from day06 import find_nonrepeating_substring_of_length_n

targets = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]


def test_problem_statement_test_cases_part_1():
    expecteds = [7, 5, 6, 10, 11]
    actuals = [find_nonrepeating_substring_of_length_n(target, 4) for target in targets]

    assert expecteds == actuals


def test_problem_statement_test_cases_part_2():
    expecteds = [19, 23, 23, 29, 26]
    actuals = [
        find_nonrepeating_substring_of_length_n(target, 14) for target in targets
    ]

    assert expecteds == actuals
