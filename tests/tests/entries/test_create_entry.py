import pytest

from tests.helpers.utils import random_string


@pytest.mark.parametrize("adult", [(True), (False)])
def test_create_entry_verify_response(entry_helper, adult):
    print(entry_helper, adult)
    return
    # ontent = random_string()
    # res = entry_helper.create_entry(content, adult)
    # assert res["content"] == content
    # assert res["adult"] == adult
