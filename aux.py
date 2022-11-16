#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# Auxiliary process (ATP)

import time

from common import config
from common import iop
from common import twitter


# MAIN
if __name__ == '__main__':

	# Grab logger configuration
	logger = config.logger

	logger.info('Initiating the ATP...')
	# inf loop
	while(True):
		try:
			tweets = iop.get_tweets()
			for tweet in tweets:
				twitter.post_tweet(tweet)
		except Exception as e:
			logger.error('Failed to grab tweets: {}'.format(e))
		time.sleep(1)
