import logging
import random
from typing import Dict

from pywykop3 import ApiException, Photo, WykopAPI
from tests.helpers.utils import run_function_with_retry


class MediaHelper:
    def __init__(self, api: WykopAPI) -> None:
        self.api = api
        self._created_photos: Dict[str, Photo] = {}

    def upload_photo(self) -> Photo:
        photo = None
        with open("tests/helpers/pictures/1.jpg", "rb") as f:
            photo = f.read()
        res = self.api.post_media_photo("content", photo, "1.jpg", "image/jpeg")
        self._created_photos[res["key"]] = res
        return res

    def upload_photo_with_url(self, url: str) -> Photo:
        res = self.api.post_media_photo_by_url("comments", url)
        self._created_photos[res["key"]] = res

        return res

    def get_or_upload_photo(self) -> Photo:
        if self._created_photos:
            return random.choice(list(self._created_photos.values()))
        return self.upload_photo()

    def delete_photo(self, photo_key) -> None:
        logging.info("Deleted photo with id %s", photo_key)
        self.api.delete_media_photo(photo_key)
        del self._created_photos[photo_key]

    def cleanup(self) -> None:
        # Delete created photos
        for photo_key in self._created_photos.copy():
            try:
                run_function_with_retry(
                    self.delete_photo, args=[photo_key], max_retries=3
                )
                self.delete_photo(photo_key)
            except ApiException as ex:
                if ex.code == 404:
                    del self._created_photos[photo_key]
                    continue
                logging.exception("Cannot remove photo with id: %s", photo_key)
            except Exception:  # pylint: disable= broad-exception-caught
                logging.exception("Cannot remove photo with id: %s", photo_key)
        if self._created_photos:
            logging.error(
                "Following photos were not deleted: %s",
                ", ".join([str(entry_id) for entry_id in self._created_photos]),
            )
