#!/bin/python

# Class to expose the classifier
# Inputs set of training data
# The training data needs to be formatted one tweet per line

class NBClassifier:

	def get_word_dictionary(self, tweet_array):
		dictionary = {}
		for (review, sentiment) in tweet_array:
			for word in review.split(' '):
				#print word
				try:
					dictionary[word][sentiment] += 1
				except:
					dictionary[word] = {"neg":1, "pos":1, "neutral":1}
					dictionary[word][sentiment] += 1
		return dictionary
	
	def total_neg_words(self):
		count = 0
		for key in self.sentiment_dictionary:
			count += self.sentiment_dictionary[key]['neg']
		return count

	def total_pos_words(self):
		count = 0
		for key in self.sentiment_dictionary:
			count += self.sentiment_dictionary[key]['pos']
		return count

	def total_neu_words(self):
		count = 0
		for key in self.sentiment_dictionary:
			count += self.sentiment_dictionary[key]['neutral']
		return count

	def prob_word_given_pos(self, some_word):
		try:
			pos_score = self.sentiment_dictionary[some_word]['pos']
		except:
			pos_score = 1
		return float(pos_score)/float(self.totalPos)

	def prob_word_given_neg(self, some_word):
		try:
			neg_score = self.sentiment_dictionary[some_word]['neg']
		except:
			neg_score = 1
		return float(neg_score)/float(self.totalNeg)

	def prob_word_given_neutral(self, some_word):
		try:
			neutral_score = self.sentiment_dictionary[some_word]['neutral']
		except:
			neutral_score = 1

		return float(neutral_score)/float(self.totalNeutral)

	def test_sentence(self, sentence):
		pos = 1.0
		neg = 1.0
		neutral = 1.0
		sent = {'pos':0, 'neg':0}
		for word in sentence.split(' '):
			pos *= self.prob_word_given_pos(word)
			neg *= self.prob_word_given_neg(word)
			neutral *= self.prob_word_given_neutral(word)
		sum_ = pos + neg + neutral
		sent['pos'] += (pos + (neutral/2))/sum_
		sent['neg'] += (neg + (neutral/2))/sum_
		#print json.dumps(sent)
		return sent

	def __init__(self, pos_training, neg_training):
		self.pos_tweets = open(pos_training, 'r').readlines()
		self.neg_tweets = open(neg_training, 'r').readlines()
		self.tweet_array = []

		## fill array with tuples of (line, sentiment)
		for line in self.pos_tweets:
			self.tweet_array.append((line, 'pos'))
		for line in self.neg_tweets:
			self.tweet_array.append((line, 'neg'))

		self.sentiment_dictionary = self.get_word_dictionary(self.tweet_array)

		# count sum up pos, neg, neutral
		self.totalPos = self.total_pos_words()
		self.totalNeg = self.total_neg_words()
		self.totalNeutral = self.total_neu_words()
