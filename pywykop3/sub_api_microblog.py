from typing import Literal, cast

from .methods import HttpMethod
from .sub_api import DictLoggedPaginatedResponse, DictResponse, SubApi
from .utils import NotEmptyDict


class ApiMicroblog(SubApi):
    def get_entries(
        self,
        page: int | str | None = None,
        limit: int = 25,
        category: str | None = None,
        bucket: str | None = None,
        sort: Literal["newest", "active", "hot"] = "hot",
        last_update: Literal[1, 2, 3, 6, 12, 24] = 12,
    ) -> DictLoggedPaginatedResponse[list]:
        params: dict[str, str | int | None] = NotEmptyDict()
        params["page"] = page
        params["limit"] = limit
        params["sort"] = sort
        params["last_update"] = last_update
        params["category"] = category
        params["bucket"] = bucket
        return cast(
            DictLoggedPaginatedResponse[list],
            self.send_request(HttpMethod.GET, url_parts=["entries"], params=params),
        )

    def get_entry(self, entry_id: int) -> DictResponse:
        return cast(
            DictResponse,
            self.send_request(HttpMethod.GET, url_parts=["entries", entry_id]),
        )

    def add_entry(
        self,
        content: str,
        photo: str | None = None,
        embed: str | None = None,
        survey: str | None = None,
        adult: bool = False,
    ) -> DictResponse:
        """
        Dodanie nowego wpisu na mikroblogu

        Args:
            content (str): Treść własna użytkownika.
            photo (str | None, optional): Załącznik użytkownika.
            W celu dodania należy podać "key" pliku z media/photo.
            Akceptowane są tylko pliki przesłane jako typ comments.
            Defaults to None.
            embed (str | None, optional): Unikatowy identyfikator embed.
            Defaults to None.
            survey (str | None, optional): Ankieta użytkownika.
            W celu dodania należy podać Indentyfikator. Defaults to None.
            adult (bool, optional): Wpis tylko dla dorosłych.
            Defaults to False.

        Returns:
            DictResponse: Dodany wpis
        """
        body = NotEmptyDict()
        body["content"] = content
        body["photo"] = photo
        body["embed"] = embed
        body["survey"] = survey
        body["adult"] = adult
        return cast(
            DictResponse,
            self.send_request(
                HttpMethod.POST, url_parts=["entries"], payload={"data": body}
            ),
        )

    def edit_entry(
        self,
        entry_id: int,
        content: str | None = None,
        photo: str | None = None,
        embed: str | None = None,
        survey: str | None = None,
        adult: bool = False,
    ) -> DictResponse:
        """
        Dodanie nowego wpisu na mikroblogu

        Args:
            entry_id (int): Id wpisu
            content (str | None, optional): Treść własna użytkownika.
            Defaults to None.
            photo (str | None, optional): Załącznik użytkownika.
            W celu dodania należy podać "key" pliku z media/photo.
            Akceptowane są tylko pliki przesłane jako typ comments.
            Defaults to None.
            embed (str | None, optional): Unikatowy identyfikator embed.
            Defaults to None.
            survey (str | None, optional): Ankieta użytkownika.
            W celu dodania należy podać Indentyfikator. Defaults to None.
            adult (bool, optional): Wpis tylko dla dorosłych.
            Defaults to False.

        Returns:
            DictResponse: Dodany wpis
        """
        body = NotEmptyDict()
        body["content"] = content
        body["photo"] = photo
        body["embed"] = embed
        body["survey"] = survey
        body["adult"] = adult
        return cast(
            DictResponse,
            self.send_request(
                HttpMethod.PUT, url_parts=["entries", entry_id], payload={"data": body}
            ),
        )

    def delete_entry(self, entry_id: int) -> DictResponse:
        return cast(
            DictResponse,
            self.send_request(HttpMethod.DELETE, url_parts=["entries", entry_id]),
        )

    def votes(
        self,
        entry_id: int,
        page: int | str | None = None,
    ) -> DictLoggedPaginatedResponse[list]:
        """_summary_

        Args:
            entry_id (int): _description_
            page (int | str | None, optional): Numer strony do pobrania.
            Prawdopodomnie można ominąć.
            Defaults to None.

        Returns:
            DictLoggedPaginatedResponse: _description_
        """
        params: dict[str, str | int | None] = NotEmptyDict()
        params["page"] = page

        return cast(
            DictLoggedPaginatedResponse[list],
            self.send_request(
                HttpMethod.GET, url_parts=["entries", entry_id, "votes"], params=params
            ),
        )

    def vote(self, entry_id: int) -> None:
        return cast(
            None,
            self.send_request(
                HttpMethod.POST, url_parts=["entries", entry_id, "votes"]
            ),
        )

    def unvote(self, entry_id: int) -> None:
        return cast(
            None,
            self.send_request(
                HttpMethod.DELETE, url_parts=["entries", entry_id, "votes"]
            ),
        )

    def get_newer_entries_amount(
        self,
        entry_id: int,
        category: str | None = None,
    ) -> DictResponse[dict]:
        params = NotEmptyDict()
        params["category"] = category
        return cast(
            DictResponse[dict],
            self.send_request(
                HttpMethod.GET, url_parts=["entries", entry_id, "newer"], params=params
            ),
        )

    def observe(self, entry_id: int) -> None:
        return cast(
            None,
            self.send_request(
                HttpMethod.POST, url_parts=["entries", entry_id, "observed-discussions"]
            ),
        )

    def unobserve(self, entry_id: int) -> None:
        return cast(
            None,
            self.send_request(
                HttpMethod.DELETE,
                url_parts=["entries", entry_id, "observed-discussions"],
            ),
        )
