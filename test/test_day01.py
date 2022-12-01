from day01 import (
    calorie_sum_of_top_three_elves,
    max_calories_of_elf_with_most_calories,
    tabulate_elf_calories,
)


def test_tabulate_elf_categories():
    in_filename = "input/day01_test01.txt"
    in_str = open(in_filename).read()

    calorie_dict = tabulate_elf_calories(in_str)

    assert len(calorie_dict) == 5
    assert calorie_dict[0] == 6000
    assert calorie_dict[1] == 4000
    assert calorie_dict[2] == 11000
    assert calorie_dict[3] == 24000
    assert calorie_dict[4] == 10000


def test_max_calories_of_elf_with_most_calories():
    in_filename = "input/day01_test01.txt"
    in_str = open(in_filename).read()

    max_calories = max_calories_of_elf_with_most_calories(in_str)
    assert max_calories == 24000


def test_calorie_sum_of_top_three_elves():
    in_filename = "input/day01_test01.txt"
    in_str = open(in_filename).read()

    top_three_sum = calorie_sum_of_top_three_elves(in_str)
    assert top_three_sum == 45000
