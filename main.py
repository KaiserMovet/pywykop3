import sys
from pprint import pprint
from typing import cast

import logger
from pywykop3 import WykopAPI


def get_token() -> str:
    with open("refresh_token.txt", "r", encoding="utf-8") as file:
        file_content = file.read()  # Wczytanie całej zawartości pliku do zmiennej
    return file_content


def save_token(token):
    with open("refresh_token.txt", "w", encoding="utf-8") as file:
        file.write(token)  # Zapisuje zawartość zmiennej do pliku


def main(token: str) -> str | None:
    api = WykopAPI(refresh_token=token)
    print(api.header)
    return api.refresh_token


if __name__ == "__main__":
    logger.init()
    token = get_token()
    try:
        token = main(token)
    except Exception as e:
        raise e
    finally:
        if token:
            save_token(token)
