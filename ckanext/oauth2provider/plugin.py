from __future__ import unicode_literals

import constants
import logging
import oauth2

from datetime import timedelta

from ckan import plugins
from ckan import toolkit

log = logging.getLogger(__name__)

class Oauth2ProviderPlugin(plugins.SingletonPlugin):
	plugins.implements(plugins.IConfigurer)
	plugins.implements(plugins.IAuthFunctions)

	# IConfigurer

	def update_config(self, config_):
		toolkit.add_template_directory(config_, 'templates')
		toolkit.add_public_directory(config_, 'public')
		toolkit.add_resource('fanstatic', 'oauth2provider')

		# Add a new admin tab to ckan-admin
		toolkit.add_ckan_admin_tab(config, 'ckanext_oauth2provider',
                                   'OAuth2 Provider')


	def update_config_schema(self, schema):

		ignore_missing = toolkit.get_validator('ignore_missing')
		is_positive_integer = toolkit.get_validator('is_positive_integer')
		is_boolean = toolkit.get_validator('is_boolean')

		schema.update({
			# Provide a salt for token hashes
			'ckanext.oauth2provider.secret_key': [unicode],

			'ckanext.oauth2provider.expire_delta': [ignore_missing, is_positive_integer],

			# Expiry delta for public clients (which typically have shorter lived tokens)
			'ckanext.oauth2provider.expire_delta_public': [ignore_missing, is_positive_integer],

			'ckanext.oauth2provider.expire_code_delta': [ignore_missing, is_positive_integer],

			'ckanext.oauth2provider.delete_expired': [ignore_missing, is_boolean],

			'ckanext.oauth2provider.enforce_secure': [ignore_missing, is_boolean],
			'ckanext.oauth2provider.enforce_client_secure': [ignore_missing, is_boolean],

			'ckanext.oauth2provider.session_key': [ignore_missing, unicode],

			'ckanext.oauth2provider.single_access_token': [ignore_missing, is_boolean],
		})

		return schema
