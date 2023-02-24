import nltk
import pickle

nltk.download('words')

english_vocab = set(w.lower() for w in nltk.corpus.words.words())

five_letter_words = [w for w in english_vocab if len(w) == 5]

print(len(five_letter_words))

with open('five_letter_words.pickle', 'wb') as f:
    pickle.dump(five_letter_words, f)

# REFERENCE: retrieve the list of 5-letter words from the file
# with open('five_letter_words.pickle', 'rb') as f:
#     retrieved_words = pickle.load(f)
