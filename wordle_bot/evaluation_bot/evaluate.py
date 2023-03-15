from enum import Enum
from wordle_bot.utils import VocabUtil
from wordle_bot.evaluation_bot.utils import EvaluationUtils

import time
import matplotlib.pyplot as plt
from wordle_bot.utils import VocabUtil
# from evaluation_bot.utils import EvaluationUtils
# from wordle_bot.evaluation_bot.evaluate import EvaluationBot
import random

N_ITERATIONS = 10000

class Colour(Enum):
    GRAY = 0
    YELLOW = 1
    GREEN = 2

class EvaluationBot:
    def __init__(self, DATA_FOLDER_PATH, ALL_VOCAB_FILENAME) -> None:
        vocalUtil = VocabUtil()
        self.corpus = vocalUtil.read_valid_vocab(ALL_VOCAB_FILENAME, DATA_FOLDER_PATH)

    def invalid_word_response():
        return [], False

    def brute_force(self, guess_word, correct_word):

        for word in self.corpus:
            if word == guess_word:
                valid_word = True
                break
        if not valid_word:
            return self.invalid_word_response()

        return self.get_letter_colours(guess_word, correct_word)

    def get_letter_colours():
        letter_colours = []

        guess_word = guess_word.lower()
        correct_word = correct_word.lower()
        for ind, letter in enumerate(guess_word):
            if letter not in correct_word:
                letter_colours.append(Colour.GRAY.value)

            elif letter == correct_word[ind]:
                letter_colours.append(Colour.GREEN.value)

            else:
                letter_colours.append(Colour.YELLOW.value)

        return letter_colours, True

    def evaluate_guessed_word_optimal(self, guess_word, correct_word):
        if not self.is_valid_word(guess_word):
            return self.invalid_word_response()

        return self.get_letter_colours(guess_word, correct_word)

    def create_trie(self, corpus):
        trie = Trie()
        for word in corpus:
            trie.insert_word(word)
        return trie
        
    def is_valid_word(self, word, corpus):
        trie = self.create_trie(corpus)
        return trie.search_word(word)


    # function to create a time graph for comparing brute_force and evaluate_guessed_word_optimal

    def create_time_graph(self, ):
        evaluationBot = EvaluationBot("wordle_bot/data", "all_vocab.txt")

        time_brute_force = []
        time_optimal = []
        for iterations in range(N_ITERATIONS):
            correct_word = EvaluationUtils.select_correct_word()
            guess_word =EvaluationUtils.generate_random_word(self.corpus)
            start_time = time.time()
            evaluationBot.brute_force(guess_word, correct_word)
            end_time = time.time()
            time_brute_force.append(end_time - start_time)

            start_time = time.time()
            evaluationBot.evaluate_guessed_word_optimal(guess_word, correct_word)
            end_time = time.time()
            time_optimal.append(end_time - start_time)

        plt.plot(time_brute_force, label="brute_force")
        plt.plot(time_optimal, label="optimal")
        plt.legend()
        plt.show()
        print("plot created")

        # save the plot as time_graph.png
        plt.savefig("time_graph.png")


class Trie:
    def __init__(self):
        self.alp = dict()
        self.term = False

    def insert_word(self, word):
        root = self
        for letter in word:
            if letter not in root.alp:
                root.alp[letter] = Trie()
            root = root.alp[letter]
        root.term = True

    def search_word(self, word):
        root = self
        for letter in word:
            if letter in root.alp:
                root = root.alp[letter]
            else:
                return False
        return root.term