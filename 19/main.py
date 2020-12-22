import os


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.read()

    return data.split("\n\n")


def _parse_rules(rules):
    rules = rules.split("\n")
    new_rules = {}

    for rule in rules:
        k, values = rule.split(":")
        new_rules.setdefault(k, [])
        values = values.strip().split("|")
        for value in values:
            value = value.strip(" \"").split(" ")
            new_rules[k].append(value)

    return new_rules


def monster_messages_2(rules, keys_super):
    """
    0: 4 1 5
    1: 2 3 | 3 2
    2: 4 4 | 5 5
    3: 4 5 | 5 4
    4: "a"
    5: "b"

    [[4 1 5]]
    [[1 5]] - > [["a"]]

    [[2 3 5], [3 2 5]] -> ["a", "a"]

    [[4 4 3 5], [5 5 3 5], [3 2 5]] -> [["a"], ["a"], ["a"]]
    [[4 3 5], [5 5 3 5], [3 2 5]] -> [["aa"], ["a"], ["a"]]
    [[3 5], [5 5 3 5], [3 2 5]] -> [["aaa"], ["a"], ["a"]]
    """
    allowed_strings = []
    allowed_strings_super = []

    while keys_super:
        keys = keys_super.pop(0)
        while True:
            try:
                key = keys.pop(0)
            except IndexError:
                s = allowed_strings.pop(0)
                allowed_strings_super.append(s)
                break

            values = rules[key]

            if values[0][0] in ["a", "b"]:
                if len(allowed_strings) == 0:
                    allowed_strings = [values[0][0]]
                else:
                    allowed_strings[0] = allowed_strings[0] + values[0][0]
                continue

            split_keys = []
            for i, split in enumerate(values):
                split_keys.append(split + keys)

            keys_super = split_keys + keys_super

            if i > 0:
                if len(allowed_strings) == 0:
                    allowed_string_to_replicate = ""
                else:
                    allowed_string_to_replicate = allowed_strings[0]
                allowed_strings = [allowed_string_to_replicate for _ in range(i)] + allowed_strings

            break

    return allowed_strings_super


if __name__ == "__main__":
    rules, messages = read_input()
    rules = _parse_rules(rules)
    messages = messages.split("\n")
    valid = monster_messages_2(rules, [["0"]])
    valid_sum = sum([1 for x in messages if x in valid])
    print(f"Part 1: {valid_sum}")
    valid_31 = monster_messages_2(rules, [["31"]])
    valid_42 = monster_messages_2(rules, [["42"]])
    chunk_size = len(valid_42[0])

    count = 0
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    # 0: 8 11
    # This implies that 0: x*42 y*31. So just needed my chunks to match
    # valid 42, and when they stop matching 42, start matching 31 to be
    # valid. 0 < y < x.
    for message in messages:
        if len(message) % chunk_size:
            continue
        x, y = 0, 0
        is_forty_two = True
        match = True

        chunks = [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]
        for chunk in chunks:
            if is_forty_two:
                if chunk not in valid_42:
                    is_forty_two = False
                else:
                    x += 1

            if not is_forty_two:
                if chunk not in valid_31:
                    match = False
                    break
                else:
                    y += 1

            if y > x - 1:
                match = False
                break

        if match and y > 0:
            count += 1

    print("Part 2: ", count)
