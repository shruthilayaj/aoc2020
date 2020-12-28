import os
import re


class Node(object):
    def __init__(self, data):
        self.data = data
        self.contains = []
        self.contained_in = []

    def __repr__(self):
        return self.data


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.readlines()

    return data


def _parse_input(records):
    parsed = {}
    for record in records:
        parent, children = record.split("contain")
        parent = re.match(r"(.*) bags", parent).group(1)
        children = re.findall(r" {0,}(\d*|no) (.*?) bag", children)

        try:
            bag = parsed[parent]
        except KeyError:
            bag = Node(parent)

        parsed[parent] = bag
        for num, child in children:
            try:
                child_ = parsed[child]
            except KeyError:
                child_ = Node(child)

            child_.contained_in.append(bag)
            parsed[child] = child_

            if num != "no":
                bag.contains.append((child_, int(num)))

    return parsed


def handy_haversack(head):
    allowed_bags = set()
    search = [head]

    while search:
        bag = search.pop()
        allowed_bags = allowed_bags.union(set(bag.contained_in))
        search.extend(bag.contained_in)

    return len(allowed_bags)


def handy_haversack_2_linked(bag):
    count = 1
    if not bag.contains:
        return count

    for child, num in bag.contains:
        count += num * handy_haversack_2_linked(child)

    return count


if __name__ == "__main__":
    records = _parse_input(read_input())

    print(f"Part 1: {handy_haversack(records['shiny gold'])}")
    print(f"Part 2: {handy_haversack_2_linked(records['shiny gold']) - 1}")
