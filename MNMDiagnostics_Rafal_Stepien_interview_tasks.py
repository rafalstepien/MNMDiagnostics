#!bin/python3

from collections import Counter

# ------------------------------- TASK 1 -------------------------------------------

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



# ------------------------------- TASK 2 -------------------------------------------

def get_number_of_redundant(input_string):
    main = Counter(list(input_string.lower()))
    more_than_once = []
    for letter, occurrences in main.items():
    	if occurrences > 1:
    		more_than_once.append(letter)
    return len(more_than_once)


if __name__ == "__main__":
    print(change_letters_size("abcdef"))
    print(get_number_of_redundant('abba'))