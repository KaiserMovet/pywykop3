import pytest

from pywykop3 import WykopAPI


class TestGetEntryComments:
    @pytest.fixture(scope="class", name="comments")
    def fixture_comments(
        self, wykop_api: WykopAPI, hottest_microblog_entry_id: int
    ) -> list[dict]:
        return wykop_api.microblog_comments.get_comments(hottest_microblog_entry_id)[
            "data"
        ]

    def test_comment_amount(self, comments: list[dict]):
        assert len(comments)
