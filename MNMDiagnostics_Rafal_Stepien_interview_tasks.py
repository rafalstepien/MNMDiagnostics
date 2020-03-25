#!bin/python3


def change_letters_size(input_string):
    """
    :param input_string: String to be changed
    :return: List with two strings
    """
    str_1, str_2 = '', ''
    for id, letter in enumerate(input_string):
        if id % 2 == 0:
            str_1 += letter.upper()
            str_2 += letter
        else:
            str_1 += letter
            str_2 += letter.upper()
    return [str_1, str_2]

if __name__ == "__main__":
    print(change_letters_size("abcdef"))