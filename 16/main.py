import os
import re


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.readlines()

    return data


def _parse_input(data):
    rules = {}
    records = []

    is_my_ticket = False
    my_ticket = None

    for line in data:
        match = re.match(r"(.*): (\d*)-(\d*) or (\d*)-(\d*)", line)
        if match:
            rules[match.group(1)] = [
                (int(match.group(2)), int(match.group(3))),
                (int(match.group(4)), int(match.group(5))),
            ]
            continue

        if re.match("your ticket:", line):
            is_my_ticket = True
            continue

        record = re.findall("(\d{1,}),{0,1}", line)
        if not record:
            continue

        record = [int(x) for x in record]
        if is_my_ticket:
            is_my_ticket = False
            my_ticket = record
        else:
            records.append(record)

    return rules, my_ticket, records


def ticket_translation(rules, records):
    def is_valid(num):
        is_valid = False
        for _, ranges in rules.items():
            for lower_, upper_ in ranges:
                is_valid |= lower_ <= num <= upper_
                if is_valid:
                    return 0
        return num

    total = sum([is_valid(num) for record in records for num in record])

    return total


def ticket_translation_2(rules, my_ticket, records):
    index_map = {}
    final_index = {}

    def get_rule(num):
        possible_match = []
        for rule, ranges in rules.items():
            for lower_, upper_ in ranges:
                if lower_ <= num <= upper_ and rule not in final_index.values():
                    possible_match.append(rule)
                    continue

        return possible_match

    while True:
        for record in records:
            for i, num in enumerate(record):
                if i in final_index:
                    continue
                rules_ = get_rule(num)
                if rules_:
                    if i in index_map:
                        index_map[i] = index_map[i].intersection(set(rules_))
                    else:
                        index_map[i] = set(rules_)
                    if len(index_map[i]) == 1:
                        final_index[i] = list(index_map[i])[0]

        if len(final_index) == len(rules):
            break

    total = 1
    for i, rule in final_index.items():
        if "departure" in rule:
            total *= my_ticket[i]

    return total


if __name__ == "__main__":
    rules, my_ticket, records = _parse_input(read_input())
    print(ticket_translation(rules, records))
    print(ticket_translation_2(rules, my_ticket, records))
