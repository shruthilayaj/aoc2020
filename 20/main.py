import math
import os
import re


class Tile(object):
    def __init__(self, id, grid):
        self.id = int(id)
        self.grid = grid
        self.orientation = 0

    def __repr__(self):
        return f"{self.id}"

    @property
    def top(self):
        return self.grid[0]

    @property
    def bottom(self):
        return self.grid[-1]

    @property
    def left(self):
        return [line[0] for line in self.grid]

    @property
    def right(self):
        return [line[-1] for line in self.grid]

    @property
    def possible_edges(self):
        return [
            self.top,
            self.top[::-1],
            self.right,
            self.right[::-1],
            self.bottom,
            self.bottom[::-1],
            self.left,
            self.left[::-1],
        ]

    @property
    def edges(self):
        return [
            self.top,
            self.right,
            self.bottom,
            self.left,
        ]

    def rotate(self):
        if self.orientation == 3 or self.orientation == 7:
            flipped = [self.grid[len(self.grid)-i-1] for i in range(len(self.grid))]
            self.grid = flipped
            self.orientation = (self.orientation + 1) % 8

            return

        rotated = [list(reversed(col)) for col in zip(*self.grid)]
        self.grid = rotated
        self.orientation = (self.orientation + 1) % 8

    def stringify(self):
        string = ""
        for line in self.grid:
            string += "".join(line)
            string += "\n"

        return string


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.read()

    return data.split("\n\n")


def _parse_tiles(records):
    tiles = []
    for tile in records:
        lines = tile.split("\n")
        title = lines.pop(0)
        m = re.match(r"Tile (\d+):", title)
        id_ = m.group(1)
        tile_lines = [list(line) for line in lines]
        tiles.append(Tile(id_, tile_lines))

    return tiles


def jurassic_jigsaw(tiles):
    dim = int(math.sqrt(len(tiles)))
    grid = [[0] * dim for _ in range(dim)]

    all_edges = [edge for tile in tiles for edge in tile.edges]

    # Get a signle corner tile
    for tile in tiles:
        unique_edges = []
        for edge in tile.edges:
            if all_edges.count(edge) + all_edges.count(edge[::-1]) == 1:
                unique_edges.append(edge)

        if len(unique_edges) == 2:
            corner_tile = tile
            tiles.remove(tile)
            break

    while True:
        if all([
            corner_tile.left == unique_edges[0] or corner_tile.left == unique_edges[0][::-1],
            corner_tile.top == unique_edges[1] or corner_tile.top == unique_edges[1][::-1],
        ]):
            break

        corner_tile.rotate()

    for row in range(dim):
        for col in range(dim):
            if row == 0 and col == 0:
                grid[row][col] = corner_tile
                continue

            if col == 0:
                adjacent_tile = grid[row - 1][col]
                adjacent_edge = adjacent_tile.bottom
                attr_ = "top"

            else:
                adjacent_tile = grid[row][col - 1]
                adjacent_edge = adjacent_tile.right
                attr_ = "left"

            for tile in tiles:
                if adjacent_edge not in tile.possible_edges:
                    continue

                while True:
                    if getattr(tile, attr_) == adjacent_edge:
                        break
                    tile.rotate()

                grid[row][col] = tile
                tiles.remove(tile)
                break

    prod = grid[0][0].id * grid[0][dim-1].id * grid[dim -1][dim-1].id * grid[dim-1][0].id
    print(f"Part 1: {prod}")

    # Stich grid
    image = ""
    for i in range(dim):
        for n in range(len(tile.top)):
            if n == 0 or n == len(tile.top) - 1:
                continue
            for section in grid[i]:
                lines = section.grid
                image += "".join(lines[n][1:9])
            image += "\n"

    total_hash = image.count("#")
    image = image.strip("\n").split("\n")

    def _rotate(lines):
        pre_rotated = [list(x) for x in lines]
        rotated = [list(reversed(col)) for col in zip(*pre_rotated)]
        rotated = ["".join(r) for r in rotated]

        return rotated

    def _flip(lines):
        pre_flipped = [list(x) for x in lines]
        flipped = [pre_flipped[len(pre_flipped)-i-1] for i in range(len(pre_flipped))]
        flipped = ["".join(f) for f in flipped]

        return flipped

    monsters = 0
    orientation = 0

    while monsters == 0:
        for line_num, line in enumerate(image):
            if line_num == 0:
                continue
            if line_num == len(image) - 1:
                continue
            i = 0
            while i <= len(line):
                try:
                    line[i + 19]
                except IndexError:
                    break
                if all([
                    line[i] == "#",
                    line[i + 5] == "#",
                    line[i + 6] == "#",
                    line[i + 11] == "#",
                    line[i + 12] == "#",
                    line[i + 17] == "#",
                    line[i + 18] == "#",
                    line[i + 19] == "#",
                ]):
                    if all([
                        image[line_num + 1][i + 1] == "#",
                        image[line_num + 1][i + 4] == "#",
                        image[line_num + 1][i + 7] == "#",
                        image[line_num + 1][i + 10] == "#",
                        image[line_num + 1][i + 13] == "#",
                        image[line_num + 1][i + 16] == "#",
                    ]):
                        if image[line_num - 1][i + 18] == "#":
                            monsters += 1
                            i += 19

                i += 1

        image = _rotate(image)
        orientation += 1
        if orientation == 4:
            image = _flip(image)

    print(f"Part 2: {total_hash - monsters * 15}")


if __name__ == "__main__":
    tiles = _parse_tiles(read_input())
    jurassic_jigsaw(tiles)
