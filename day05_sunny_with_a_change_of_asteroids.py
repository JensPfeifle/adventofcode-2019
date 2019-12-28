import sys
from typing import List
from intcode import IntCode

"""
Day 5
"""

INPUT_FILE = "day05.inp"


def read(filename, split_on="\n"):
    """ Read and clean up input file """
    with open(filename, "r") as f:
        inpt = f.read().strip().split(split_on)

    return [int(i) for i in inpt]


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

if __name__ == "__main__":
    INPUT = read(INPUT_FILE, split_on=",")

    computer = IntCode(program=INPUT)
    # add input
    computer.stdinput.append("1")
    computer.run_to_halt(output_to_console=True)
