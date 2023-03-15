import nltk
import pickle, os

# Global constants
DATA_FOLDER_PATH = "././data/"
ALL_VOCAB_FILENAME = "five_letter_words.pickle"

class VocabUtil:
    def __init__(self) -> None:
        pass

    def generate_valid_vocab(self, filename: str = ALL_VOCAB_FILENAME, folder: str = DATA_FOLDER_PATH) -> None:
        if not nltk.corpus.words.words():
            nltk.download('words')

        english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        five_letter_words = [w for w in english_vocab if len(w) == 5]

        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(five_letter_words, f)

    def read_valid_vocab(self, filename: str = ALL_VOCAB_FILENAME, folder: str = DATA_FOLDER_PATH) -> str:
        words = []
        filepath = os.path.join(folder, filename)

        with (open(filepath, "rb")) as openfile:
            words = pickle.load(openfile)

        # print(len(words))
        return words

class PrioritizeVocabUtil:
    def __init__(self) -> None:
        pass

    def non_duplicate(self, words: str, indexes: int) -> str:
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
        sorted_words = [word for _, word in sorted(zip(num_duplicates, words))]
        return sorted_words

    def letter_frequency_same_index(self, words: str, indexes: int) -> str:
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

        # Sort the words based on their average frequency
        sorted_words = [word for _, word in sorted(zip(avg_freq, words), reverse=True)]
        return sorted_words

    def letter_frequency_cross_index(self, words: str, indexes: int) -> str:
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

        # Sort the words based on their average frequency
        sorted_words = [word for _, word in sorted(zip(avg_freq, words), reverse=True)]
        return sorted_words
