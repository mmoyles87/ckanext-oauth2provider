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
