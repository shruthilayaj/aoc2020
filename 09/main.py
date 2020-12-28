import os


class SumNotFound(Exception):
    pass


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.readlines()

    return data


def encoding_error(records):
    sliding_window = records[:25]

    def get_sum(target):
        for i, x in enumerate(sliding_window):
            remainder = target - x
            if remainder in sliding_window[i:]:
                return
        else:
            raise SumNotFound

    for num in records[25:]:
        try:
            get_sum(num)
        except SumNotFound:
            return num
        else:
            sliding_window.pop(0)
            sliding_window.append(num)


def encoding_error_2(target):
    sliding_window = records[:2]

    i = 2
    while True:
        if sum(sliding_window) == target:
            return min(sliding_window) + max(sliding_window)
        if sum(sliding_window) < target:
            sliding_window.append(records[i])
            i += 1
        elif sum(sliding_window) > target:
            sliding_window.pop(0)


if __name__ == "__main__":
    records = [int(x) for x in read_input()]

    target = encoding_error(records)
    print(f"Part 1: {target}")
    print(f"Part 2: {encoding_error_2(target)}")
