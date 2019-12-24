"""
Day 3
"""
from typing import List, Tuple
import matplotlib.pyplot as plt

INPUT_FILE = "day03.inp"


def read(filename, split_on="\n"):
    """ Read and clean up input file """
    with open(filename, "r") as f:
        inpt = f.read().strip().split(split_on)

    return inpt


def manhattan(xy1, xy2=(0, 0)) -> int:
    """manhattan distance"""
    return abs(xy2[0] - xy1[0]) + abs(xy2[1] - xy1[1])


def plot(wirepath):
    fig, ax_lst = plt.subplots(1, 1)
    ax_lst.plot(*points_from_path(wirepath))
    plt.show()


def points_from_path(path_segments: List[str]) -> List[Tuple[int, int]]:
    """
    Convert path (e.g. [U300,R200,D150]) to path points [(x1,y1),(x2,y2),...]
    """
    xpoints = [0]
    ypoints = [0]
    for segment in path_segments:
        direction = segment[0]
        steps = int(segment[1:])
        if direction == "L":
            xpoints.extend([xpoints[-1] - x for x in range(1, steps + 1)])
            ypoints.extend(steps * [ypoints[-1]])
        elif direction == "R":
            xpoints.extend([xpoints[-1] + x for x in range(1, steps + 1)])
            ypoints.extend(steps * [ypoints[-1]])
        elif direction == "U":
            xpoints.extend(steps * [xpoints[-1]])
            ypoints.extend([ypoints[-1] + y for y in range(1, steps + 1)])
        elif direction == "D":
            xpoints.extend(steps * [xpoints[-1]])
            ypoints.extend([ypoints[-1] - y for y in range(1, steps + 1)])
    return list(zip(xpoints, ypoints))


def num_steps_to_point(
    points: List[Tuple[int, int]], target_point: Tuple[int, int]
) -> int:
    "Given list of point tuples, count steps until a given target point is reached"
    for n, xytuple in enumerate(points):
        if xytuple == target_point:
            return n
    print("point not found!")
    return -1


def find_intersections(
    points1: List[Tuple[int, int]], points2: List[Tuple[int, int]], sort_func=manhattan,
) -> List[Tuple[int, int]]:
    """
    given point tuples [(x1,y1),(x2,y2),...] return list of intersections, sorted by a function
    by default sorted by increasing manhattan distance from center
    """
    intersections = set(points1).intersection(set(points2))
    intersections.remove((0, 0))
    intersections = sorted(list(intersections), key=sort_func)
    return intersections


def find_fewest_steps_to_intersection(points1, points2, intersections):
    fewest = 9999999
    for point in intersections:
        nsteps1 = num_steps_to_point(points1, target_point=point)
        nsteps2 = num_steps_to_point(points2, target_point=point)
        if nsteps1 + nsteps2 < fewest:
            fewest = nsteps1 + nsteps2
    return fewest


def test(path1, path2, correctanswer):
    points1 = points_from_path(path1)
    points2 = points_from_path(path2)
    intersections = find_intersections(points1, points2)
    closest = intersections[0]
    print(f"closest intersection = {closest}")
    print(f"distance to closest intersection = {manhattan(closest)}")
    nsteps1 = num_steps_to_point(points1, target_point=closest)
    nsteps2 = num_steps_to_point(points2, target_point=closest)
    print(f"{nsteps1} and {nsteps2} steps to closest intersection")
    fewest = find_fewest_steps_to_intersection(points1, points2, intersections)
    print(f"{fewest} steps to intersection with fewest steps")


def tests():
    testpath1 = "R8,U5,L5,D3".split(",")
    testpath2 = "U7,R6,D4,L4".split(",")
    test(testpath1, testpath2, correctanswer=6)

    testpath1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(",")
    testpath2 = "U62,R66,U55,R34,D71,R55,D58,R83".split(",")
    test(testpath1, testpath2, correctanswer=159)

    testpath1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(",")
    testpath2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(",")
    test(testpath1, testpath2, correctanswer=135)

    print("tests passed.")


def solve(inpt):
    wire1path, wire2path = (row.split(",") for row in inpt)
    # plot(wire1path)
    points1 = points_from_path(wire1path)
    points2 = points_from_path(wire2path)
    intersections = find_intersections(points1, points2)
    closest = intersections[0]
    print(f"closest intersection = {closest}")
    print(f"distance to closest intersection = {manhattan(closest)}")
    fewest = find_fewest_steps_to_intersection(points1, points2, intersections)
    print(f"{fewest} steps to intersection with fewest steps")


if __name__ == "__main__":
    tests()
    INPUT = read(INPUT_FILE)
    solve(INPUT)
