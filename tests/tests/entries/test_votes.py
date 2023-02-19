import pytest


@pytest.mark.skip(reason="Do not have proper permissions")
def test_vote(entry_helper):
    entry_id = entry_helper.get_static_entry()["id"]
    entry_helper.vote(entry_id)
    users = entry_helper.get_votes(entry_id)
    usernames = [user["username"] for user in users]
    assert "Movet" in usernames


@pytest.mark.skip(reason="Do not have proper permissions")
def test_unvote(entry_helper):
    entry_id = entry_helper.get_voted_entry()["id"]
    entry_helper.unvote(entry_id)
    users = entry_helper.get_votes(entry_id)
    usernames = [user["username"] for user in users]
    assert "Movet" not in usernames


def test_get_votes(entry_helper):
    entry_id = 70475387
    users = entry_helper.get_votes(entry_id)
    usernames = [user["username"] for user in users]
    assert "Movet" in usernames
