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
    for i in range(len(word_list)-n+1):
        ngrams.append(word_list[i:i+n])
    return ngrams

def make_database(word_list, order):
    '''
    Takes in a list of words and creates a dictionary where the keys are every ngram and the 
    values are a list of every possible word that follows them (including duplicates).

    The keys are tuples so they will work in Python dictionaries. If ngrams occur multiple times
    in the word list, then they are appended to the list in the value, e.g. if the key size is 1
    and 'Gregor Samsa' is in the text 3 times, the dictionary will look like {('Gregor'):['Samsa','Samsa','Samsa']}

    EXAMPLE:
    With a order of 2 and the word_list as ['One', 'morning,', 'when', 'Gregor', 'Samsa', 'woke'],
    the function produces:
    {('One', 'morning,'): ['when'],
    ('morning,', 'when'): ['Gregor'],
    ('when', 'Gregor'): ['Samsa'],
    ('Gregor', 'Samsa'): ['woke']}
    '''
    database = {}
    for ngram in words_to_ngrams(n=order+1, word_list=word_list):
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
    Works by creating concatenting all last letters of words in the key and checking for any ending 
    punctuation marks.
    
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
    Returns a random key to start a generated sentence with from a dictionary.

    The key must fit the criteria of the functions key_has_valid_capitalization
    and key_has_valid_punctuation. 
    '''
    valid_start_keys = []
    for i in database.keys():
        if key_has_valid_capitalization(i) and key_has_valid_punctuation(i):
            valid_start_keys.append(i)
    return random.choice(valid_start_keys)

def main(filename, order, sentence_cutoff_length, ending_punctuation=['.', '?', '!']):
    '''
    Given a text file, this function will create a dictionary (called the database) which 
    indicates how often a certain word follows another given word or words. It will then 
    randomly generate a sentence using this database by making each word in the sentence 
    a random function of its predecessor(s). The order of the sentence indicates how many 
    predecessors are taken into account. A sentence with order-1 is constructed by randomly
    choosing a word that follows the previous one and might look like:

    "Drops of greeting and her hurry she approached the unknown nourishment he thought."

    A sentence with order-2 or order-3 would likely look more realistic (possibly because
    depending on the text it can copy entire sentences)

    A generated sentence is returned if it reaches a word that ends in ending_punctuation or 
    it reaches sentence_cutoff_length. If the function can't proceed because the last few words 
    in the generated sentence don't occur anywhere in the text, it restarts the process. 
    '''
    words = file_to_words(filename)
    database = make_database(words, order)
    while True:
        return_sentence = True
        generated_words = list(find_start_seed(database, ending_punctuation))
        while (len(generated_words) < sentence_cutoff_length) and (generated_words[-1][-1] not in ending_punctuation):
            try:#possibly shorten
                next_word = generated_words[-order:]
                next_word = tuple(next_word)
                next_word = random.choice(database[next_word])
            except KeyError:
                return_sentence = False
                break
            generated_words.append(next_word)
        if return_sentence:
            return ' '.join(generated_words)

if __name__ == "__main__":
    print(main (filename='metamorphosis', order=2, sentence_cutoff_length=100))

'''
Future Improvements (No guarantee of readability):
>Store non-proper nouns as lowercase?
>Add command line support.
>Convert functions to generators where useful for performance.
>Possible problem with conversion to tuple, list(('cat')) returns ('c','a','t').
Might cause issues with order=1, but it hasn't so far.
>Consider switching from having tuple keys to string keys.
>Instead of essentially stepping with (order = 1) if a key
isn't in the dictionary, construct databases for order ... 2.
This means that if a key of length 4 isn't in the dictionary, it tries
the last 3 words, then the last 2, and then just randomly selects from
words that follow the last word, instead of going straight to the last step.
'''
