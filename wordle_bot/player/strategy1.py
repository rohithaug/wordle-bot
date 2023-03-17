#from .skeleton import Player
#from .skeleton import Vn_DS
import skeleton
#from wordle_bot.evaluation_bot.evaluate import Colour
from tqdm import tqdm
import numpy as np

Player =  skeleton.Player

GY = 0 #Colour.GRAY.value
YE = 1 #Colour.YELLOW.value
GR = 2 #Colour.GREEN.value

class PlayerStrategy1_BruteForce(Player):
    def __init__(self, Wn):
        super().__init__()
        self.Wn = set(Wn)
        self.Vn = set(Wn) #list
    
    def update_game_state(self, word, colors):
        self.row = list(zip(word, colors))
        # update Vn
        self.Vn = self.get_Vn(self.row)
        print ("Vn size: ", len(self.Vn))

    def get_next_guess(self):
        if len(self.Vn) == 1:
            return list(self.Vn)[0]
        Vn_reduction_scores = [0]*len(self.Wn)
        print("Computing Vn reductions for each guess...")
        
        # convert Vn to numpy array for faster iteration
        # Vn is a set of strings of same length
        # numpy array will be of shape (|Vn|, len(Vn[0]))
        Wn = np.array(list(self.Wn))
        Vn = np.array(list(self.Vn))
        for i in tqdm(range(len(self.Wn))):
            guess = Wn[i]
            #print("Guess: ", guess)
            #print("Checking all possible wins...")
            # conver guess to numpy array for faster iteration
            #guess = np.array(list(guess))
            for win in (Vn):
                # update game state
                attempt = self.get_next_row(win, guess)
                # get new Vn
                #new_Vn = self.get_Vn(attempt)
                # calculate Vn reduction
                Vn_reduction = self.get_Vn(attempt, Vn, only_reduction=True)
                # update Vn reduction score
                Vn_reduction_scores[i] += Vn_reduction
        best_guess = Wn[np.argmax(Vn_reduction_scores)]
        return best_guess

        
        
    def get_next_row(self, win_word, guess):
        # create new attempt row as a list
        new_attempt = []
        for i in range(len(win_word)):
            letter = guess[i]
            # check all 3 conditions
            if letter in win_word:
                if win_word[i] == letter:
                    new_attempt.append([letter, GR])
                else:
                    new_attempt.append([letter, YE])
            else:
                new_attempt.append([letter, GY])
        return new_attempt
    
    def single_word_reduction(self, word, attempt):
        # check if word is reduced with attempt
        #print("Word: ", word)
        #assert False
        #print ("Attempt: ", attempt)
        for i, letter in enumerate(word):
            if attempt[i][1] == GY and attempt[i][0] in word:
                return 1
            elif attempt[i][1] == YE and (attempt[i][0] not in word or letter == attempt[i][0]):
                return 1
            elif attempt[i][1] == GR and letter != attempt[i][0]:
                return 1
        return 0
    
    def get_Vn_onlyreduction(self, last_attempt, Vn = None):
        reduction = 0
        #print("Last attempt: ", last_attempt)
        word_reduction = np.vectorize(lambda g : self.single_word_reduction(g, last_attempt))
        reduction = word_reduction(Vn).sum()
        return reduction

    def get_Vn_VnCopy(self, last_attempt):

        Vn_copy = set(self.Vn)

        for word in self.Vn:
            for i, letter in enumerate(word):
                if last_attempt[i][1] == GY and last_attempt[i][0] in word:
                    Vn_copy.remove(word)
                    break
                elif last_attempt[i][1] == YE and (last_attempt[i][0] not in word or letter == last_attempt[i][0]):
                    Vn_copy.remove(word)
                    break
                elif last_attempt[i][1] == GR and letter != last_attempt[i][0]:
                    Vn_copy.remove(word)
                    break
        
        return Vn_copy
    
    def get_Vn(self, last_attempt, Vn = None, only_reduction=False):
        if only_reduction:
            assert Vn is not None
            return self.get_Vn_onlyreduction(last_attempt, Vn)
        else:
            return self.get_Vn_VnCopy(last_attempt)

