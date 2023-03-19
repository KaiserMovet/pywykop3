import pytest

from pywykop3 import User, WykopAPI


@pytest.mark.parametrize(
    "partial_username,username",
    [
        ("m__", "m__b"),
        ("m__b", "m__b"),
        ("", "m__b"),
    ],
)
def test_user_autocomplete(
    wykop_api: WykopAPI, partial_username, username
) -> None:
    users = wykop_api.get_users_autocomplete(partial_username)
    usernames = [user["username"] for user in users]
    assert username in usernames
