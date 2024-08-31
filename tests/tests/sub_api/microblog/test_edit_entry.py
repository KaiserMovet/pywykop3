import pytest

from pywykop3 import WykopAPI
from tests.helpers.utils import random_string, suppress_exceptions
from tests.tests.sub_api.microblog.test_add_entry import (
    TestEntryWithText as EntryWithText,
)


class TestEditedEntryWithText(EntryWithText):
    @pytest.fixture(scope="class", name="created_entry")
    def fixture_created_entry(self, wykop_api: WykopAPI, content: str):
        entry_id = wykop_api.microblog.add_entry(content=random_string())["data"]["id"]
        wykop_api.microblog.edit_entry(entry_id, content=content)
        created_entry = wykop_api.microblog.get_entry(entry_id)
        yield created_entry["data"]
        with suppress_exceptions():
            wykop_api.microblog.delete_entry(entry_id)
