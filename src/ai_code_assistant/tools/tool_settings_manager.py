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


class ToolSettingsManager:
    """
    Tool settings manager.
    - Manage enabling and disabling of multiple tools
    - Save tool settings to json file.
    - Read settings file and load tools
    """

    def __init__(self, app_context: AppContext) -> None:
        super().__init__()
        self._tools: dict[str, ToolSettings] = {}
        self._app_context = app_context

    async def load_tool_settings(self) -> list[ToolSettings]:
        """
        Load tool settings from the given directory path.
        Returns:
            List of tool settings.
        """
        results: list[ToolSettings] = []
        for subdir in self._app_context.tools_dir_path.glob("*/"):
            if not subdir.is_dir():
                continue
            tool = await self.__load_tool(subdir)
            results.append(tool)
            self._tools[tool.name] = tool

        return results

    async def save_tool_setting(self, tool: ToolSettings) -> None:
        """
        Save tool settings to json file.
        Args:
            tool: Tool settings.
        """
        tool_dir = self._app_context.tools_dir_path / tool.name
        tool_dir.mkdir(parents=True, exist_ok=True)
        setting_file = tool_dir / "setting.json"
        setting_file.write_text(tool.model_dump_json(indent=2), encoding="utf-8")
        self._tools[tool.name] = tool

    async def remove_tool_setting(self, tool_name: str) -> ToolSettings:
        """
        Remove tool settings.
        Args:
            tool_name: Tool name.
        Returns:
            Removed tool settings.
        """
        tool_dir = self._app_context.tools_dir_path / tool_name
        remove_dir_contents(tool_dir)
        removed_settings = self._tools.pop(tool_name)
        if isinstance(removed_settings, RetrieverToolSettings):
            # await RetrieverTool.remove_tool_async(self._app_context, removed_settings)
            pass
        return removed_settings

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
