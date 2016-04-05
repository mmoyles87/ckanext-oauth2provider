import hashlib
import shortuuid
from .constants import EXPIRE_DELTA, EXPIRE_DELTA_PUBLIC, EXPIRE_CODE_DELTA

from datetime import datetime, tzinfo

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

def get_token_expiry(public=True):
	"""
	Return a datetime object indicating when an access token should expire.
	Can be customized by setting :attr:`settings.OAUTH_EXPIRE_DELTA` to a
	:attr:`datetime.timedelta` object.
	"""
	if public:
		return datetime.now() + EXPIRE_DELTA_PUBLIC
	else:
		return datetime.now() + EXPIRE_DELTA

def get_code_expiry():
	"""
	Return a datetime object indicating when an authorization code should
	expire.
	Can be customized by setting :attr:`settings.OAUTH_EXPIRE_CODE_DELTA` to a
	:attr:`datetime.timedelta` object.
	"""
	return datetime.now() + EXPIRE_CODE_DELTA

def set_query_parameter(url, param_name, param_value):
	"""Given a URL, set or replace a query parameter and return the
	modified URL.

	>>> set_query_parameter('http://example.com?foo=bar&biz=baz', 'foo', 'stuff')
	'http://example.com?foo=stuff&biz=baz'

	"""
	from urllib import urlencode
	from urlparse import parse_qs, urlsplit, urlunsplit

	scheme, netloc, path, query_string, fragment = urlsplit(url)
	query_params = parse_qs(query_string)

	query_params[param_name] = [param_value]
	new_query_string = urlencode(query_params, doseq=True)

	return urlunsplit((scheme, netloc, path, new_query_string, fragment))
