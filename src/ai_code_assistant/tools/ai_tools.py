#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename
from typing import cast

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.tools import BaseTool

from ai_code_assistant.assistant.interfaces import AiTool
from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.tools.interfaces import (
    ToolSettings,
    RetrieverToolSettings,
)
from ai_code_assistant.tools.retriever_tool import RetrieverTool
from ai_code_assistant.tools.tool_settings_manager import ToolSettingsManager

logger = logging.getLogger(basename(__name__))


class AiTools:
    """
    Manages the creation, loading, and removal of AI tools.
    """

    def __init__(
        self,
        app_context: AppContext = AppContext(),
    ) -> None:
        """
        Initializes the AiTools class with the given application context.

        Args:
            app_context: The application context. Defaults to a new instance of AppContext.
        """
        super().__init__()
        self._app_context = app_context
        self._setting_manager = ToolSettingsManager(AppContext())

    async def create_tool_async(self, tool_settings: ToolSettings) -> BaseTool:
        """
        Asynchronously creates a tool based on the provided settings.

        Args:
            tool_settings: The settings for the tool to be created.

        Returns:
            The created tool.

        Raises:
            NotImplementedError: If the tool type is not supported.
        """
        logger.info(f"create_tool_async() tool_settings={tool_settings}")
        match tool_settings.type:
            case "retriever":
                tool = await RetrieverTool.create_tool_async(
                    cast(RetrieverToolSettings, tool_settings), self._app_context
                )
            case "builtin":
                tool = await self._load_builtin_tool_async(tool_settings)
            case _:
                raise NotImplementedError(f"Tool type {tool_settings.type} is not supported.")
        await self._setting_manager.save_tool_setting(tool_settings)
        return tool

    async def load_tools_async(self) -> list[AiTool]:
        """
        Asynchronously loads all tools based on the saved settings.

        Returns:
            A list of loaded tools.
        """
        logger.info("load_tools_async()")
        tool_settings = await self._setting_manager.load_tool_settings()
        return [await self._load_tool_async(self._app_context, tool_settings) for tool_settings in tool_settings]

    async def remove_tool_setting(self, tool_name: str) -> ToolSettings:
        """
        Asynchronously removes the settings for a tool with the given name.

        Args:
            tool_name: The name of the tool to remove.

        Returns:
            The settings of the removed tool.
        """
        logger.info(f"remove_tool_setting() tool_name={tool_name}")
        removed = await self._setting_manager.remove_tool_setting(tool_name)
        return removed

    @classmethod
    async def _load_tool_async(cls, app_context: AppContext, tool_settings: ToolSettings) -> AiTool:
        match tool_settings.type:
            case "retriever":
                base_tool = await RetrieverTool.load_tool_async(cast(RetrieverToolSettings, tool_settings), app_context)
                return AiTool(tool=base_tool, tool_settings=tool_settings)
            case "builtin":
                base_tool = await cls._load_builtin_tool_async(tool_settings)
                return AiTool(tool=base_tool, tool_settings=tool_settings)
            case _:
                raise NotImplementedError(f"Tool type {tool_settings.type} is not supported.")

    @classmethod
    async def _load_builtin_tool_async(cls, tool_settings: ToolSettings) -> BaseTool:
        return load_tools([tool_settings.name])[0]
