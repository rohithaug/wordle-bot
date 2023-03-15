

import random
class EvaluationUtils:



    #function to generate a random 5 letter word
    def generate_random_word():
        import random
        import string
        return ''.join(random.choice(string.ascii_lowercase) for i in range(5))

    # function to select a random word from the corpus
    def select_correct_word(corpus):
        return random.choice(corpus)