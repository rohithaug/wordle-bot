from .skeleton import Player
from .skeleton import Vn_DS

class PlayerStrategy1(Player):
    def __init__(self, Wn, Vn_ds = Vn_DS, brute_force=False):
        super().__init__(Wn, Vn_ds, brute_force)
    
    def update_game_state(self, word, colors):
        self.Vn_structure.update(word, colors)
        self.word = word
        self.colors = colors

    def get_next_guess(self):
        if self.brute_force:
            return self.get_next_guess_brute_force()
        else:
            return self.get_next_guess_optimized()
        
    def get_next_guess_brute_force(self):
        




