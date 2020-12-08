import os
import re


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.readlines()

    return data


def _parse_input(records):
    parsed = {}
    for record in records:
        parent, children = record.split("contain")
        parent = re.match("(.*) bags", parent).group(1)
        children = re.findall(" {0,}(\d*|no) (.*?) bag", children)
        parsed[parent] = {x1: x0 for x0, x1 in children}
    
    return parsed


def handy_haversack(records, search_for):
    """

    """
    new_search = []
    to_pop = []
    count=0
    for parent, children in records.items():
        if any(key in children for key in search_for):
            count += 1
            to_pop.append(parent)
            new_search.append(parent)

    [records.pop(k) for k in to_pop]

    if len(new_search) == 0:
        return count
    else:
        count += handy_haversack(records, new_search) 
        return count
    

def handy_haversack_2(records, search_through):
    count = 0
    while True:
        try:
            bag, num = search_through.pop()
        except IndexError:
            break

        for nested_bag, n in records[bag].items():
            if nested_bag != "other":
                search_through.append((nested_bag, int(n)*int(num)))
                count += int(n) * num

    return count


if __name__ == "__main__":
    records = _parse_input(read_input())

    total = handy_haversack(records, ["shiny gold"])
    print(f"Part 1: {total}")
    total = handy_haversack_2(records, [("shiny gold", 1)])
    print(f"Part 2: {total}")
