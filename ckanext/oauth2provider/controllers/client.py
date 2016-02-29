from ckan import model
from ckan.plugins import toolkit as tk

c = tk.c

class OAuth2ProviderClientController(tk.BaseController):
	def _get_context(self):
		return {'model': model, 'session': model.Session,
				'user': c.user, 'auth_user_obj': c.userobj}

	def index(self, data=None):
		context = self._get_context()

		try:
			tk.check_access('oauth2provider_client_create', context)
		except tk.NotAuthorized:
			abort(401, _('Unauthorized to view oauth2 clients'))

		data = data or {}
		data['clients'] = tk.get_action('oauth2provider_client_list')(context)

		vars = {'data': data, 'action': 'index'}

		return tk.render('ckanext/oauth2provider/client/index.html',
			extra_vars=vars)

	def new(self, data=None, errors=None, error_summary=None):
		context = self._get_context()

		try:
			tk.check_access('oauth2provider_client_create', context)
		except tk.NotAuthorized:
			abort(401, _('Unauthorized to create an oauth2 client'))

		if tk.request.method == 'POST':
			data = dict(tk.request.params)
			try:
				data['user_id'] = model.User.by_name(data['username']).id
			except AttributeError:
				data['user_id'] = None
			client = tk.get_action('oauth2provider_client_create')(context, data)
			tk.redirect_to('oauth2provider_client_list')

		data = data or {}
		errors = errors or {}
		error_summary = error_summary or {}
		vars = {'data': data, 'errors': errors,
				'error_summary': error_summary, 'action': 'new'}

		return tk.render('ckanext/oauth2provider/client/new.html',
			extra_vars=vars)
