from typing import Iterator

import pytest
import requests

from pywykop3 import WykopAPI
from tests.helpers.utils import random_string, suppress_exceptions


class TestDeleteEntry:
    @pytest.fixture(scope="class", name="content")
    def fixture_content(self) -> str:
        return random_string()

    @pytest.fixture(scope="class", name="created_entry")
    def fixture_created_entry(self, wykop_api: WykopAPI, content: str) -> Iterator[int]:
        entry_id = wykop_api.microblog.add_entry(content=content)["data"]["id"]
        yield entry_id
        with suppress_exceptions():
            wykop_api.microblog.delete_entry(entry_id)

    def test_deletion(self, wykop_api: WykopAPI, created_entry: int) -> None:
        wykop_api.microblog.delete_entry(entry_id=created_entry)
        with pytest.raises(requests.exceptions.HTTPError):
            wykop_api.microblog.get_entry(entry_id=created_entry)
