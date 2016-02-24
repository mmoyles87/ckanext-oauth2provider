import logging

from ckan.plugins import toolkit as tk

log = logging.getLogger(__name__)

@tk.auth_disallow_anonymous_access
def token_create(context, data_dict=None):
    user = context['user']
    return {'success': True }
