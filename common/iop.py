#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# IOP related functionality

import os
import sys

import requests

from configparser import ConfigParser
from loguru import logger

####################
## INITIALIZATION ##
####################
# Read configuration file
config = ConfigParser()
config.read('/app/praetorian-backend/config.ini')

# Configure IOP credentials and request headers
appID = os.getenv('IOP_APPID')
keyID = os.getenv('IOP_KEYID')
if not appID or not keyID:
	logger.error('Failed to get twitter credentials from environment variables.')
	sys.exit(config['Exit Codes']['missing_credentials'])
query_params = { 'appId' : appID, 'keyId' : keyID }
headers = {'content-type': 'application/json'}

###############
## FUNCTIONS ##
###############
# Gets crawling rules from the IOP
def get_rules(tag):
	logger.log('COMM', 'Quering the IOP for crawling rules...')
	r = requests.get(config['URLs']['iop_socialMedia'], params=query_params)
	try:
		r.raise_for_status()
	except:
		logger.error('Query failed (HTTP {}).'.format(r.status_code))
		logger.error('Message: {}.'.format(r.text))
		sys.exit(config['Exit Codes']['iop_get'])
	# Generate list of rules
	query_rules = []
	for element in r.json()['data']:
		if 'collection' in element and element['collection'] == tag:
			query_rules.append({'value': element['value'], 'tag': element['tag']})
	if not query_rules:
		logger.error('No rules found in the IOP.')
		sys.exit(config['Exit Codes']['missing_rules'])
	logger.success('{} rules received from IOP.'.format(len(query_rules)))
	return(query_rules)

# Gets CI identifiers from the IOP
def get_identifiers(tag):
	logger.log('COMM', 'Quering the IOP for CI identifiers...')
	r = requests.get(config['URLs']['iop_socialMedia'], params=query_params)
	try:
		r.raise_for_status()
	except:
		logger.error('Query failed (HTTP {}).'.format(r.status_code))
		logger.error('Message: {}.'.format(r.text))
		sys.exit(config['Exit Codes']['iop_get'])
	# Generate list of identifiers
	identifiers = []
	for element in r.json()['data']:
		if 'collection' in element and element['collection'] == tag:
			identifiers.append({'value': element['value'], 'type': element['type'], 'priority': element['priority']})
	if not identifiers:
		logger.error('No identifiers found in the IOP.')
		sys.exit(config['Exit Codes']['missing_identifiers'])
	logger.success('{} CI identifiers received from IOP.'.format(len(identifiers)))
	return(identifiers)

# Registers tweet on the IOP
def register_tweet(payload):
	logger.log('COMM', 'Registering the tweet on the IOP...')
	while True:
		r = requests.post(config['URLs']['iop_socialMedia'], data=payload, params=query_params, headers=headers)
		try:
			r.raise_for_status()
		except:
			logger.error('Failed to register tweet on IOP (HTTP {}).'.format(r.status_code))
			logger.error('Message: {}.'.format(r.text))
			logger.log('COMM', 'Retrying...')
		else:
			logger.success('Tweet registered on IOP.')
			return(True)

# Gets status flag from IOP
def get_status(previous_status):
	r = requests.get(config['URLs']['iop_socialMedia'] + config['IOP']['status_flag_key'], params=query_params)
	try:
		r.raise_for_status()
	except:
		logger.error('Failed to get status flag from IOP (HTTP {}).'.format(r.status_code))
		logger.error('Message: {}.'.format(r.text))
		return(previous_status)
	return(r.json()['data']['value'])
