import os
import re


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.read()

    return data


def passport_processing(records):
    def is_match(line):
        matches = re.findall("(ecl|pid|eyr|hcl|byr|iyr|hgt):([^\n\s]*)", line)
        return len(matches) == 7

    return sum(map(is_match, records))


def passport_processing_2(records):
    regex_match_map = {
        "hgt": r"^(1[5-8][0-9]cm|19[0-3]cm|59in|6[0-9]in|7[0-6]in)$",
        "byr": r"^(19[2-9][0-9]|200[0-2])$",
        "iyr": r"^(201[0-9]|2020)$",
        "eyr": r"^(202[0-9]|2030)$",
        "pid": r"^(\d{9})$",
        "ecl": r"^(amb|blu|brn|gry|grn|hzl|oth)$",
        "hcl": r"^#[0-9a-f]{6}$",
    }
    lines = 0
    for line in records:
        matches = re.findall(r"(ecl|pid|eyr|hcl|byr|iyr|hgt):([^\n\s]*)", line)
        match_index = 0
        for key, value in matches:
            try:
                match_str = regex_match_map[key]
            except KeyError:
                continue

            if re.match(match_str, value):
                match_index += 1

        if match_index == 7:
            lines += 1

    return lines


if __name__ == "__main__":
    records = read_input().split("\n\n")

    print(f"Part 1: {passport_processing(records)}")
    print(f"Part 1: {passport_processing_2(records)}")
