from typing import Iterator

import pytest

from pywykop3 import WykopAPI
from tests import config
from tests.helpers.utils import random_string, suppress_exceptions
from tests.tests.sub_api.microblog_comment.test_add_comment import (
    TestCommentWithText as CommentWithText,
)


class TestEditCommentWithText(CommentWithText):
    @pytest.fixture(scope="class", name="created_entry")
    def fixture_created_comment(
        self, wykop_api: WykopAPI, last_microblog_entry_id: int, content: str
    ) -> Iterator[dict]:
        comment_id = wykop_api.microblog_comments.add_comment(
            last_microblog_entry_id, content=random_string()
        )["data"]["id"]
        wykop_api.microblog_comments.edit_comment(
            last_microblog_entry_id, comment_id, content=content
        )
        created_comment = wykop_api.microblog_comments.get_comment(
            last_microblog_entry_id, comment_id
        )
        yield created_comment["data"]
        with suppress_exceptions():
            wykop_api.microblog_comments.delete_comment(
                last_microblog_entry_id, comment_id
            )
