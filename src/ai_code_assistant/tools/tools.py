#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import BaseTool, Tool

from ai_code_assistant.tools.interfaces import ToolSettings


class AiTools:
    def __init__(self):
        super().__init__()
        self._tools: dict[str, BaseTool] = {}

    def create_tools(self, tool_settings: list[ToolSettings]) -> list[BaseTool]:
        print(f"Creating tool tool_settings={tool_settings}, {self._tools}")
        return [self._create_tool(tool_settings) for tool_settings in tool_settings]

    @classmethod
    def _create_tool(cls, tool_settings: ToolSettings) -> BaseTool:
        search = GoogleSearchAPIWrapper()

        tool = Tool(
            name="google_search",
            description="Search Google for recent results.",
            func=search.run,
        )
        return tool
