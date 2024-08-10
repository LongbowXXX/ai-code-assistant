#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import time
from typing import Generator

import mesop
from mesop import labs


@mesop.page(path="/text_to_text", title="Text I/O Example")  # type: ignore[misc]
def app() -> None:
    labs.text_to_text(
        upper_case_stream,
        title="Text I/O Example",
    )


def upper_case_stream(s: str) -> Generator[str, None, None]:
    yield s.capitalize()
    time.sleep(0.5)
    yield "Done"
