#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename
from typing import Generator

import mesop as me
import mesop.labs as mel
from dotenv import load_dotenv

from ai_code_assistant.gui.view_model.ai_assistant_state import AiAssistantState, AiAssistantViewModel
from ai_code_assistant.utils.logger import setup_logger

logger = logging.getLogger(basename(__name__))
assistant_model = AiAssistantViewModel()


@me.page(path="/text_to_text", title="Text I/O Example")  # type: ignore[misc]
def app() -> None:
    load_dotenv()
    setup_logger()
    mel.text_to_text(
        upper_case_stream,
        title="Text I/O Example",
    )


def upper_case_stream(s: str) -> Generator[str, None, None]:
    assistant_state = me.state(AiAssistantState)
    assistant_state.input = s
    assistant_model.setup_assistant_if_needed(assistant_state)

    yield from assistant_model.ask()
