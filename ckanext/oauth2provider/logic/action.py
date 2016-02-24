import logging

from ckan.plugins import toolkit as tk

from ckanext.oauth2provider.model.access_token import AccessToken

log = logging.getLogger(__name__)

@tk.auth_disallow_anonymous_access
def token_create(context, data_dict):

    user = context['user']

    tk.check_access('token_create', context, data_dict)
