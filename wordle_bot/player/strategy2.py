from .skeleton import Player
from wordle_bot.utils import VocabUtil
from wordle_bot.evaluation_bot import Colour

class PlayerStrategy2(Player):
    def __init__(self, Wn, VN_DS, brute_force=False):
        self.Vn_structure = VN_DS(Wn)
        self.Wn = Wn
        self.colors = [-1]*len(Wn[0])

    def get_next_guess(self):
        indexes = self.colors
        for color, idx in enumerate(self.colors):
            if color != Colour.GREEN.value:
                indexes.append(idx)

        Vn_words = self.Vn_structure.get_Vn()
        Vn_words = VocabUtil.non_duplicate(Vn_words, indexes)
        Vn_words = VocabUtil.letter_frequency_same_index(Vn_words, indexes)
        Vn_words = VocabUtil.letter_frequency_cross_index(Vn_words, indexes)

        return Vn_words[0]

    def update_game_state(self, wordle_row):
        self.Vn_structure.update(word, colors)
        self.word = word
