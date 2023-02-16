from pywykop3.utils import NotEmptyDict


def test_not_empty_dict() -> None:
    base = {"1": "1", "2": 2, "3": 3, "4": None, "5": None, "6": 6}
    not_empty = NotEmptyDict()
    for key, value in base.items():
        not_empty[key] = value
    assert not_empty == {"1": "1", "2": 2, "3": 3, "6": 6}
