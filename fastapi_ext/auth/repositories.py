

from fastapi_ext.auth.models import Identity
from fastapi_ext.sqla.repository import BaseRepository


class IdentityRepository(BaseRepository[Identity]):
    ...
