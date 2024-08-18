#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename
from typing import Generator

import mesop as me
from dotenv import load_dotenv

from ai_code_assistant.gui.chat_page import chat_ui, ChatUiMessage
from ai_code_assistant.gui.view_model.ai_assistant_state import AiAssistantViewModel
from ai_code_assistant.utils.logger import setup_logger

load_dotenv()
setup_logger()

logger = logging.getLogger(basename(__name__))
assistant_model = AiAssistantViewModel()


@me.page(path="/ai_code_assistant", title="AI Code Assistant")  # type: ignore[misc]
def app() -> None:
    chat_ui(
        transform,
        title="AI Code Assistant",
        bot_user="AI Assistant",
    )


def transform(sentence: str, _: list[ChatUiMessage]) -> Generator[str, None, None]:
    assistant_model.setup_assistant_if_needed()
    try:
        yield from assistant_model.ask(sentence)
    except StopIteration as error:
        logger.info(f"transform(): StopIteration={error.value}")
