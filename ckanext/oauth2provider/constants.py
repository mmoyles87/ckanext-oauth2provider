from datetime import timedelta

CONFIDENTIAL = 0
PUBLIC = 1

CLIENT_TYPES = (
    (CONFIDENTIAL, "Confidential (Web applications)"),
    (PUBLIC, "Public (Native and JS applications)")
)

TOKEN_TYPE = 'Bearer'

READ = 1 << 1
WRITE = 1 << 2
READ_WRITE = READ | WRITE

DEFAULT_SCOPES = (
    (READ, 'read'),
    (WRITE, 'write'),
    (READ_WRITE, 'read+write'),
)


EXPIRE_DELTA = timedelta(days=365)

# Expiry delta for public clients (which typically have shorter lived tokens)
EXPIRE_DELTA_PUBLIC = timedelta(days=30)

EXPIRE_CODE_DELTA = timedelta(seconds=10 * 60)
