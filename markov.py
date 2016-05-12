import random

def file_to_words(filename):
	words = []
	with open(filename,'r') as f:
		for line in f:
			for word in line.split():
			   words.append(word)
	return words

def ngrams(num_key_words, word_list):
	for i in range(len(word_list)-num_key_words):
		yield word_list[i:i+num_key_words+1]

def make_database(word_list, num_key_words):
	database = {}
	for ngram in ngrams(num_key_words=num_key_words, word_list=word_list):
		key = tuple(ngram[0:len(ngram)-1])
		database[key] = ngram[-1]
	return database

def find_start_keys(database):#names and start words
	start_keys = []
	for key in database.keys():
		if key[0][0].isupper():
			start_keys.append(key)
	return start_keys

def valid_seed(seed):
	ending_punctuation = ['.', '?', '!']
	for word in seed:
		for punctuation in ending_punctuation:
			if punctuation in word:
				return False
	return True

def main(filename, num_key_words, chain_length):#make smaller and smaller databases
	words = file_to_words(filename)
	database = make_database(words, num_key_words)
	ending_punctuation = ['.', '?', '!']
	start_words = find_start_keys(database)
	seed = ['.']
	while valid_seed(seed) == False:#needs to be rewritten for all ending marks
		seed = random.choice(start_words)
	gen_words = list(seed)

	while len(gen_words) < chain_length and gen_words[-1][-1] not in ending_punctuation:
		try:
			next_word = database[tuple(gen_words[-3:])]#not sure if necessary
		except KeyError:
			possible_next_words = []
			for i in range(len(words)):
				if words[i] == gen_words[-1]:
					possible_next_words.append(words[i+1])#what if only word is at the end?
			next_word = random.choice(possible_next_words)
		gen_words.append(next_word)
	print ' '.join(gen_words)

for i in range(4):
	main ('portrait', 4, float('inf'))


#replace things with correct general things, like names
#store everything as lower, so these only caps things dont happen

# seed = ('cat','dog')
# print any('.' in i or '?' in i or '!' in i for i in seed)