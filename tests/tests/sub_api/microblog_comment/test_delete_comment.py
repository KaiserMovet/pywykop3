from typing import Iterator

import pytest
import requests

from pywykop3 import WykopAPI
from tests import config
from tests.helpers.utils import CommentID, random_string, suppress_exceptions


class TestCommentWithText:
    @pytest.fixture(scope="class", name="content")
    def fixture_content(self) -> str:
        return random_string()

    @pytest.fixture(scope="class", name="created_comment")
    def fixture_created_comment(
        self, wykop_api: WykopAPI, last_microblog_entry_id: int, content: str
    ) -> Iterator[CommentID]:
        comment_id = wykop_api.microblog_comments.add_comment(
            last_microblog_entry_id, content=content
        )["data"]["id"]
        yield CommentID(entry_id=last_microblog_entry_id, comment_id=comment_id)
        with suppress_exceptions():
            wykop_api.microblog_comments.delete_comment(
                last_microblog_entry_id, comment_id
            )

    def test_delete(
        self,
        wykop_api: WykopAPI,
        created_comment: CommentID,
    ) -> None:
        wykop_api.microblog_comments.delete_comment(
            created_comment.entry_id, created_comment.comment_id
        )
        with pytest.raises(requests.exceptions.HTTPError):
            wykop_api.microblog_comments.get_comment(
                created_comment.entry_id, created_comment.comment_id
            )
