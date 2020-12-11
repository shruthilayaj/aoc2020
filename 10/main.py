import os


class InvalidJoltage(Exception):
    pass


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.readlines()

    return data


def adapter_array(records):
    jolt_diff = {3: 0, 2: 0, 1: 0}
    current_joltage = 0


    for j in sorted(records):
        try:
            jolt_diff[j - current_joltage] += 1
        except KeyError:
            raise InvalidJoltage

        current_joltage = j

    return jolt_diff[3] * jolt_diff[1]


def adapter_array_2(records):
    records = sorted(records)
    permutations_dict = {0: 1}
    records.insert(0, 0)

    for record in records:
        for j in range(1, 4):
            if record + j in records:
                paths_from_record += 1
                permutations_dict[record + j] = permutations_dict[record] + permutations_dict.get(record + j, 0)
    
    return permutations_dict[max(records)]



if __name__ == "__main__":
    records = [int(x) for x in read_input()]
    records.append(max(records) + 3)  # Adding the connection to the device

    print(f"Part 1: {adapter_array(records)}")
    print(f"Part 2: {adapter_array_2(records)}")
