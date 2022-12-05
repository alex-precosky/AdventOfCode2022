# Advent of Code 2022

These are my solutions to the 2022 Advent of code problems: https://adventofcode.com/2022

![pytest](https://github.com/alex-precosky/AdventOfCode2022/actions/workflows/python-package.yml/badge.svg)

# Requirements

- python 3.6+
- pytest

# Run

Each solution is in a file named after what day's problem that solution is for. To run the day 1 solution, simply run:

python day01.py

# Testing

From the project directory, run the unit tests for a day with:

```
export PYTHONPATH=$PYTHONPATH:$PWD
pytest test/test_day01.py
```
