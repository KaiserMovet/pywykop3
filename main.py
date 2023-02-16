import sys

import logger
from pywykop3 import WykopAPI


def main() -> None:

    # api = WykopAPI(sys.argv[1], sys.argv[2])
    # print(api.connect())

    api = WykopAPI(refresh_token=sys.argv[3])
    print(f"{api.connector._token=}")
    print(api.get_entry_comment_votes(70432439, 249723413))


if __name__ == "__main__":
    logger.init()
    main()
