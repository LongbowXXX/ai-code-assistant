#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import asyncio

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from ai_code_assistant.assistant.assistant import AiAssistant
from ai_code_assistant.assistant.interfaces import AiConfig
from ai_code_assistant.llm.interfaces import LlmConfig
from ai_code_assistant.tools.interfaces import ToolSettings
from ai_code_assistant.utils.logger import setup_logger


async def main() -> None:
    load_dotenv()
    setup_logger()
    ai_config = AiConfig(
        chat_llm=LlmConfig(llm_provider="openai", llm_model="gpt-4o"),
        tools=[ToolSettings(name="google_search")],
    )
    assistant = AiAssistant.create(ai_config=ai_config)
    ask_result = assistant.a_ask(HumanMessage("オバマ大統領のフルネームと経歴教えて。"))
    async for result in ask_result:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
