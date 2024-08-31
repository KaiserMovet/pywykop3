import logging
import random
import re
import string
import time
from contextlib import contextmanager
from typing import Any, NamedTuple


class CommentID(NamedTuple):
    entry_id: int
    comment_id: int


def random_string(length=25) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def run_function_with_retry(
    function,
    args=None,
    kwargs=None,
    max_retries=5,
    wait_time=3,
    wait_multiplier=2,
) -> Any:
    args = args or []
    kwargs = kwargs or {}
    last_exc: Exception = None  # type: ignore
    for _ in range(max_retries):
        try:
            result = function(*args, **kwargs)
            return result
        except Exception as exc:  # pylint: disable=broad-exception-caught
            last_exc = exc
            logging.warning(
                "Cannot run %s. Waiting %s seconds. Exception: %s",
                str(function),
                str(wait_time),
                str(exc),
            )
            time.sleep(wait_time)
            wait_time *= wait_multiplier
    raise last_exc


@contextmanager
def suppress_exceptions(exception=Exception, *exceptions):
    exceptions = tuple([exception]) + exceptions
    try:
        yield
    except exceptions as exc:
        logging.warning("Exception was raised", exc_info=exc)
        pass


def get_last_5_voters(entry: dict) -> list[str]:
    return extract_usernames_from_user_list(entry["votes"]["users"])


def extract_usernames_from_user_list(user_list: list[dict]) -> list[str]:
    return [user["username"] for user in user_list]


def remove_whitespace(text: str) -> str:
    return re.sub(r"\s+", "", text)
