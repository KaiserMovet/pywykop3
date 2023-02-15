import logging
from datetime import datetime
from typing import Dict, List

from .connector import Methods, WykopConnector, WykopResponse


class ApiException(Exception):
    def __init__(self, code, msg) -> None:
        super().__init__(f"CODE {code}: {msg}")


class WykopAPI:
    def __init__(
        self,
        connector: WykopConnector | None = None,
        key: str | None = None,
        secret: str | None = None,
        refresh_token: str | None = None,
    ) -> None:

        self.connector = connector or WykopConnector(key, secret, refresh_token)

    def connect(self) -> str:
        """
        Istnieje możliwość zalogowania użytkownika przy użyciu WykopConnect.
        Aplikacja która próbuje zalogować użytkownika powinna posiadać
        odpowiednie uprawnienia nadane przez administratora.
        """
        return self.connector.connect()

    def raise_error_if_needed(
        self, res: WykopResponse, error_dict: Dict | None = None
    ) -> None:
        error_dict = error_dict or {}
        for code, msg in error_dict.items():
            if res.code == code:
                raise ApiException(res.code, f"{msg} {res.error}")
        if 200 > res.code or res.code > 299:
            raise ApiException(res.code, str(res.error))

    # Users

    def get_users_autocomplete(self, query: str) -> List:
        """
        Podpowiada użytkowników po nickname

        Args:
            query (str): Zapytanie

        Returns:
            List: Kolekcja wyszukanych użytkowników
        """
        endpoint = "users/autocomplete"
        data = {"query": query}
        res = self.connector.request(Methods.GET, endpoint, params=data)
        self.raise_error_if_needed(
            res, {400: "Brak parametru query lub parametr zbyt krótki"}
        )
        return res.data  # type: ignore

    # Tags

    def get_tags_autocomplete(self, query: str) -> List:
        """
        Podpowiada tagi.

        Args:
            query (str): Zapytanie

        Returns:
            List: Kolekcja wyszukanych tagów (max do 10 wyników)
        """
        endpoint = "tags/autocomplete"
        data = {"query": query}
        res = self.connector.request(Methods.GET, endpoint, params=data)
        self.raise_error_if_needed(
            res, {400: "Brak parametru query lub parametr zbyt krótki"}
        )
        return res.data  # type: ignore

    def get_tags_popular(self) -> List:
        """
        Zwraca listę popularnych tagów.

        Returns:
            List: Lista tagów
        """
        endpoint = "tags/popular"
        res = self.connector.request(Methods.GET, endpoint)
        self.raise_error_if_needed(res)
        return res.data  # type: ignore

    def get_tags_popular_user_tags(self) -> List:
        """
        Zwraca listę popularnych tagów autorskich.

        Returns:
            List: Kolekcja popularnych tagów autorskich (max do 10 wyników)
        """
        endpoint = "tags/popular-user-tags"
        res = self.connector.request(Methods.GET, endpoint)
        self.raise_error_if_needed(res)
        return res.data  # type: ignore

    def get_tags_related(self, tag_name: str) -> List:
        """
        Powiązane tagi

        Args:
            tag_name (str): Nazwa tagu

        Returns:
            List: Kolekcja powiązanych tagów (max do 10 wyników)
        """
        endpoint = f"tags/{tag_name}/related"
        res = self.connector.request(Methods.GET, endpoint)
        self.raise_error_if_needed(
            res, {400: "Brak tagu lub tag jest za krótki"}
        )
        return res.data  # type: ignore

    def get_tag(self, tag_name: str) -> Dict:
        endpoint = f"tags/{tag_name}"
        res = self.connector.request(Methods.GET, endpoint)
        self.raise_error_if_needed(res)
        return res.data  # type: ignore

    def put_tag(self, tag_name: str, data: Dict) -> None:
        endpoint = f"tags/{tag_name}"
        res = self.connector.request(Methods.PUT, endpoint, data=data)
        self.raise_error_if_needed(
            res,
            {
                400: "Brak uprawnień do usunięcia znaleziska.",
                404: "Tag nie istnieje",
                409: "Wystąpił błąd podczas walidacji formularza.",
            },
        )

    def get_tag_stream(
        self,
        tag_name: str,
        page: int | str,
        sort: str = "best",
        type_of_content: str = "all",
        year: int | None = None,
        month: int | None = None,
        page_count: int = 1,
    ) -> List:
        """
        Zwraca pełną liste wpisów i znalezisk z konkretnego tagu

        UWAGA: Parametr page przyjmuje dla użytkowników niezalogowanych int z
        numerem strony, a dla zalogowanych hash strony.

        UWAGA2: Standardowa paginacja jest dostępna tylko dla użytkowników
        niezalogowanych. Paginacja dla użytkowników zalogowanych będzie
        zwracać hash next dla następnej strony i prev dla poprzedniej.

        Args:
            tag_name (str): Nazwa tagu
            page (int | str): Numer strony do pobrania.
            sort (str, optional): Rodzaj sortowania. Available values : "all",
            "best". Defaults to "best".
            type_of_content (str, optional): Rodzaj. Available values : "all",
            "author", "link", "entry". Defaults to "all".
            year (int | None, optional): Rok. Defaults to None.
            month (int | None, optional): Miesiąc. Defaults to None.
            page_count (int, optional): Liczba stron do pobrania. Defaults to 1.

        Returns:
            List: Lista wpisów i znalezisk
        """
        endpoint = f"tags/{tag_name}/stream"
        params: Dict[str, str | int] = {}
        params["sort"] = sort
        params["type"] = type_of_content
        if year:
            params["year"] = year
        if month:
            params["month"] = month

        res = self.connector.request_with_pagination(
            Methods.GET, endpoint, page=page, page_count=page_count
        )
        self.raise_error_if_needed(
            res,
            {
                404: "Podany tag nie istnieje lub jego dane są niedostępne.",
            },
        )
        return res.data  # type: ignore

    def get_tag_newer(
        self,
        tag_name: str,
        type_of_content: str = "all",
        sort: str = "best",
        date: datetime | None = None,
        obj_id: str | None = None,
    ) -> int:
        """
        Zwraca informację, czy są wpisy, linki w tagu

        Args:
            tag_name (str): Nazwa tagu
            type_of_content (str, optional): Rodzaj. Available values : "all",
            "author", "link", "entry". Defaults to "all".
            sort (str, optional): Rodzaj sortowania. Available values : "all",
            "best". Defaults to "best".
            date (datetime | None, optional): Data, od której sprawdzamy, czy
            pojawiły się nowe treści. Defaults to None.
            obj_id (str | None, optional): Identyfikator ostatniego widzianego
            wpisu lub znaleziska. Defaults to None.

        Returns:
            int: Licznik nowych obiektów
        """

        endpoint = f"tags/{tag_name}/newer"
        params: Dict[str, str | int] = {}
        params["sort"] = sort
        params["type"] = type_of_content
        if date:
            params["date"] = date.strftime("%Y-%m-%d %H:%M:%S")
        if obj_id:
            params["id"] = obj_id

        res = self.connector.request(Methods.GET, endpoint, params=params)
        self.raise_error_if_needed(
            res, {404: "Podany tag nie istnieje lub jego dane są niedostępne."}
        )
        return res.data.get("count", 0)  # type: ignore

    def get_tag_users(self, tag_name: str) -> List:
        """
        Lista autorów tagu autorskiego

        Args:
            tag_name (str): Nazwa tagu

        Returns:
            List: Kolekcja autorów tagu (short profile)
        """
        endpoint = f"tags/{tag_name}/users"
        res = self.connector.request(Methods.GET, endpoint)
        self.raise_error_if_needed(
            res,
            {
                404: "Podany tag nie istnieje lub jego dane są niedostępne.",
            },
        )
        return res.data  # type: ignore

    def post_tag_user(self, tag_name: str, username: str) -> None:
        """
        Dodanie nowego współautora tagu (głównego dodaje moderator)

        Args:
            tag_name (str): Nazwa tagu
            username (str): Nazwa użytkownika
        """
        endpoint = f"tags/{tag_name}/users/{username}"
        res = self.connector.request(Methods.POST, endpoint)
        self.raise_error_if_needed(
            res,
            {
                400: "Brak wymaganych uprawnień.",
                404: "Podany tag nie istnieje lub jego dane są niedostępne.",
            },
        )

    def delete_tag_user(self, tag_name: str, username: str) -> None:
        """
        Usuwanie współautora tagu (głównego dodaje moderator)

        Args:
            tag_name (str): Nazwa tagu
            username (str): Nazwa użytkownika
        """
        endpoint = f"tags/{tag_name}/users/{username}"
        res = self.connector.request(Methods.DELETE, endpoint)
        self.raise_error_if_needed(
            res,
            {
                400: "Brak wymaganych uprawnień.",
                404: "Podany tag nie istnieje lub jego dane są niedostępne.",
            },
        )
