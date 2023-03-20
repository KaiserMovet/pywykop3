import sys
from pprint import pprint

import logger
from pywykop3 import WykopAPI


def main() -> None:
    # api = WykopAPI(sys.argv[1], sys.argv[2])
    # print(api.connect())

    api = WykopAPI(refresh_token=sys.argv[3])
    # with open("1.jpg", "rb") as f:
    #     photo = f.read()

    # print(f"{api.connector._token=}")
    # res = api.post_media_photo("comments", photo, "xd.jpg", "mage/jpg")
    res = api.post_media_photo_by_url(
        "comments",
        "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg",
    )
    pprint(res)
    api.delete_media_photo(res["key"])


if __name__ == "__main__":
    logger.init()
    main()
