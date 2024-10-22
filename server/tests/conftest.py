from fastapi.testclient import TestClient
import pytest

from run import app
from server.db import get_db_session, get_casbin_enf
from server.tests.utils.fixture_db import get_test_db_session
from server.tests.utils.fixture_casbin import get_test_casbin_enf
from server.tests.utils.fixture_setup import superuser_token, ordinary_token, not_exist_token


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_db_session] = get_test_db_session
    app.dependency_overrides[get_casbin_enf] = get_test_casbin_enf

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
async def db_session():
    return get_test_db_session()
