import os
import re
from itertools import product

from aoc2020.utils.decorators import timer


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.readlines()

    return data


def _parse_input(records):
    data = []

    for line in records:
        match = re.match("mask = ([01X]{36})", line)
        if match:
            mask = match.group(1)
            ones = int(mask.replace("X", "0"), 2)
            zeros = int(mask.replace("X", "1"), 2)
            # floats = mask.replace("1", "0").replace("X", "1")
            floats = mask

            continue

        match = re.match(r"mem\[(\d*)\] = (\d*)", line)
        mem_address, value = match.group(1), match.group(2)

        data.append((int(mem_address), int(value), ones, zeros, floats))

    return data


@timer
def docking_data(records):
    mem = {}
    for key, value, ones, zeros, _ in records:
        mem[key] = (value, ones, zeros)

    total = sum(map(lambda v: (v[0] | v[1]) & v[2], mem.values()))

    return total


@timer
def docking_data_2(records):
    mem = {}

    for k, val, _, _, floats in records:
        num_float = floats.count("X")
        base = (k | int(floats.replace("X", "0"), 2))
        permuations = list(product(["0", "1"], repeat=num_float))
        for p in permuations:
            new_bin = ""
            count = 0
            for i, char in enumerate(f"{base:036b}"):
                if floats[i] == "X":
                    new_bin += p[count]
                    count += 1
                else:
                    new_bin += char

            mem[new_bin] = val

    return sum(mem.values())


if __name__ == "__main__":
    records = _parse_input(read_input())

    print(f"Part 1: {docking_data(records)}")
    print(f"Part 2: {docking_data_2(records)}")
