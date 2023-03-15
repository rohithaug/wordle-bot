class Vn_DS:
    def __init__(self, Wn):
        pass

    def update(self, word, colors):
        raise NotImplementedError

    def get_Vn(self):
        raise NotImplementedError


class Player:
    def __init__(self, Wn, VN_DS, brute_force=False):
        self.brute_force = brute_force
        self.Vn_structure = VN_DS(Wn)

    def get_next_guess(self):
        raise NotImplementedError

    def update_game_state(self, wordle_row):
        raise NotImplementedError

