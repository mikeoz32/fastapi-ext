import pytest
from fastapi_ext.auth.models import Account

@pytest.fixture(autouse=True)
def auth_test_data(data_mapping):
    data_mapping["accounts"] = {
        "active": Account(
            identity_id="test_identity", name="TestAccount"
        )
    }
