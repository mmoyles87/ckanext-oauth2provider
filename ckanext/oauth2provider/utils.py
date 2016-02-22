import hashlib
import shortuuid

def short_token():
	"""
	Generate a hash that can be used as an application identifier
	"""
	hash = hashlib.sha1(shortuuid.uuid())
	hash.update(settings.SECRET_KEY)
	return hash.hexdigest()[::2]


def long_token():
	"""
	Generate a hash that can be used as an application secret
	"""
	hash = hashlib.sha1(shortuuid.uuid())
	hash.update(settings.SECRET_KEY)
	return hash.hexdigest()
