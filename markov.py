import random

def file_to_words(filename):
    '''
    Converts a text file into a list of word strings.
    '''
    words = []
    with open(filename,'r') as f:
        for line in f:
            for word in line.split():
               words.append(word)
    return words

def ngrams(num_key_words, word_list):
    '''
    Iterates through the list of word strings and returns all groups of
    num_key_words + 1 strings in a list.
    '''
    for i in range(len(word_list)-num_key_words):
        yield word_list[i:i+num_key_words+1]

def make_database(word_list, num_key_words):
    '''
    Returns a dictionary where the keys are all num_key_words length
    adjacent string sequences in the word_list and the values are
    all words (including duplicates) that imediately follow the key.
    '''
    database = {}
    for ngram in ngrams(num_key_words=num_key_words, word_list=word_list):
        key = tuple(ngram[0:len(ngram)-1])
        try:
            database[key] = database[key] + [ngram[-1]]
        except KeyError:
            database[key] = [ngram[-1]]
    return database

def find_start_keys(database):
    '''
    Returns keys in a database where the first letter of the
    first word is uppercase.
    '''
    start_keys = []
    for key in database.keys():
        if key[0][0].isupper():
            start_keys.append(key)
    return start_keys

def find_valid_seed(database, ending_punctuation):
    '''
    Generates a list of start keys, shuffles and iterates through them, and returns the first one that
    contains no strings in the list ending_punctuation.
    Ex: ['The', 'dog', 'jumped.'] wouldn't be returned because there's a '.' but ['No','way'] would be.
    '''
    possible_start_keys = find_start_keys(database)
    random.shuffle(possible_start_keys)
    for start_key in possible_start_keys:
        if not any(punctuation in ''.join(start_key) for punctuation in ending_punctuation):
            return list(start_key)

def main(filename, num_key_words, chain_length, ending_punctuation=['.', '?', '!']):
    '''
    Given a file, create a database and generate a sentence beginning with
    a random starting key. To generate the next word, check if the last
    num_key_words are in the database. If so, randomly select the next word
    from the words that follow the last num_key_words. If not, pick a word
    at random from the words that follow the last word in the sentence. If
    a word is generated that ends in ending_punctuation or the sentence
    length reaches chain_length, break and return the sentence as a joined string.
    '''
    words = file_to_words(filename)
    database = make_database(words, num_key_words)
    gen_words = find_valid_seed(database, ending_punctuation)

    while (len(gen_words) < chain_length) and (gen_words[-1][-1] not in ending_punctuation):
        try:
            next_word = random.choice(database[tuple(gen_words[-num_key_words:])])
        except KeyError:
            possible_next_words = []
            for i in range(len(words)):
                if words[i] == gen_words[-1]:
                    possible_next_words.append(words[i+1])#what if only word is at the end?
            next_word = random.choice(possible_next_words)
        gen_words.append(next_word)
    print (' '.join(gen_words))

if __name__ == "__main__":
    main (filename='metamorphosis', num_key_words=4, chain_length=100)

'''
Future Improvements:
>Instead of essentially stepping with (num_key_words = 1) if a key
isn't in the dictionary, construct databases for num_key_words ... 2.
This means that if a key of length 4 isn't in the dictionary, it tries
the last 3 words, then the last 2, and then just randomly selects from
words that follow the last word, instead of going straight to the last step.
>Create one function find_valid_seed() that performs the same as
find_start_keys() and valid_seed()
>Store non-proper nouns as lowercase?
>Add command line support.
>Add error handling.
>Convert functions to generators where useful for performance
>Add examples to function descriptions
'''
