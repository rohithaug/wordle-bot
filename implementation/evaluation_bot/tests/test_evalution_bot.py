import unittest

from evaluate import evaluate_guessed_word, is_valid_word
from evaluate import read_valid_vocab # move this to some other utils file
from evaluate import Colour


class EvaluationBotTest(unittest.TestCase):

    def test_evaluate_guessed_word(self):
        res = evaluate_guessed_word("APPLE", "apple")
        assert res == [Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value]

        res = evaluate_guessed_word("mAnGo", "MANGO")
        assert res == [Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value, Colour.GREEN.value]

        res = evaluate_guessed_word("puppy", "funny")
        assert res == [Colour.GRAY.value, Colour.GREEN.value, Colour.GRAY.value, Colour.GRAY.value, Colour.GREEN.value]

        res = evaluate_guessed_word("puppy", "apple")
        assert res == [Colour.YELLOW.value, Colour.GRAY.value, Colour.GREEN.value, Colour.YELLOW.value, Colour.GRAY.value]

        res = evaluate_guessed_word("zzzzz", "apple")
        assert res == [Colour.GRAY.value, Colour.GRAY.value, Colour.GRAY.value, Colour.GRAY.value, Colour.GRAY.value]

    def test_is_valid_word():
        corpus = read_valid_vocab()
        res = is_valid_word("apple", corpus)
        
        assert res == True

        res = is_valid_word("zzzzz", corpus)
        assert res == False

        res = is_valid_word("appl", corpus)
        assert res == False

        res = is_valid_word("ball", corpus)
        assert res == False