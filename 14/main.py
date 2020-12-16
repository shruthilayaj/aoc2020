import functools
import os
import re

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
            floats = mask.replace("1", "0").replace("X", "1")

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

    total = functools.reduce(
        lambda x, y: x + y,
        list(map(lambda v: (v[0] | v[1]) & v[2], mem.values())),
    )

    return total


@timer
def docking_data_2(records):
    mem = {}

    for k, val, ones, zeros, floats in records:
        base = ((k | int(floats, 2)) ^ int(floats, 2)) | ones
        floats = list(floats)
        a = []
        for i, binary in enumerate(floats):
            if binary == "1":
                if len(a) == 0:
                    a = ["0", "1"]
                else:
                    a.extend(a)
                    for i, num in enumerate(a[:]):
                        if i < len(a)/2:
                            a[i] = num + "0"
                        else:
                            a[i] = num + "1"
            else:
                if len(a) == 0:
                    a = ["0"]
                else:
                    a = [x + "0" for x in a]

        for v in a:
            k_ = base | int(v, 2)
            mem[k_] = val

    return sum(mem.values())


if __name__ == "__main__":
    records = _parse_input(read_input())

    print(f"Part 1: {docking_data(records)}")
    print(f"Part 2: {docking_data_2(records)}")
