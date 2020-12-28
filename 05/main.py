import math
import os


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.read()
        data = data.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1")

    return data


def binary_boarding(records):
    seat_ids = []

    for row, column in records:
        row = int(row, 2)
        column = int(column, 2)
        seat_ids.append((row * 8) + column)

    return seat_ids


def binary_boarding_2(seat_ids):
    sorted_seat_ids = [seat_ids.pop()]

    for seat_id in seat_ids:
        lower = 0
        upper = len(sorted_seat_ids)

        while True:
            mid = lower + (upper - lower)/2

            if sorted_seat_ids[math.floor(mid)] < seat_id:
                lower = math.ceil(mid)
            if sorted_seat_ids[math.floor(mid)] > seat_id:
                upper = math.floor(mid)
            if sorted_seat_ids[math.floor(mid)] == seat_id:
                upper = lower = math.floor(mid)

            if lower >= upper:
                sorted_seat_ids.insert(lower, seat_id)
                break

    for i in range(len(sorted_seat_ids)):
        if sorted_seat_ids[i] == (sorted_seat_ids[i + 1] - 2):
            return sorted_seat_ids[i] + 1

    return sorted_seat_ids


if __name__ == "__main__":
    records = read_input().split("\n")
    records = [(rec[:7], rec[7:]) for rec in records]
    seat_ids = binary_boarding(records)

    print(f"Part 1: {max(seat_ids)}")
    print(f"Part 1: {binary_boarding_2(seat_ids)}")
