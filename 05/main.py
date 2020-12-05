import math
import os


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.readlines()

    return data


def binary_boarding(records):
    seat_ids = []

    for record in records:
        lower = 0
        upper = 127

        for char in record[:7]:
            mid = lower + (upper - lower)/2
            if char == "F":
                upper = math.floor(mid)

            if char == "B":
                lower = math.ceil(mid)

        left = 0
        right = 7
        for char in record[7:]:
            mid = left + (right - left)/2
            if char == "L":
                right = math.floor(mid)
            if char == "R":
                left = math.ceil(mid)

        seat_id = (lower * 8) + left
        seat_ids.append(seat_id)

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
    records = [l.strip("\n") for l in read_input()]
    seat_ids = binary_boarding(records)

    print(f"Part 1: {max(seat_ids)}")
    print(f"Part 1: {binary_boarding_2(seat_ids)}")
