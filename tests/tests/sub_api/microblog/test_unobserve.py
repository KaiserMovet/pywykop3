from typing import Iterator

import pytest

from pywykop3 import WykopAPI
from tests.helpers.utils import suppress_exceptions


@pytest.fixture(scope="function", name="entry_to_unobserve")
def fixture_entry_to_unobserve(
    wykop_api: WykopAPI, last_microblog_entry_id: int
) -> Iterator[int]:
    wykop_api.microblog.observe(last_microblog_entry_id)
    entry = wykop_api.microblog.get_entry(last_microblog_entry_id)["data"]
    assert entry["observed_discussion"]
    yield last_microblog_entry_id
    with suppress_exceptions():
        wykop_api.microblog.unobserve(entry_id=last_microblog_entry_id)


def test_unobserve(wykop_api: WykopAPI, entry_to_unobserve: int):
    wykop_api.microblog.unobserve(entry_to_unobserve)
    entry = wykop_api.microblog.get_entry(entry_to_unobserve)["data"]
    assert not entry["observed_discussion"]
