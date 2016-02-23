from __future__ import unicode_literals

import logging
import oauth2

from ckan import plugins
from ckan.plugins import toolkit

from .model import access_token, client, grant, refresh_token

log = logging.getLogger(__name__)

class Oauth2ProviderPlugin(plugins.SingletonPlugin):
	plugins.implements(plugins.IConfigurer)
	plugins.implements(plugins.IConfigurable)
	plugins.implements(plugins.IRoutes)

	# IConfigurable
	def configure(self, config):
		if not client.client_table.exists():
			client.client_table.create()

		if not grant.grant_table.exists():
			grant.grant_table.create()

		if not access_token.access_token_table.exists():
			access_token.access_token_table.create()

		if not refresh_token.refresh_token_table.exists():
			refresh_token.refresh_token_table.create()

		# Ensure that a secret key has been set
		secret_key = config.get('ckanext.oauth2provider.secret_key', '')
		if not secret_key:
			raise RuntimeError(
				'ckanext.oauth2provider.secret_key is not configured and it must'
				' have a value. Please amend your .ini file.')

	# IConfigurer
	def update_config(self, config):
		toolkit.add_template_directory(config, 'templates')
		toolkit.add_public_directory(config, 'public')
		toolkit.add_resource('fanstatic', 'oauth2provider')

		# Add a new admin tab to ckan-admin
		toolkit.add_ckan_admin_tab(config, 'ckanext_oauth2provider',
								   'OAuth2 Provider')

	def before_map(self, route_map):
		controller = 'ckanext.oauth2provider.controllers.view:OAuth2ProviderController'

		route_map.connect('/oauth2/authorize', controller=controller,
			action='authorize')

		return route_map

	def after_map(self, route_map):
			return route_map
