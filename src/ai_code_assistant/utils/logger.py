#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
import sys
import types
from os.path import basename
from typing import Type


def setup_logger() -> None:
    file_handler = logging.FileHandler("app.log", encoding='utf-8')
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), file_handler],
    )
    sys.excepthook = _handle_unhandled_exception


def _handle_unhandled_exception(
    exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: types.TracebackType | None
) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        # Call the default excepthook saved at __excepthook__
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger = logging.getLogger(basename(__name__))
    logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))
