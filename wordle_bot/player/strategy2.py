import os
import pickle
from enum import Enum
from skeleton import Player
from skeleton import Vn_DS
import matplotlib.pyplot as plt

class Colour(Enum):
    GRAY = 0
    YELLOW = 1
    GREEN = 2

# Global constants
DATA_FOLDER_PATH = "././data/"
ALL_VOCAB_FILENAME = "five_letter_words.pickle"
VALID_WORDLE_WORDS_FILENAME = "valid-wordle-words.pickle"

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

def generate_valid_vocab(filename: str, folder: str) -> None:
    if not nltk.corpus.words.words():
        nltk.download('words')

    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    five_letter_words = [w for w in english_vocab if len(w) == 5]

    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as f:
        pickle.dump(five_letter_words, f)

def read_valid_vocab(filename: str, folder: str) -> str:
    words = []
    filepath = os.path.join(folder, filename)

    with (open(filepath, "rb")) as openfile:
        words = pickle.load(openfile)

    # print(len(words))
    return words

def get_letter_colours(guess_word, correct_word):
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

def non_duplicate(words: str, indexes: int) -> str:
    """
    Prioritizes words based on the number of duplicates in the given indexes of each word.
    """
    # Count the number of duplicates for each word
    num_duplicates = []
    for word in words:
        duplicates = set()
        for i in indexes:
            letter = word[i]
            if letter in duplicates:
                continue
            duplicates.add(letter)
        num_duplicates.append(len(duplicates))

    # Sort the words based on the number of duplicates
    grouped_words = [[] for _ in range(len(words[0]) + 1)]

    for i, word in enumerate(words):
        grouped_words[num_duplicates[i]].append(word)

    return grouped_words[::-1]

def letter_frequency_same_index(words: str, indexes: int) -> str:
    """
    Prioritizes words based on the frequency of letters in the given indexes of each word.
    """
    # initialize a dictionary to store the frequency of each letter in the indexes
    freq_dict = {i: {} for i in indexes}

    # Count the frequency of letters in the indexes for each word
    for word in words:
        for i in indexes:
            letter = word[i]
            freq_dict[i][letter] = freq_dict[i].get(letter, 0) + 1

    # Calculate the average frequency for each word
    avg_freq = []
    for word in words:
        total_freq = sum([freq_dict[i].get(word[i], 0) for i in indexes])
        avg_freq.append(total_freq / len(indexes))

    grouped_words = {}
    for i in avg_freq:
        if i not in grouped_words: grouped_words[i] = []

    for i, word in enumerate(words):
        grouped_words[avg_freq[i]].append(word)

    grouped_words = list(grouped_words.items())
    grouped_words.sort(key=lambda x: x[1])
    grouped_words = [x[1] for x in grouped_words]

    return grouped_words

    # Sort the words based on their average frequency
    # sorted_words = [word for _, word in sorted(zip(avg_freq, words), reverse=True)]
    # return sorted_words

def letter_frequency_cross_index(words: str, indexes: int) -> str:
    """
    Prioritizes words based on the frequency of letters across all indexes of each word.
    """
    # Count the frequency of letters in the indexes for each word
    freq_dict = {}
    for word in words:
        for i in indexes:
            letter = word[i]
            freq_dict[letter] = freq_dict.get(letter, 0) + 1

    # Calculate the average frequency for each word
    avg_freq = []
    for word in words:
        total_freq = sum([freq_dict.get(word[i], 0) for i in indexes])
        avg_freq.append(total_freq / len(indexes))

    grouped_words = {}
    for i in avg_freq:
        if i not in grouped_words: grouped_words[i] = []

    for i, word in enumerate(words):
        grouped_words[avg_freq[i]].append(word)

    grouped_words = list(grouped_words.items())
    grouped_words.sort(key=lambda x: x[1])
    grouped_words = [x[1] for x in grouped_words]

    return grouped_words

    # Sort the words based on their average frequency
    # sorted_words = [word for _, word in sorted(zip(avg_freq, words), reverse=True)]
    # return sorted_words

