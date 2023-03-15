class Vn_DS:
    def __init__(self, Wn):
        pass

    def update(self, word, colors):
        raise NotImplementedError

    def get_Vn(self):
        raise NotImplementedError


class Player:
    def __init__(self, Wn = None, Vn_DS = None, brute_force=False):
        pass

    def get_next_guess(self):
        raise NotImplementedError

    def update_game_state(self, word, colors):
        raise NotImplementedError

