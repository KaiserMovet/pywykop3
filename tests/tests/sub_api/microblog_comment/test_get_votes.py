from typing import Iterator

import pytest

from pywykop3 import WykopAPI
from tests.helpers.utils import CommentID


class TestCommentVotes:
    @pytest.fixture(scope="function", name="comment")
    def fixture_comment(
        self,
        wykop_api: WykopAPI,
        hottest_microblog_comment_entry_id: CommentID,
    ) -> dict:
        comment = wykop_api.microblog_comments.get_comment(
            hottest_microblog_comment_entry_id.entry_id,
            hottest_microblog_comment_entry_id.comment_id,
        )["data"]
        return comment

    @pytest.fixture(scope="function", name="votes")
    def fixture_votes(
        self,
        wykop_api: WykopAPI,
        hottest_microblog_comment_entry_id: CommentID,
    ) -> list[dict]:
        votes = wykop_api.microblog_comments.votes(
            hottest_microblog_comment_entry_id.entry_id,
            hottest_microblog_comment_entry_id.comment_id,
        )["data"]
        return votes

    def test_correct_number_of_votes(self, comment: dict, votes: list[dict]):
        assert len(votes) == comment["votes"]["up"]
