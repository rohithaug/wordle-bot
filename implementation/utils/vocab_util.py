# %%
ALL_VOCAB_FILENAME = "five_letter_words.pickle"
PICKLE_FOLDER_PATH = "../data/"

# %%
import pickle, os
def read_valid_vocab(filename):
    words = []
    with (open(filename, "rb")) as openfile:
      words = pickle.load(openfile)
    
    print(len(words))
    return words

words = read_valid_vocab(os.path.join(PICKLE_FOLDER_PATH, ALL_VOCAB_FILENAME))


# %%



