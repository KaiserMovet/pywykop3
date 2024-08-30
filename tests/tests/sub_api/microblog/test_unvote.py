from typing import Iterator

import pytest

from pywykop3 import WykopAPI
from tests import config
from tests.helpers.utils import get_last_5_voters, suppress_exceptions


@pytest.fixture(scope="function", name="entry_to_unvote")
def fixture_entry_to_unvote(
    wykop_api: WykopAPI, last_microblog_entry_id: int
) -> Iterator[int]:
    wykop_api.microblog.vote(last_microblog_entry_id)
    entry = wykop_api.microblog.get_entry(last_microblog_entry_id)["data"]
    voters = get_last_5_voters(entry)
    assert config.USERNAME in voters
    yield last_microblog_entry_id
    with suppress_exceptions():
        wykop_api.microblog.unvote(entry_id=last_microblog_entry_id)


def test_unvote(wykop_api: WykopAPI, entry_to_unvote: int):
    wykop_api.microblog.unvote(entry_id=entry_to_unvote)
    entry = wykop_api.microblog.get_entry(entry_to_unvote)["data"]
    voters = get_last_5_voters(entry)
    assert config.USERNAME not in voters
