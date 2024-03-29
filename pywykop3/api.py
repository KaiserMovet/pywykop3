from datetime import datetime
from typing import Dict, List, NewType

from .connector import Methods, WykopConnector, WykopResponse
from .utils import NotEmptyDict

User = NewType("User", Dict)
Entry = NewType("Entry", Dict)
Comment = NewType("Comment", Dict)
Photo = NewType("Photo", Dict)


class ApiException(Exception):
    """
    This exception is raised by :class:`WykopAPI` when code of request is other than 2xx.
    Exception has 2 additional attributes:

        - stacode - response code of request
        - api_msg - message
    """

    def __init__(self, code: int, api_msg: str) -> None:
        """
        Api Exception

        Args:
            code (int): code of request
            api_msg (str): message
        """
        self.code = code
        self.api_msg = api_msg
        super().__init__(f"CODE {self.code}: {api_msg}")


class WykopAPI:
    """
    Main interface to communicate with Wykop
    You need to provide

        - connector

        OR

        - key
        - secret

        OR

        - refresh token

    If you pass key and secret, Wykop will provide information as
    for non-logged in users.
    If you refresh_token, Wykop will provide information as
    for logged in users.

    Args:
        connector (WykopConnector | None, optional): Connector object. Can be safely ignored.
            Defaults to None.
        key (str | None, optional): Key. Defaults to None.
        secret (str | None, optional): Secret. Defaults to None.
        refresh_token (str | None, optional): Refresh token. To obtain it,
            see :meth:`connect()` method. Defaults to None.
    """

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
        page: int | str | None = None,
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
            page (int | str| None): Numer strony do pobrania. Defaults to None.
            sort (str, optional): Rodzaj sortowania. Available values : "all",
            "best". Defaults to "best".
            type_of_content (str, optional): Rodzaj. Available values : "all",
            "author", "link", "entry". Defaults to "all".
            year (int | None, optional): Rok. Defaults to None.
            month (int | None, optional): Miesiąc. Defaults to None.
            page_count (int, optional): Liczba stron do pobrania.
            Podaj -1, żeby pobrać wszystko. Defaults to 1.

        Returns:
            List: Lista wpisów i znalezisk
        """
        endpoint = f"tags/{tag_name}/stream"
        params: Dict[str, str | int | None] = NotEmptyDict()
        params["sort"] = sort
        params["type"] = type_of_content
        params["year"] = year
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
        params: Dict[str, str | int | None] = NotEmptyDict()
        params["sort"] = sort
        params["type"] = type_of_content
        params["date"] = date.strftime("%Y-%m-%d %H:%M:%S") if date else None
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

    # Mikroblog

    def get_entries(
        self,
        sort: str = "hot",
        last_update: int = 12,
        page_count: int = 1,
        page: int | str | None = None,
        category: str | None = None,
        bucket: str | None = None,
    ) -> List[Entry]:
        """
        Zwraca wpisy z mikrobloga. UWAGA: Parametr page przyjmuje dla
        użytkowników niezalogowanych int z numerem strony, a dla zalogowanych
        hash strony. UWAGA2: Standardowa paginacja jest dostępna tylko dla
        użytkowników niezalogowanych. Paginacja dla użytkowników zalogowanych
        będzie zwracać hash next dla następnej strony i prev dla poprzedniej.

        Args:
            sort (str, optional): Rodzaj sortowania.
                Available values : newest, active, hot. Defaults to "hot".
            last_update (int, optional): Pokaż wyniki z ostatnich godzin
                [1, 2, 3, 6, 12, 24]. Filtr dostępny tylko wraz z filtrem gorące.
                Defaults to 12.
            page_count (int, optional): Liczba stron do pobrania.
                Podaj -1, żeby pobrać wszystko. Defaults to 1.
            page (int | str | None, optional): Numer strony do pobrania.
                Defaults to None.
            category (str | None, optional): Kategoria.
                Defaults to None.
            bucket (str | None, optional): Hash kategorii użytkownika. Defaults to None.

        Returns:
            List: Wpisy z mikrobloga.
        """

        endpoint = "entries"

        params: Dict[str, str | int | None] = NotEmptyDict()
        params["sort"] = sort
        params["last_update"] = last_update
        params["category"] = category
        params["bucket"] = bucket

        res = self.connector.request_with_pagination(
            Methods.GET, endpoint, page=page, page_count=page_count
        )
        self.raise_error_if_needed(
            res,
            {
                400: "Osiągnięto limit paginacji.",
            },
        )
        return res.data  # type: ignore

    def post_entry(
        self,
        content: str,
        photo: str | None = None,
        embed: str | None = None,
        survey: str | None = None,
        adult: bool = False,
    ) -> Entry:
        """
        Dodawanie nowego wpisu na mikroblogu

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
            adult (bool, optional): Wpis tylko dla dorosłych. Defaults to False.

        Returns:
            Dict: Dodany wpis
        """

        endpoint = "entries"
        data: Dict[str, str | int | None] = NotEmptyDict()
        data["content"] = content
        data["photo"] = photo
        data["embed"] = embed
        data["survey"] = survey
        data["adult"] = adult
        res = self.connector.request(Methods.POST, endpoint, data=data)
        self.raise_error_if_needed(
            res,
            {
                400: "Gdy użytkownik wykona niepoprawny request.",
                409: "Wystąpił błąd podczas walidacji formularza.",
            },
        )
        return res.data  # type: ignore

    def get_entry_by_id(self, entry_id: int) -> Entry:
        """
        Zwraca wpisz z mikrobloga.

        Args:
            entry_id (int): Identyfikator wpisu

        Returns:
            Dict: Wpis z mikrobloga
        """
        endpoint = f"/entries/{entry_id}"
        res = self.connector.request(Methods.GET, endpoint)
        self.raise_error_if_needed(
            res,
            {
                404: "Nie odnaleziono wpisu.",
            },
        )
        return res.data  # type: ignore

    def put_entry(
        self,
        entry_id: int,
        content: str,
        photo: str | None = None,
        embed: str | None = None,
        survey: str | None = None,
        adult: bool = False,
    ) -> Entry:
        """
        Edycja wpisu na mikroblogu. Można modyfikwać tylko własne wpisy.
        Autor może modyfikować wpis przez 15 minut od daty dodania.

        Args:
            entry_id (int): Identyfikator wpisu
            content (str): Treść własna użytkownika.
            photo (str | None, optional): Załącznik użytkownika.
                W celu dodania należy podać "key" pliku z media/photo.
                Akceptowane są tylko pliki przesłane jako typ comments.
                Defaults to None.
            embed (str | None, optional): Unikatowy identyfikator embed.
                Defaults to None.
            survey (str | None, optional): Ankieta użytkownika.
                W celu dodania należy podać Indentyfikator. Defaults to None.
            adult (bool, optional): Wpis tylko dla dorosłych. Defaults to False.

        Returns:
            Dict: Dodany wpis
        """

        endpoint = f"/entries/{entry_id}"
        data: Dict[str, str | int | None] = NotEmptyDict()
        data["content"] = content
        data["photo"] = photo
        data["embed"] = embed
        data["survey"] = survey
        data["adult"] = adult
        res = self.connector.request(Methods.PUT, endpoint, data=data)
        self.raise_error_if_needed(
            res,
            {
                400: "Brak uprawnień do modyfikacji wpisu.",
                404: "Nie odnaleziono wpisu.",
                409: "Wystąpił błąd podczas walidacji formularza.",
            },
        )
        return res.data  # type: ignore

    def delete_entry_by_id(self, entry_id: int) -> None:
        """
        Usuwanie wpisu. Autor może zawsze usunąć własny wpis.

        Args:
            entry_id (int): Identyfikator wpisu

        """
        endpoint = f"/entries/{entry_id}"
        res = self.connector.request(Methods.DELETE, endpoint)
        self.raise_error_if_needed(
            res,
            {
                400: "Brak uprawnień do usunięcia wpisu.",
                404: "Nie odnaleziono wpisu.",
            },
        )

    def get_entry_votes(self, entry_id: int) -> List[User]:
        """
        Pobiera nazwy użytkowników którzy głosowali na wpis z mikrobloga.

        Args:
            entry_id (int): Identyfikator wpisu

        Returns:
            List: Lista użytkowników, który oddali głos.
        """
        endpoint = f"/entries/{entry_id}/votes"
        res = self.connector.request(Methods.GET, endpoint)
        self.raise_error_if_needed(
            res,
            {
                404: "Nie odnaleziono wpisu.",
            },
        )
        return res.data  # type: ignore

    def post_entry_vote(self, entry_id: int) -> None:
        """
        Głosowanie na wpis

        Args:
            entry_id (int): Identyfikator wpisu
        """
        endpoint = f"/entries/{entry_id}/votes"
        res = self.connector.request(Methods.POST, endpoint)
        self.raise_error_if_needed(
            res,
            {
                400: "Użytkownik głosował wcześniej na wpis lub jest jego autorem.",
                404: "Nie odnaleziono wpisu.",
            },
        )

    def delete_entry_vote(self, entry_id: str) -> None:
        """
        Cofnięcie głosu na wpis

        Args:
            entry_id (str): Identyfikator wpisu
        """
        endpoint = f"/entries/{entry_id}/votes"
        res = self.connector.request(Methods.DELETE, endpoint)
        self.raise_error_if_needed(
            res,
            {
                400: "Użytkownik nie głosował wcześniej na wpis.",
                404: "Nie odnaleziono wpisu.",
            },
        )

    def get_entries_newer(
        self, entry_id: int, category: str | None = None
    ) -> int:
        """
        Zwraca liczbę nowszych wpisów.

        Args:
            entry_id (int): Identyfikator wpisu
            category (str | None, optional): Kategoria. Defaults to None.

        Returns:
            int: Liczba nowszych wpisów.
        """
        endpoint = f"/entries/{entry_id}/newer"
        params = NotEmptyDict()
        params["category"] = category
        res = self.connector.request(Methods.GET, endpoint, params=params)
        self.raise_error_if_needed(
            res,
            {
                404: "Nie odnaleziono wpisu.",
            },
        )
        return res.data["count"]  # type: ignore

    # Mikroblog - Komentarz

    def get_entry_comments(
        self, entry_id: int, page: int = 1, page_count: int = 1
    ) -> List[Comment]:
        """
        Lista komentarzy do wpisu z mikrobloga

        Args:
            entry_id (int): Identyfikator wpisu
            page (int, optional): Numer strony do pobrania.
                Defaults to 1.
            page_count (int, optional): Liczba stron do pobrania.
                Podaj -1, żeby pobrać wszystko. Defaults to 1.

        Returns:
            List[Comment]: _description_
        """

        endpoint = f"entries/{entry_id}/comments"
        res = self.connector.request_with_pagination(
            Methods.GET, endpoint, page=page, page_count=page_count
        )
        self.raise_error_if_needed(res)
        return res.data  # type: ignore

    def post_entry_comment(
        self,
        entry_id: int,
        content: str,
        embed: str | None = None,
        photo: str | None = None,
        adult: bool = False,
    ) -> Comment:
        """
        Dodawanie nowego komentarza do wpisu na mikroblogu

        Args:
            entry_id (int): Identyfikator wpisu
            content (str): Treść własna użytkownika. Treść może być pusta w
                przypadku dodania innych multimediów.
                W przypadku samej treści musi zawierać min. 5 znaków.
            embed (str | None, optional): Unikatowy identyfikator pliku.
                Defaults to None.
            photo (str | None, optional): Załącznik użytkownika. W celu
                dodania należy podać "key" pliku z media/photo.
                Akceptowane są tylko pliki przesłane jako typ comments.
                Defaults to None.
            adult (bool, optional): Komentarz tylko dla dorosłych.
                Defaults to False.

        Returns:
            Comment: Dodany komentarz
        """
        endpoint = f"entries/{entry_id}/comments"

        data = NotEmptyDict()
        data["content"] = content
        data["embed"] = embed
        data["photo"] = photo
        data["adult"] = adult
        res = self.connector.request(Methods.POST, endpoint, data=data)
        self.raise_error_if_needed(
            res,
            {
                404: "Nie odnaleziono znaleziska lub komentarza",
                409: "Wystąpił błąd podczas walidacji formularza.",
            },
        )
        return res.data  # type: ignore

    def get_entry_comment(self, entry_id: int, comment_id: int) -> Comment:
        """
        Zwraca komentarz z mikroblogu.

        Args:
            entry_id (int): Identyfikator wpisu
            comment_id (int): Identyfikator komentarza

        Returns:
            Comment: Komentarz z mikroblogu
        """
        endpoint = f"entries/{entry_id}/comments/{comment_id}"
        res = self.connector.request(Methods.GET, endpoint)
        self.raise_error_if_needed(
            res,
            {
                404: "Nie odnaleziono wpisu lub komentarza.",
            },
        )
        return res.data  # type: ignore

    def put_entry_comment(
        self,
        entry_id: int,
        comment_id: int,
        content: str,
        embed: str | None = None,
        photo: str | None = None,
        adult: bool = False,
    ) -> Comment:
        """
        Dodawanie nowego komentarza do wpisu na mikroblogu.
        Można modyfikwać tylko własne komentarze.
        Autor może modyfikować komentarz 15 minut od daty dodania.

        Args:
            entry_id (int): Identyfikator wpisu
            comment_id (int): Identyfikator komentarza
            content (str): Treść własna użytkownika. Treść może być pusta w
                przypadku dodania innych multimediów.
                W przypadku samej treści musi zawierać min. 5 znaków.
            embed (str | None, optional): Unikatowy identyfikator pliku.
                Defaults to None.
            photo (str | None, optional): Załącznik użytkownika. W celu
                dodania należy podać "key" pliku z media/photo.
                Akceptowane są tylko pliki przesłane jako typ comments.
                Defaults to None.
            adult (bool, optional): Komentarz tylko dla dorosłych.
                Defaults to False.

        Returns:
            Comment: Zmodyfikowany komentarz
        """
        endpoint = f"entries/{entry_id}/comments/{comment_id}"

        data = NotEmptyDict()
        data["content"] = content
        data["embed"] = embed
        data["photo"] = photo
        data["adult"] = adult
        res = self.connector.request(Methods.PUT, endpoint, data=data)
        self.raise_error_if_needed(
            res,
            {
                400: "Brak uprawnień do modyfikacji komentarza.",
                404: "Nie odnaleziono wpisu lub komentarza.",
                409: "Wystąpił błąd podczas walidacji formularza.",
            },
        )
        return res.data  # type: ignore

    def delete_entry_comment(self, entry_id: int, comment_id: int) -> None:
        """
        Usuwanie komentarza
        Autor komentarza może go usunąć 15 minut od daty
        dodania lub autor wpisu przez cały czas.

        Args:
            entry_id (int): Identyfikator wpisu
            comment_id (int): Identyfikator komentarza
        """
        endpoint = f"entries/{entry_id}/comments/{comment_id}"
        res = self.connector.request(Methods.DELETE, endpoint)
        self.raise_error_if_needed(
            res,
            {
                400: "Brak uprawnień do usunięcia komentarza.",
                404: "Nie odnaleziono wpisu lub komentarza.",
            },
        )

    def get_entry_comment_votes(
        self, entry_id: int, comment_id: int
    ) -> List[User]:
        """
        Pobiera użytkowników którzy głosowali na komentarz z mikroblogu.

        Args:
            entry_id (int): Identyfikator wpisu
            comment_id (int): Identyfikator komentarza

        Returns:
            List[User]: Lista głosujących użytkowników
        """
        endpoint = f"entries/{entry_id}/comments/{comment_id}/votes"
        res = self.connector.request(Methods.GET, endpoint)
        self.raise_error_if_needed(
            res,
            {
                404: "Nie odnaleziono wpisu lub komentarza.",
            },
        )
        return res.data  # type: ignore

    def post_entry_comment_vote(self, entry_id: int, comment_id: int) -> None:
        """
        Głosowanie na wpis

        Args:
            entry_id (int): Identyfikator wpisu
            comment_id (int): Identyfikator komentarza
        """
        endpoint = f"entries/{entry_id}/comments/{comment_id}/votes"
        res = self.connector.request(Methods.POST, endpoint)
        self.raise_error_if_needed(
            res,
            {
                400: "Użytkownik głosował wcześniej na komentarz"
                "lub jest jego autorem.",
                404: "Nie odnaleziono wpisu lub komentarza.",
            },
        )

    def delete_entry_comment_vote(self, entry_id: int, comment_id: int) -> None:
        """
        Cofnięcie głosu na komentarz

        Args:
            entry_id (int): Identyfikator wpisu
            comment_id (int): Identyfikator komentarza
        """
        endpoint = f"entries/{entry_id}/comments/{comment_id}/votes"
        res = self.connector.request(Methods.DELETE, endpoint)
        self.raise_error_if_needed(
            res,
            {
                400: "Użytkownik nie głosował wcześniej na komentarz.",
                404: "Nie odnaleziono wpisu lub komentarza.",
            },
        )

    # Media - Zdjęcia
    def post_media_photo(
        self, media_type: str, photo: bytes, photo_name: str, photo_type: str
    ) -> Photo:
        """
        Wgrywanie nowego pliku na serwer
        Dozwolone jest wgrywanie multimedialnych plików o następujących
        mimetype: 'image/jpeg', 'image/jpg', 'image/pjpeg', 'image/gif',
        'image/png', 'image/x-png'. Maksymalny rozmiar pliku to 10 MB.

        Args:
            media_type (str): Nazwa obszaru z plikami na serwerze
                [settings, comments, links, content]
            photo (bytes): Plik do wysłania
            photo_name (str): Nazwa pliku
            photo_type (str): mimetype
        """
        endpoint = "media/photos/upload"
        data = NotEmptyDict()
        data["type"] = media_type
        files = {
            "file": (photo_name, photo, photo_type),
        }
        res = self.connector.request(
            Methods.POST,
            endpoint,
            params=data,
            files=files,
        )
        self.raise_error_if_needed(
            res,
            {
                400: "Nie załączono pliku.",
                413: "Za duży plik.",
                415: "Nieobsługiwane mime type.",
                429: "Za dużo prób dodania zdjęcia w którtkim okresie czasu.",
            },
        )
        return res.data  # type: ignore

    def post_media_photo_by_url(self, media_type: str, photo_url: str) -> Photo:
        """
        Wgrywanie wskazanego pliku przez URL na serwer
        Dozwolone jest wgrywanie multimedialnych plików o następujących
        mimetype: 'image/jpeg', 'image/jpg', 'image/pjpeg', 'image/gif',
        'image/png', 'image/x-png'. Maksymalny rozmiar pliku to 10 MB.

        Args:
            media_type (str): Nazwa obszaru z plikami na serwerze
                [settings, comments, links, content]
            photo_url (str): Adres na jakim znajduję się obrazek

        """
        endpoint = "media/photos"
        params = NotEmptyDict()
        params["type"] = media_type
        data = NotEmptyDict()
        data["url"] = photo_url
        res = self.connector.request(
            Methods.POST,
            endpoint,
            params=params,
            data=data,
        )
        self.raise_error_if_needed(
            res,
            {
                400: "Nie załączono pliku.",
                409: "Wystąpił błąd podczas walidacji formularza",
                413: "Za duży plik.",
                415: "Nieobsługiwane mime type.",
                429: "Za dużo prób dodania zdjęcia w którtkim okresie czasu.",
            },
        )
        return res.data  # type: ignore

    def delete_media_photo(self, photo_key: str) -> None:
        """
        Usunięcie pliku
        Właściciel pliku posiada możliwość jego usunięcia z serwera.

        Args:
            photo_key (str): Identyfikator pliku

        """
        endpoint = f"media/photos/{photo_key}"
        res = self.connector.request(Methods.DELETE, endpoint, timeout=30)
        self.raise_error_if_needed(
            res,
            {
                400: "Brak uprawnień do usunięcia pliku.",
                404: "Plik nie został odnaleziony lub neleży "
                "do innego użytkownika.",
            },
        )
