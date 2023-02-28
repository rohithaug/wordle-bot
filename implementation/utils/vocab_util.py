ALL_VOCAB_FILENAME = "five_letter_words.pickle"
PICKLE_FOLDER_PATH = "../data/"

import pickle, os
def read_valid_vocab(filename = ALL_VOCAB_FILENAME):
    words = []
    filepath = os.path.join(PICKLE_FOLDER_PATH, filename)
    with (open(filepath, "rb")) as openfile:
      words = pickle.load(openfile)
    
    # print(len(words))
    return words

corpus = read_valid_vocab(ALL_VOCAB_FILENAME)