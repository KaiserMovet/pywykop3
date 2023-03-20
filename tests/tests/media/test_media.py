import logging
import time

import pytest
import requests

from pywykop3 import ApiException
from tests.helpers.utils import run_function_with_retry


def test_upload_foto(media_helper) -> None:
    photo = media_helper.upload_photo()
    response = requests.get(photo["url"], timeout=30)
    assert (
        response.status_code // 100 == 2
    ), f"Response status code is {response.status_code}"


@pytest.mark.parametrize(
    "url", ["https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg"]
)
def test_upload_foto_with_url(media_helper, url) -> None:
    photo = media_helper.upload_photo_with_url(url)
    response = requests.get(photo["url"], timeout=30)
    assert (
        response.status_code // 100 == 2
    ), f"Response status code is {response.status_code}"


def test_delete_foto(media_helper) -> None:
    photo = media_helper.get_or_upload_photo()
    try:
        run_function_with_retry(
            media_helper.delete_photo, args=[photo["key"]], max_retries=3
        )
    except ApiException as ex:
        logging.error(ex)

    i = 5
    while i:
        response = requests.get(photo["url"], timeout=30)
        if response.status_code // 100 != 2:
            return
        i -= 1
        time.sleep(10)
    assert (
        response.status_code // 100 != 2
    ), f"Response status code is {response.status_code}, {photo['url']=}"
