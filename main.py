#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# Main process (SMSTD & CO)

import array
import json
import time

import keras
import nlu
import requests
import touch

from common import config
from common import iop
from common import twitter



# Initializes text classifier (NLU)
def init_text_classifier():
	time_start = time.perf_counter()
	try:
		model = nlu.load(path=config.text_model_path)
	except Exception as e:
		logger.error('Failed to load text classification model: {}.'.format(e))
		sys.exit(config.exit_codes['misc']['file_missing'])
	logger.success('Text classification model loaded in {:.2f} seconds.'.format(time.perf_counter() - time_start))
	return(model)

# Initializes image classifier (Keras)
def init_image_classifier():
	time_start = time.perf_counter()
	try:
		model = keras.models.load_model(config.image_model_path)
	except Exception as e:
		logger.error('Failed to load image classification model: {}.'.format(e))
		sys.exit(config.exit_codes['misc']['file_missing'])
	logger.success('Image classification model loaded in {:.2f} seconds.'.format(time.perf_counter() - time_start))
	return(model)


# MAIN
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
	touch.touch('/app/ready')

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
			# Get current rules from IOP
			rules = iop.get_rules(tag_rules)
			# Get old rules from twitter
			old_rules = twitter.get_rules()
			# Delete old rules from twitter
			twitter.delete_rules(old_rules)
			# Set new rules on twitter
			twitter.set_rules(rules)
			# Get CI identifiers from IOP
			identifiers = (iop.get_identifiers(tag_identifiers) if status == 'SMSTD' else None)

			# Initiate twitter stream
			r = requests.get(config.urls['twitter']['stream'], auth=twitter.bearer_oauth, params=config.query_params, stream=True)
			try:
				r.raise_for_status()
			except:
				logger.error('Failed initiating twitter stream (HTTP {}): {}'.format(r.status_code, r.text))
				sys.exit(config.exit_codes['twitter']['get_stream'])
			logger.success('Initiating twitter stream...')
			# Stream, each line is a tweet
			for line in r.iter_lines():
				if line:
					cnt[a] += 1
					# Load tweet object
					tweet = json.loads(line)
					for rule in tweet['matching_rules']:
						logger.info('Crawling rule matched: {}.'.format(rule['tag']))
					# Classify tweet as pertinent or not
					classification, annotated_text, matched_identifiers = classifyTweet(tweet, identifiers, text_model, image_model)
					if classification == 'low' or classification == 'high':
						for identifier in matched_identifiers:
							logger.info('CI identifier matched: {}.'.format(identifier))
						cnt[b] += 1
						# Format tweet object for IOP storing
						del tweet['matching_rules']
						del tweet['data']['author_id']
						del tweet['data']['edit_history_tweet_ids']
						tweet['data']['text'] = tweet['data']['text'].replace('Disclaimer: This tweet contains false information.', '')
						tweet['data']['text_annotated'] = annotated_text
						tweet['data']['url'] = 'https://twitter.com/' + tweet['includes']['users'][0]['username'] + '/status/' + tweet['data']['id']
						payload = json.dumps({ 'tweet': tweet, 'text': annotated_text, 'priority': classification, 'collection': tag_tweets })
						success = False
						while not success:
							try:
								r = requests.post(config.urls['iop']['socialMedia'], data=payload, params=config.query, headers=config.headers)
								r.raise_for_status()
							except:
								logger.error('Failed registering tweet on IOP (HTTP {}): {}'.format(r.status_code, r.text))
							else:
								logger.info('Pertinent tweet registered on IOP.')
								success = True
					logger.info('{} tweets crawled, of which {} identified as pertinent'.format(cnt[a], cnt[b]))
				# Recheck running flag
				next_status = iop.get_status()
				if status != next_status:
					status = next_status
					logger.info('Process stopped, idling...')
					break
