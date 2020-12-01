import os


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.readlines()

    return data


def report_repair(data):
    for x in data:
        remainder = 2020 - x
        if remainder in data:
            return x * remainder


def report_repair_2(data):
    for i, num_1 in enumerate(data):
        for j, num_2 in enumerate(data[i + 1:]):
            remainder = 2020 - (num_1 + num_2)
            if remainder in data[i + j + 2:]:
                return num_1 * num_2 * remainder


if __name__ == "__main__":
    data = [int(v) for v in read_input()]
    print(f"Part 1: {report_repair(data)}")
    print(f"Part 2: {report_repair_2(data)}")
