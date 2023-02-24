def order_by_duplicate(words, indexes):
    # calculate the number of duplicates for each word
    num_duplicates = []
    for word in words:
        seen = set()
        duplicates = []

        for i in indexes:
            letter = word[i]
            if letter in seen:
                duplicates.append(letter)
            else:
                seen.add(letter)

        num_duplicates.append(len(duplicates))
       
    # sort the words based on the number of duplicates
    sorted_words = [word for _, word in sorted(zip(num_duplicates, words))]
    return sorted_words

def average_letter_frequency(words, indexes):
    # initialize a dictionary to store the frequency of each letter in the indexes
    freq_dict = {i: {} for i in indexes}

    # calculate the frequency of letters in the indexes for each word
    for word in words:
        for i in indexes:
            letter = word[i]
            freq_dict[i][letter] = freq_dict[i].get(letter, 0) + 1

    # calculate the average frequency for each word
    avg_freq = []
    for word in words:
        total_freq = sum([freq_dict[i].get(word[i], 0) for i in indexes])
        avg_freq.append(total_freq / len(indexes))
    
    # sort the words based on their average frequency
    sorted_words = [word for _, word in sorted(zip(avg_freq, words), reverse=True)]
    return sorted_words

def average_letter_frequency_whole(words, indexes):
    # initialize a dictionary to store the frequency of each letter
    freq_dict = {}

    # calculate the frequency of letters in the indexes for each word
    for word in words:
        for i in indexes:
            letter = word[i]
            freq_dict[letter] = freq_dict.get(letter, 0) + 1

    # calculate the average frequency for each word
    avg_freq = []
    for word in words:
        total_freq = sum([freq_dict.get(word[i], 0) for i in indexes])
        avg_freq.append(total_freq / len(indexes))
    
    # sort the words based on their average frequency
    sorted_words = [word for _, word in sorted(zip(avg_freq, words), reverse=True)]
    return sorted_words
