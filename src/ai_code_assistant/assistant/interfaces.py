#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php

from langchain_core.tools import BaseTool
from pydantic import BaseModel

from ai_code_assistant.llm.interfaces import LlmConfig
from ai_code_assistant.tools.interfaces import ToolSettings


class AiTool(BaseModel):
    """
    Represents an AI tool with its settings.

    Attributes:
        tool: The base tool used by the AI.
        tool_settings: The settings for the tool.
    """

    tool: BaseTool
    tool_settings: ToolSettings


class AiConfig(BaseModel):
    """
    Configuration for the AI, including language model and tools.

    Attributes:
        chat_llm: The configuration for the chat language model.
        tools: A list of AI tools with their settings.
    """

    chat_llm: LlmConfig
    tools: list[AiTool]
