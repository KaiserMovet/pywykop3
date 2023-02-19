import inspect
from unittest import mock

import pytest

from pywykop3 import Methods, WykopAPI


class DummyWykopConnector:
    def __init__(self) -> None:
        ...

    request: mock.Mock = mock.MagicMock()

    def request_with_pagination(self, *args, **kwargs) -> mock.Mock:
        return self.request(*args, **kwargs)


class TestMethods:
    @staticmethod
    def get_client() -> WykopAPI:
        connector = DummyWykopConnector()
        api = WykopAPI(connector=connector)  # type: ignore
        api.raise_error_if_needed = mock.Mock()  # type: ignore
        return api  # type: ignore

    def execute_function(self, method) -> None:
        args_count = len(inspect.signature(method).parameters.keys())
        args = [mock.Mock()] * args_count
        method(*args)

    def check_method(self, method_name: str, expected_method: Methods) -> None:
        client: WykopAPI = self.get_client()
        function = getattr(client, method_name)
        self.execute_function(function)
        call_args = client.connector.request.call_args  # type: ignore
        used_method = (
            call_args.args[0]
            if call_args.args
            else call_args.kwargs.get("method")
        )
        assert (
            used_method == expected_method
        ), f"Method {method_name} used {used_method} instead of {expected_method}"

    @pytest.mark.parametrize(
        "method_name,expected_method",
        [
            ("get_users_autocomplete", Methods.GET),
            ("get_tags_popular", Methods.GET),
            ("get_tags_popular_user_tags", Methods.GET),
            ("get_tags_related", Methods.GET),
            ("get_tag", Methods.GET),
            ("put_tag", Methods.PUT),
            ("get_tag_stream", Methods.GET),
            ("get_tag_newer", Methods.GET),
            ("get_tag_users", Methods.GET),
            ("post_tag_user", Methods.POST),
            ("delete_tag_user", Methods.DELETE),
        ],
    )
    def test_tags_methods(
        self, method_name: str, expected_method: Methods
    ) -> None:
        self.check_method(
            method_name=method_name, expected_method=expected_method
        )

    @pytest.mark.parametrize(
        "method_name,expected_method",
        [
            ("get_entries", Methods.GET),
            ("post_entry", Methods.POST),
            ("get_entry_by_id", Methods.GET),
            ("put_entry", Methods.PUT),
            ("delete_entry_by_id", Methods.DELETE),
            ("get_entry_votes", Methods.GET),
            ("post_entry_vote", Methods.POST),
            ("delete_entry_vote", Methods.DELETE),
            ("get_entries_newer", Methods.GET),
        ],
    )
    def test_mikroblog_methods(
        self, method_name: str, expected_method: Methods
    ) -> None:
        self.check_method(
            method_name=method_name, expected_method=expected_method
        )

    @pytest.mark.parametrize(
        "method_name,expected_method",
        [
            ("get_entry_comments", Methods.GET),
            ("post_entry_comment", Methods.POST),
            ("get_entry_comment", Methods.GET),
            ("put_entry_comment", Methods.PUT),
            ("delete_entry_comment", Methods.DELETE),
            ("get_entry_comment_votes", Methods.GET),
            ("post_entry_comment_vote", Methods.POST),
            ("delete_entry_comment_vote", Methods.DELETE),
        ],
    )
    def test_mikroblog_comments_methods(
        self, method_name: str, expected_method: Methods
    ) -> None:
        self.check_method(
            method_name=method_name, expected_method=expected_method
        )
