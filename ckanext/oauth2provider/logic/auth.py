import logging

from ckan.plugins import toolkit as tk

log = logging.getLogger(__name__)

@tk.auth_disallow_anonymous_access
def token_create(context, data_dict):
	return {'success': True}

def client_create(context, data_dict):
	# sysadmins only
	return {'success': False}

def client_show(context, data_dict):
	# sysadmins only
	return {'success': False}

def client_list(context, data_dict):
	# sysadmins only
	return {'success': False}
