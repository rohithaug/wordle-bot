from wordle_bot.utils import VocabUtil
from skeleton import Vn_DS
from wordle_bot.evaluation_bot import Colour

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

    def reset(self):
        self.Vn = self.Wn.copy()

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

    def get_Vn(self):
        return self.Vn

vn_red = Vn_reduction(corpus)
vn_red.update('apple', [2, 0, 0, 1, 2])
print(vn_red.get_Vn())
