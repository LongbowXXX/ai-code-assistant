#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import pytest

from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.tools.ai_tools import AiTools
from ai_code_assistant.tools.interfaces import RetrieverToolSettings, ToolType, GitDocumentSourceSettings


@pytest.mark.skip(reason="needs ollama server")
@pytest.mark.asyncio
async def test_create_tool_async() -> None:
    app_context = AppContext()
    ai_tools = AiTools(app_context)
    retriever_tool_settings = RetrieverToolSettings(
        name="git retriever",
        type=ToolType.RETRIEVER,
        enabled=True,
        description="source code retriever",
        embedding_model="bge-m3",
        embedding_service="ollama",
        source=GitDocumentSourceSettings(
            type="git",
            clone_url="clone_url",
            branch="branch",
        ),
    )
    await ai_tools.create_tool_async(retriever_tool_settings)
