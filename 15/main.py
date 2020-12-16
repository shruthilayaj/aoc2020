from aoc2020.utils.decorators import timer


@timer
def rambunctious_recitation(records, count):
    tracking_dict = {}
    i = 1
    while len(records) > 1:
        last = records.pop(0)
        tracking_dict[last] = i

        i += 1

    for j in range(i, count):
        if records:
            last = records.pop(0)

        if last in tracking_dict:
            temp = j - tracking_dict[last]
            tracking_dict[last] = j
            last = temp
        else:
            tracking_dict[last] = j
            last = 0

    return last


if __name__ == "__main__":
    input_ = [0, 13, 1, 16, 6, 17]

    print(f"Part 1: {rambunctious_recitation(input_[:], 2020)}")
    print(f"Part 1: {rambunctious_recitation(input_[:], 30000000)}")
