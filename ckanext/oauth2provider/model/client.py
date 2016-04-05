from __future__ import unicode_literals

from logging import getLogger

from sqlalchemy import types, Column, Table, ForeignKey, and_, UniqueConstraint

from ckan.lib.base import config
from ckan import model
from ckan.model import Session
from ckan.model import meta
from ckan.model import types as _types
from ckan.model.domain_object import DomainObject

from ckanext.oauth2provider.utils import short_token, long_token
from ckanext.oauth2provider import constants

log = getLogger(__name__)

client_table = Table('oauth2provider_client', meta.metadata,
	Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
	Column('user_id', types.UnicodeText,
		ForeignKey('user.id', onupdate='CASCADE',
			ondelete='CASCADE'), nullable=True),
	Column('name', types.UnicodeText, unique=True),
	Column('url', types.UnicodeText),
	Column('redirect_uri', types.UnicodeText),
	Column('client_id', types.UnicodeText, default=short_token, unique=True),
	Column('client_secret', types.UnicodeText, default=long_token),
	Column('client_type', types.Integer)
)

class Client(DomainObject):
	"""
	Default client implementation.
	Expected fields:
	* :attr:`user`
	* :attr:`name`
	* :attr:`url`
	* :attr:`redirect_url`
	* :attr:`client_id`
	* :attr:`client_secret`
	* :attr:`client_type`
	Clients are outlined in the :rfc:`2` and its subsections.
	"""
	def __init__(self, user_id='',
	 			name='', url='', redirect_uri='',
				client_type=constants.CONFIDENTIAL):
		self.user_id = user_id
		self.name = name
		self.url = url
		self.redirect_uri = redirect_uri
		self.client_type = client_type

	@classmethod
	def get(cls, **kw):
		query = model.Session.query(cls).autoflush(False)
		return query.filter_by(**kw).first()

	@classmethod
	def find(cls, **kw):
		query = model.Session.query(cls).autoflush(False)
		return query.filter_by(**kw)

## --------------------------------------------------------
## Mapper Stuff

meta.mapper(Client, client_table)
