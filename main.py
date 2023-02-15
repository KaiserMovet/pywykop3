import sys
from datetime import datetime
from pprint import pprint

import logger
from pywykop3 import WykopAPI


def main() -> None:

    # api = WykopAPI(sys.argv[1], sys.argv[2])
    # print(api.connect())

    api = WykopAPI(refresh_token=sys.argv[3])
    # print(f"{api.connector._token=}")
    pprint(
        api.get_tag_newer("heheszki", date=datetime(2023, 1, 15, 12, 12, 12))
    )


if __name__ == "__main__":
    logger.init()
    main()
