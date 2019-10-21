#!/usr/bin/env python3

import sys
import re
import collections


def clean(text):
    return re.sub(r'[^ADFGVX]', '', text.upper())


def get_groups_difference(a, b):
    a_counter = dict(collections.Counter(a))
    b_counter = dict(collections.Counter(b))
    diff = {}
    for letter in 'ADFGVX':
        if letter not in a_counter:
            a_counter[letter] = 0
        if letter not in b_counter:
            b_counter[letter] = 0
        diff[letter] = abs(a_counter[letter] - b_counter[letter])
        # print('\t' + letter + '/A -> ' + '|' * a_counter[letter])
        # print('\t' + letter + '/B -> ' + '|' * b_counter[letter])
        # print()
    return sum(diff.values()) / (len(a) + len(b))


def find_transposition_rectangle_parity(cipher, max_width=25):
    print('## Determining the parity of the transposition rectangle (TR) width ##')
    print('\tSplitting cipher... Max TR width: {}'.format(max_width))
    min_column_height = len(cipher) // max_width
    print('\tMinimal safe column height: {}'.format(min_column_height))
    relative_difference = get_groups_difference(cipher[:min_column_height:2], cipher[1:min_column_height:2])
    print('\t-> Relative difference: {:.2f}'.format(relative_difference))
    parity = relative_difference < 0.2
    print('\t-> TR width is probably ' + ('even' if parity else 'odd'))
    return parity


def get_abcd(cipher, parity, height):
    if parity:
        return cipher[:height], cipher[height:height * 2], cipher[height * 2:height * 3], cipher[height * 3:height * 4]
    return cipher[:height * 2:2], cipher[1:height * 2:2], cipher[height * 2:height * 4:2], cipher[height * 2 + 1:height * 4:2]


def find_transposition_rectangle_size(cipher, max_width=25):
    parity = find_transposition_rectangle_parity(cipher, max_width)
    # TODO Here. This part is not really working, should be based on width instead of height and testing with short columns combinations
    for i in range(len(cipher) // max_width, len(cipher) // 3):
        a, b, c, d = get_abcd(cipher, parity, i)
        score = get_groups_difference(a, c) + get_groups_difference(b, d)
        print('i: {:02d} ({:02d}) = {:.2f}: '.format(i, len(cipher) // i, score) + '|' * round(score * 50))
        # print('\tAB: {:.2f} Higher is better'.format(get_groups_difference(a, b)))
        # print('\tAC: {:.2f} Lower is better'.format(get_groups_difference(a, c)))
        # print('\tBC: {:.2f} Higher is better'.format(get_groups_difference(b, c)))
        # print('\tBD: {:.2f} Lower is better'.format(get_groups_difference(b, d)))
    pass


def main(argv):
    cipher = clean(argv[1])
    # parity = find_transposition_rectangle_parity(cipher)
    find_transposition_rectangle_size(cipher, max_width=30)
    return 0


if __name__ == '__main__':
    exit(main(sys.argv))
