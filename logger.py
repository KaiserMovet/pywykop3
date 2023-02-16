import logging

# from logging.handlers import RotatingFileHandler

FORMAT = "%(asctime)s - %(levelname)-8s %(filename)s/%(funcName)s : %(message)s"
DATEFMT = "%d/%m/%Y %I:%M:%S"


def get_formatter() -> logging.Formatter:
    formatter = logging.Formatter(
        FORMAT,
        datefmt=DATEFMT,
    )
    return formatter


def get_colored_formatter() -> logging.Formatter:
    """
    Stealed from https://stackoverflow.com/a/56944256/3638629
    """

    class CustomFormatter(logging.Formatter):

        grey = "\x1b[38;21m"
        blue = "\x1b[38;5;39m"
        yellow = "\x1b[38;5;226m"
        red = "\x1b[38;5;196m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"

        def __init__(self, fmt, datefmt):
            super().__init__(fmt=fmt, datefmt=datefmt)
            self.fmt = fmt
            self.FORMATS = {  # pylint: disable=invalid-name
                logging.DEBUG: self.grey + self.fmt + self.reset,
                logging.INFO: self.blue + self.fmt + self.reset,
                logging.WARNING: self.yellow + self.fmt + self.reset,
                logging.ERROR: self.red + self.fmt + self.reset,
                logging.CRITICAL: self.bold_red + self.fmt + self.reset,
            }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    return CustomFormatter(
        FORMAT,
        datefmt=DATEFMT,
    )


def init() -> logging.Logger:
    logger = logging.getLogger("root")
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # log_file = "log.txt"
    # fileHandler = RotatingFileHandler(
    #     log_file,
    #     mode="a",
    #     maxBytes=100 * 1024,
    #     backupCount=3,
    #     encoding=None,
    #     delay=False,
    # )
    # fileHandler.setLevel(logging.INFO)

    console_handler.setFormatter(get_colored_formatter())
    # fileHandler.setFormatter(get_formatter())

    logger.addHandler(console_handler)
    # logger.addHandler(fileHandler)

    return logger
