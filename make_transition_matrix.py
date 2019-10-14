#! /usr/bin/env python

import argparse
import json
import re

PHRASE_START = 'PHRASE_START'
"""This special string represents the starting symbol"""

PHRASE_END = 'PHRASE_END'
"""This special string represents the ending symbol"""

def add_transition(transition_matrix, from_word, to_word):
    """Adds a count to the transition matrix."""
    if from_word not in transition_matrix:
        transition_matrix[from_word] = dict()

    if to_word not in transition_matrix[from_word]:
        transition_matrix[from_word][to_word] = 1
    else:
        transition_matrix[from_word][to_word] += 1


def compute_probabilities(transition_matrix):
    """Convert the occurence matrix to a probability matrix of the
    transitions."""
    for from_word, to_words in transition_matrix.items():
        total = sum(to_words.values())
        for to_word in to_words:
            transition_matrix[from_word][to_word] /= total


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a transition matrix from a list of phrases.")
    parser.add_argument('input_file', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('output_file', type=argparse.FileType('w', encoding='UTF-8'))
    args = parser.parse_args()
    
    transition_matrix = dict()

    for line in args.input_file:
        # Remove any whitespace before/after the phrase, and convert to
        # lower-case.
        line = line.strip().lower()

        # Split the sentences into words
        words = re.findall(r'[\w\']+', line)

        # Iterate over the transitions and add them to the matrix. (In sparse
        # encoding, not a full matrix.)
        word_iter = iter(words)
        prev = next(word_iter)
        add_transition(transition_matrix, PHRASE_START, prev)
        for word in word_iter:
            add_transition(transition_matrix, prev, word)
            prev = word
        add_transition(transition_matrix, prev, PHRASE_END)
    
    compute_probabilities(transition_matrix)

    json.dump(transition_matrix, args.output_file, ensure_ascii=False)
