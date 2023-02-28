from enum import Enum
from wordle_bot.utils import VocabUtil

class Colour(Enum):
    GRAY = 0
    YELLOW = 1
    GREEN = 2

class EvaluationBot:
    def __init__(self) -> None:
        pass

    def evaluate_guessed_word(self, guess_word, correct_word):
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

        return letter_colours

    def create_trie(self, corpus):
        trie = Trie()
        for word in corpus:
            trie.insert_word(word)
        return trie
        
    def is_valid_word(self, word, corpus):
        trie = self.create_trie(corpus)
        return trie.search_word(word)


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