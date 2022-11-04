#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# Twitter related functionality

import json
import os
import sys

import requests
import tweepy

from common import config



# Grab logger configuration
logger = config.logger

############
# API v1.1 #
############
# Generates an authentication object via OAuth 1.0a (API v1.1) (tweepy)
# https://docs.tweepy.org/en/stable/authentication.html#oauth-1-0a-user-context
def authorize_OAuth():
	logger.log('AUTH', 'Authenticating with Twitter (API v1.1).')
	# Grab the credentials from the enviroment variables
	consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
	consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
	access_token = os.getenv('TWITTER_ACCESS_TOKEN')
	access_secret = os.getenv('TWITTER_ACCESS_SECRET')
	if not consumer_key or not consumer_secret or not access_token or not access_secret:
		logger.error('Failed to grab one or more credentials from environment variables.')
		sys.exit(-1)
	try:
		# Authorize via tweepy
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_secret)
		# Generate & Return API object
		api = tweepy.API(auth)
	except Exception as e:
		logger.error('Error during authentication (API v1.1): {}.'.format(str(e)))
		sys.exit(-1)
	#logger.success('Returning authentication object (API v1.1).')
	return(api)

# Gets the username of the current authorized user (API v1.1)
# https://docs.tweepy.org/en/stable/api.html#tweepy.API.verify_credentials
# CURRENTLY NOT USED
def get_username():
	logger.log('COMM', 'Quering Twitter for the screen name of the user currently logged in. (API v1.1)')
	api = authorize_OAuth()
	try:
		screen_name = api.verify_credentials().screen_name
		logger.success('Query successful, currently logged in as {}.'.format(screen_name))
	except Exception as e:
		logger.error('Query failed: {}.'.format(str(e)))
	return(screen_name)

# Posts a tweet (API v1.1) (tweepy)
# https://docs.tweepy.org/en/stable/api.html#tweepy.API.update_status
def post_tweet(text):
	# Create API object /w OAuth 1.0a authorization
	api = authorize_OAuth()

	# Add fake tweet disclaimer
	text += """

	Disclaimer: This tweet contains false information.
	"""

	# Post tweet, return response
	logger.log('COMM', 'Creating tweet on twitter (API v1.1).')
	try:
		response = api.update_status(text)
		logger.success('Tweet created.')
		return(response)
	except Exception as e:
		logger.error('Failed to create tweet: {}'.format(str(e)))
		return(None)

##########
# API v2 #
##########
# Generates an authentication object via bearer token (API v2)
def bearer_oauth(r):
	logger.log('AUTH', 'Authenticating with Twitter (API v2).')
	# Grab the credential from the enviroment variable
	bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
	if not bearer_token:
		logger.error('Failed to grab bearer token from environment variable.')
		sys.exit(-1)
	# Fill the headers
	try:
		r.headers['Authorization'] = f'Bearer {bearer_token}'
		r.headers['User-Agent'] = 'v2FilteredStreamPython'
	except Exception as e:
		logger.error('Error during authentication (API v2): {}.'.format(str(e)))
		sys.exit(-1)
	#logger.success('Returning authentication object (API v2).')
	return(r)

# Gets current query rules from Twitter (API v2)
def get_rules():
	logger.log('COMM', 'Quering Twitter for current crawling rules. (API v2)')
	r = requests.get(config.urls['twitter']['rules'], auth=bearer_oauth)
	try:
		r.raise_for_status()
	except:
		logger.warn('Query failed (HTTP {}): {}.'.format(r.status_code, r.text))
		return(None)
	logger.success('{} old rules received from Twitter.'.format(r.json()['meta']['result_count']))
	return(r.json())

# Deletes current query rules on Twitter (API v2)
def delete_rules(rules):
	try:
		ids = list(map(lambda rule: rule["id"], rules["data"]))
	except:
		logger.warn('No preexisting rules detected, skipping rule deletion.')
		return(None)
	payload = { "delete" : { "ids" : ids } }
	logger.log('COMM', 'Quering Twitter to delete current crawling rules. (API v2)')
	r = requests.post(config.urls['twitter']['rules'], auth=bearer_oauth, json=payload)
	try:
		r.raise_for_status()
	except:
		logger.warn('Query failed (HTTP {}): {}.'.format(r.status_code, r.text))
		return(None)
	logger.success('{} old rules deleted on Twitter.'.format(r.json()['meta']['summary']['deleted']))
	if r.json()['meta']['summary']['not_deleted']:
		logger.warn('{} old rules not deleted.'.format(r.json()['meta']['summary']['not_deleted']))
	return(r.json())

# Sets new query rules (API v2)
def set_rules(rules):
	payload = { "add" : rules }
	logger.log('COMM', 'Quering Twitter to set new crawling rules. (API v2)')
	r = requests.post(config.urls['twitter']['rules'], auth=bearer_oauth, json=payload)
	try:
		r.raise_for_status()
	except:
		logger.error('Query failed (HTTP {}): {}'.format(r.status_code, r.text))
		sys.exit(-1)
	logger.success('{} new rules set on Twitter.'.format(str(r.json()['meta']['summary']['created'])))
	return(r.json())

