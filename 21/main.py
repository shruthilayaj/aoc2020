import os


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.readlines()

    return data


def _parse_input(records):
    data = []
    for line in records:
        ingredients, allergen = line.split("(")
        ingredients = ingredients.strip().split(" ")
        allergen = allergen.replace("contains", "").replace(")", "").strip().split(", ")

        data.append([set(ingredients), set(allergen)])

    return data


def allergen_assessment(records):
    allergen_possibilities = {}
    used_ingredients = set()
    used_allergens = set()
    all_allergens = set()
    all_ingredients = []

    for ingredients, allergens in records:
        all_allergens = all_allergens.union(allergens)
        all_ingredients.extend(ingredients)

    i = len(all_allergens - used_allergens)
    while i > 0:
        for ingredients, allergens in records:
            for allergen in allergens:
                if allergen in used_allergens:
                    continue
                if allergen in allergen_possibilities:
                    intersect = ingredients.intersection(allergen_possibilities[allergen]) - used_ingredients
                    allergen_possibilities[allergen] = intersect
                    if len(intersect) == 1:
                        allergen_possibilities[allergen] = list(intersect)[0]
                        used_ingredients.add(list(intersect)[0])
                        used_allergens.add(allergen)
                else:
                    allergen_possibilities[allergen] = ingredients - used_ingredients

        i = len(all_allergens - used_allergens)

    unused_ingredients = [i for i in all_ingredients if i not in used_ingredients]
    return len(unused_ingredients), allergen_possibilities


def allergen_assessment_2(allergen_map):
    return ",".join([allergen_map[k] for k in sorted(allergen_map.keys())])


if __name__ == "__main__":
    records = _parse_input(read_input())
    num, allergen_possibilities = allergen_assessment(records)
    print(f"Part 1: {num}")
    print(f"Part 2: {allergen_assessment_2(allergen_possibilities)}")
