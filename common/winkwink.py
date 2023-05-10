#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# IOP related functionality

import json
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
	sys.exit(config['Exit Codes'].getint('missing_credentials'))
query_params = { 'appId' : appID, 'keyId' : keyID }
headers = {'content-type': 'application/json'}

# Initialize requests session with retries
session = requests.Session()
retries = requests.adapters.Retry(total=config['IOP'].getint('max_retries'), backoff_factor=config['IOP'].getint('backoff_factor'), status_forcelist=tuple(range(400, 600)))
session.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))

###############
## FUNCTIONS ##
###############
# Registers tweet on the IOP
def register_tweet(payload):
	logger.info('Registering the tweet on the IOP...')
	while True:
		r = session.post(config['URLs']['iop_socialMedia'], data=payload, params=query_params, headers=headers, timeout=config['IOP'].getint('timeout'))
		try:
			r.raise_for_status()
		except:
			logger.error('Failed to register tweet on IOP (HTTP {}).'.format(r.status_code))
			logger.error('Message: {}.'.format(r.text))
		else:
			logger.success('Tweet registered on IOP.')
			return(True)

def generate_1st_tweet():
	first_tweet = json.dumps({
		'collection' : 'TD_tweets',
		'priority' : 'low',
		'text' : 'New Weaponized Android App With 1M Installs $Steals$ $2FA$ Codes & $Passwords$ https://t.co/xka6VxHevt #androidapps #cyber #cybersecurity #informationsecurity #$malware$ #android #playstore',
		'tweet': {
			'data': {
				'created_at': '2023-05-05T06:22:25.000Z',
				'id': '1654371007094833152',
				'lang': 'en',
				'text_annotated': 'New Weaponized Android App With 1M Installs $Steals$ $2FA$ Codes & $Passwords$ https://t.co/xka6VxHevt #androidapps #cyber #cybersecurity #informationsecurity #$malware$ #android #playstore',
				'text': 'New Weaponized Android App With 1M Installs $Steals$ $2FA$ Codes & $Passwords$ https://t.co/xka6VxHevt #androidapps #cyber #cybersecurity #informationsecurity #$malware$ #android #playstore',
				'url': 'https://twitter.com/The_Cyber_News/status/1654371007094833152'
			},
			'includes': {
				'users': [{'id': '1165106855879704577', 'name': 'Cyber Security News', 'profile_image_url': 'https://pbs.twimg.com/profile_images/1174924326807592960/aJMuU6Ms_400x400.jpg', 'username': 'The_Cyber_News'}]
			}
		}
	})
	register_tweet(first_tweet)


def generate_2nd_tweet():
	first_tweet = json.dumps({
		'collection' : 'TD_tweets',
		'priority' : 'low',
		'text' : 'MSI $data$ $breach$ just got even more concerning.\n\nHackers have leaked private code signing keys, including Intel Boot Guard, on the #DarkWeb, which could lead to further attacks.\nLearn more: https://t.co/xDRZZbvCmv #cybersecurity #informationsecurity',
		'tweet': {
			'data': {
				'created_at': '2023-05-09T07:04:25.000Z',
				'id': '1656012157786669056',
				'lang': 'en',
				'text_annotated': 'MSI $data$ $breach$ just got even more concerning.\n\nHackers have leaked private code signing keys, including Intel Boot Guard, on the #DarkWeb, which could lead to further attacks.\nLearn more: https://t.co/xDRZZbvCmv #cybersecurity #informationsecurity',
				'text': 'MSI data breach just got even more concerning.\n\nHackers have leaked private code signing keys, including Intel Boot Guard, on the #DarkWeb, which could lead to further attacks.\nLearn more: https://t.co/xDRZZbvCmv #cybersecurity #informationsecurity',
				'url': 'https://twitter.com/TheHackersNews/status/1656012157786669056'
			},
			'includes': {
				'users': [{'id': '209811713', 'name': 'The Hacker News', 'profile_image_url': 'https://pbs.twimg.com/profile_images/1597647879811657728/FLgHrLHy_400x400.jpg', 'username': 'TheHackerNews'}]
			}
		}
	})
	register_tweet(first_tweet)
