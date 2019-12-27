import sys
from typing import List
from intcode import IntCode

"""
Day 2
"""

INPUT_FILE = "day02.inp"


def read(filename, split_on="\n"):
    """ Read and clean up input file """
    with open(filename, "r") as f:
        inpt = f.read().strip().split(split_on)

    return [int(i) for i in inpt]


def evaluate(program):
    computer = IntCode(program)
    computer.run_to_halt()
    return computer.memory


def tests():
    """ run tests, AssertionError on fail """
    testprogram = [1, 0, 0, 0, 99]
    result = evaluate(testprogram)
    assert result == [2, 0, 0, 0, 99]

    testprogram = [2, 3, 0, 3, 99]
    result = evaluate(testprogram)
    assert result == [2, 3, 0, 6, 99]

    testprogram = [2, 4, 4, 5, 99, 0]
    result = evaluate(testprogram)
    assert result == [2, 4, 4, 5, 99, 9801]

    testprogram = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    result = evaluate(testprogram)
    assert result == [30, 1, 1, 4, 2, 5, 6, 0, 99]

    print("tests passed.")


def solve(inpt):
    """ solve the puzzle and print the result"""
    # replacements specified by puzzle
    inpt[1] = 12
    inpt[2] = 2
    result = evaluate(inpt)
    print(f"part1: {result[0]}")
    # part1 solution: 3790689

    for i in range(100):
        for j in range(100):
            inpt[1] = i
            inpt[2] = j
            result = evaluate(inpt)
            if result[0] == 19690720:
                print(f"part2: {100 * i + j}") # part2 solution


if __name__ == "__main__":
    INPUT = read(INPUT_FILE, split_on=",")
    tests()
    solve(INPUT)

