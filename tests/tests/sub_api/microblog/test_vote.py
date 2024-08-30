from typing import Iterator

import pytest

from pywykop3 import WykopAPI
from tests import config
from tests.helpers.utils import get_last_5_voters, suppress_exceptions


@pytest.fixture(scope="function", name="entry_to_vote")
def fixture_entry_to_vote(
    wykop_api: WykopAPI, last_microblog_entry_id: int
) -> Iterator[int]:
    entry = wykop_api.microblog.get_entry(last_microblog_entry_id)["data"]
    voters = get_last_5_voters(entry)
    assert config.USERNAME not in voters
    yield last_microblog_entry_id
    with suppress_exceptions():
        wykop_api.microblog.unvote(entry_id=last_microblog_entry_id)


def test_vote(wykop_api: WykopAPI, entry_to_vote: int):
    wykop_api.microblog.vote(entry_to_vote)
    entry = wykop_api.microblog.get_entry(entry_to_vote)["data"]
    voters = get_last_5_voters(entry)
    assert config.USERNAME in voters
