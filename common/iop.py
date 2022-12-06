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
		sys.exit(config.exit_codes['iop']['get'])
	# Generate list of rules
	query_rules = []
	for element in r.json()['data']:
		if 'collection' in element and element['collection'] == tag:
			query_rules.append({'value': element['value'], 'tag': element['tag']})
	if not query_rules:
		logger.error('No rules found in the IOP.')
		sys.exit(config.exit_codes['misc']['no_rules'])
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
		sys.exit(config.exit_codes['iop']['get'])
	# Generate list of identifiers
	identifiers = []
	for element in r.json()['data']:
		if 'collection' in element and element['collection'] == tag:
			identifiers.append({'value': element['value'], 'type': element['type'], 'priority': element['priority']})
	if not identifiers:
		logger.error('No identifiers found in the IOP.')
		sys.exit(config.exit_codes['misc']['no_identifiers'])
	logger.success('{} CI identifiers received from IOP.'.format(len(identifiers)))
	return(identifiers)

# Gets status flag from IOP
def get_status():
	# Get running flag from IOP
	r = requests.get(config.urls['iop']['socialMedia'] + 'BkP9xH8s2dqgYuJKS', params=config.query)
	try:
		r.raise_for_status()
	except:
		logger.error('Failed to get status flag from IOP (HTTP {}): {}'.format(r.status_code, r.text))
	return(r.json()['data']['value'])
