from typing import TYPE_CHECKING, Generic, TypedDict, TypeVar

if TYPE_CHECKING:
    from .wykop_api import HttpMethod, WykopAPI

T = TypeVar("T")


class DictResponse(Generic[T], TypedDict):
    data: T


class DictPagination(TypedDict):
    per_page: int
    total: int


class DictPaginationLogged(TypedDict):
    next: str
    prev: str | None


class DictLoggedPaginatedResponse(Generic[T], TypedDict):
    data: T
    pagination: DictPagination | DictPaginationLogged


class DictPaginatedResponse(Generic[T], TypedDict):
    data: T
    pagination: DictPagination


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