class PlayerStrategy1_Optimized(Player):
    def __init__(self, Wn):
        super().__init__()
        self.Wn = set(Wn)
        self.Vn = set(Wn)
        self.best_guess = self.compute_reductions()

    def get_next_row(self, win_word, guess):
        # create new attempt row as a list
        new_attempt = []
        for i in range(len(win_word)):
            letter = guess[i]
            # check all 3 conditions
            if letter in win_word:
                if win_word[i] == letter:
                    new_attempt.append([letter, GR])
                else:
                    new_attempt.append([letter, YE])
            else:
                new_attempt.append([letter, GY])
        return new_attempt

    def compute_reductions(self):
        # will be a dictionary of the form {guess : win : reduction}
        # and a dictionary of removals of the form {guess : reduction}
        # and a dictionary of removals of the form {removed : win} 
    
        self.guess_win_reductions = {} # mapping from guess to win to the reduction it causes
        self.removed2wins = {} # mapping from removal words to the wins that caused them for easy guess
        self.total_reductions = {} # mapping from guess to the total reduction it causes
        
        max_guess_reduction = float('-inf')
        best_guess = None

        print ("Computing Vn reductions for each guess...")
        for guess in tqdm(self.Wn):
            
            self.guess_win_reductions[guess] = {}
            self.total_reductions[guess] = 0
            self.removed2wins[guess] = {}
            
            for win in self.Vn:
                
                attempt = self.get_next_row(win, guess)
                reduction, removeds = self.get_Vn(attempt, only_reduction=True, ret_removed=True)
                
                self.guess_win_reductions[guess][win] = reduction
                self.total_reductions[guess] += reduction               
                
                for removed in removeds:
                    if removed not in self.removed2wins[guess]:
                        self.removed2wins[guess][removed] = set()
                    self.removed2wins[guess][removed].add(win)

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
                for win_causing_delete in self.removed2wins[guess][deleted]: # O(|removals|)
                    # prune the removals dictionary for free
                    if win_causing_delete in deleted_words: # O(|deleted_words|)
                        self.removed2wins[guess][deleted].remove(win_causing_delete) # O(1)
                    else:
                        self.guess_win_reductions[guess][win_causing_delete] -= 1 # O(1)
                        self.total_reductions[guess] -= 1 # O(1)
                
            # update the best guess
            if self.total_reductions[guess] > max_guess_reduction:
                max_guess_reduction = self.total_reductions[guess]
                best_guess = guess

        return best_guess

    def update_game_state(self, word, colors):
        self.row = list(zip(word, colors))
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

def get_color(guess, win):
    """
    :param guess: a string
    :param win: a string
    :return: a list of colors
    """
    colors = []
    for i, letter in enumerate(guess):
        if letter == win[i]:
            colors.append(GR)
        elif letter in win:
            colors.append(YE)
        else:
            colors.append(GY)
    return colors


import random

def play_random_game(Wn, brute_force=False):
    player = PlayerStrategy1(Wn, brute_force=brute_force)
    win = random.sample(Wn, 1)[0]
    guess = player.get_next_guess()
    while guess != win:
        player.update_game_state(guess, get_color(guess, win))
        guess = player.get_next_guess()
    


if __name__ == '__main__':
    DATA_FOLDER_PATH = "../../data/"
    ALL_VOCAB_FILENAME = "wordle-answers-alphabetical.txt"

    with open(DATA_FOLDER_PATH + ALL_VOCAB_FILENAME, "r") as f:
        corpus = f.read().splitlines()

    import numpy as np

    time_taken = []

    # play 500 games with Wn size increasing from 10 to 1000
    for i in r




if __name__ != '__main__':
    # test the player
    DATA_FOLDER_PATH = "../../data/"
    ALL_VOCAB_FILENAME = "wordle-answers-alphabetical.txt"

    import numpy as np

    # read and parse the text file
    with open(DATA_FOLDER_PATH + ALL_VOCAB_FILENAME, "r") as f:
        corpus = f.read().splitlines()
    
    corpus = [word.lower().strip() for word in corpus][:100]
    #print(corpus)
    #corpus.remove("shode")
    player = PlayerStrategy1(corpus, brute_force=True)
    #player.update_game_state("abhor", [GY, GY, GY, GY, GY])
    #player.update_game_state("piner", [YE, GY, GY, GR, GY])



    while True:
        guess = player.get_next_guess()
        print("Guess: {}".format(guess))
        print(player.player.Vn)
        # take color as input from user
        colors = input("Enter colors: ")
        colors = colors.split()
        colors = [int(color) for color in colors]
        player.update_game_state(guess, colors)
        




    

    






