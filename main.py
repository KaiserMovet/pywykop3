import sys

import logger
from pywykop3 import WykopAPI

# from pprint import pprint


def main() -> None:
    # api = WykopAPI(sys.argv[1], sys.argv[2])
    # print(api.connect())

    api = WykopAPI(refresh_token=sys.argv[3])
    # print(f"{api.connector._token=}")
    api.post_entry_vote(70475373)


if __name__ == "__main__":
    logger.init()
    main()
