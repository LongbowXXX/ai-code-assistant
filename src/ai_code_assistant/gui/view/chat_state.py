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
    role: ChatUiRole = "user"
    content: str = ""


@me.stateclass
class ChatState:
    user_input: str
    system_prompt: str = 'You are a cat beast-man. Please add "nya" to the end of your sentences.'
    system_prompt_tab: bool = False
    chat_history: list[ChatUiMessage]
    in_progress: bool = False
