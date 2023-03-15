from .skeleton import Player
from .skeleton import Vn_DS

class PlayerStrategy1(Player):
    def __init__(self, Wn, Vn_ds = Vn_DS, brute_force=False):
        self.brute_force = brute_force
        self.Vn_structure = Vn_ds(Wn)
        self.Wn = Wn
    
    def update_game_state(self, wordle_row):
        self.Vn_structure.update(wordle_row)

    def get_next_guess(self):
        if self.brute_force:
            return self.get_next_guess_brute_force(game, Vn, Wn)
        else:
            return self.get_next_guess_optimized(game, Vn, Wn)
        
    def get_next_guess_brute_force(self, Wn):



