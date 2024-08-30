from typing import Iterator

import pytest

from pywykop3 import WykopAPI
from tests import config
from tests.helpers.utils import random_string, suppress_exceptions


class TestEntryWithText:
    @pytest.fixture(scope="class", name="content")
    def fixture_content(self) -> str:
        return random_string()

    @pytest.fixture(scope="class", name="created_entry")
    def fixture_created_entry(self, wykop_api: WykopAPI, content: str):
        entry_id = wykop_api.microblog.add_entry(content=content)["data"]["id"]
        created_entry = wykop_api.microblog.get_entry(entry_id)
        yield created_entry["data"]
        with suppress_exceptions():
            wykop_api.microblog.delete_entry(entry_id)

    def test_content(self, created_entry: dict, content: str) -> None:
        assert created_entry["content"] == content

    def test_author(self, created_entry: dict) -> None:
        assert created_entry["author"]["username"] == config.USERNAME

    def test_id(self, created_entry: dict) -> None:
        assert not created_entry["adult"]
