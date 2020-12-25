def get_encryption(public_key_1, public_key_2):
    loop_size_1 = None
    loop_size_2 = None
    subject_number = 7
    value = 1
    i = 0
    while True:
        value *= subject_number
        value %= 20201227

        if value == public_key_1:
            loop_size_1 = i + 1
        if value == public_key_2:
            loop_size_2 = i + 1

        if loop_size_1 and loop_size_2:
            break

        i += 1

    value = 1
    for i in range(loop_size_2):
        value *= public_key_1
        value %= 20201227

    return value


if __name__ == "__main__":
    print(get_encryption(13316116, 13651422))
