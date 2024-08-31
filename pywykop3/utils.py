from datetime import datetime


class NotEmptyDict(dict):
    """
    Subclass of dictionary. None values are ignored.
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        for key, value in dict(*args, **kwargs).items():
            if value is not None:
                self[key] = value

    def __setitem__(self, key, value) -> None:
        if value is not None:
            super().__setitem__(key, value)


def datetime_to_string(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def string_to_datetime(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
