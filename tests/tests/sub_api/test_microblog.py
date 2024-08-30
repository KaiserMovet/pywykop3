from typing import Iterator

import pytest

from pywykop3 import WykopAPI
from tests.helpers.utils import suppress_exceptions


@pytest.fixture(scope="function", name="entry_to_vote")
def fixture_entry_to_vote(
    wykop_api: WykopAPI, last_microblog_entry_id: int
) -> Iterator[int]:
    yield last_microblog_entry_id
    with suppress_exceptions():
        wykop_api.microblog.unvote(entry_id=last_microblog_entry_id)


def test_vote(wykop_api: WykopAPI, entry_to_vote: int, username: str):
    wykop_api.microblog.vote(entry_to_vote)
    entry = wykop_api.microblog.get_entry(entry_to_vote)["data"]
    voters = [user["username"] for user in entry["votes"]["users"]]
    assert username in voters


@pytest.fixture(scope="function", name="entry_to_unvote")
def fixture_entry_to_unvote(wykop_api: WykopAPI, last_microblog_entry_id: int) -> int:
    wykop_api.microblog.vote(last_microblog_entry_id)
    return last_microblog_entry_id


def test_unvote(wykop_api: WykopAPI, entry_to_unvote: int, username: str):
    wykop_api.microblog.unvote(entry_id=entry_to_unvote)
    entry = wykop_api.microblog.get_entry(entry_to_unvote)["data"]
    voters = [user["username"] for user in entry["votes"]["users"]]
    assert username not in voters


@pytest.fixture(scope="function", name="entry_to_observe")
def fixture_entry_to_observe(
    wykop_api: WykopAPI, last_microblog_entry_id: int
) -> Iterator[int]:
    yield last_microblog_entry_id
    with suppress_exceptions():
        wykop_api.microblog.unobserve(entry_id=last_microblog_entry_id)


def test_observe(wykop_api: WykopAPI, entry_to_vote: int, username: str):
    wykop_api.microblog.observe(entry_to_vote)
    entry = wykop_api.microblog.get_entry(entry_to_vote)["data"]
    assert entry["observed_discussion"]


@pytest.fixture(scope="function", name="entry_to_unobserve")
def fixture_entry_to_unobserve(
    wykop_api: WykopAPI, last_microblog_entry_id: int
) -> int:
    wykop_api.microblog.observe(last_microblog_entry_id)
    return last_microblog_entry_id


def test_unobserve(wykop_api: WykopAPI, entry_to_unvote: int, username: str):
    wykop_api.microblog.unobserve(entry_id=entry_to_unvote)
    entry = wykop_api.microblog.get_entry(entry_to_unvote)["data"]
    assert not entry["observed_discussion"]
