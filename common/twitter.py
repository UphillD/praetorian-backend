#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# Twitter related functionality (API v2)

import json
import os
import sys

import requests

from common import config



# Grab logger configuration
logger = config.logger

# Generates an authentication object via bearer token
def bearer_oauth(r):
	logger.log('AUTH', 'Authenticating with Twitter.')
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
		logger.error('Error during authentication: {}.'.format(str(e)))
		sys.exit(-1)
	#logger.success('Returning authentication object.')
	return(r)

# Gets current query rules from Twitter
def get_rules():
	logger.log('COMM', 'Quering Twitter for current crawling rules.')
	r = requests.get(config.urls['twitter']['rules'], auth=bearer_oauth)
	try:
		r.raise_for_status()
	except:
		logger.warn('Query failed (HTTP {}): {}.'.format(r.status_code, r.text))
		return(None)
	logger.success('{} old rules received from Twitter.'.format(r.json()['meta']['result_count']))
	return(r.json())

# Deletes current query rules on Twitter
def delete_rules(rules):
	try:
		ids = list(map(lambda rule: rule["id"], rules["data"]))
	except:
		logger.warn('No preexisting rules detected, skipping rule deletion.')
		return(None)
	payload = { "delete" : { "ids" : ids } }
	logger.log('COMM', 'Quering Twitter to delete current crawling rules.')
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

# Sets new query rules
def set_rules(rules):
	payload = { "add" : rules }
	logger.log('COMM', 'Quering Twitter to set new crawling rules.')
	r = requests.post(config.urls['twitter']['rules'], auth=bearer_oauth, json=payload)
	try:
		r.raise_for_status()
	except:
		logger.error('Query failed (HTTP {}): {}'.format(r.status_code, r.text))
		sys.exit(-1)
	logger.success('{} new rules set on Twitter.'.format(str(r.json()['meta']['summary']['created'])))
	return(r.json())

