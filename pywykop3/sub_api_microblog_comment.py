from datetime import datetime
from typing import cast

from .methods import HttpMethod
from .sub_api import DictPaginatedResponse, DictResponse, SubApi
from .utils import NotEmptyDict, datetime_to_string


class ApiMicroblogComment(SubApi):
    def get_comments(self, entry_id: int) -> DictPaginatedResponse[list]:
        return cast(
            DictPaginatedResponse,
            self.send_request(
                HttpMethod.GET, url_parts=["entries", entry_id, "comments"]
            ),
        )

    def add_comment(
        self,
        entry_id: int,
        content: str,
        embed: str | None = None,
        photo: str | None = None,
        adult: bool = False,
    ) -> DictResponse[dict]:
        body = NotEmptyDict()
        body["content"] = content
        body["photo"] = photo
        body["embed"] = embed
        body["adult"] = adult
        return cast(
            DictResponse[dict],
            self.send_request(
                HttpMethod.POST,
                url_parts=["entries", entry_id, "comments"],
                payload={"data": body},
            ),
        )

    def edit_comment(
        self,
        entry_id: int,
        comment_id: int,
        content: str,
        embed: str | None = None,
        photo: str | None = None,
        adult: bool = False,
    ) -> DictResponse[dict]:
        body = NotEmptyDict()
        body["content"] = content
        body["photo"] = photo
        body["embed"] = embed
        body["adult"] = adult
        return cast(
            DictResponse[dict],
            self.send_request(
                HttpMethod.PUT,
                url_parts=["entries", entry_id, "comments", comment_id],
                payload={"data": body},
            ),
        )

    def get_comment(self, entry_id: int, comment_id: int) -> DictResponse[dict]:
        return cast(
            DictResponse[dict],
            self.send_request(
                HttpMethod.GET,
                url_parts=["entries", entry_id, "comments", comment_id],
            ),
        )

    def delete_comment(self, entry_id: int, comment_id: int) -> str:
        return cast(
            str,
            self.send_request(
                HttpMethod.DELETE,
                url_parts=["entries", entry_id, "comments", comment_id],
            ),
        )

    def get_newer_comments_amount(
        self, entry_id: int, date: datetime
    ) -> DictResponse[dict]:
        params = {"date": datetime_to_string(date)}
        return cast(
            DictResponse[dict],
            self.send_request(
                HttpMethod.GET,
                url_parts=["entries", entry_id, "comments", "newer"],
                params=params,
            ),
        )

    def votes(
        self,
        entry_id: int,
        comment_id: int,
        page: int | str | None = None,
    ) -> DictPaginatedResponse[list[dict]]:
        """_summary_

        Args:
            entry_id (int): _description_
            page (int | str | None, optional): Numer strony do pobrania.
            Prawdopodomnie można ominąć.
            Defaults to None.

        Returns:
            DictPaginatedResponse: _description_
        """
        params: dict[str, str | int | None] = NotEmptyDict()
        params["page"] = page

        return cast(
            DictPaginatedResponse[list[dict]],
            self.send_request(
                HttpMethod.GET,
                url_parts=["entries", entry_id, "comments", comment_id, "votes"],
                params=params,
            ),
        )

    def vote(
        self,
        entry_id: int,
        comment_id: int,
    ) -> None:
        return cast(
            None,
            self.send_request(
                HttpMethod.POST,
                url_parts=["entries", entry_id, "comments", comment_id, "votes"],
            ),
        )

    def unvote(
        self,
        entry_id: int,
        comment_id: int,
    ) -> None:
        return cast(
            None,
            self.send_request(
                HttpMethod.DELETE,
                url_parts=["entries", entry_id, "comments", comment_id, "votes"],
            ),
        )
