#! /usr/bin/env python

import argparse
import json
import random

PHRASE_START = 'PHRASE_START'
"""This special string represents the starting symbol"""

PHRASE_END = 'PHRASE_END'
"""This special string represents the ending symbol"""


def make_phrase(transition_matrix, word=PHRASE_START):
    """Returns a phrase (string) constructing from following the probabilities
    in the transition matrix."""
    phrase = ''

    while word != PHRASE_END:
        previous = word
        
        # Pick a random word using the probabilities.
        word = random.choices(
            list(transition_matrix[previous].keys()),
            list(transition_matrix[previous].values())
        )[0]

        if word == PHRASE_END:
            phrase += '?'
        else:
            if previous != PHRASE_START:
                phrase += ' '
            phrase += word

    return phrase

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a question from a transition matrix.")
    parser.add_argument('input_file', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('--n_questions', type=int, default=1, help='Number of questions to print.')
    args = parser.parse_args()

    transition_matrix = json.load(args.input_file)

    for _ in range(args.n_questions):
        print(make_phrase(transition_matrix))
