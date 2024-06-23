#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from dataclasses import dataclass

from ai_code_assistant.llm.interfaces import LlmConfig
from ai_code_assistant.tools.interfaces import ToolSettings


@dataclass
class AiConfig:
    chat_llm: LlmConfig
    tools: list[ToolSettings]
