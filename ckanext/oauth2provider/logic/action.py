import logging

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

	client = Client(data_dict)
	print client
	
	model.Session.add(client)
	model.Session.commit()
