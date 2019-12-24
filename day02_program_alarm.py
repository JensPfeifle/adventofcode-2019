import sys
from typing import List

"""
Day 2
"""

INPUT_FILE = "day02.inp"


# instruction = [opcode, ....parameters...]
# instruction_pointer = current pos
# step = insttruction pointer + len(instruction)


def add(state: List[int], pos1: int, pos2: int, result_pos: int) -> List[int]:
    newstate = state.copy()
    newstate[result_pos] = state[pos1] + state[pos2]
    return newstate


def multiply(state: List[int], pos1: int, pos2: int, result_pos: int) -> List[int]:
    newstate = state.copy()
    newstate[result_pos] = state[pos1] * state[pos2]
    return newstate


OPERATIONS = {1: add, 2: multiply}

INSTRUCTION_LENGTHS = {1: 4, 2: 4}

def step(state: List[int], inst_ptr: int) -> List[int]:
    opcode = state[inst_ptr]
    if opcode == 99:
        # print("program halted.")
        return state, -1
    elif opcode not in OPERATIONS.keys():
        print(f"ERROR: Unkown opcode {opcode}!")
        return state, -1
    else:
        operation = OPERATIONS[opcode]
        instruction_len = INSTRUCTION_LENGTHS[opcode]
        parameters = list(state[inst_ptr+1 : inst_ptr + instruction_len])
        new_state = operation(state, *parameters)
        new_ptr = inst_ptr + instruction_len
        return new_state, new_ptr

def evaluate(initial_state: List[int]) -> List[int]:
    instruction_pointer = 0
    state = initial_state.copy()
    while True:
        state, instruction_pointer = step(state, instruction_pointer)
        if instruction_pointer == -1:
            break
    return state


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


def solve(inpt):
    """ solve the puzzle and print the result"""
    # replacements specified by puzzle
    inpt[1] = 12
    inpt[2] = 2
    result = evaluate(inpt)
    print(result)
    print(result[0])
    # part1 solution: 3790689

    for i in range(100):
        for j in range(100):
            inpt[1] = i
            inpt[2] = j
            result = evaluate(inpt)
            if result[0] == 19690720:
                print(100*i+j) # part2 solution


if __name__ == "__main__":
    INPUT = read(INPUT_FILE, split_on=",")
    tests()
    solve(INPUT)
