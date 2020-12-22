import os
from copy import deepcopy


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.read()
        data = data.split("\n")
        data = [list(r) for r in data]

    return data


def seating_system(records):
    occupied = 0
    while True:
        records_ = deepcopy(records)
        for i, row in enumerate(records_):
            for j, seat in enumerate(row):
                if seat == ".":
                    continue
                filled_count = 0
                relative_coordinates = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
                for i_, j_ in relative_coordinates:
                    if i + i_ < 0 or j + j_ < 0:
                        continue
                    try:
                        adj_seat = records_[i + i_][j + j_]
                    except IndexError:
                        continue
                    if adj_seat == "#":
                        filled_count += 1

                if seat == "L" and filled_count == 0:
                    records[i][j] = "#"
                    occupied += 1
                elif seat == "#" and filled_count >= 4:
                    records[i][j] = "L"
                    occupied -= 1

        if records == records_:
            break
                
    return occupied


def seating_system_2(records):
    occupied = 0
    while True:
        records_ = deepcopy(records)
        for i, row in enumerate(records_):
            for j, seat in enumerate(row):
                if seat == ".":
                    continue

                filled_count = 0
                relative_coordinates = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

                while len(relative_coordinates) > 0:
                    i_, j_ = relative_coordinates.pop(0)
                    if i + i_ < 0 or j + j_ < 0:
                        continue
                    try:
                        adj_seat = records_[i + i_][j + j_]
                    except IndexError:
                        continue

                    if adj_seat == "#":
                        filled_count += 1

                    elif adj_seat == ".":
                        if i_ == 0:
                            new_x = 0
                        elif i_ > 0:
                            new_x = i_ + 1
                        else:
                            new_x = i_ - 1

                        if j_ == 0:
                            new_y = 0
                        elif j_ > 0:
                            new_y = j_ + 1
                        else:
                            new_y = j_ - 1

                        relative_coordinates.append((new_x, new_y))

                if seat == "L" and filled_count == 0:
                    records[i][j] = "#"
                    occupied += 1
                elif seat == "#" and filled_count >= 5:
                    records[i][j] = "L"
                    occupied -= 1

        if records == records_:
            break
                
    return occupied


if __name__ == "__main__":
    records = read_input()
    print(f"Part 1: {seating_system(read_input())}")
    print(f"Part 2: {seating_system_2(read_input())}")
