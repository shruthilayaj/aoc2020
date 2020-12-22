import os


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.read()

    player_1, player_2 = data.split("\n\n")
    player_1, player_2 = player_1.split("\n"), player_2.split("\n")
    player_1.pop(0)
    player_2.pop(0)
    player_1 = [int(n) for n in player_1]
    player_2 = [int(n) for n in player_2]

    return player_1, player_2


def crab_combat(deck_1, deck_2):
    while len(deck_1) > 0 and len(deck_2) > 0:
        card_1 = deck_1.pop(0)
        card_2 = deck_2.pop(0)

        if card_1 > card_2:
            deck_1.append(card_1)
            deck_1.append(card_2)
        else:
            deck_2.append(card_2)
            deck_2.append(card_1)

    winning_deck = deck_1 if deck_1 else deck_2
    total = sum([(i + 1) * num for i, num in enumerate(reversed(winning_deck))])

    return total


def _recursive_combat(deck_1, deck_2):
    snapshot_1 = [deck_1[:]]
    snapshot_2 = [deck_2[:]]
    while len(deck_1) > 0 and len(deck_2) > 0:
        card_1 = deck_1.pop(0)
        card_2 = deck_2.pop(0)

        if len(deck_1) >= card_1 and len(deck_2) >= card_2:
            winner = _recursive_combat(deck_1[:card_1], deck_2[:card_2])

            if winner == "player_1":
                deck_1.append(card_1)
                deck_1.append(card_2)
            else:
                deck_2.append(card_2)
                deck_2.append(card_1)

        else:
            if card_1 > card_2:
                deck_1.append(card_1)
                deck_1.append(card_2)
            else:
                deck_2.append(card_2)
                deck_2.append(card_1)

        if deck_1 in snapshot_1 or deck_2 in snapshot_2:
            return "player_1"

        snapshot_1.append(deck_1[:])
        snapshot_2.append(deck_2[:])

    return "player_1" if deck_1 else "player_2"


def crab_combat_2(deck_1, deck_2):
    _recursive_combat(deck_1, deck_2)
    winning_deck = deck_1 if deck_1 else deck_2
    total = sum([(i + 1) * num for i, num in enumerate(reversed(winning_deck))])

    return total


if __name__ == "__main__":
    deck_1, deck_2 = read_input()
    print(f"Part 1: {crab_combat(deck_1[:], deck_2[:])}")
    print(f"Part 2: {crab_combat_2(deck_1[:], deck_2[:])}")
