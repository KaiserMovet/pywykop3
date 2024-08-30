import logging
from typing import Iterator

import pytest

from pywykop3 import WykopAPI


def get_token() -> str:
    with open("refresh_token.txt", "r", encoding="utf-8") as file:
        file_content = file.read()  # Wczytanie całej zawartości pliku do zmiennej
    return file_content


def save_token(token):
    with open("refresh_token.txt", "w", encoding="utf-8") as file:
        file.write(token)  # Zapisuje zawartość zmiennej do pliku


@pytest.fixture(scope="session", name="wykop_api")
def fixture_wykop_api() -> Iterator[WykopAPI]:
    token = get_token()
    api = WykopAPI(
        refresh_token=token,
    )
    yield api
    if token := api.refresh_token:
        save_token(token)


@pytest.fixture(scope="function")
def last_microblog_entry_id(wykop_api: WykopAPI) -> int:
    entry_id = wykop_api.microblog.get_entries(limit=1, sort="newest")["data"][0]["id"]
    logging.info("Getting last entry with id: %s", entry_id)
    return entry_id
