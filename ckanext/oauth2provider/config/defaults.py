from datetime import timedelta

# Default configuration values, these can be overriden in the config ini file
# eg: ckanext.oauth2provider.expire_delta = 86400
CKANEXT_OAUTH2PROVIDER = {
	EXPIRE_DETLA: timedelta(days=365),
	EXPIRE_DELTA_PUBLIC: timedelta(days=30),
	EXPIRE_CODE_DELTA: timedelta(seconds=10 * 60),
	DELETE_EXPIRED: False,
	ENFORCE_SECURE: False,
	ENFORCE_CLIENT_SECURE: False,
	SESSION_KEY: 'ckan_oauth',
	SINGLE_ACCESS_TOKEN: False,
}
