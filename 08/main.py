import os
import re


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.readlines()

    return data


def _parse_input(records):
    parsed = []
    for record in records:
        match = re.match("(nop|acc|jmp) ((\+|-)\d*)", record)
        parsed.append((match.group(1), int(match.group(2))))
    
    return parsed


def handheld_halting(records):
    traversed_indexes = []
    current_index = 0
    accumulator = 0

    while True:
        if current_index in traversed_indexes:
            return accumulator

        traversed_indexes.append(current_index)
        op, arg = records[current_index]
        if op == "nop":
            current_index += 1
        elif op == "acc":
            accumulator += arg
            current_index += 1
        else:
            current_index += arg


def handheld_halting_2(records):
    # Tracking the indexes of no-op/jmp operations that have been
    # switched in the while loop so they are not flipped again as we
    # follow the ops.
    changed_indexes = []
    while True:
        has_changed = False
        current_index = 0
        accumulator = 0
        traversed_indexes = []
        while True:
            if current_index in traversed_indexes:
                # Breaking if it hits the infinite loop and tries changing the next
                # jmp or no-op opeator it will traverse.
                break

            traversed_indexes.append(current_index)
            try:
                op, arg = records[current_index]
            # Index Error implies the list of ops have been traversed
            except IndexError:
                return accumulator

            can_change = (not has_changed) and (current_index not in changed_indexes)
            if op == "nop":
                if can_change and op != 0:
                    has_changed = True
                    changed_indexes.append(current_index)

                    current_index += arg  # This is the jmp operation
                else:
                    current_index += 1

            elif op == "jmp":
                if can_change:
                    has_changed = True
                    changed_indexes.append(current_index)

                    current_index += 1  # This is the no-op
                else:
                    current_index += arg

            else:
                accumulator += arg
                current_index += 1


if __name__ == "__main__":
    records = _parse_input(read_input())

    print(f"Part 1: {handheld_halting(records)}")
    print(f"Part 2: {handheld_halting_2(records)}")

