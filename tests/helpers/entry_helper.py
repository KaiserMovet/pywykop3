import logging
import random
from typing import List, NewType

from pywykop3 import Entry, User, WykopAPI
from tests.helpers.utils import random_string

EntryId = NewType("EntryId", int)


class EntryHelper:
    def __init__(self, api: WykopAPI):
        self.api = api
        self._created_entries: List[EntryId] = []
        self._static_entries: List[EntryId] = [  # type: ignore
            70475539,  # type: ignore
            70475387,  # type: ignore
            70475373,  # type: ignore
        ]
        self._voted_entries: List[EntryId] = []

    def create_entry(
        self, content: str | None = None, adult: bool = False
    ) -> Entry:
        content = content or random_string()
        res = self.api.post_entry(content=content, adult=adult)
        logging.info("Created entry with id %s", res["id"])
        self._created_entries.append(res["id"])
        print(f"{self._created_entries=}")
        return res

    def get_entry(self, entry_id: EntryId) -> Entry:
        logging.info("Getting entry with id %s", entry_id)
        return self.api.get_entry_by_id(entry_id)

    def get_or_create_entry(self) -> Entry:
        """Get or create a new entry"""
        if not self._created_entries:
            self.create_entry()
        return self.get_entry(random.choice(self._created_entries))

    def edit_entry(self, entry_id: EntryId, content, adult) -> Entry:
        logging.info("Editing entry with id %s", entry_id)
        return self.api.put_entry(entry_id, content=content, adult=adult)

    def delete_entry(self, entry_id: EntryId) -> None:
        logging.info("Deleted entry with id %s", entry_id)
        self.api.delete_entry_by_id(entry_id)
        self._created_entries.remove(entry_id)

    def get_static_entry(self) -> Entry:
        return self.get_entry(random.choice(self._static_entries))

    def get_voted_entry(self) -> Entry:
        if not self._voted_entries:
            self.vote(random.choice(self._static_entries))
        return self.get_entry(random.choice(self._voted_entries))

    def get_votes(self, entry_id: EntryId) -> List[User]:
        logging.info("Getting votes for entry with id %s", entry_id)
        return self.api.get_entry_votes(entry_id)

    def vote(self, entry_id: EntryId) -> None:
        logging.info("Vote for entry with id %s", entry_id)
        self.api.post_entry_vote(entry_id)
        self._voted_entries.append(entry_id)

    def unvote(self, entry_id: EntryId) -> None:
        logging.info("Unvote for entry with id %s", entry_id)
        self.api.post_entry_vote(entry_id)
        self._voted_entries.remove(entry_id)

    def cleanup(self):

        # Unvote all entries
        for entry_id in self._voted_entries.copy():
            try:
                self.unvote(entry_id)
            except Exception:  # pylint: disable= broad-exception-caught
                logging.exception("Cannot unvote entry with id: %s", entry_id)
        if self._voted_entries:
            logging.error(
                "Following entries were not unvoted: %s",
                ", ".join([str(entry_id) for entry_id in self._voted_entries]),
            )

        # Delete created entries
        for entry_id in self._created_entries.copy():
            try:
                self.delete_entry(entry_id)
            except Exception:  # pylint: disable= broad-exception-caught
                logging.exception("Cannot remove entry with id: %s", entry_id)
        if self._created_entries:
            logging.error(
                "Following entries were not deleted: %s",
                ", ".join(
                    [str(entry_id) for entry_id in self._created_entries]
                ),
            )
