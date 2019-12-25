INPUT = range(109165, 576723 + 1)


def test_adjacent_digits_part1(number):
    " returns True if the number is valid"
    number_string = str(number)
    numbrs = set(number_string)
    groups = [number_string.count(numbr) for numbr in numbrs]
    checks = [group >= 2 for group in groups]
    return any(checks)

def test_adjacent_digits_part2(number):
    " returns True if the number is valid"
    number_string = str(number)
    numbrs = [number_string.count(digit) for digit in set(number_string)]
    checks = [numbr==2 for numbr in numbrs]
    return any(checks)


def test_increasing_digits(number):
    " returns True if the number is valid"
    number_string = str(number)
    checks = []
    for n in range(len(number_string) - 1):
        checks.append(number_string[n + 1] >= number_string[n])
    if all(checks):
        return True
    return False


for number in [112233, 123444, 111122]:
    if test_adjacent_digits_part2(number) and test_increasing_digits(number):
        print(number)
print("tests complete.")

# part1
count = 0
for number in INPUT:
    if test_adjacent_digits_part1(number) and test_increasing_digits(number):
        count += 1
print(f"part1: {count}")

# part2
count = 0
for number in INPUT:
    if test_adjacent_digits_part2(number) and test_increasing_digits(number):
        count += 1
print(f"part2: {count}")