#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from dataclasses import dataclass
from typing import Literal

import mesop as me

ChatUiRole = Literal["user", "assistant"]


@dataclass(kw_only=True)
class ChatUiMessage:
    """
    Represents a message in the chat UI.

    Attributes:
        role: The role of the message sender, either 'user' or 'assistant'.
        content: The content of the message.
    """

    role: ChatUiRole = "user"
    content: str = ""


@me.stateclass
class ChatState:
    """
    Represents the state of the chat UI.

    Attributes:
        user_input: The current input from the user.
        system_prompt: The system prompt displayed to the user.
        system_prompt_tab: Indicates if the system prompt tab is active.
        chat_history: The history of chat messages.
        in_progress: Indicates if a chat operation is in progress.
    """

    user_input: str
    system_prompt: str = "You are a coding assistant.\nExamine the source code and answer user questions."
    system_prompt_tab: bool = False
    chat_history: list[ChatUiMessage]
    in_progress: bool = False
