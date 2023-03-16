from wordle_bot.utils import VocabUtil
from skeleton import Vn_DS
from wordle_bot.evaluation_bot import Colour
import timeit
import numpy as np

# Global constants
DATA_FOLDER_PATH = "././data/"
ALL_VOCAB_FILENAME = "five_letter_words.pickle"

vocalUtil = VocabUtil()
corpus = vocalUtil.read_valid_vocab(ALL_VOCAB_FILENAME, DATA_FOLDER_PATH)

# make class extending vn class from skeleton code
class Vn_reduction(Vn_DS):
    def flatten(self, l):
        return [item for sublist in l for item in sublist]

    def __init__(self, W_n):
        self.Wn = set(W_n)
        self.Vn = set(W_n.copy())
        self.hashtable = [[[] for _ in range(26)] for _ in range(5)]
        for word in W_n:
            for i in range(5):
                self.hashtable[i][ord(word[i]) - ord('a')].append(word)

    def reset(self, Vn = None):
        self.Vn = self.Wn.copy() if Vn is None else Vn

    def update(self, word, colors):
        for i, letter in enumerate(word):
            if colors[i] == Colour.GRAY.value:
                for j in range(len(self.hashtable)):
                    to_delete = self.hashtable[j][ord(letter) - ord('a')]
                    for word in to_delete:
                        self.Vn.discard(word)
            elif colors[i] == Colour.YELLOW.value:
                to_delete = self.hashtable[i][ord(letter) - ord('a')]
                words_containing_letter = []
                for j in range(len(self.hashtable)):
                    if j != i:
                        words_containing_letter.extend(self.hashtable[j][ord(letter) - ord('a')])
                words_containing_letter = set(words_containing_letter)
                self.Vn = set.intersection(self.Vn, words_containing_letter)
                for word in to_delete:
                    self.Vn.discard(word)
            else:
                to_delete = self.flatten(self.hashtable[i][:ord(letter) - ord('a')])
                to_delete.extend(self.flatten(self.hashtable[i][ord(letter) - ord('a')+1:]))
                for word in to_delete:
                    self.Vn.discard(word)

    def update2(self, word, colors):
        vn2 = self.Vn.copy()
        for current in vn2:
            for i, letter in enumerate(current):
                if colors[i] == 0 and word[i] in current:
                    self.Vn.remove(current)
                    break
                elif colors[i] == 1 and (word[i] not in current or letter == word[i]):
                    self.Vn.remove(current)
                    break
                elif colors[i] == 2 and letter != word[i]:
                    self.Vn.remove(current)
                    break
        return self.Vn

    def get_Vn(self):
        return self.Vn

if __name__ == "__main__":
    vn_red = Vn_reduction(corpus)
    v =vn_red.update('slate', [0, 0, 0, 0, 0])
    v =vn_red.update('bingo', [0, 0, 0, 0, 0])
    v =vn_red.update('furzy', [0, 2, 0, 0, 2])
    v =vn_red.update('yucky', [1, 2, 0, 0, 2])
    v =vn_red.update('dumpy', [0, 2, 0, 2, 2])

    print(vn_red.get_Vn())

    def time_check1():
        vn_red.reset()
        vn_red.update(np.random.choice(corpus), np.random.randint(0, 3, 5))

    def time_check2():
        vn_red.reset()
        vn_red.update2(np.random.choice(corpus), np.random.randint(0, 3, 5))

    print(timeit.timeit("time_check1()", setup="from __main__ import time_check1", number=1000))

    print(timeit.timeit("time_check2()", setup="from __main__ import time_check2", number=1000))