class PlayerStrategy2(Player):
    def __init__(self, Wn, Vn, brute_force=False):
        self.Vn = Vn
        self.Wn = Wn
        self.colors = [-1 for _ in range(len(Wn[0]))]

    def get_next_guess(self):
        indexes = []
        for idx, color in enumerate(self.colors):
            if color != Colour.GREEN.value:
                indexes.append(idx)

        Vn_words = list(self.Vn.get_Vn())

        grouped_words = non_duplicate(Vn_words, indexes)

        # vn_red.update('apple', [2, 0, 0, 1, 2])

        for words in grouped_words:
            if len(words) == 0:
                continue
            elif len(words) == 1:
                return words[0]
            else:
                prioritized_words_1_list = letter_frequency_same_index(words, indexes)
                for prioritized_words_1 in prioritized_words_1_list:
                    if len(prioritized_words_1) <= 0:
                        continue
                    elif len(prioritized_words_1) == 1:
                        return prioritized_words_1[0]
                    else:
                        prioritized_words_2_list = letter_frequency_cross_index(words, indexes)
                        for prioritized_words_2 in prioritized_words_2_list:
                            if len(prioritized_words_2) <= 0:
                                continue
                            else:
                                return prioritized_words_2[0]
 
        # print("Test 2: ", words)
        # Vn_words = prioritizeVocabUtil.letter_frequency_same_index(Vn_words, indexes)
        # Vn_words = prioritizeVocabUtil.letter_frequency_cross_index(Vn_words, indexes)

    def update_game_state(self, wordle_row):
        self.Vn.update(word, colors)
        self.word = word

class Vn_DS:
    def __init__(self, Wn):
        self.Vn = Wn

    def update(self, word, colors):
        pass

    def get_Vn(self):
        return self.Vn

def get_color_word(words, colors):
    green = "\033[32m"
    yellow = "\033[33m"
    gray = "\033[37m"
    reset = "\033[0m"
    color_word = [0] * 5
    ind = 0
    for letter, color_val in zip(words, colors):
        if color_val == 0:
            color_word[ind] = gray + letter + reset
        elif color_val == 1:
            color_word[ind] = yellow + letter + reset
        elif color_val == 2:
            color_word[ind] = green + letter + reset
        ind += 1
    return "".join(color_word)

if __name__ == "__main__":
    # filepath = os.path.join(DATA_FOLDER_PATH, "number_guesses.pickle")
    # with (open(filepath, "rb")) as openfile:
    #     num_guesses = pickle.load(openfile)
    # print(num_guesses)

    Wn = read_valid_vocab(VALID_WORDLE_WORDS_FILENAME, DATA_FOLDER_PATH)
    Vn = Vn_reduction(Wn)

    num_guesses = {}
    num = 0
    for word in Wn[::-1]:
        # print("\n---------------------------------------\n")
        player2 = PlayerStrategy2(Wn, Vn)
        correct_word = word
        guess_word = ""
        i = 0
        while guess_word != correct_word:
            len1 = len(Vn.get_Vn())
            guess_word = player2.get_next_guess()
            [color, _] = get_letter_colours(guess_word, correct_word)
            color_word = get_color_word(guess_word, color)
            print(f"Guess {i}: {guess_word}, colors: {color_word}")
            Vn.update(guess_word, color)
            len2 = len(Vn.get_Vn())
            print(f"Len of in Vn reduced from {len1} to {len2}")
            i += 1

    #     num_guesses[i] = num_guesses.get(i, 0) + 1
    #     Vn.reset()
    #     # print("Number of guesses: ", i)
    #     # print("\n---------------------------------------\n")
    #     num += 1
    #     if num % 200 == 0:
    #         print("Average number of guesses: ", num_guesses)

    # print("Average number of guesses: ", num_guesses)

    # filepath = os.path.join(DATA_FOLDER_PATH, "number_guesses.pickle")
    # with open(filepath, 'wb') as f:
    #     pickle.dump(num_guesses, f)
 
    # Create two lists from dictionary for x and y axis data
    x = list(num_guesses.keys())
    y = list(num_guesses.values())

    # Create a histogram
    plt.bar(x, y, alpha=0.6)

    # Add labels to each bar
    for i in range(len(x)):
        plt.text(x[i], y[i], str(y[i]), ha='center', va='bottom', alpha=0.8)

    plt.xlabel("Number of guesses")
    plt.ylabel("Number of words")

    total = 0
    count = 0
    for key, value in num_guesses.items():
        total += key * value
        count += value

    print("Average number of guesses: ", total/count)

    # save the plot as time_graph.png
    plt.savefig("strategy2_hist.png")

#puppy

# 1 - saite