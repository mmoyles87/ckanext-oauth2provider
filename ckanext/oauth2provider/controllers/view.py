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

c = tk.c

class OAuth2ProviderController(tk.BaseController):
	def _get_context(self):
		return {'model': model, 'session': model.Session,
				'user': c.user, 'auth_user_obj': c.userobj}

	def authorize(self, data=None, errors=None, error_summary=None):

		context = self._get_context()

		try:
			tk.check_access('oauth2provider_token_create', context)
		except tk.NotAuthorized:
			tk.abort(401, tk._('You must be logged in before creating an \
				authorization token.'))

		return tk.render('ckanext/oauth2provider/authorize.html')

	def authorize_confirm(self):
		return

	def access_token(self):
		return

	def redirect(self):
		return
