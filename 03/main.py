import os


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.readlines()

    return data


def toboggan_trajectory(topography):
    """
    0 -> 0
    1 -> 2
    2 -> 5
    3 -> 8

    f(y) = y/m % 11  # m == slope == 1/3
    """
    trees = 0
    width = len(topography[0])

    for y, line in enumerate(topography):
        x = ((3 * y) % width)
        if line[x] == "#":
            trees += 1

    return trees


def toboggan_trajectory_2(topography):
    """
    f(y) = y/m % width  # m == slope == down/right
    """
    SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    width = len(topography[0])
    total = 1
    for right, down in SLOPES:
        y = 0
        trees = 0
        while y < len(topography):
            x = int((right/down * y) % width)
            if topography[y][x] == "#":
                trees += 1
            y += down
        
        total *= trees

    return total


if __name__ == "__main__":
    data = [list(x.strip("\n")) for x in read_input()]
    print(f"Part 1: {toboggan_trajectory(data)}")
    print(f"Part 2: {toboggan_trajectory_2(data)}")
