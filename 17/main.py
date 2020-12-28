import os
from copy import deepcopy

from aoc2020.utils.decorators import timer


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.read()
        data = data.replace(".", "0")
        data = data.replace("#", "1")
        data = data.split("\n")
        data = [list(map(int, r)) for r in data]

    return data


def conway_cubes(records, cycles):
    total = sum([sum(rec) for rec in records])
    records = [records]
    relative_coordinates = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (0, 0)]
    i = 0

    while i < cycles:
        records = (
            [[[0]*len(records[0][0]) for _ in range(len(records[0]))]] +
            records +
            [[[0]*len(records[0][0]) for _ in range(len(records[0]))]]
        )
        for j, plane in enumerate(records):
            plane.insert(0, [0]*len(plane[0]))
            plane.append([0]*len(plane[0]))
            for y in plane:
                y.insert(0, 0)
                y.append(0)

        records_ = deepcopy(records)

        for z, plane in enumerate(records_):
            for y, row in enumerate(plane):
                for x, cube in enumerate(row):
                    active_count = 0
                    for dz in (-1, 0, 1):
                        for dx, dy in relative_coordinates:
                            z_, y_, x_ = z + dz, y + dy, x + dx
                            if any([z_ < 0, y_ < 0, x_ < 0]):
                                continue
                            if all([dz == 0, dy == 0, dx == 0]):
                                continue
                            try:
                                val = records_[z_][y_][x_]
                            except IndexError:
                                continue
                            active_count += val

                    if cube and (active_count != 2 and active_count != 3):
                        total -= 1
                        records[z][y][x] = 0
                    elif not cube and active_count == 3:
                        total += 1
                        records[z][y][x] = 1

        i += 1

    return total


@timer
def conway_cubes_2(records, cycles):
    total = sum([sum(rec) for rec in records])
    records = [[records]]
    relative_coordinates = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (0, 0)]
    i = 0

    while i < cycles:
        records = (
            records +
            [[[[0]*len(records[0][0][0]) for _ in range(len(records[0][0]))] for _ in range(len(records[0]))]]
        )
        for _, three_d in enumerate(records):
            three_d.insert(0, [[0]*len(records[0][0][0]) for _ in range(len(records[0][0]))])
            three_d.append([[0]*len(records[0][0][0]) for _ in range(len(records[0][0]))])
            for j, plane in enumerate(three_d):
                plane.insert(0, [0]*len(plane[0]))
                plane.append([0]*len(plane[0]))
                for y in plane:
                    y.insert(0, 0)
                    y.append(0)

        records_ = deepcopy(records)

        for w, three_d in enumerate(records_):
            for z, plane in enumerate(three_d):
                for y, row in enumerate(plane):
                    for x, cube in enumerate(row):
                        active_count = 0
                        for dw in (-1, 0, 1):
                            for dz in (-1, 0, 1):
                                for dx, dy in relative_coordinates:
                                    w_, z_, y_, x_ = w + dw, z + dz, y + dy, x + dx
                                    if any([w_<0, z_ < 0, y_ < 0, x_ < 0]):
                                        continue
                                    if all([dw == 0, dz == 0, dy == 0, dx == 0]):
                                        continue
                                    try:
                                        val = records_[w_][z_][y_][x_]
                                    except IndexError:
                                        continue
                                    active_count += val
                                    if w == 0 and w_ == 1:
                                        active_count += val

                        if cube and (active_count != 2 and active_count != 3):
                            total -= 1
                            if w > 0:
                                total -= 1
                            records[w][z][y][x] = 0
                        elif not cube and active_count == 3:
                            total += 1
                            if w > 0:
                                total += 1
                            records[w][z][y][x] = 1

        i += 1

    return total


if __name__ == "__main__":
    records = read_input()
    print(conway_cubes(deepcopy(records), 6))
    print(conway_cubes_2(deepcopy(records), 6))
