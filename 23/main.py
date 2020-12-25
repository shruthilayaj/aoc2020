from aoc2020.utils.decorators import timer


class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return str(self.data)


@timer
def crab_cups(cups, iterations):
    node_map = {}
    max_ = max(cups)

    first = cups.pop(0)
    node = Node(first)
    node_map[first] = node

    for cup in cups:
        node.next = Node(cup)
        node = node.next
        node_map[cup] = node

    node.next = node_map[first]

    current_node = node_map[first]
    for i in range(iterations):
        label = current_node.data
        three_cups_1 = current_node.next
        three_cups_2 = three_cups_1.next
        three_cups_3 = three_cups_2.next

        current_node.next = three_cups_3.next

        destination_label = label - 1
        while True:
            try:
                destination = node_map[destination_label]
            except KeyError:
                destination_label = max_
                destination = node_map[destination_label]
            if destination != three_cups_1 and destination != three_cups_2 and destination != three_cups_3:
                break
            destination_label -= 1

        destination_end = destination.next
        destination.next = three_cups_1
        three_cups_3.next = destination_end
        current_node = current_node.next

    head = node_map[1]

    return head


if __name__ == "__main__":
    cups = [int(x) for x in list('739862541')]
    head = crab_cups(cups, 100)
    node = head
    str_ = ""
    while True:
        node = node.next
        if node == head:
            break
        str_ += str(node.data)

    print(f"Part 1: {str_}")

    cups = [int(x) for x in list('739862541')] + [x for x in range(10, 1000001)]
    head = crab_cups(cups, 10000000)
    first = head.next.data
    second = head.next.next.data

    print(f"Part 2: {first * second}")
