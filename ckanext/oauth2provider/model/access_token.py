from logging import getLogger

from sqlalchemy import Table

from ckan.lib.base import config
from ckan import model
from ckan.model import Session
from ckan.model import meta
from ckan.model.domain_object import DomainObject

log = getLogger(__name__)
