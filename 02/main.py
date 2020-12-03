import functools
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
    def is_match(line):
        min_occurence, max_occurence, match_char, password = parse_line(line)
        count = password.count(match_char)

        return count <= max_occurence and count >= min_occurence
    
    return functools.reduce(lambda x, y: x + y, list(map(is_match, data)))


def password_philosophy_2(data):
    def is_match(line):
        index_1, index_2, match_char, password = parse_line(line)

        return (password[index_1 - 1] == match_char) ^ (password[index_2 - 1] == match_char)
    
    return functools.reduce(lambda x, y: x + y, list(map(is_match, data)))


if __name__ == "__main__":
    data = read_input()
    print(f"Part 1: {password_philosophy(data)}")
    print(f"Part 2: {password_philosophy_2(data)}")
