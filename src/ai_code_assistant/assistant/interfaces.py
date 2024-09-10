#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from dataclasses import dataclass

from langchain_core.tools import BaseTool

from ai_code_assistant.llm.interfaces import LlmConfig


@dataclass
class AiConfig:
    chat_llm: LlmConfig
    tools: list[BaseTool]
