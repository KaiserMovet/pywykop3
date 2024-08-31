from typing import Iterator

import pytest

from pywykop3 import WykopAPI
from tests import config
from tests.helpers.utils import (
    CommentID,
    extract_usernames_from_user_list,
    get_last_5_voters,
    suppress_exceptions,
)


@pytest.fixture(scope="function", name="comment_to_unvote")
def fixture_comment_to_unvote(
    wykop_api: WykopAPI, hottest_microblog_comment_entry_id: CommentID
) -> Iterator[CommentID]:
    wykop_api.microblog_comments.vote(
        entry_id=hottest_microblog_comment_entry_id.entry_id,
        comment_id=hottest_microblog_comment_entry_id.comment_id,
    )
    votes = wykop_api.microblog_comments.votes(
        entry_id=hottest_microblog_comment_entry_id.entry_id,
        comment_id=hottest_microblog_comment_entry_id.comment_id,
    )["data"]
    voters = extract_usernames_from_user_list(votes)
    assert config.USERNAME in voters
    yield hottest_microblog_comment_entry_id
    with suppress_exceptions():
        wykop_api.microblog_comments.unvote(
            entry_id=hottest_microblog_comment_entry_id.entry_id,
            comment_id=hottest_microblog_comment_entry_id.comment_id,
        )


def test_unvote(wykop_api: WykopAPI, comment_to_unvote: CommentID):
    wykop_api.microblog_comments.unvote(
        entry_id=comment_to_unvote.entry_id,
        comment_id=comment_to_unvote.comment_id,
    )
    votes = wykop_api.microblog_comments.votes(
        entry_id=comment_to_unvote.entry_id,
        comment_id=comment_to_unvote.comment_id,
    )["data"]
    voters = extract_usernames_from_user_list(votes)
    assert config.USERNAME not in voters
