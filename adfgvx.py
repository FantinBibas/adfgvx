#!/usr/bin/env python3

import sys
import re
import collections


def clean(text):
    return re.sub(r'[^ADFGVX]', '', text.upper())


def find_transposition_rectangle_parity(cipher, max_width=25):
    print('## Determining the parity of the transposition rectangle (TR) width ##')
    print('\tSplitting cipher... Max TR width: {}'.format(max_width))
    min_column_height = len(cipher) // max_width
    print('\tMinimal safe column height: {}'.format(min_column_height))
    a_counter = dict(collections.Counter(cipher[:min_column_height:2]))
    b_counter = dict(collections.Counter(cipher[1:min_column_height:2]))
    diff = {}
    print('\n\tLetter/Group -> Count\n')
    for letter in 'ADFGVX':
        if letter not in a_counter:
            a_counter[letter] = 0
        if letter not in b_counter:
            b_counter[letter] = 0
        diff[letter] = abs(a_counter[letter] - b_counter[letter])
        print('\t' + letter + '/A -> ' + '|' * a_counter[letter])
        print('\t' + letter + '/B -> ' + '|' * b_counter[letter])
        print()
    relative_difference = sum(diff.values()) / min_column_height
    print('\t-> Relative difference: {:.2f}'.format(relative_difference))
    parity = relative_difference < 0.2
    print('\t-> TR width is probably ' + ('even' if parity else 'odd'))
    return parity


def main(argv):
    cipher = clean(argv[1])
    parity = find_transposition_rectangle_parity(cipher)
    return 0


if __name__ == '__main__':
    exit(main(sys.argv))
