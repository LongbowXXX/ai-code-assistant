#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename
from typing import cast

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.tools import BaseTool

from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.tools.interfaces import ToolSettings, RetrieverToolSettings
from ai_code_assistant.tools.retriever_tool import RetrieverTool

logger = logging.getLogger(basename(__name__))


class AiTools:
    def __init__(self) -> None:
        super().__init__()
        self._tools: dict[str, BaseTool] = {}

    async def load_tools_async(self, tool_settings: list[ToolSettings], app_context: AppContext) -> list[BaseTool]:
        logger.info(f"Load tool tool_settings={tool_settings}, {self._tools}")
        return [await self._load_tool_async(tool_settings, app_context) for tool_settings in tool_settings]

    @classmethod
    async def _load_tool_async(cls, tool_settings: ToolSettings, app_context: AppContext) -> BaseTool:
        match tool_settings.type:
            case "retriever":
                return await RetrieverTool.load_tool_async(cast(RetrieverToolSettings, tool_settings), app_context)
            case "builtin":
                return await cls._load_builtin_tool_async(tool_settings)
            case _:
                raise NotImplementedError(f"Tool type {tool_settings.type} is not supported.")

    @classmethod
    async def _load_builtin_tool_async(cls, tool_settings: ToolSettings) -> BaseTool:
        return load_tools([tool_settings.name])[0]
