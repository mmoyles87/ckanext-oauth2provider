import logging

from ckan.model import User
from ckan.plugins import toolkit as tk

from ckanext.oauth2provider.model.client import Client
from ckanext.oauth2provider.model.grant import Grant
from ckanext.oauth2provider.model.access_token import AccessToken

log = logging.getLogger(__name__)

def token_create(context, data_dict):
	user = context['user']
	model = context['model']

	tk.check_access('oauth2provider_token_create', context, data_dict)

def grant_create(context, data_dict):
	user = context['user']
	model = context['model']

	tk.check_access('oauth2provider_grant_create', context, data_dict)

	grant = Grant(user_id=data_dict.get('user_id'),
		client_id=data_dict.get('client_id'),
		redirect_uri=data_dict.get('redirect_uri', ''),
		scope=data_dict.get('scope'))

	grant.save()
	model.repo.commit()

	return grant

def client_create(context, data_dict):
	model = context['model']
	user = context['user']

	tk.check_access('oauth2provider_client_create', context, data_dict)

	client = Client(user_id=data_dict['user_id'],
		name=data_dict['name'],
		url=data_dict['url'],
		redirect_uri=data_dict['redirect_uri'],
		client_type=data_dict['client_type'])

	client.save()
	model.repo.commit()

	return client

def client_show(context, data_dict):
	tk.check_access('oauth2provider_client_show', context, data_dict)
	id = tk.get_or_bust(data_dict, 'id')
	client = Client.get(id)

	return client

def client_list(context, data_dict):
	tk.check_access('oauth2provider_client_list', context, data_dict)
	clients = Client.find().all()

	return clients

def client_delete(context, data_dict):
	model = context['model']
	user = context['user']

	tk.check_access('oauth2provider_client_delete', context, data_dict)
	id = tk.get_or_bust(data_dict, 'id')
	client = Client.get(id=id)

	client.delete()
	model.repo.commit()
