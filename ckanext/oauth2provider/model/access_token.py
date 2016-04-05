from logging import getLogger

from sqlalchemy import types, Column, Table, ForeignKey, and_, UniqueConstraint

from ckan.lib.base import config
from ckan import model
from ckan.model import Session
from ckan.model import meta
from ckan.model import types as _types
from ckan.model.domain_object import DomainObject

from ckanext.oauth2provider.utils import long_token

log = getLogger(__name__)

access_token_table = Table('oauth2provider_access_token', meta.metadata,
	Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
	Column('user_id', types.UnicodeText,
		ForeignKey('user.id', onupdate='CASCADE',
			ondelete='CASCADE')),
	Column('token', types.UnicodeText, default=long_token),
	Column('client_id', types.UnicodeText,
		ForeignKey('oauth2provider_client.id', onupdate='CASCADE',
			ondelete='CASCADE')),
	Column('expires', types.DateTime),
	Column('scope', types.UnicodeText, default=0)
)

class AccessToken(DomainObject):
	"""
	Default access token implementation. An access token is a time limited
	token to access a user's resources.
	Access tokens are outlined :rfc:`5`.
	Expected fields:
	* :attr:`user_id`
	* :attr:`token`
	* :attr:`client_id` - :class:`Client`
	* :attr:`expires` - :attr:`datetime.datetime`
	* :attr:`scope`
	Expected methods:
	* :meth:`get_expire_delta` - returns an integer representing seconds to
		expiry
	"""
	def __init__(self, user_id='', client_id='', expires='', scope=''):

		self.user_id = user_id
		self.client_id = client_id
		self.expires = expires
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

meta.mapper(AccessToken, access_token_table)
