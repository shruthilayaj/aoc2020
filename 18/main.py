import functools
import os
import re


def read_input():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filename) as f:
        data = f.read()

    return data.split("\n")


def get_nested_expression(record):
    new_record = ""
    parens = 1
    if record[0] == "(":
        record = record[1:]
    else:
        record = record[2:]

    while True:
        for c in record[:]:
            if c == "(":
                parens += 1
            elif c == ")":
                parens -= 1
            if parens == 0:
                record = record[1:]
                return new_record, record
            new_record += c
            record = record[1:]


def operation_order_(record):
    if record[0] == "(":
        fragment, record = get_nested_expression(record)
        initial_count = operation_order_(fragment)

    else:
        m = re.match(r"(\d*)", record)
        initial_count = int(m.group(1))
        record = record[m.end(1):]

    m = re.match(r" ([\+\*]+)", record)
    operator = m.group(1)
    record = record[m.end(1):]

    next_input = None
    fragment = None
    while record:
        if not operator:
            m = re.match(r" ([\+\*]+)", record)
            operator = m.group(1)
            record = record[m.end(1):]
        if not next_input:
            m = re.match(r"[^\(](\d+)", record)
            if m:
                next_input = int(m.group(1))
                record = record[m.end(1):]
            else:
                fragment, record = get_nested_expression(record)
        if next_input and operator:
            if operator == "*":
                initial_count *= next_input
            elif operator == "+":
                initial_count += next_input

            operator = None
            next_input = None

        elif fragment and operator:
            if operator == "*":
                initial_count *= operation_order_(fragment)
            elif operator == "+":
                initial_count += operation_order_(fragment)

            operator = None
            fragment = None

    return initial_count


def operation_order(records):
    total = functools.reduce(
        lambda x, y: x + y,
        list(map(operation_order_, records))
    )

    return total


def operation_order_2_(record):
    if record[0] == "(":
        fragment, record = get_nested_expression(record)
        initial_count, _ = operation_order_2_(fragment)
    else:
        m = re.match(r"(\d*)", record)
        initial_count = int(m.group(1))
        record = record[m.end(1):]

    next_input = None
    fragment = None
    operator = None
    while record:
        if not operator:
            m = re.match(r" ([\+\*]+)", record)
            operator = m.group(1)
            record = record[m.end(1):]
        if not next_input:
            m = re.match(r"[^\(](\d+)", record)
            if m:
                if operator == "+":
                    next_input = int(m.group(1))
                    record = record[m.end(1):]
            else:
                fragment, record = get_nested_expression(record)
        if next_input and operator == "+":
            initial_count += next_input
            operator = None
            next_input = None

        elif fragment and operator == "+":
            x, _ = operation_order_2_(fragment)
            initial_count += x

            operator = None
            fragment = None

        elif fragment and operator == "*":
            x, record = operation_order_2_(f"({fragment}){record}")
            initial_count *= x

            operator = None
            fragment = None

        elif operator == "*":
            record = record[1:]
            x, record = operation_order_2_(record)
            initial_count *= x

    return initial_count, record


def operation_order_2(records):
    total = functools.reduce(
        lambda x, y: x + y,
        [k[0] for k in list(map(operation_order_2_, records))],
    )

    return total


if __name__ == "__main__":
    records = read_input()
    print(operation_order_2(records))
