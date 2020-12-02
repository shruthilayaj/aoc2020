import os
import re


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:    
        data = f.readlines()

    return data


def parse_line(line):
    match = re.match("(\d*)-(\d*) (.): (.*)", line)
    return int(match.group(1)), int(match.group(2)), match.group(3), match.group(4)


def password_philosophy(data):
    valid_lines = 0
    for line in data:
        min_occurence, max_occurence, match_char, password = parse_line(line)
        count = password.count(match_char)
        
        if count <= max_occurence and count >= min_occurence:
            valid_lines += 1
    
    return valid_lines


def password_philosophy_2(data):
    valid_lines = 0
    for line in data:
        index_1, index_2, match_char, password = parse_line(line)
        try:
            is_match = (
                not(password[index_1 - 1] == match_char and password[index_2 - 1] == match_char) and
                not(password[index_1 - 1] != match_char and password[index_2 - 1] != match_char)
            )
        except IndexError:
            continue

        if is_match:
            valid_lines += 1
    
    return valid_lines


if __name__ == "__main__":
    data = read_input()
    print(f"Part 1: {password_philosophy(data)}")
    print(f"Part 2: {password_philosophy_2(data)}")
