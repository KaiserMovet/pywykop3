import pytest

from pywykop3 import ApiException
from tests.helpers.utils import random_string, run_function_with_retry


def assert_entry(res, msg, content, adult) -> None:
    assert res["content"] == content, msg
    assert res["adult"] == adult, msg


@pytest.mark.parametrize("adult", [(True), (False)])
def test_create_entry(entry_helper, adult) -> None:
    content = random_string()
    res = entry_helper.create_entry(content, adult)
    entry_id = res["id"]
    assert_entry(res, "Validating response", content, adult)
    res_from_get = entry_helper.get_entry(entry_id)
    assert_entry(res_from_get, "Validating GET response", content, adult)


def test_edit_entry(entry_helper) -> None:
    existing_entry = entry_helper.get_or_create_entry()
    entry_id = existing_entry["id"]

    new_content = random_string()
    new_adult = not existing_entry["adult"]

    res = entry_helper.edit_entry(entry_id, new_content, new_adult)
    entry_id = res["id"]
    assert_entry(res, "Validating response", new_content, new_adult)
    res_from_get = entry_helper.get_entry(entry_id)
    assert_entry(
        res_from_get, "Validating GET response", new_content, new_adult
    )


def test_delete_entry(entry_helper):
    existing_entry = entry_helper.get_or_create_entry()
    entry_id = existing_entry["id"]
    run_function_with_retry(
        entry_helper.delete_entry, args=[entry_id], max_retries=3
    )
    exception = None
    try:
        entry_helper.get_entry(entry_id)
    except ApiException as exc:
        exception = exc
    assert isinstance(exception, ApiException)
    assert exception.code == 404
