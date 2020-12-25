import os


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.read()

    return data.split("\n")


def parse_input(records):
    data = []
    for line in records:
        tile_path = []
        i = 0
        while i < len(line):
            if line[i] in ['s', 'n']:
                tile_path.append(line[i:i+2])
                i += 2
            else:
                tile_path.append(line[i])
                i += 1

        data.append(tile_path)

    return data


def lobby_layout(records):
    reference = (0, 0, 0)
    tiles_dict = {reference: False}

    for path in records:
        x, y, z = reference
        for direction in path:
            if direction == "e":
                x, y, z = x + 1, y - 1, z
            elif direction == "se":
                x, y, z = x, y - 1, z + 1
            elif direction == "sw":
                x, y, z = x - 1, y, z + 1
            elif direction == "w":
                x, y, z = x - 1, y + 1, z
            elif direction == "nw":
                x, y, z = x, y + 1, z - 1
            elif direction == "ne":
                x, y, z = x + 1, y, z - 1

        try:
            tile = tiles_dict[(x, y, z)]
        except KeyError:
            tiles_dict[(x, y, z)] = True
        else:
            tiles_dict[(x, y, z)] = not(tile)

    return tiles_dict


def lobby_layout_2(tiles_dict):
    adjacent_coords = [(0, 1, -1), (1, 0, -1), (1, -1, 0), (0, -1, 1), (-1, 0, 1), (-1, 1, 0)]
    i = 0
    while i < 100:
        new_dict = {}
        for tile, is_black in tiles_dict.items():
            x, y, z = tile[0], tile[1], tile[2]
            adjacent_tiles = [(x + dx, y + dy, z + dz) for dx, dy, dz in adjacent_coords]

            count = 0
            for adj in adjacent_tiles:
                try:
                    tile = tiles_dict[adj]
                except KeyError:
                    pass
                else:
                    if tile:
                        count += 1

            if is_black and (count == 0 or count > 2):
                new_dict[(x, y, z)] = False
            if not is_black and count == 2:
                new_dict[(x, y, z)] = True

            for adj in adjacent_tiles:
                if adj not in tiles_dict:
                    x, y, z = adj[0], adj[1], adj[2]
                    adj_ = [(x + dx, y + dy, z + dz) for dx, dy, dz in adjacent_coords]
                    count = 0
                    for t in adj_:
                        if t in tiles_dict and tiles_dict[t]:
                            count += 1

                    if count == 2:
                        new_dict[(x, y, z)] = True

        i += 1
        tiles_dict.update(new_dict)

    print(sum(tiles_dict.values()))


if __name__ == "__main__":
    records = parse_input(read_input())
    tiles_dict = lobby_layout(records)
    print(f"{sum(tiles_dict.values())}")
    lobby_layout_2(tiles_dict)
