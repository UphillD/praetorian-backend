#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# Main implementation (SMSTD & CO)

import array
import json
import time

import keras
import nlu
import requests

from common import config
from common import iop
from common import twitter



# Initializes text classifier
def init_text_classifier():
	time_start = time.perf_counter()
	model = nlu.load(path=config.text_model_path)
	logger.success('Text model loaded in {:.2f} seconds.'.format(time.perf_counter() - time_start))
	return(model)

# Initializes image classifier
def init_image_classifier():
	time_start = time.perf_counter()
	model = keras.models.load_model(config.image_model_path)
	logger.success('Image model loaded in {:.2f} seconds.'.format(time.perf_counter() - time_start))
	return(model)



if __name__ == '__main__':

	# Get logger configuration
	logger = config.logger

	# Initialize tweet counter array
	# SMSTD Crawled | SMSTD Suspicious | CO Crawled | CO Informative
	# type: unsigned short (max 65535)
	cnt = array.array('H', [0, 0, 0, 0])

	# Initialize classification models
	#text_model = init_text_classifier()
	text_model = None
	#image_model = init_image_classifier()
	image_model = None

	logger.info('Process ready to start.')

	status = iop.get_status()
	# inf loop
	while(True):

		if not status:
			time.sleep(1)
			status = iop.get_status()
		else:
			if status == 'SMSTD':
				from common.SMSTD import *
			elif status == 'CO':
				from common.CO import *
			logger.info('{} process running...'.format(status))
			# Get new rules from IOP
			rules = iop.get_rules(tag_rules)
			# Get old rules from twitter
			old_rules = twitter.get_rules()
			# Delete old rules from twitter
			twitter.delete_rules(old_rules)
			# Set new rules on twitter
			twitter.set_rules(rules)
			# Get identifiers from IOP
			identifiers = (iop.get_identifiers(tag_identifiers) if status == 'SMSTD' else None)
			logger.success('Initiating twitter stream...')

			# Start twitter stream
			r = requests.get(config.urls['twitter']['stream'], auth=twitter.bearer_oauth, params=config.query_params, stream=True)
			try:
				r.raise_for_status()
			except:
				logger.error('Failed initiating twitter stream (HTTP {}): {}'.format(r.status_code, r.text))
				sys.exit(-1)
			for line in r.iter_lines():
				if line:
					cnt[a] += 1
					# Load tweet object
					tweet = json.loads(line)
					# Classify tweet as pertinent or not
					classification, annotated_tweet = classifyTweet(tweet, identifiers, text_model, image_model)
					if classification:
						cnt[b] += 1
						payload = json.dumps({ 'tweet': tweet, 'text': annotated_tweet, 'collection': tag_tweets })
						r = requests.post(config.urls['iop']['socialMedia'], params=config.query, data=payload, headers=config.headers)
						try:
							r.raise_for_status()
						except:
							logger.error('Failed registering tweet on IOP (HTTP {}): {}'.format(r.status_code, r.text))
						else:
							logger.info('Pertinent tweet registered on IOP.')
					logger.info('{} tweets detected, of which {} identified as pertinent'.format(cnt[a], cnt[b]))
				# Recheck running flag
				next_status = iop.get_status()
				if status != next_status:
					status = next_status
					logger.info('Process stopped, idling...')
					break
