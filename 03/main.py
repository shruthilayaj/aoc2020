import os


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.readlines()

    return data


def toboggan_trajectory(topography, slopes):
    """
    f(y) = y/m % width  # m == slope == down/right
    """

    width = len(topography[0])
    total = 1
    for right, down in slopes:
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

    SLOPES_1 = [(3, 1)]
    print(f"Part 1: {toboggan_trajectory(data, SLOPES_1)}")

    SLOPES_2 = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    print(f"Part 2: {toboggan_trajectory(data, SLOPES_2)}")
