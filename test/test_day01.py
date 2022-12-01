from day01 import tabulate_elf_calories

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
