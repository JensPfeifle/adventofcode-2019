"""
Day 1
What is the sum of the fuel requirements for all of the modules on your spacecraft?
(when also taking into account the mass of the added fuel?)
"""


def read(filename="day01.inp"):
    """ Read and clean up input file """
    with open(filename, "r") as f:
        inpt = f.read().strip().split("\n")

    return [int(i) for i in inpt]


def fuel_required(module_mass: int) -> int:
    """ Calculate the fuel required to launch a module with a given mass"""
    # take its mass
    # divide by three
    # round down
    # and subtract 2.
    fuel_req = max(0, int(module_mass) // 3 - 2)
    # account for fuel required to launch the required fuel
    if fuel_req > 0:
        fuel_req += fuel_required(fuel_req)
    return fuel_req


def tests():
    """ run tests, AssertionError on fail """
    # tests
    assert fuel_required(12) == 2
    assert fuel_required(14) == 2
    assert fuel_required(1969) == 966
    assert fuel_required(100756) == 50346
    print("tests passed.")


def solve(inpt):
    """ solve the puzzle and print the result"""
    total_fuel_requirement = 0
    # individually calculate the fuel needed for the mass of each module
    # then add together all the fuel values
    for module_mass in inpt:
        total_fuel_requirement += fuel_required(module_mass)
    print(f"total_fuel_requirement = {total_fuel_requirement}")


if __name__ == "__main__":
    INPUT = read()
    tests()
    solve(INPUT)
