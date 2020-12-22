import math
import os
import re
from copy import deepcopy


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.read()

    return data.split("\n\n")


def _parse_tiles(records):
    tiles = {}
    tiles_full = {}
    for tile in records:
        lines = tile.split("\n")
        left = ""
        right = ""
        tile_all_lines = []
        for i, line in enumerate(lines):
            m = re.match(r"Tile (\d+):", line)
            if m:
                id_ = m.group(1)
                continue
            if i == 1:
                top = line
            bottom = line
            left += line[0]
            right += line[-1]
            tile_all_lines.append(list(line))

        tiles[id_] = [top, right, bottom, left]
        tiles_full[id_] = tile_all_lines

    return tiles, tiles_full


def _rotate(tile, tile_full):
    top, right, bottom, left = tile
    tile = [left[::-1], top, right[::-1], bottom]

    rotated = [list(reversed(col)) for col in zip(*tile_full)]

    return tile, rotated


def _flip(tile, tile_full):
    top, right, bottom, left = tile
    tile = [bottom, right[::-1], top, left[::-1]]

    flipped = [tile_full[len(tile_full)-i-1] for i in range(len(tile_full))]

    return tile, flipped


def find_corners(tiles, tiles_full):
    tiles_ = deepcopy(tiles)
    dim = int(math.sqrt(len(tiles)))
    grid = [[0] * dim for _ in range(dim)]
    flattened = [v for key in tiles for v in tiles[key]]
    corner_ids = {}
    edge_ids = {}
    for id_, tile in tiles.items():
        unique_edges = []
        for edge in tile:
            count = flattened.count(edge)
            count += flattened.count(edge[::-1])
            if count == 1:
                unique_edges.append(edge)

        if len(unique_edges) == 2:
            corner_ids[id_] = unique_edges
            edge_ids[id_] = unique_edges

        if len(unique_edges) == 1:
            edge_ids[id_] = unique_edges

    first = list(corner_ids.keys())[0]
    tiles_.pop(first)
    unique_edges = corner_ids[first]
    edge_ids.pop(first)
    match = False
    for _ in range(4):
        tile = tiles[first]
        tile_full = tiles_full[first]
        if tile[3] != unique_edges[0]:
            tile, tile_full = _rotate(tile, tile_full)
            tiles[first] = tile
            tiles_full[first] = tile_full
        else:
            grid[0][0] = first
            match = True
            break
    if not match:
        tile, tile_full = _flip(tile, tile_full)
        tiles[first] = tile
        tiles_full[first] = tile_full
        for _ in range(4):
            tile = tiles[first]
            tile_full = tiles_full[first]
            if tile[3] != unique_edges[0]:
                tile, tile_full = _rotate(tile, tile_full)
                tiles[first] = tile
                tiles_full[first] = tile_full
            else:
                grid[0][0] = first
                match = True
                break

    x = 0
    y = 0
    diagonal = 0
    while dim > 0:
        for i in range(0, dim):
            if grid[x][y + i] != 0:
                continue

            left_tile_id = grid[x][y + i - 1]
            left_tile = tiles[left_tile_id]

            left_tile_right_edge = left_tile[1]

            keys = tiles_.keys()
            for edge_tile_id in keys:
                match = False
                edge_tile = tiles[edge_tile_id]
                edge_full_tile = tiles_full[edge_tile_id]
                if not any([
                    left_tile_right_edge in edge_tile,
                    left_tile_right_edge[::-1] in edge_tile,
                ]):
                    continue
                for _ in range(4):
                    edge_tile = tiles[edge_tile_id]
                    edge_full_tile = tiles_full[edge_tile_id]
                    if edge_tile[3] != left_tile_right_edge:
                        edge_tile, edge_full_tile = _rotate(edge_tile, edge_full_tile)
                        tiles[edge_tile_id] = edge_tile
                        tiles_full[edge_tile_id] = edge_full_tile
                    else:
                        grid[x][y + i] = edge_tile_id
                        tiles_.pop(edge_tile_id)
                        match = True
                        break
                if not match:
                    edge_tile = tiles[edge_tile_id]
                    edge_full_tile = tiles_full[edge_tile_id]
                    edge_tile, edge_full_tile = _flip(edge_tile, edge_full_tile)
                    tiles[edge_tile_id] = edge_tile
                    tiles_full[edge_tile_id] = edge_full_tile
                    for _ in range(4):
                        edge_tile = tiles[edge_tile_id]
                        edge_full_tile = tiles_full[edge_tile_id]
                        if edge_tile[3] != left_tile_right_edge:
                            edge_tile, edge_full_tile = _rotate(edge_tile, edge_full_tile)
                            tiles[edge_tile_id] = edge_tile
                            tiles_full[edge_tile_id] = edge_full_tile
                        else:
                            grid[x][y + i] = edge_tile_id
                            tiles_.pop(edge_tile_id)
                            match = True
                            break

                if match:
                    break
            else:
                raise Exception(f"No match found for {left_tile_id}, {grid}")

        y = diagonal + dim - 1
        for i in range(0, dim):
            if grid[x + i][y] != 0:
                continue
            top_tile_id = grid[x + i - 1][y]
            top_tile = tiles[top_tile_id]

            top_tile_bottom_edge = top_tile[2]

            keys = tiles_.keys()
            for edge_tile_id in keys:
                match = False
                edge_tile = tiles[edge_tile_id]
                edge_full_tile = tiles_full[edge_tile_id]
                if not any([
                    top_tile_bottom_edge in edge_tile,
                    top_tile_bottom_edge[::-1] in edge_tile,
                ]):
                    continue
                for _ in range(4):
                    edge_tile = tiles[edge_tile_id]
                    edge_full_tile = tiles_full[edge_tile_id]
                    if edge_tile[0] != top_tile_bottom_edge:
                        edge_tile, edge_full_tile = _rotate(edge_tile, edge_full_tile)
                        tiles[edge_tile_id] = edge_tile
                        tiles_full[edge_tile_id] = edge_full_tile
                    else:
                        grid[x + i][y] = edge_tile_id
                        tiles_.pop(edge_tile_id)
                        match = True
                        break
                if not match:
                    edge_tile = tiles[edge_tile_id]
                    edge_full_tile = tiles_full[edge_tile_id]
                    edge_tile, edge_full_tile = _flip(edge_tile, edge_full_tile)
                    tiles[edge_tile_id] = edge_tile
                    tiles_full[edge_tile_id] = edge_full_tile
                    for _ in range(4):
                        edge_tile = tiles[edge_tile_id]
                        edge_full_tile = tiles_full[edge_tile_id]
                        if edge_tile[0] != top_tile_bottom_edge:
                            edge_tile, edge_full_tile = _rotate(edge_tile, edge_full_tile)
                            tiles[edge_tile_id] = edge_tile
                            tiles_full[edge_tile_id] = edge_full_tile
                        else:
                            grid[x + i][y] = edge_tile_id
                            tiles_.pop(edge_tile_id)
                            match = True
                            break

                if match:
                    break
            else:
                raise Exception(f"No match found for {top_tile_bottom_edge}, {grid}")

        x = diagonal + dim - 1
        for i in range(1, dim):
            if grid[x][y - i] != 0:
                continue
            right_tile_id = grid[x][y - i + 1]
            right_tile = tiles[right_tile_id]

            right_tile_left_edge = right_tile[3]

            keys = tiles_.keys()
            for edge_tile_id in keys:
                match = False
                edge_tile = tiles[edge_tile_id]
                edge_full_tile = tiles_full[edge_tile_id]
                if not any([
                    right_tile_left_edge in edge_tile,
                    right_tile_left_edge[::-1] in edge_tile,
                ]):
                    continue
                for _ in range(4):
                    edge_tile = tiles[edge_tile_id]
                    edge_full_tile = tiles_full[edge_tile_id]
                    if edge_tile[1] != right_tile_left_edge:
                        edge_tile, edge_full_tile = _rotate(edge_tile, edge_full_tile)
                        tiles[edge_tile_id] = edge_tile
                        tiles_full[edge_tile_id] = edge_full_tile
                    else:
                        grid[x][y - i] = edge_tile_id
                        tiles_.pop(edge_tile_id)
                        match = True
                        break
                if not match:
                    edge_tile = tiles[edge_tile_id]
                    edge_full_tile = tiles_full[edge_tile_id]
                    edge_tile, edge_full_tile = _flip(edge_tile, edge_full_tile)
                    tiles[edge_tile_id] = edge_tile
                    tiles_full[edge_tile_id] = edge_full_tile
                    for _ in range(4):
                        edge_tile = tiles[edge_tile_id]
                        edge_full_tile = tiles_full[edge_tile_id]
                        if edge_tile[1] != right_tile_left_edge:
                            edge_tile, edge_full_tile = _rotate(edge_tile, edge_full_tile)
                            tiles[edge_tile_id] = edge_tile
                            tiles_full[edge_tile_id] = edge_full_tile
                        else:
                            grid[x][y - i] = edge_tile_id
                            tiles_.pop(edge_tile_id)
                            match = True
                            break
                if match:
                    break
            else:
                raise Exception(f"No match found for {left_tile_id}, {grid}")

        y = y - i
        for i in range(1, dim):
            if grid[x - i][y] != 0:
                continue
            bottom_tile_id = grid[x - i + 1][y]
            bottom_tile = tiles[bottom_tile_id]

            bottom_tile_top_edge = bottom_tile[0]

            keys = tiles_.keys()
            for edge_tile_id in keys:
                match = False
                edge_tile = tiles[edge_tile_id]
                edge_full_tile = tiles_full[edge_tile_id]
                if not any([
                    bottom_tile_top_edge in edge_tile,
                    bottom_tile_top_edge[::-1] in edge_tile,
                ]):
                    continue
                for _ in range(4):
                    edge_tile = tiles[edge_tile_id]
                    edge_full_tile = tiles_full[edge_tile_id]
                    if edge_tile[2] != bottom_tile_top_edge:
                        edge_tile, tile_full = _rotate(edge_tile, edge_full_tile)
                        tiles[edge_tile_id] = edge_tile
                        tiles_full[edge_tile_id] = tile_full
                    else:
                        grid[x - i][y] = edge_tile_id
                        tiles_.pop(edge_tile_id)
                        match = True
                        break
                if not match:
                    edge_tile = tiles[edge_tile_id]
                    edge_full_tile = tiles_full[edge_tile_id]
                    edge_tile, tile_full = _flip(edge_tile, edge_full_tile)
                    tiles[edge_tile_id] = edge_tile
                    tiles_full[edge_tile_id] = tile_full
                    for _ in range(4):
                        edge_tile = tiles[edge_tile_id]
                        edge_full_tile = tiles_full[edge_tile_id]
                        if edge_tile[2] != bottom_tile_top_edge:
                            edge_tile, tile_full = _rotate(edge_tile, edge_full_tile)
                            tiles[edge_tile_id] = edge_tile
                            tiles_full[edge_tile_id] = tile_full
                        else:
                            grid[x - i][y] = edge_tile_id
                            tiles_.pop(edge_tile_id)
                            match = True
                            break
                if match:
                    break
            else:
                raise Exception(f"No match found for {left_tile_id}, {grid}")

        dim = dim - 2
        diagonal += 1
        x = diagonal
        y = diagonal

    # Visualize grid

    line = ""
    for i in range(len(grid)):
        for n in range(10):
            if n == 0 or n == 9:
                continue
            for tile in grid[i]:
                tile_lines = tiles_full[tile]
                line += "".join(tile_lines[n][1:9])
            line += "\n"

    total_hash = line.count("#")
    lines = line.strip("\n").split("\n")
    total_monster_count = 0

    def _rotate_lines(lines):
        pre_rotated = [list(x) for x in lines]
        rotated = [list(reversed(col)) for col in zip(*pre_rotated)]
        rotated = ["".join(r) for r in rotated]

        return rotated

    def _flip_lines(lines):
        pre_flipped = [list(x) for x in lines]
        flipped = [pre_flipped[len(pre_flipped)-i-1] for i in range(len(pre_flipped))]
        flipped = ["".join(f) for f in flipped]

        return flipped

    orientation = 0
    total_final_monster_count = 0
    while orientation < 8:
        total_monster_count = 0
        for line_num, line in enumerate(lines):
            if line_num == 0:
                continue
            if line_num == len(lines) - 1:
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
                        lines[line_num + 1][i + 1] == "#",
                        lines[line_num + 1][i + 4] == "#",
                        lines[line_num + 1][i + 7] == "#",
                        lines[line_num + 1][i + 10] == "#",
                        lines[line_num + 1][i + 13] == "#",
                        lines[line_num + 1][i + 16] == "#",
                    ]):
                        if lines[line_num - 1][i + 18] == "#":
                            total_monster_count += 1
                            i += 19

                i += 1

        if total_monster_count > total_final_monster_count:
            total_final_monster_count = total_monster_count

        lines = _rotate_lines(lines)
        orientation += 1
        if orientation == 4:
            lines = _flip_lines(lines)

    print(total_hash - (total_final_monster_count * 15))


if __name__ == "__main__":
    tiles, tiles_full = _parse_tiles(read_input())
    find_corners(tiles, tiles_full)
