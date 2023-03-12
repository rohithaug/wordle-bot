import os, unittest
from pathlib import Path
from wordle_bot.utils import VocabUtil

# Global constants
DATA_FOLDER_PATH = "././data/"
ALL_VOCAB_FILENAME = "five_letter_words.pickle"

class VocabUtilTest(unittest.TestCase):
    def test_generate_valid_vocab(self):
        vocalUtil = VocabUtil()
        corpus = vocalUtil.generate_valid_vocab(ALL_VOCAB_FILENAME, DATA_FOLDER_PATH)

        filepath = os.path.join(DATA_FOLDER_PATH, ALL_VOCAB_FILENAME)
        path = Path(filepath)
        
        self.assertTrue(path.is_file())

    def test_read_valid_vocab(self):
        vocalUtil = VocabUtil()
        corpus = vocalUtil.read_valid_vocab(ALL_VOCAB_FILENAME, DATA_FOLDER_PATH)

        # verify if corpus is list
        self.assertIsInstance(corpus, list)

        # verify if every word in corpus is a string
        for word in corpus:
            self.assertIsInstance(word, str)

class PrioritizeVocabUtilTest(unittest.TestCase):
    def test_non_duplicate(self):
        # TODO
        pass

    def test_letter_frequency_same_index(self):
        # TODO
        pass

    def test_letter_frequency_cross_index(self):
        # TODO
        pass

if __name__ == '__main__':
    unittest.main()