#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# Main implementation (PR)

import time

from common import config
from common import iop
from common import twitter



if __name__ == '__main__':

	# Grab logger configuration
	logger = config.logger

	logger.info('Initializing the Tweet Poster module.')
	# inf loop
	while(True):
		tweets = iop.get_tweets()
		if tweets:
			for tweet in tweets:
				twitter.post_tweet(tweet)
		else:
			logger.info('No tweets found.')
		time.sleep(1)
