import pytest

from pywykop3 import WykopAPI


class TestGetEntries:
    LIMIT = 35

    @pytest.fixture(scope="class", name="newest_entries")
    def fixture_newest_entries(self, wykop_api: WykopAPI) -> list:
        return wykop_api.microblog.get_entries(sort="newest", limit=self.LIMIT)["data"]

    def test_entries_amount(self, newest_entries: list[dict]):
        assert len(newest_entries) == self.LIMIT
