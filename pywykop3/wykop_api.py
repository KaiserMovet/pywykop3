from enum import Enum
from typing import Any

import requests
from requests.compat import urljoin

from .methods import HttpMethod
from .sub_api_microblog import ApiMicroblog


class WykopConnectorException(Exception): ...


class WykopAPI:
    """
    Main interface to communicate with Wykop
    You need to provide

        - key
        - secret

        OR

        - refresh token

    If you pass key and secret, Wykop will provide information as
    for non-logged in users.
    If you refresh_token, Wykop will provide information as
    for logged in users.

    Args:
        key (str | None, optional): Key. Defaults to None.
        secret (str | None, optional): Secret. Defaults to None.
        refresh_token (str | None, optional): Refresh token. To obtain it,
            see :meth:`connect()` method. Defaults to None.
    """

    URL = "https://wykop.pl/api/v3/"

    def __init__(
        self,
        key: str | None = None,
        secret: str | None = None,
        refresh_token: str | None = None,
    ):
        self._key = key
        self._secret = secret
        self.refresh_token = refresh_token
        self._token: str | None = None
        self._set_token()

        self.microblog = ApiMicroblog(self)

    @property
    def header(self) -> dict[str, str]:
        print(self._token)
        return {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}",
        }

    @classmethod
    def build_url(cls, *args):
        path = "/".join(map(str, args))
        return urljoin(cls.URL, path)

    def _set_token(self):
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        if self._key and self._secret:
            # Auth
            url = urljoin(self.URL, "auth")
            data = {"key": self._key, "secret": self._secret}
        elif self.refresh_token:
            # Refresh token
            url = urljoin(self.URL, "refresh-token")
            data = {"refresh_token": self.refresh_token}

        else:
            raise ValueError("You need to provide key and secret OR refresh_token")

        res = requests.post(
            url=url, json={"data": data}, headers=header, timeout=15
        ).json()

        self.refresh_token = res["data"].get("refresh_token")
        self._token = res["data"]["token"]

    def get_login_link(self) -> str:
        """LInk that allow to obtain refresh token."""
        res = requests.get(self.build_url("connect"), headers=self.header, timeout=15)
        return res.json()["data"]["connect_url"]

    def send_request(
        self,
        method: HttpMethod,
        url_parts: list,
        payload: dict | None = None,
        params: dict | None = None,
    ) -> Any:
        url = self.build_url(*url_parts)
        response = requests.request(
            method=method.value,  # Metoda HTTP (np. GET, POST)
            url=url,  # Zbudowany URL
            headers=self.header,  # Nagłówki, np. Authorization
            json=payload,
            params=params,
        )
        print(f"{payload=}")
        print(f"{params=}")

        response.raise_for_status()
        if not response.text:
            return None
        return response.json()
