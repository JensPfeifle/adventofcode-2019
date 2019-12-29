import sys
import logging
from typing import List
from intcode import IntCode

"""
Day 5
"""

logging.basicConfig()
intcodelogger = logging.getLogger("intcode")
intcodelogger.setLevel(logging.INFO)

INPUT_FILE = "day05.inp"

def read(filename, split_on="\n"):
    """ Read and clean up input file """
    with open(filename, "r") as f:
        inpt = f.read().strip().split(split_on)

    return [int(i) for i in inpt]


def tests():
    """ run tests, AssertionError on fail """
    
    # day05 part1 tests

    testprogram = [1, 0, 0, 0, 99]
    computer = IntCode(program=testprogram)
    computer.run_to_halt()
    assert computer.memory == [2, 0, 0, 0, 99]

    testprogram = [2, 3, 0, 3, 99]
    computer = IntCode(program=testprogram)
    computer.run_to_halt()
    assert computer.memory == [2, 3, 0, 6, 99]

    testprogram = [2, 4, 4, 5, 99, 0]
    computer = IntCode(program=testprogram)
    computer.run_to_halt()
    assert computer.memory == [2, 4, 4, 5, 99, 9801]

    testprogram = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    computer = IntCode(program=testprogram)
    computer.run_to_halt()
    assert computer.memory == [30, 1, 1, 4, 2, 5, 6, 0, 99]


    # comparison tests

    testprogram = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    computer = IntCode(program=testprogram)
    computer.stdinput.append("8")
    result = computer.run_to_halt(output_to_console=False)
    assert result == [1]

    testprogram = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    computer = IntCode(program=testprogram)
    computer.stdinput.append("10")
    result = computer.run_to_halt(output_to_console=False)
    assert result == [0]

    testprogram = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    computer = IntCode(program=testprogram)
    computer.stdinput.append("100")
    result = computer.run_to_halt(output_to_console=False)
    assert result == [0]

    testprogram = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    computer = IntCode(program=testprogram)
    computer.stdinput.append("2")
    result = computer.run_to_halt(output_to_console=False)
    assert result == [1]

    # jump tests

    testprogram = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    computer = IntCode(program=testprogram)
    computer.stdinput.append("0")
    result = computer.run_to_halt(output_to_console=False)
    assert result == [0]

    testprogram = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    computer = IntCode(program=testprogram)
    computer.stdinput.append("0")
    result = computer.run_to_halt(output_to_console=False)
    assert result == [0]

    # large example
    testprogram = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                   1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                   999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    computer = IntCode(program=testprogram)
    computer.stdinput.append("7")
    result = computer.run_to_halt(output_to_console=False)
    assert result == [999]

    computer = IntCode(program=testprogram)
    computer.stdinput.append("8")
    result = computer.run_to_halt(output_to_console=False)
    assert result == [1000]

    computer = IntCode(program=testprogram)
    computer.stdinput.append("9")
    result = computer.run_to_halt(output_to_console=False)
    assert result == [1001]
    print("tests passed.")


if __name__ == "__main__":
    INPUT = read(INPUT_FILE, split_on=",")
    tests()

    computer = IntCode(program=INPUT)
    # add input
    computer.stdinput.append("5")
    computer.run_to_halt(output_to_console=True)
