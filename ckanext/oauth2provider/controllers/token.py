"""
The default implementation of the OAuth provider includes two public endpoints
that are meant for client (as defined in :rfc:`1`) interaction.
.. attribute:: ^authorize/$
	This is the URL where a client should redirect a user to for authorization.
	This endpoint expects the parameters defined in :rfc:`4.1.1` and returns
	responses as defined in :rfc:`4.1.2` and :rfc:`4.1.2.1`.
.. attribute:: ^access_token/$
	This is the URL where a client exchanges a grant for an access tokens.
	This endpoint expects different parameters depending on the grant type:
	* Access tokens: :rfc:`4.1.3`
	* Refresh tokens: :rfc:`6`
	* Password grant: :rfc:`4.3.2`
	This endpoint returns responses depending on the grant type:
	* Access tokens: :rfc:`4.1.4` and :rfc:`5.1`
	* Refresh tokens: :rfc:`4.1.4` and :rfc:`5.1`
	* Password grant: :rfc:`5.1`
	Errors are outlined in :rfc:`5.2`.
"""

from ckan import model
from ckan.plugins import toolkit as tk

from ckanext.oauth2provider.model.client import Client
from ckanext.oauth2provider.model.grant import Grant
from ckanext.oauth2provider.model.access_token import AccessToken

c = tk.c

class OAuth2ProviderTokenController(tk.BaseController):
	def _get_context(self):
		return {'model': model, 'session': model.Session,
				'user': c.user, 'auth_user_obj': c.userobj}

	def _get_required_param(self, key):
		param = tk.request.params.get(key)
		if not param:
			tk.abort(400, ('"%s" is a required parameter' % key))
		return param

	def authorize(self):
		# Test url
		# http://localhost:5000/oauth2/authorize?client_id=36c890d9c4342b28fd19&scope=read+write&response_type=token
		context = self._get_context()

		try:
			tk.check_access('oauth2provider_token_create', context)
		except tk.NotAuthorized:
			tk.abort(401, tk._('You must be logged in to authorize a grant.'))

		client_id = self._get_required_param('client_id')
		response_type = self._get_required_param('response_type')
		scopes = self._get_required_param('scope').split(' ')
		redirect_uri = tk.request.params.get('redirect_uri', '')

		client = Client.get(client_id=client_id)

		data = {
			'client_name': client.name,
			'client_id': client.client_id,
			'response_type': response_type,
			'redirect_uri': redirect_uri,
			'scopes': scopes,
		}

		vars = {'data': data, 'action': 'authorize'}
		return tk.render('ckanext/oauth2provider/authorize.html',
			extra_vars=vars)

	def authorize_confirm(self, data=None):
		context = self._get_context()

		try:
			tk.check_access('oauth2provider_token_create', context)
		except tk.NotAuthorized:
			tk.abort(401, tk._('You must be logged in to authorize a grant.'))

		authorize = tk.request.params.get('authorize')
		if not authorize:
			tk.abort(401, tk._('Authorization was not confirmed.'))

		client_id = self._get_required_param('client_id')
		scope = '+'.join(tk.request.params.getall('scope'))
		redirect_uri = tk.request.params.get('redirect_uri', '')

		user = model.User.by_name(context['user'])

		# Check if the client exists
		client = Client.get(client_id=client_id)
		grant = tk.get_action('oauth2provider_grant_create')(context, {
			'client_id': client.id,
			'user_id': user.id,
			'redirect_uri': redirect_uri,
			'scope': scope,
		})

		return

	def access_token(self):
		print tk.request.params

		return

	def redirect(self):
		return

	def index(self, data=None, errors=None, error_summary=None):

		context = self._get_context()

		data = data or {}
		errors = errors or {}
		error_summary = error_summary or {}
		vars = {'data': data, 'errors': errors,
				'error_summary': error_summary, 'action': 'index'}

		return tk.render('ckanext/oauth2provider/token/index.html')
