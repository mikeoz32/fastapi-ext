
from fastapi_ext.session.session import InMemorySessionStorage


def test_empty_storage():
    storage = InMemorySessionStorage()
    assert storage
