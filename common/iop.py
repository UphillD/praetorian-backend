#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# IOP related functionality

import json
import sys

import requests

from common import config



# Grab logger configuration
logger = config.logger

# Gets crawling rules from the IOP
def get_rules(tag):
	# Query the IOP
	logger.log('COMM', 'Quering the IOP for crawling rules...')
	r = requests.get(config.urls['iop']['socialMedia'], params=config.query)
	try:
		r.raise_for_status()
	except:
		logger.error('Query failed (HTTP {}): {}.'.format(r.status_code, r.text))
		sys.exit(-1)
	# Generate list of rules
	query_rules = []
	for element in r.json()['data']:
		if 'collection' in element and element['collection'] == tag:
			query_rules.append({'value': element['value'], 'tag': element['tag']})
	if not query_rules:
		logger.error('No rules found in the IOP.')
		sys.exit(-1)
	logger.success('{} rules received from IOP.'.format(len(query_rules)))
	return(query_rules)

# Gets CI identifiers from the IOP
def get_identifiers(tag):
	# Query the IOP
	logger.log('COMM', 'Quering the IOP for CI identifiers...')
	r = requests.get(config.urls['iop']['socialMedia'], params=config.query)
	try:
		r.raise_for_status()
	except:
		logger.error('Query failed (HTTP {}): {}.'.format(r.status_code, r.text))
		sys.exit(-1)
	# Generate list of identifiers
	identifiers = []
	for element in r.json()['data']:
		if 'collection' in element and element['collection'] == tag:
			identifiers.append({'value': element['value'], 'type': element['type']})
	if not identifiers:
		logger.error('No identifiers found in the IOP.')
		sys.exit(-1)
	logger.success('{} CI identifiers received from IOP.'.format(len(identifiers)))
	return(identifiers)

# Gets queued tweets from the IOP
def get_tweets():
	# Initialize tweet list
	tweets = []
	logger.log('COMM', 'Quering the IOP for queued tweets.')
	r = requests.get(config.urls['iop']['socialMedia'], params=config.query)
	try:
		r.raise_for_status()
	except:
		logger.error('Query failed (HTTP {}): {}.'.format(r.status_code, r.text))
	else:
		for element in r.json()['data']:
			if 'collection' in element and element['collection'] == 'tweets2post':
				logger.success('Tweet found: {}.'.format(element['_id']))
				logger.info('Storing tweet locally')
				tweets.append(element['text'])
				logger.log('COMM', 'Quering the IOP to delete tweet.')
				r = requests.delete(config.urls['iop']['socialMedia'] + element['_id'], params=config.query)
				try:
					r.raise_for_status
				except:
					logger.warn('Query failed (HTTP {}): {}.'.format(r.status_code, r.text))
	return(tweets)

# Initializes status flag in IOP
# CURRENTLY NOT USED
def init_status():
	logger.log('COMM', 'Deleting flag from IOP.')
	# Get running flag from IOP
	r = requests.delete(config.urls['iop']['socialMedia'] + 'BkP9xH8s2dqgYuJKS', params=config.query)
	try:
		r.raise_for_status()
	except Exception as e:
		logger.error('Failed to communicate with IOP to delete status flag: {}'.format(str(e)))
		return(False)
	# Reset running flag
	logger.log('COMM', 'Creating flag in IOP.')
	payload = json.dumps({ '_id': 'BkP9xH8s2dqgYuJKS', 'value': False, 'collection': 'status' })
	r = requests.post(config.urls['iop']['socialMedia'], params=config.query, data=payload, headers=config.headers)
	try:
		r.raise_for_status()
	except Exception as e:
		logger.error('Failed to communicate with IOP to create status flag: {}'.format(str(e)))
		return(False)
	return(True)

# Gets status flag from IOP
def get_status():
	# Get running flag from IOP
	r = requests.get(config.urls['iop']['socialMedia'] + 'BkP9xH8s2dqgYuJKS', params=config.query)
	try:
		r.raise_for_status()
	except:
		logger.error('Failed to get status flag from IOP (HTTP {}): {}'.format(r.status_code, r.text))
	return(r.json()['data']['value'])
