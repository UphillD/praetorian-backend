#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# CO-specific functionality

import cv2
import numpy
import re
import urllib

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
	return(prediction.iat[0, 2] == 'informative')

def classify_image(image_url, image_model):
	# Open image
	r = urllib.request.urlopen(image_url)
	# Transform image to numpy array
	a = numpy.asarray(bytearray(r.read()), dtype=numpy.uint8)
	# Expand image dimensions from 3 to 4
	image = numpy.expand_dims(cv2.imdecode(a, -1), axis=0)
	# Predict
	return(image_model.predict(image)[0][0] == 1.0)

def classifyTweet(tweet, _, text_model, image_model):

	# Initialize found flag
	found = False
	text = tweet['data']['text']

	# CLASSIFICATION
	# Classify the tweet's text
	found = classify_text(text, text_model):
	# Classify the tweet's media
	if not found and 'media' in tweet['includes']:
		for media in tweet['includes']['media']:
			if classify_image(media['url'], image_model):
				found = True
				break

	# TAGGING
	# Surround words matching crawling rules with '&'
	for rule in tweet['matching_rules']:
		for word in rule['tag']:
			text = text.replace(word, '&' + word + '&')

	# CLASSIFICATION
	# Classify the tweet's images
	return(found, text, None)
