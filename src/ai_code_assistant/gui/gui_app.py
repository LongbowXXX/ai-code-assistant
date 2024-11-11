#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import asyncio
import logging
from os.path import basename
from typing import Generator

import mesop as me
from dotenv import load_dotenv

from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.gui.chat_state import ChatUiMessage
from ai_code_assistant.gui.model.ai_assistant_model import AiAssistantModel
from ai_code_assistant.gui.view.chat_page import chat_ui
from ai_code_assistant.gui.view.tool_settings.tool_widget import tool_settings_ui
from ai_code_assistant.utils.logger import setup_logger

load_dotenv()
setup_logger()

logger = logging.getLogger(basename(__name__))

app_context: AppContext = AppContext()
ai_assistant_model = asyncio.run(AiAssistantModel.create(app_context))


def ai_assistant() -> AiAssistantModel:
    return ai_assistant_model


@me.page(
    path="/",
    title="AI Code Assistant",
    security_policy=me.SecurityPolicy(dangerously_disable_trusted_types=True),
)  # type: ignore[misc]
def main_page() -> None:
    """
    Renders the main page of the AI Code Assistant application.

    This page includes the chat UI for interacting with the AI Assistant.
    """
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
    """
    Renders the tool settings page of the AI Code Assistant application.

    This page includes the UI for configuring tool settings.
    """
    tool_settings_ui(ai_assistant)


def transform(sentence: str, system_prompt: str, history: list[ChatUiMessage]) -> Generator[str, None, None]:
    """
    Transforms the user input into a response from the AI Assistant.

    Args:
        sentence: The user input sentence.
        system_prompt: The system prompt to guide the AI Assistant.
        history: The history of chat messages.

    Yields:
        The response from the AI Assistant.
    """
    if not history:
        ai_assistant_model.clear_history()
    ai_assistant_model.system = system_prompt
    try:
        yield from ai_assistant_model.ask(sentence)
    except StopIteration as error:
        logger.info(f"transform(): StopIteration={error.value}")
