# pywykop3

Python REST API Client for Wykop2 (via api v3)

[![Pylint](https://github.com/KaiserMovet/pywykop3/actions/workflows/pylint.yml/badge.svg)](https://github.com/KaiserMovet/pywykop3/actions/workflows/pylint.yml)
[![Create Release](https://github.com/KaiserMovet/pywykop3/actions/workflows/create_release.yml/badge.svg)](https://github.com/KaiserMovet/pywykop3/actions/workflows/create_release.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Full documentation can be found [HERE](https://kaisermovet.github.io/pywykop3/index.html)
API documentation can be found [HERE](https://kaisermovet.github.io/pywykop3/api.html)

## Usage

    from pywykop3 import WykopAPI

    # Without login
    api = WykopAPI(key=key, secret=secret)

    # User logged in
    api = WykopAPI(refresh_token=refresh_token)

    list_of_users = api.get_entry_comment_votes(70432439, 249723413)

## Obtaining Refresh Token

1.  Execute code:

        from pywykop3 import WykopAPI
        api = WykopAPI(key=key, secret=secret)
        url = api.connect()
        print(url)

2.  Open url, log into your accout
3.  Allow access to your account
4.  Copy refresh token from url ('rtoken' variable)

After execution of your app, you should save new refresh-token
(wyko_api.connector.refresh_token) and use it next time

## Available methods

- ❌ - Not tested
- ✔️ - Tested
- ⛔ - Unable to test

### Users

| Method                                                                                                                 | Tested? |
| ---------------------------------------------------------------------------------------------------------------------- | ------- |
| [get_users_autocomplete](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_users_autocomplete) | ✔️      |

### Tags

| Method                                                                                                                         | Tested? |
| ------------------------------------------------------------------------------------------------------------------------------ | ------- |
| [get_tags_popular](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_tags_popular)                     | ❌      |
| [get_tags_popular_user_tags](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_tags_popular_user_tags) | ❌      |
| [get_tags_related](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_tags_related)                     | ❌      |
| [get_tag](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_tag)                                       | ❌      |
| [put_tag](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.put_tag)                                       | ❌      |
| [get_tag_stream](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_tag_stream)                         | ❌      |
| [get_tag_newer](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_tag_newer)                           | ❌      |
| [get_tag_users](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_tag_users)                           | ❌      |
| [post_tag_user](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.post_tag_user)                           | ❌      |
| [delete_tag_user](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.delete_tag_user)                       | ❌      |

### Mikroblog

| Method                                                                                                         | Tested? |
| -------------------------------------------------------------------------------------------------------------- | ------- |
| [get_entries](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_entries)               | ❌      |
| [post_entry](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.post_entry)                 | ✔️      |
| [get_entry_by_id](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_entry_by_id)       | ✔️      |
| [put_entry](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.put_entry)                   | ✔️      |
| [delete_entry_by_id](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.delete_entry_by_id) | ✔️      |
| [get_entry_votes](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_entry_votes)       | ✔️      |
| [post_entry_vote](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.post_entry_vote)       | ⛔      |
| [delete_entry_vote](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.delete_entry_vote)   | ⛔      |
| [get_entries_newer](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_entries_newer)   | ❌      |

### Mikroblog - komentarze

| Method                                                                                                                       | Tested? |
| ---------------------------------------------------------------------------------------------------------------------------- | ------- |
| [get_entry_comments](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_entry_comments)               | ❌      |
| [post_entry_comment](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.post_entry_comment)               | ❌      |
| [get_entry_comment](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_entry_comment)                 | ❌      |
| [put_entry_comment](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.put_entry_comment)                 | ❌      |
| [delete_entry_comment](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.delete_entry_comment)           | ❌      |
| [get_entry_comment_votes](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.get_entry_comment_votes)     | ❌      |
| [post_entry_comment_vote](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.post_entry_comment_vote)     | ❌      |
| [delete_entry_comment_vote](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.delete_entry_comment_vote) | ❌      |

### Media

| Method                                                                                                                   | Tested? |
| ------------------------------------------------------------------------------------------------------------------------ | ------- |
| [post_media_photo](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.post_media_photo)               | ✔️      |
| [post_media_photo_by_url](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.post_media_photo_by_url) | ✔️      |
| [delete_media_photo](https://kaisermovet.github.io/pywykop3/api.html#pywykop3.api.WykopAPI.delete_media_photo)           | ❌      |
