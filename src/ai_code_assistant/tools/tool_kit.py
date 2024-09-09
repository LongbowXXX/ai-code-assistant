#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import json
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.common.path import remove_dir_contents
from ai_code_assistant.tools.interfaces import ToolSettings, RetrieverToolSettings
from ai_code_assistant.tools.retriever_tool import RetrieverTool


class ToolKit:
    """
    ToolKit class.
    - Manage enabling and disabling of multiple tools
    - Save tool settings to json file.
    - Read settings file and load tools
    """

    def __init__(self) -> None:
        super().__init__()
        self._tools: dict[str, ToolSettings] = {}

    async def load_tool_settings(self, app_context: AppContext) -> list[ToolSettings]:
        """
        Load tool settings from the given directory path.
        Args:
            app_context: Application context.
        Returns:
            List of tool settings.
        """
        results: list[ToolSettings] = []
        for subdir in app_context.tools_dir_path.glob("*/"):
            if not subdir.is_dir():
                continue
            tool = await self.__load_tool(subdir)
            results.append(tool)
            self._tools[tool.name] = tool

        return results

    async def save_tool_setting(self, app_context: AppContext, tool: ToolSettings) -> None:
        """
        Save tool settings to json file.
        Args:
            app_context: Application context.
            tool: Tool settings.
        """
        tool_dir = app_context.tools_dir_path / tool.name
        tool_dir.mkdir(parents=True, exist_ok=True)
        setting_file = tool_dir / "setting.json"
        setting_file.write_text(tool.model_dump_json(indent=2), encoding="utf-8")
        self._tools[tool.name] = tool

    async def remove_tool_setting(self, app_context: AppContext, tool_name: str) -> None:
        """
        Remove tool settings.
        Args:
            app_context: Application context.
            tool_name: Tool name.
        """
        tool_dir = app_context.tools_dir_path / tool_name
        remove_dir_contents(tool_dir)
        removed_settings = self._tools.pop(tool_name)
        await self.__remove_tool(app_context, removed_settings)

    @classmethod
    async def __remove_tool(cls, app_context: AppContext, settings: ToolSettings) -> None:
        if isinstance(settings, RetrieverToolSettings):
            await RetrieverTool.remove_tool_async(app_context, settings)

    @classmethod
    async def __load_tool(cls, tool_dir_path: Path) -> ToolSettings:
        setting_file = tool_dir_path / "setting.json"
        json_str = setting_file.read_text(encoding="utf-8")
        settings_dict: dict[str, Any] = json.loads(json_str)

        settings = TypeAdapter(ToolSettings).validate_python(settings_dict)
        match settings.type:
            case "retriever":
                retriever_settings = TypeAdapter(RetrieverToolSettings).validate_python(settings_dict)
                return retriever_settings
            case "builtin":
                return settings
            case _:
                raise NotImplementedError(f"Tool type {settings.type} is not supported.")
