#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# CO-specific functionality

import re

tag_rules = 'lexicon_CO'
tag_identifiers = ''
tag_tweets = 'CO_tweets'
a = 2
b = 3

def cleanup_text(text):
	text = text.replace('Disclaimer: This tweet contains false information.', '')
	text = re.sub(r'@\S+', '', text)            # Remove mentions
	text = re.sub(r'http\S+', '<link>', text)   # Remove URLs
	text = re.sub(r'[\W]', ' ', text)           # Remove symbols
	text = " ".join(text.split())               # Remove duplicate spaces
	text = text.strip()                         # Remove heading or trailing spaces
	return(text)

# Classify a tweet's text
def classify_text(text, model):
	text_clean = [ cleanup_text(text) ]
	prediction = model.predict(text_clean)
	if prediction.iat[0, 2] == 'informative':
		return(True)
	else:
		return(False)

def classifyTweet(tweet, _, text_model, image_model):

	# Initialize found flag
	found = False

	# DATA EXTRACTION
	# Classify the tweet's text
	text = tweet['data']['text']
	if classify_text(text, text_model):
		found = True

	# TAGGING
	# Surround words matching crawling rules with '&'
	for rule in tweet['matching_rules']:
		for word in rule['tag']:
			text = text.replace(word, '&' + word + '&')

	# CLASSIFICATION
	# Classify the tweet's images
	return(found, text, None)
