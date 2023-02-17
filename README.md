# pywykop3

Python REST API Client for Wykop2 (via api v3)

[![Pylint](https://github.com/KaiserMovet/pywykop3/actions/workflows/pylint.yml/badge.svg)](https://github.com/KaiserMovet/pywykop3/actions/workflows/pylint.yml)
[![Pytest](https://github.com/KaiserMovet/pywykop3/actions/workflows/python-package.yml/badge.svg)](https://github.com/KaiserMovet/pywykop3/actions/workflows/python-package.yml)
[![Upload Python Package](https://github.com/KaiserMovet/pywykop3/actions/workflows/python-publish.yml/badge.svg)](https://github.com/KaiserMovet/pywykop3/actions/workflows/python-publish.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Usage

    from pywykop3 import WykopAPI

    # Without login
    api = WykopAPI(key=key, secret=secret)

    # User logged in
    api = WykopAPI(refresh_token=refresh_token)

## Obtaining Refresh Token

1.  Execute code:

        from pywykop3 import WykopAPI
        api = WykopAPI(key=key, secret=secret)
        url = api.connect()
        print(url)

2.  Open url, log into your accout
3.  Allow access to your account
4.  Copy refresh token from url ('rtoken' variable)

## Available methods

### Users

- get_users_autocomplete

### Tags

- get_users_autocomplete
- get_tags_popular
- get_tags_popular_user_tags
- get_tags_related
- get_tag
- put_tag
- get_tag_stream
- get_tag_newer
- get_tag_users
- post_tag_user
- delete_tag_user

### Mikroblog

- get_entries
- post_entries
- get_entry_by_id
- put_entries
- delete_entry_by_id
- get_entry_votes
- post_entry_vote
- delete_entry_vote
- get_entries_newer

### Mikroblog - komentarze

- get_entry_comments
- post_entry_comment
- get_entry_comment
- put_entry_comment
- delete_entry_comment
- get_entry_comment_votes
- post_entry_comment_vote
- delete_entry_comment_vote
