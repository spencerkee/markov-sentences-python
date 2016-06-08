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
	Finds a key in a database where the first letter of the
	first word is uppercase.
	'''
	start_keys = []
	for key in database.keys():
		if key[0][0].isupper():
			start_keys.append(key)
	return start_keys

def valid_seed(seed):
	'''
	Returns True if there are no ending_punctuation marks in
	a list of strings and False otherwise.
	'''
	ending_punctuation = ['.', '?', '!']
	for word in seed:
		for punctuation in ending_punctuation:
			if punctuation in word:
				return False
	return True

def main(filename, num_key_words, chain_length):
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
	ending_punctuation = ['.', '?', '!']
	start_words = find_start_keys(database)
	seed = ['.']
	while valid_seed(seed) == False:
		seed = random.choice(start_words)
	gen_words = list(seed)

	while (len(gen_words) < chain_length) and (gen_words[-1][-1] not in ending_punctuation):
		try:
			next_word = database[tuple(gen_words[-3:])]#not sure if necessary
		except KeyError:
			possible_next_words = []
			for i in range(len(words)):
				if words[i] == gen_words[-1]:
					possible_next_words.append(words[i+1])#what if only word is at the end?
			next_word = random.choice(possible_next_words)
		gen_words.append(next_word)
	print (' '.join(gen_words))

if __name__ == "__main__":
	main ('metamorphosis', 4, 100)

'''
Future Improvements:
>Store everything as lowercase.
>Instead of essentially stepping with (num_key_words = 1) if a key \
isn't in the dictionary, construct databases for num_key_words ... 2.
This means that if a key of length 4 isn't in the dictionary, it tries
the last 3 words, then the last 2, and then just randomly selects from
words that follow the last word, instead of going straight to the last step.
>Add command line support.
'''
