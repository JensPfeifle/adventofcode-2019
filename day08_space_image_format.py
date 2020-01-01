from typing import List
import matplotlib.pyplot as plt
import numpy as np

INPUT_FILE = "day08.inp"


def read(filename, split_on="\n", cast_func=None):
    """ Read and clean up input file """
    with open(filename, "r") as f:
        inpt = f.read().strip().split(split_on)
    if cast_func:
        return list(map(cast_func, inpt))
    return inpt


def decode(data, width, height):
    ppl = width * height  # pixels per layer
    num_layers = int(len(data) / ppl)
    layers = []
    for n in range(num_layers):
        layers.append(list(map(int, data[ppl * n : ppl * (n + 1)])))
    return tuple(layers)


def stack_pixel(layers):
    "determine pixel color from layers for that pixel"
    for layer in layers:
        if layer == 0:
            return 0
        elif layer == 1:
            return 1
        elif layer == 2:
            # transparent
            pass


def count_digits(layers: List[List[int]]):
    counts = [{} for _ in range(len(layers))]
    for n, layer in enumerate(layers):
        for i in range(10):
            counts[n][i] = layer.count(i)
    return counts


def decode_and_stack(data, width, height):
    final_image = []
    layers = decode(data, width, height)
    pixel_layers = list(zip((*layers)))
    for pixel_layer in pixel_layers:
        final_image.append(stack_pixel(pixel_layer))
    return final_image


def tests():
    data = "123456789012"
    layers = decode(data, width=3, height=2)
    num_zeros = [layer.count(0) for layer in layers]
    layer_with_min_zeros = layers[num_zeros.index(min(num_zeros))]

    assert stack_pixel([0, 1, 2, 0]) == 0
    assert stack_pixel([2, 1, 2, 0]) == 1
    assert stack_pixel([2, 2, 1, 0]) == 1
    assert stack_pixel([2, 2, 2, 0]) == 0

    data = "0222112222120000"
    assert decode_and_stack(data, width=2, height=2) == [0, 1, 1, 0]

    print("tests passed")


if __name__ == "__main__":
    INPUT = read(INPUT_FILE, split_on=",", cast_func=None)[0]
    tests()
    print("part1")
    layers = decode(INPUT, width=25, height=6)
    num_zeros = [layer.count(0) for layer in layers]
    layer_with_min_zeros = layers[num_zeros.index(min(num_zeros))]
    print(layer_with_min_zeros.count(1) * layer_with_min_zeros.count(2))
    print("part2")
    final_image = decode_and_stack(INPUT, width=25, height=6)
    img = np.array(final_image)
    img.resize(6, 25)
    plt.imshow(img)
    plt.show()
