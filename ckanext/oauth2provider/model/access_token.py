from logging import getLogger

from sqlalchemy import types, Column, Table, ForeignKey, and_, UniqueConstraint

from ckan.lib.base import config
from ckan import model
from ckan.model import Session
from ckan.model import meta
from ckan.model import types as _types
from ckan.model.domain_object import DomainObject

from ..utils import long_token

log = getLogger(__name__)

access_token_table = Table('oauth2provider_acess_token', meta.metadata,
	Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
	Column('user_id', sqlalchemy.types.UnicodeText,
		sqlalchemy.ForeignKey('user.id', onupdate='CASCADE',
			ondelete='CASCADE')),
	Column('token', types.UnicodeText, default=long_token),
	Column('client_id', sqlalchemy.types.UnicodeText,
		sqlalchemy.ForeignKey('oauth2provider_client.id', onupdate='CASCADE',
			ondelete='CASCADE')),
	Column('expires', types.DateTime),
	Column('scope', types.Integer, default=0)
)

vdm.sqlalchemy.make_table_stateful(access_token_table)

class AccessToken(vdm.sqlalchemy.StatefulObjectMixin, DomainObject):
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

meta.mapper(AccessToken, access_token_table)
