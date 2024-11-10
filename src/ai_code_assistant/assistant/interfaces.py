#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php

from langchain_core.tools import BaseTool
from pydantic import BaseModel

from ai_code_assistant.llm.interfaces import LlmConfig
from ai_code_assistant.tools.interfaces import ToolSettings


class AiTool(BaseModel):
    tool: BaseTool
    tool_settings: ToolSettings


class AiConfig(BaseModel):
    chat_llm: LlmConfig
    tools: list[AiTool]
