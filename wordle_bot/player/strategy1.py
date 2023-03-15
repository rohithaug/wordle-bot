from .skeleton import Player
from .skeleton import Vn_DS
from evaluation_bot.evaluate import Colour

GY = Colour.GRAY.value
YE = Colour.YELLOW.value
GR = Colour.GREEN.value

class PlayerStrategy1_BruteForce(Player):
    def __init__(self, Wn):
        super().__init__()
        self.Wn = set(Wn)
        self.Vn = set(Wn) #list
    
    def update_game_state(self, word, colors):
        self.row = zip(word, colors)
        # update Vn
        self.Vn = self.get_Vn(self.row)

    def get_next_guess(self):
        Vn_reduction_scores = [0]*len(self.Wn)
        for i, guess in enumerate(self.Wn):
            for win in self.Vn:
                # update game state
                attempt = self.get_next_row(win, guess)
                # get new Vn
                new_Vn = self.get_Vn(attempt)
                # calculate Vn reduction
                Vn_reduction = - len(new_Vn)
                # update Vn reduction score
                Vn_reduction_scores[i] += Vn_reduction
        best_guess = self.Wn[Vn_reduction_scores.index(max(Vn_reduction_scores))]
        return best_guess

        
        
    def get_next_row(self, win_word, guess):
        # create new attempt row as a list
        new_attempt = []
        for i, letter in enumerate(guess):
            # check all 3 conditions
            if letter in win_word:
                if win_word[i] == letter:
                    new_attempt.append([letter, GR])
                else:
                    new_attempt.append([letter, YE])
            else:
                new_attempt.append([letter, GY])
        return new_attempt
    
    def get_Vn(self, last_attempt, only_reduction=False):
        reduction = 0
        
        # saves O(|Vn|) time by not copying Vn if only reduction is needed
        if not only_reduction:
            Vn_copy = set(self.Vn)        
        
        for word in self.Vn:
            for i, letter in enumerate(word):
                if last_attempt[i][1] == GY and last_attempt[i][0] in word:
                    reduction += 1
                    if not only_reduction:
                        Vn_copy.remove(word)
                    break
                elif last_attempt[i][1] == YE and (last_attempt[i][0] not in word or letter == last_attempt[i][0]):
                    reduction += 1
                    if not only_reduction:
                        Vn_copy.remove(word)
                    break
                elif last_attempt[i][1] == GR and letter != last_attempt[i][0]:
                    reduction += 1
                    if not only_reduction:
                        Vn_copy.remove(word)
                    break
        
        if only_reduction:
            return reduction
        else:
            return Vn_copy

class PlayerStrategy1_Optimized(Player):
    def __init__(self, Wn):
        super().__init__()
        self.Wn = set(Wn)
        self.Vn = set(Wn)
        self.best_guess = self.compute_reductions()

    def compute_reductions(self):
        # will be a dictionary of the form {guess : win : reduction}
        # and a dictionary of removals of the form {guess : reduction}
        # and a dictionary of removals of the form {removed : win} 
    
        self.guess_win_reductions = {} # mapping from guess to win to the reduction it causes
        self.removed2wins = {} # mapping from removal words to the wins that caused them
        self.total_reductions = {} # mapping from guess to the total reduction it causes
        
        max_guess_reduction = float('-inf')
        best_guess = None

        for guess in self.Wn:
            
            self.guess_win_reductions[guess] = {}
            self.total_reductions[guess] = 0
            
            for win in self.Vn:
                
                attempt = self.get_next_row(win, guess)
                reduction, removeds = self.get_Vn(attempt, only_reduction=True, ret_removed=True)
                
                self.guess_win_reductions[guess][win] = reduction
                self.total_reductions[guess] += reduction               
                
                for removed in removeds:
                    if removed not in self.removed2wins:
                        self.removed2wins[removed] = set()
                    self.removed2wins[removed].add(win)

            if self.total_reductions[guess] > max_guess_reduction:
                max_guess_reduction = self.total_reductions[guess]
                best_guess = guess

        return best_guess

    def update_reductions(self, deleted_words):
        max_guess_reduction = float('-inf')
        best_guess = None
        for guess in self.Wn: # O(|Wn|)
            for deleted in deleted_words: # O(|deleted_words|)
                # update the guess_reductions dictionary
                self.total_reductions[guess] -= self.guess_win_reductions[guess][deleted] # O(1)
                del self.guess_win_reductions[guess][deleted]  # O(1)
                for win_causing_delete in self.removed2wins[deleted]: # O(|removals|)
                    # prune the removals dictionary for free
                    if win_causing_delete in deleted_words: # O(|deleted_words|)
                        self.removed2wins[deleted].remove(win_causing_delete) # O(1)
                    else:
                        self.guess_win_reductions[guess][win_causing_delete] -= 1 # O(1)
                        self.total_reductions[guess] -= 1 # O(1)
                
            # update the best guess
            if self.total_reductions[guess] > max_guess_reduction:
                max_guess_reduction = self.total_reductions[guess]
                best_guess = guess

        return best_guess

    def update_game_state(self, word, colors):
        self.row = zip(word, colors)
        # update Vn
        self.Vn, removed = self.get_Vn(self.row, ret_removed=True)
        # update reductions
        self.best_guess = self.update_reductions(removed)


    def get_Vn(self, last_attempt, only_reduction = False, ret_removed = False):
        reduction = 0
        
        if not only_reduction:
            Vn_copy = set(self.Vn)

        removed = set()
        
        for word in self.Vn:
            for i, letter in enumerate(word):
                if last_attempt[i][1] == GY and last_attempt[i][0] in word:
                    reduction += 1
                    if not only_reduction:
                        Vn_copy.remove(word)
                    if ret_removed:
                        removed.add(word)
                    break
                elif last_attempt[i][1] == YE and (last_attempt[i][0] not in word or letter == last_attempt[i][0]):
                    reduction += 1
                    if not only_reduction:
                        Vn_copy.remove(word)
                    if ret_removed:
                        removed.add(word)
                    break
                elif last_attempt[i][1] == GR and letter != last_attempt[i][0]:
                    reduction += 1
                    if not only_reduction:
                        Vn_copy.remove(word)
                    if ret_removed:
                        removed.add(word)
                    break
 
        if only_reduction:
            return reduction, removed
        else:
            return Vn_copy, removed

    def get_next_guess(self):
        """
        :return: a string
        """
        return self.best_guess

class PlayerStrategy1(Player):
    def __init__(self, Wn, brute_force=False):
        super().__init__()
        if brute_force:
            self.player = PlayerStrategy1_BruteForce(Wn)
        else:
            self.player = PlayerStrategy1_Optimized(Wn) 
    
    def update_game_state(self, word, colors):
        self.player.update_game_state(word, colors)

    def get_next_guess(self):
        return self.player.get_next_guess()







