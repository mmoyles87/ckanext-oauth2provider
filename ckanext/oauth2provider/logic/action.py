import logging

from ckan.model import User
from ckan.plugins import toolkit as tk

from ckanext.oauth2provider.model.client import Client
from ckanext.oauth2provider.model.access_token import AccessToken

log = logging.getLogger(__name__)

def token_create(context, data_dict):
	user = context['user']
	model = context['model']

	tk.check_access('oauth2provider_token_create', context, data_dict)

def client_create(context, data_dict):
	model = context['model']
	user = context['user']

	tk.check_access('oauth2provider_client_create', context, data_dict)

	client = Client(user_id=data_dict['user_id'],
					name=data_dict['name'],
					url=data_dict['url'],
					redirect_uri=data_dict['redirect_uri'],
					client_type=data_dict['client_type'])
	model.Session.add(client)
	model.Session.commit()

def client_show(context, data_dict):
	model = context['model']
	user = context['user']

	tk.check_access('oauth2provider_client_create', context, data_dict)

	id = data_dict.get('id', None)
	if id:
		return Client.get(id)
	else:
		raise tk.NotFound
