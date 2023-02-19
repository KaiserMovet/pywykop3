import pytest

from pywykop3 import WykopAPI
from tests.helpers import EntryHelper


def pytest_addoption(parser):
    parser.addoption("--refresh-token", action="store", default="")


@pytest.fixture(scope="session")
def entry_helper(request):
    token = request.config.getoption("--refresh-token")
    api = WykopAPI(refresh_token=token)
    helper = EntryHelper(api)
    yield helper
    helper.cleanup()
