import logging

from ckan.plugins import toolkit as tk

log = logging.getLogger(__name__)

def token_create(context, data_dict):
	if context.get('user'):
		return {'success': True}
	else:
		return {'success': False}
def grant_create(context, data_dict):
	if context.get('user'):
		return {'success': True}
	else:
		return {'success': False}

def client_create(context, data_dict):
	# sysadmins only
	return {'success': False}

def client_show(context, data_dict):
	# sysadmins only
	return {'success': False}

def client_list(context, data_dict):
	# sysadmins only
	return {'success': False}

def client_delete(context, data_dict):
	# sysadmins only
	return {'success': False}
