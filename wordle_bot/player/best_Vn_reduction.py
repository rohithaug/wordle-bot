def update_game_state(guess, win_word, game):
    """
    :param guess: string
    :param game: Game state is a mxnx2 matrix .
    Each row contains each word attempt.
    Each index of a word attempt contains a letter and a integer
    representing the status of the letter. 0 means not guessed, 1 means
    letter not present in winning word, 2 means letter present in winning
    word but not in correct position, 3 means letter present in winning word
    and in correct position.
    :return: Updated game state
    """
    game = game.copy()
    
    # create new attempt row as a list
    new_attempt = []
    for i, letter in enumerate(guess):
        # check all 3 conditions
        if letter in win_word:
            if win_word[i] == letter:
                new_attempt.append([letter, 3])
            else:
                new_attempt.append([letter, 2])
        else:
            new_attempt.append([letter, 1])

    # append new attempt to game state
    #game.append(new_attempt)
    
    return new_attempt

def get_Vn(last_attempt, Vn_copy, verbose=True):
    """
    :param game: Game state is a mxnx2 matrix .
    Each row contains each word attempt.
    Each index of a word attempt contains a letter and a integer
    representing the status of the letter. 0 means not guessed, 1 means
    letter not present in winning word, 2 means letter present in winning
    word but not in correct position, 3 means letter present in winning word
    and in correct position.
    :param Vn: List of all possible winning words given the current game state
    :return: List of all possible winning words given the current game state
    """
    Vn_copy = Vn.copy()
    
    last_attempt = game[-1]
    if verbose:
        print("last_attempt: ", last_attempt)
    for word in Vn:
        if verbose:
            print("word: ", word)
        for i, letter in enumerate(word):
            if last_attempt[i][1] == 1 and last_attempt[i][0] in word:
                Vn_copy.remove(word)
                break
            elif last_attempt[i][1] == 2 and (last_attempt[i][0] not in word or letter == last_attempt[i][0]):
                Vn_copy.remove(word)
                break
            elif last_attempt[i][1] == 3 and letter != last_attempt[i][0]:
                Vn_copy.remove(word)
                break

            if verbose:
                print("Didn't remove word: ", word)
    
    return Vn_copy


def best_next_guess(game, Vn, Wn):
    """
    :param game: Game state is a mxnx2 matrix .
    Each row contains each word attempt.
    Each index of a word attempt contains a letter and a integer
    representing the status of the letter. 0 means not guessed, 1 means
    letter not present in winning word, 2 means letter present in winning
    word but not in correct position, 3 means letter present in winning word
    and in correct position.
    :param Vn: List of all possible winning words given the current game state
    :param Wn: List of all possible words (vocab) that can be used to guess
    :return: Best next guess chosen from Wn
    """
    Vn_reduction_scores = [0]*len(Wn)
    for i, guess in enumerate(Wn):
        for win in Vn:
            # update game state
            attempt = update_game_state(guess, win, game)
            # get new Vn
            new_Vn = get_Vn(attempt, Vn)
            # calculate Vn reduction
            Vn_reduction = len(Vn) - len(new_Vn)
            # update Vn reduction score
            Vn_reduction_scores[i] += Vn_reduction
    
    print(Vn_reduction_scores)

    # get best guess
    best_guess = Wn[Vn_reduction_scores.index(max(Vn_reduction_scores))]
    return best_guess

if __name__ == '__main__':
    # create game state
    game = []
    # Wn
    Wn = ['ABCD', 'ABCE', 'ABCF', 'ABCG', 'DEFG']
    # Vn
    Vn = ['ABCD', 'ABCE', 'ABCF', 'ABCG', 'DEFG']
    
    # get best guess
    best_guess = best_next_guess(game, Vn, Wn)
    print(best_guess)


        
        
    
