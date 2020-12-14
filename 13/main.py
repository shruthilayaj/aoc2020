import collections
import math
import os
import re


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.readlines()

    return data


def shuttle_search(earliest_time, available_buses):
    bus = available_buses[0]
    min_time = int(math.floor(earliest_time/bus) * bus) + bus

    for b in available_buses[1:]:
        next_scheduled = int(math.floor(earliest_time/b) * b) + b

        if next_scheduled < min_time:
            min_time = next_scheduled
            bus = b
    
    return bus * (min_time - earliest_time)


def shuttle_search_2(available_buses):
    increment = available_buses.pop(0)
    timestamp = increment

    while True:
        is_match = True

        for offset, bus in enumerate(available_buses, start=1):
            if bus == "x":
                continue
            while True:
                if (timestamp + offset) % bus:
                    timestamp += increment
                    is_match = False
                else:
                    # Had to peek at https://www.reddit.com/r/adventofcode/comments/kc4njx/2020_day_13_solutions/
                    # to get this beautiful line of code.
                    increment *= bus
                    break
        
        if is_match == True:
            break

    return timestamp



if __name__ == "__main__":
    records = read_input()
    earliest_time = int(records[0])
    available_buses = [int(m) for m in re.findall("(\d{1,})", records[1])]

    print(f"Part 1: {shuttle_search(earliest_time, available_buses)}")

    buses = [int(m) if m != "x" else m for m in re.findall("(\d{1,}|x)", records[1])]
    print(f"Part 2: {shuttle_search_2(buses)}")
