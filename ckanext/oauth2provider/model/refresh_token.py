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

refresh_token_table = Table('oauth2provider_refresh_token', meta.metadata,
	Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
	Column('user_id', types.UnicodeText,
		ForeignKey('user.id', onupdate='CASCADE',
			ondelete='CASCADE')),
	Column('token', types.UnicodeText, default=long_token),
	Column('access_token_id', types.UnicodeText,
		ForeignKey('oauth2provider_access_token.id', onupdate='CASCADE',
			ondelete='CASCADE')),
	Column('client_id', types.UnicodeText,
		ForeignKey('oauth2provider_client.id', onupdate='CASCADE',
			ondelete='CASCADE')),
	Column('expired', types.Boolean, default=False)
)

class RefreshToken(DomainObject):
	"""
	Default refresh token implementation. A refresh token can be swapped for a
	new access token when said token expires.
	Expected fields:
	* :attr:`user`
	* :attr:`token`
	* :attr:`access_token` - :class:`AccessToken`
	* :attr:`client` - :class:`Client`
	* :attr:`expired` - ``boolean``
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

meta.mapper(RefreshToken, refresh_token_table)
