import pytest

from pywykop3 import WykopAPI
from tests.helpers.utils import remove_whitespace


class TestGetEntry:
    ENTRY_ID = 35980065
    VOTES = 12
    CONTENT = (
        "Dodalemwyjasnieniewczotajszej[aferki]"
        "(https://www.wykop.pl/link/4588649/manipulacja-wykopu-czyli-jak-atencjusz-nakarmil-pelikany/)"
        " #famemma #wykop #afera"
    )
    USERNAME = "m__b"

    @pytest.fixture(scope="class", name="entry")
    def fixture_entry_to_vote(
        self, wykop_api: WykopAPI, last_microblog_entry_id: int
    ) -> dict:
        entry = wykop_api.microblog.get_entry(self.ENTRY_ID)["data"]
        return entry

    def test_content(self, entry: dict):
        assert remove_whitespace(entry["content"]) == remove_whitespace(self.CONTENT)

    def test_votes_amount(self, entry: dict):
        assert entry["votes"]["up"] == self.VOTES

    def test_author_usernames(self, entry: dict):
        assert entry["author"]["username"] == self.USERNAME
