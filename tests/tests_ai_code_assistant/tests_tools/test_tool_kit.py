#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import json
from pathlib import Path

import pytest

from pytest import TempPathFactory
from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.tools.interfaces import RetrieverToolSettings, GitDocumentSourceSettings, ToolType
from ai_code_assistant.tools.tool_kit import ToolKit


@pytest.fixture(scope="session")
def app_context(tmp_path_factory: TempPathFactory) -> AppContext:
    tool_dir_path = tmp_path_factory.mktemp("tools")
    data_dir = tmp_path_factory.mktemp("data")
    db_dir = tmp_path_factory.mktemp("db")
    repository_dir = tmp_path_factory.mktemp("repository")

    return AppContext(
        data_dir=Path(str(data_dir)),
        db_dir=Path(str(db_dir)),
        repository_dir=Path(str(repository_dir)),
        tools_dir_path=Path(str(tool_dir_path)),
    )


@pytest.mark.asyncio
async def test_save_tool_setting(app_context: AppContext) -> None:
    toolkit = ToolKit()
    await toolkit.save_tool_setting(
        app_context,
        RetrieverToolSettings(
            name="tool1",
            type=ToolType.RETRIEVER,
            enabled=True,
            description="description",
            embedding_model="model",
            source=GitDocumentSourceSettings(
                type="git",
                clone_url="clone_url",
                branch="branch",
            ),
        ),
    )
    app_context.tools_dir_path.joinpath("tool1").joinpath("setting.json").exists()

    # check setting.json
    setting_json = app_context.tools_dir_path.joinpath("tool1").joinpath("setting.json").read_text()
    print(setting_json)
    setting = json.loads(setting_json)
    assert setting["name"] == "tool1"
    assert setting["type"] == "retriever"
    assert setting["enabled"] is True
    assert setting["description"] == "description"
    assert setting["embedding_model"] == "model"
    assert setting["source"]["type"] == "git"
    assert setting["source"]["clone_url"] == "clone_url"
    assert setting["source"]["branch"] == "branch"
