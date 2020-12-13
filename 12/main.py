from math import sin, cos, radians
import os
import re

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.readlines()

    records = []
    for line in data:
        m = re.match("(N|E|W|S|F|L|R)(\d*)", line)
        records.append((m.group(1), int(m.group(2))))

    return records


def rain_risk(records):
    bearing = 90
    x = 0
    y = 0

    coordinate = (x, y, bearing)
    traversed_coordinates = [coordinate]

    func = {
        "N": lambda c, v: (c[0], c[1] + v, c[2]),
        "S": lambda c, v: (c[0], c[1] - v, c[2]),
        "E": lambda c, v: (c[0] + v, c[1], c[2]),
        "W": lambda c, v: (c[0] - v, c[1], c[2]),
        "R": lambda c, v: (c[0], c[1], (c[2] + v) % 360),
        "L": lambda c, v: (c[0], c[1], (c[2] - v) % 360),
        "F": lambda c, v: (c[0] + int(sin(radians(c[2]))) * v, c[1] + int(cos(radians(c[2]))) * v, c[2]),
    }

    for action, magnitude in records:
        coordinate = func[action](coordinate, magnitude)
        traversed_coordinates.append(coordinate)

    x = [c[0] for c in traversed_coordinates]
    y = [c[1] for c in traversed_coordinates]

    fig = plt.figure()
    plt.xlim(min(x) - 5, max(x) + 5)
    plt.ylim(min(y) - 5, max(y) + 5)

    graph, = plt.plot([], [])

    def animate(i):
        graph.set_data(x[:i+1], y[:i+1])
        return graph

    ani = FuncAnimation(fig, animate, repeat=False, interval=200)
    plt.show()
    
    return abs(coordinate[0]) + abs(coordinate[1])


def rain_risk_2(records):
    waypoint_coordinates = (10, 1)
    ship_coordinates = (0, 0)

    func = {
        "N": lambda c, w, v: (c, (w[0], w[1] + v)),
        "S": lambda c, w, v: (c, (w[0], w[1] - v)),
        "E": lambda c, w, v: (c, (w[0] + v, w[1])),
        "W": lambda c, w, v: (c, (w[0] - v, w[1])),
        "R": lambda c, w, v: (c, (w[0] * int(cos(radians(v))) + w[1] * int(sin(radians(v))), w[1] * int(cos(radians(v))) - w[0] * int(sin(radians(v))))),
        "L": lambda c, w, v: (c, (w[0] * int(cos(radians(v))) - w[1] * int(sin(radians(v))), w[0] * int(sin(radians(v))) + w[1] * int(cos(radians(v))))),
        "F": lambda c, w, v: ((c[0] + v * w[0], c[1] + v* w[1]), w),
    }

    for action, magnitude in records:
        ship_coordinates, waypoint_coordinates = func[action](ship_coordinates, waypoint_coordinates, magnitude)
    
    return abs(ship_coordinates[0]) + abs(ship_coordinates[1])


if __name__ == "__main__":
    records = read_input()
    print(f"Part 1: {rain_risk(records)}")
    print(f"Part 2: {rain_risk_2(records)}")
