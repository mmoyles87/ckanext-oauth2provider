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
import json

import logging
log = logging.getLogger(__name__)

from pylons import session, config, request, response

from ckan import model
from ckan.plugins import toolkit as tk

from ckanext.oauth2provider.model.client import Client
from ckanext.oauth2provider.model.grant import Grant
from ckanext.oauth2provider.model.access_token import AccessToken

from ckanext.oauth2provider.utils import set_query_parameter, get_token_expiry

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

	def _get_repoze_handler(self, handler_name):
		'''Returns the URL that repoze.who will respond to and perform a
		login or logout.'''
		return getattr(tk.request.environ['repoze.who.plugins']['friendlyform'], handler_name)

	def _json_response(self, data):
		response.headers['Content-Type'] = 'application/json;charset=utf-8'
		return json.dumps(data)

	def authorize(self):
		context = self._get_context()

		try:
			tk.check_access('oauth2provider_token_create', context)
		except tk.NotAuthorized:
			return tk.abort(401)

		client_id = self._get_required_param('client_id')
		response_type = tk.request.params.get('redirect_uri', 'code')
		scopes = self._get_required_param('scope').split(' ')
		redirect_uri = tk.request.params.get('redirect_uri', '')
		state = tk.request.params.get('state', '')

		if state:
			session['oauth2provider_state'] = state
			session.save()

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
			return tk.abort(401, tk._('You must be logged in to authorize a grant.'))

		authorize = tk.request.params.get('authorize')
		if not authorize:
			return tk.abort(401, tk._('Authorization was not confirmed.'))

		client_id = self._get_required_param('client_id')
		scope = '+'.join(tk.request.params.getall('scope'))
		redirect_uri = tk.request.params.get('redirect_uri', '')

		user = model.User.by_name(context['user'])

		# Check if the client exists
		client = Client.get(client_id=client_id)
		grant = tk.get_action('oauth2provider_grant_create')(context, {
			'client_id': client.client_id,
			'user_id': user.id,
			'redirect_uri': redirect_uri,
			'scope': scope,
		})

		# Get an optional saved state that clients can pass in
		# (Meteor's accounts-oauth lib does this)
		state = session.get('oauth2provider_state', '')
		if state:
			redirect_uri = set_query_parameter(redirect_uri, 'state', state)

		# Send the grant code to client via GET as defined by OAuth spec
		redirect_uri = set_query_parameter(redirect_uri, 'code', grant.code)

		return tk.redirect_to(str(redirect_uri))

	def access_token(self):
		context = self._get_context()

		code = self._get_required_param('code')
		client_id = self._get_required_param('client_id')
		client_secret = self._get_required_param('client_secret')
		response_type = tk.request.params.get('redirect_uri', 'code')
		redirect_uri = tk.request.params.get('redirect_uri', '')

		client = Client.get(client_id=client_id)
		grant = Grant.get(code=code)

		if client_id != client.client_id or grant.client_id != client_id:
			return self._json_response({
				'error': 'Invalid clientId for this grant'
			})

		if client.client_secret != client_secret:
			return self._json_response({
				'error': 'Invalid client_secret'
			})

		#TODO check for expired grant


		# Create an access token
		token = AccessToken(user_id=grant.user_id,
			client_id=client.id,
			expires=get_token_expiry(public=False),
			scope=grant.scope)
		token.save()
		model.repo.commit()

		return self._json_response({
			'access_token': token.token,
			'expires': int(token.expires.strftime("%s")),
			'refresh_token': '',
			'scope': token.scope,
		})

	def identity(self):
		context = self._get_context()

		access_token = self._get_required_param('access_token')

		try:
			token = AccessToken.get(token=access_token)
			user = model.User.get(token.user_id)

			return self._json_response({
				'name': user.fullname,
				'login': user.name,
				'email': user.email,
				'id': user.id,
				'apikey': user.apikey
			})
		except:
			log.warn('Oauth2Provider could not retrieve the user identity')
			return self._json_response({
				'error': 'Could not retrieve user identity'
			})


	def index(self, data=None, errors=None, error_summary=None):

		context = self._get_context()

		data = data or {}
		errors = errors or {}
		error_summary = error_summary or {}
		vars = {'data': data, 'errors': errors,
				'error_summary': error_summary, 'action': 'index'}

		return tk.render('ckanext/oauth2provider/token/index.html')
