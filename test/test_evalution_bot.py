import unittest

from wordle_bot.evaluation_bot import EvaluationBot
from wordle_bot.evaluation_bot import Colour
from wordle_bot.utils import VocabUtil

# Global constants
DATA_FOLDER_PATH = "././data/"
ALL_VOCAB_FILENAME = "five_letter_words.pickle"

class EvaluationBotTest(unittest.TestCase):
    def test_evaluate_guessed_word_optimal(self):
        evaluation_bot = EvaluationBot()

        res = evaluation_bot.evaluate_guessed_word_optimal("APPLE", "apple")
        assert res == [Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value], True

        res = evaluation_bot.evaluate_guessed_word_optimal("mAnGo", "MANGO")
        assert res == [Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value], True

        res = evaluation_bot.evaluate_guessed_word_optimal("puppy", "funny")
        assert res == [Colour.GRAY.value, Colour.GREEN.value, Colour.GRAY.value, Colour.GRAY.value, Colour.GREEN.value], True

        res = evaluation_bot.evaluate_guessed_word_optimal("puppy", "apple")
        assert res == [Colour.YELLOW.value, Colour.GRAY.value, Colour.GREEN.value, Colour.YELLOW.value, Colour.GRAY.value], True

        res = evaluation_bot.evaluate_guessed_word_optimal("zzzzz", "apple")
        assert res == [Colour.GRAY.value, Colour.GRAY.value, Colour.GRAY.value, Colour.GRAY.value, Colour.GRAY.value], True

    def test_is_valid_word(self):
        vocalUtil = VocabUtil()
        corpus = vocalUtil.read_valid_vocab(ALL_VOCAB_FILENAME, DATA_FOLDER_PATH)

        evaluation_bot = EvaluationBot()

        res = evaluation_bot.is_valid_word("apple", corpus)        
        assert res == True

        res = evaluation_bot.is_valid_word("zzzzz", corpus)
        assert res == False

        res = evaluation_bot.is_valid_word("appl", corpus)
        assert res == False

        res = evaluation_bot.is_valid_word("ball", corpus)
        assert res == False

    def test_graph_creation():
        evaluation_bot = EvaluationBot()
        evaluation_bot.create_time_graph()

if __name__ == '__main__':
    unittest.main()