#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import asyncio

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

from ai_code_assistant.assistant.assistant import AiAssistant
from ai_code_assistant.assistant.interfaces import AiConfig
from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.llm.interfaces import LlmConfig
from ai_code_assistant.tools.ai_tools import AiTools
from ai_code_assistant.tools.interfaces import ToolSettings, ToolType
from ai_code_assistant.utils.logger import setup_logger


async def main() -> None:
    load_dotenv()
    setup_logger()

    app_context: AppContext = AppContext()
    ai_tools = AiTools(app_context)
    await ai_tools.create_tool_async(ToolSettings(type=ToolType.BUILTIN, name="google-search", enabled=True))
    tools = await ai_tools.load_tools_async()
    ai_config = AiConfig(
        chat_llm=LlmConfig.load_from_file(app_context.data_dir),
        tools=tools,
    )
    assistant = await AiAssistant.create_async(ai_config=ai_config)
    assistant.system = SystemMessage('You are a cat beast-man. Please add "nya" to the end of your sentences.')
    ask_result = assistant.ask_async(
        HumanMessage("What is President Obama's full name and background? Tell me the latest information.")
    )
    async for result in ask_result:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
