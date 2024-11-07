#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename
from typing import Generator

import mesop as me
from dotenv import load_dotenv

from ai_code_assistant.gui.view.chat_page import chat_ui
from ai_code_assistant.gui.view.chat_state import ChatUiMessage
from ai_code_assistant.gui.view.tool_settings.tool_widget import tool_ui
from ai_code_assistant.gui.view_model.ai_assistant_state import AiAssistantViewModel
from ai_code_assistant.utils.logger import setup_logger

load_dotenv()
setup_logger()

logger = logging.getLogger(basename(__name__))
assistant_model = AiAssistantViewModel()


@me.page(
    path="/",
    title="AI Code Assistant",
    security_policy=me.SecurityPolicy(dangerously_disable_trusted_types=True),
)  # type: ignore[misc]
def main_page() -> None:
    chat_ui(
        transform,
        title="AI Code Assistant",
        bot_user="AI Assistant",
    )


@me.page(
    path="/tool_settings",
    title="Tool Settings",
    security_policy=me.SecurityPolicy(dangerously_disable_trusted_types=True),
)  # type: ignore[misc]
def tool_settings_page() -> None:
    tool_ui()


def transform(sentence: str, system_prompt: str, _: list[ChatUiMessage]) -> Generator[str, None, None]:
    assistant_model.setup_assistant_if_needed(system_prompt)
    try:
        yield from assistant_model.ask(sentence)
    except StopIteration as error:
        logger.info(f"transform(): StopIteration={error.value}")
