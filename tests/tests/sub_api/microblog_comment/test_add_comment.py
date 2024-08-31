from typing import Iterator

import pytest

from pywykop3 import WykopAPI
from tests import config
from tests.helpers.utils import random_string, suppress_exceptions


class TestCommentWithText:
    @pytest.fixture(scope="class", name="content")
    def fixture_content(self) -> str:
        return random_string()

    @pytest.fixture(scope="class", name="created_entry")
    def fixture_created_comment(
        self, wykop_api: WykopAPI, last_microblog_entry_id: int, content: str
    ) -> Iterator[dict]:
        comment_id = wykop_api.microblog_comments.add_comment(
            last_microblog_entry_id, content=content
        )["data"]["id"]
        created_comment = wykop_api.microblog_comments.get_comment(
            last_microblog_entry_id, comment_id
        )
        yield created_comment["data"]
        with suppress_exceptions():
            wykop_api.microblog_comments.delete_comment(
                last_microblog_entry_id, comment_id
            )

    def test_content(self, created_entry: dict, content: str) -> None:
        assert created_entry["content"] == content

    def test_author(self, created_entry: dict) -> None:
        assert created_entry["author"]["username"] == config.USERNAME

    def test_adult(self, created_entry: dict) -> None:
        assert not created_entry["adult"]
