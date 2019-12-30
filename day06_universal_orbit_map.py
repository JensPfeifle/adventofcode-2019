from collections import defaultdict

INPUT_FILE = "day06.inp"

def read(filename, split_on="\n"):
    """ Read and clean up input file """
    with open(filename, "r") as f:
        inpt = f.read().strip().split(split_on)

    return inpt

def find_map_root_object(orbit_map):
    relationships = [relationship.strip().split(")") for relationship in orbit_map]
    centers, orbiters = zip(*relationships)
    root_object = set(centers) - set(orbiters)
    assert len(root_object) == 1
    return root_object.pop()

def get_total_orbits(orbit_map):
    "get total number of direct and indirect orbits"
    depth_map = {} # num orbits between object and root
    root = find_map_root_object(orbit_map)
    depth_map[root] = 0
    # num_orbiters does not count root object
    num_orbiters = len(set(relationship.strip().split(")")[1] for relationship in orbit_map))
    while True:
        for relationship in orbit_map:
            center, orbiter = relationship.strip().split(")")
            if center in depth_map.keys():
                depth_map[orbiter] = depth_map[center] + 1
        if len(depth_map) >= num_orbiters:
            break
    return sum(depth_map.values())

def orbital_transfers_required(orbit_map, obj = "YOU", target="SAN"):
    root_object = find_map_root_object(orbit_map)
    relationships = [(relationship.strip().split(")"))
                     for relationship in orbit_map]
    orbiter_center_dict = {orbiter:center for center, orbiter in relationships}
    obj_path = [obj]
    target_path = [target]
    # iterate, building paths until they share an object
    while set(obj_path).isdisjoint(set(target_path)):
        # build path backward from obj
        if not obj_path[-1] == root_object:
            obj_path.append(orbiter_center_dict[obj_path[-1]])
        # build path backward from target
        if not target_path[-1] == root_object:
            target_path.append(orbiter_center_dict[target_path[-1]])
    common_obj = set(obj_path).intersection(set(target_path))
    assert len(common_obj) == 1
    common_obj = common_obj.pop()
    # get path length between common object and obj
    pathlen_to_obj = obj_path.index(common_obj) - 1
    # get path length between common object and target
    pathlen_to_target = target_path.index(common_obj) - 1

    return pathlen_to_obj + pathlen_to_target
    

def tests():
    example_map = ['COM)B',
                    'B)C',
                    'C)D',
                    'D)E',
                    'E)F',
                    'B)G',
                    'G)H',
                    'D)I',
                    'E)J',
                    'J)K',
                    'K)L']

    total_orbits = get_total_orbits(example_map)
    assert total_orbits == 42

    example_map = ['COM)B',
                    'B)C',
                    'C)D',
                    'D)E',
                    'E)F',
                    'B)G',
                    'G)H',
                    'D)I',
                    'E)J',
                    'J)K',
                    'K)L',
                    'K)YOU',
                    'I)SAN']

    assert orbital_transfers_required(example_map) == 4


if __name__ == "__main__":
    INPUT = read(INPUT_FILE)
    tests()
    print("part1")
    print(get_total_orbits(INPUT))
    print("part2")
    print(orbital_transfers_required(INPUT))
