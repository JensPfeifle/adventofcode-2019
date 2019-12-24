"""
Day XX
"""

INPUT_FILE = "dayXX.inp"

def read(filename):
    """ Read and clean up input file """
    with open(filename, "r") as f:
        inpt = f.read().strip().split("\n")

    return inpt

def tests():
    """ run tests, AssertionError on fail """
    assert True
    print("tests passed.")


def solve(inpt):
    """ solve the puzzle and print the result"""


if __name__ == "__main__":
    INPUT = read(INPUT_FILE)
    tests()
    solve(INPUT)
