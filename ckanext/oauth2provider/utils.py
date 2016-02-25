import hashlib
import shortuuid

import pylons.config as config

def short_token():
	"""
	Generate a hash that can be used as an application identifier
	"""
	hash = hashlib.sha1(shortuuid.uuid())
	hash.update(config.get('ckanext.oauth2provider.secret_key'))
	return hash.hexdigest()[::2]


def long_token():
	"""
	Generate a hash that can be used as an application secret
	"""
	hash = hashlib.sha1(shortuuid.uuid())
	hash.update(config.get('ckanext.oauth2provider.secret_key'))
	return hash.hexdigest()
