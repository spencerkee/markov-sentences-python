#!/usr/bin/env python
import random

def file_to_words(filename):
    '''
    Converts a text file into a list of words.

    It applies the method split() on each line with whitespace as the separator.

    EXAMPLE:
    A file containing "One morning, when Gregor Samsa woke" would be converted
    to ['One', 'morning,', 'when', 'Gregor', 'Samsa', 'woke']
    '''
    words = []
    with open(filename,'r') as f:
        for line in f:
            for word in line.split():
               words.append(word)
    return words

def words_to_ngrams(n, word_list):
    '''
    Converts a list of words into a list of ngrams (a sequence of n words)

    EXAMPLE:
    ['One', 'morning,', 'when', 'Gregor', 'Samsa', 'woke'] 
    would convert to:
    [['One', 'morning,', 'when'], 
    ['morning,', 'when', 'Gregor'], 
    ['when', 'Gregor', 'Samsa'], 
    ['Gregor', 'Samsa', 'woke']]

    '''
    ngrams = []
    for i in range(len(words)-n+1):
        ngrams.append(words[i:i+n])
    return ngrams

def make_database(word_list, num_key_words):
    '''
    Takes in a list of words and creates a dictionary where the keys are every ngram and the 
    values are a list of every possible word that follows them (including duplicates).

    The keys are tuples so they will work in Python dictionaries. If ngrams occur multiple times
    in the word list, then they are appended to the list in the value, e.g. if the key size is 1
    and 'Gregor Samsa' is in the text 3 times, the dictionary will look like {('Gregor'):['Samsa','Samsa','Samsa']}

    EXAMPLE:
    With a num_key_words of 2 and the word_list as ['One', 'morning,', 'when', 'Gregor', 'Samsa', 'woke'],
    the function produces:
    {('One', 'morning,'): ['when'],
    ('morning,', 'when'): ['Gregor'],
    ('when', 'Gregor'): ['Samsa'],
    ('Gregor', 'Samsa'): ['woke']}
    '''
    database = {}
    for ngram in words_to_ngrams(n=num_key_words+1, word_list=word_list):
        key = tuple(ngram[0:len(ngram)-1])
        try:
            database[key] = database[key] + [ngram[-1]]
        except KeyError:
            database[key] = [ngram[-1]]
    return database

def key_has_valid_punctuation(key, ending_punctuation=['.', '?', '!']):
    '''
    Returns True if a key has no words that end in certain punctuation. 

    This is used so that generated sentences don't look like "all she wrote? Gregor kicked the ball."
    Works by creating concatenting all last letters of words in the key and checking for any ending punctuation marks
    
    EXAMPLE: 
    ('One', 'morning,') = True
    ('Gregor', 'Samsa') = True
    ('when', 'Gregor') = False
    '''
    return not any(punctuation in ''.join([i[-1] for i in key]) for punctuation in ending_punctuation)

def key_has_valid_capitalization(key):
    '''
    Returns True if the first letter of the first word is uppercase.

    This is used so that the generated sentences begin more realistically.

    EXAMPLE: 
    ('One', 'morning,') = True
    ('vermin.', 'He') = False
    '''
    return key[0][0][0].isupper()

def find_start_seed(database, ending_punctuation=['.', '?', '!']):
    '''
    Picks a random key to start a generated sentence with from a dictionary.

    The key must fit the criteria of the functions key_has_valid_capitalization
    and key_has_valid_punctuation. 
    '''
    valid_start_keys = []
    for i in database.keys():
        if key_has_valid_capitalization(i) and key_has_valid_punctuation(i):
            valid_start_keys.append(i)
    return random.choice(valid_start_keys)

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
