from day03 import build_priority_lut, build_rucksack_from_str, calc_rucksack_priority, find_common_letter_in_rucksack_group


def test_build_priority_lut():
    priority_lut = build_priority_lut()

    assert priority_lut["a"] == 1
    assert priority_lut["z"] == 26
    assert priority_lut["A"] == 27
    assert priority_lut["Z"] == 52


def test_calc_rucksack_priority():
    rucksack = "vJrwpWtwJgWrhcsFMMfFFhFp"
    two_compartment_rucksack = build_rucksack_from_str(rucksack)

    expected = 16
    actual = calc_rucksack_priority(two_compartment_rucksack)

    assert expected == actual


def test_find_common_letter_in_rucksack_group():
    rucksacks = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
    ]

    expected = 'r'
    actual = find_common_letter_in_rucksack_group(rucksacks)

    assert expected == actual
