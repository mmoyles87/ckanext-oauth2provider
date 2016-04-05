from logging import getLogger

from sqlalchemy import types, Column, Table, ForeignKey, and_, UniqueConstraint

from ckan.lib.base import config
from ckan import model
from ckan.model import Session
from ckan.model import meta
from ckan.model import types as _types
from ckan.model.domain_object import DomainObject

from ckanext.oauth2provider.utils import long_token, get_code_expiry

log = getLogger(__name__)

grant_table = Table('oauth2provider_grant', meta.metadata,
	Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
	Column('user_id', types.UnicodeText,
		ForeignKey('user.id', onupdate='CASCADE',
			ondelete='CASCADE')),
	Column('client_id', types.UnicodeText,
		ForeignKey('oauth2provider_client.client_id', onupdate='CASCADE',
			ondelete='CASCADE')),
	Column('code', types.UnicodeText, default=long_token),
	Column('expires', types.DateTime, default=get_code_expiry),
	Column('redirect_uri', types.UnicodeText, nullable=True),
	Column('scope', types.UnicodeText)
)

class Grant(DomainObject):
	"""
	Default grant implementation. A grant is a code that can be swapped for an
	access token. Grants have a limited lifetime as defined by
	:attr:`provider.constants.EXPIRE_CODE_DELTA` and outlined in
	:rfc:`4.1.2`
	Expected fields:
	* :attr:`user`
	* :attr:`client` - :class:`Client`
	* :attr:`code`
	* :attr:`expires` - :attr:`datetime.datetime`
	* :attr:`redirect_uri`
	* :attr:`scope`
	"""
	def __init__(self, user_id='', client_id='', redirect_uri='', scope=''):

		self.user_id = user_id
		self.client_id = client_id
		self.redirect_uri = redirect_uri
		self.scope = scope

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

meta.mapper(Grant, grant_table)
