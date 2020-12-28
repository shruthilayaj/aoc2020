import os


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.read()

    return data


def custom_customs(records):
    final_count = 0

    for group in records:
        group_count = set()
        for record in group.split("\n"):
            group_count = group_count.union(set(record))

        final_count += len(group_count)

    return final_count


def custom_customs_2(records):
    final_count = 0

    for group in records:
        group_records = group.split("\n")
        to_match = set(group_records[0])

        for record in group_records[1:]:
            to_match = to_match.intersection(set(record))

        final_count += len(to_match)

    return final_count


if __name__ == "__main__":
    records = read_input().split("\n\n")

    print(f"Part 1: {custom_customs(records)}")
    print(f"Part 1: {custom_customs_2(records)}")
