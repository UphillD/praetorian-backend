#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# Configuration file

##########
# LOGURU #
##########
from loguru import logger
from sys import stderr
import time

time.tzset()

logger.level('COMM', no=15, color='<magenta>', icon='📡')
logger.level('AUTH', no=15, color='<blue>', icon='🔒')
logger.level('BYE', no=15, color='<fg #808080>', icon='🚪')

fmt = '<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <7}</level> | <cyan>{name: <14}</cyan> | <cyan>{function: <20}</cyan> | <cyan>{line: >3}</cyan> | <level>{message}</level>'
logger.configure(
	handlers=[
		dict(sink=stderr, colorize=True, format=fmt)
	])

########
# URLs #
########
urls =	{
	'iop':	{
		'socialMedia'	:	'https://praetorian-api.k8s.etra-id.com/api/v2/praetorian/socialMedia/',
		'templates'		:	'https://praetorian-api.k8s.etra-id.com/api/v2/praetorian/warningMessagesTempl/'
	},
	'twitter': {
		'rules'		: 'https://api.twitter.com/2/tweets/search/stream/rules',
		'stream'	: 'https://api.twitter.com/2/tweets/search/stream'
	}
}

###########
# Twitter #
###########
# Query filters
#filters = '-is:retweet -is:reply -url:t.co lang:en'
filters	= '-is:retweet -is:reply lang:en'

# Parameters to include in the return object
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
# https://developer.twitter.com/en/docs/twitter-api/expansions
query_params = {
	'tweet.fields'	: 'attachments,author_id,created_at,geo,lang',		# default:	id, text
	'user.fields'	: 'profile_image_url',								# default:	id, name, username
	'media.fields'	: 'preview_image_url,url',							# default:	media_key, type
	'poll.fields'	: '',												# default:	id, options
	'place.fields'	: 'contained_within,country,name',					# default:	full_name, id
	'expansions'	: 'author_id,attachments.media_keys,geo.place_id'	# default:	-
}

#######
# IOP #
#######
import os
query = {'appId' : os.getenv('IOP_APPID'), 'keyId' : os.getenv('IOP_KEYID')}
headers = {'content-type': 'application/json'}

######
# ML #
######
text_model_path = '/app/models/xx.embed_sentence.labse'
image_model_path = '/app/models/resnet50v2'
