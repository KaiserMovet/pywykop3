from typing import TYPE_CHECKING, Any, TypedDict

if TYPE_CHECKING:
    from .wykop_api import HttpMethod, WykopAPI


class DictResponse(TypedDict):
    data: Any


class DictPaginationNotLogged(TypedDict):
    per_page: int
    total: int


class DictPaginationLogged(TypedDict):
    next: str
    prev: str | None


class DictPaginatedResponse(TypedDict):
    data: Any
    pagination: DictPaginationNotLogged | DictPaginationLogged


class SubApi:
    def __init__(self, api: "WykopAPI") -> None:
        self.api = api

    def send_request(
        self,
        method: "HttpMethod",
        url_parts: list,
        payload: dict | None = None,
        params: dict | None = None,
    ) -> DictResponse | DictPaginatedResponse:
        return self.api.send_request(method, url_parts, payload, params)
