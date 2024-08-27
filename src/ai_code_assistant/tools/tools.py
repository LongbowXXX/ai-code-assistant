#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.tools import BaseTool

from ai_code_assistant.tools.interfaces import ToolSettings, RetrieverToolSettings
from ai_code_assistant.tools.retriever_tool import RetrieverTool

logger = logging.getLogger(basename(__name__))


class AiTools:
    def __init__(self) -> None:
        super().__init__()
        self._tools: dict[str, BaseTool] = {}

    async def create_tools_async(self, tool_settings: list[ToolSettings]) -> list[BaseTool]:
        logger.info(f"Creating tool tool_settings={tool_settings}, {self._tools}")
        return [await self._create_tool_async(tool_settings) for tool_settings in tool_settings]

    @classmethod
    async def _create_tool_async(cls, tool_settings: ToolSettings) -> BaseTool:
        if isinstance(tool_settings, RetrieverToolSettings):
            return await RetrieverTool.create_tool_async(tool_settings)

        match tool_settings.name:
            case "google-search":
                return cls._create_google_search_tool()
            case _:
                raise NotImplementedError(f"{tool_settings.name} is not supported.")

    @classmethod
    def _create_google_search_tool(cls) -> BaseTool:
        tools = load_tools(["google-search"])
        return tools[0]
