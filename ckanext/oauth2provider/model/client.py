from logging import getLogger

from sqlalchemy import types, Column, Table, ForeignKey, and_, UniqueConstraint

from ckan.lib.base import config
from ckan import model
from ckan.model import Session
from ckan.model import meta
from ckan.model import types as _types
from ckan.model.domain_object import DomainObject

from ..utils import short_token, long_token

log = getLogger(__name__)

client_table = Table('oauth2provider_client', meta.metadata,
	Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
	Column('user_id', sqlalchemy.types.UnicodeText,
		sqlalchemy.ForeignKey('user.id', onupdate='CASCADE',
			ondelete='CASCADE'),
	Column('name', types.UnicodeText, unique=True),
	Column('url', types.UnicodeText),
	Column('redirect_uri', types.UnicodeText),
	Column('client_id', types.UnicodeText, default=short_token),
	Column('client_secret', types.UnicodeText, default=long_token),
	Column('client_type', types.Integer)
)

vdm.sqlalchemy.make_table_stateful(client_table)

class Client(vdm.sqlalchemy.StatefulObjectMixin, DomainObject):
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
	def __init__(self):
		return

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
