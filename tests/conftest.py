import pytest

from pywykop3 import WykopAPI
from tests.helpers import EntryHelper


def pytest_addoption(parser):
    parser.addoption("--refresh-token", action="store", default="")


@pytest.fixture(scope="session")
def wykop_api(request):
    token = request.config.getoption("--refresh-token")
    api = WykopAPI(refresh_token=token)
    return api


@pytest.fixture(scope="session")
def entry_helper(wykop_api):  # pylint: disable=redefined-outer-name
    helper = EntryHelper(wykop_api)
    yield helper
    helper.cleanup()
