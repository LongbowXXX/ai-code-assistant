#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import asyncio
import logging
from os.path import basename
from typing import Generator, AsyncGenerator

from langchain_core.messages import SystemMessage, HumanMessage

from ai_code_assistant.assistant.assistant import AiAssistant
from ai_code_assistant.assistant.interfaces import AiConfig
from ai_code_assistant.llm.interfaces import LlmConfig
from ai_code_assistant.tools.ai_tools import AiTools

logger = logging.getLogger(basename(__name__))


class AiAssistantModel:
    _ai_assistant: AiAssistant
    _loop: asyncio.AbstractEventLoop

    def __init__(
        self,
        ai_assistant: AiAssistant,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        super().__init__()
        self._ai_assistant = ai_assistant
        self._loop = loop

    @classmethod
    async def create(cls) -> "AiAssistantModel":
        assistant = await cls.__setup_async()
        loop = asyncio.new_event_loop()
        return AiAssistantModel(assistant, loop)

    @classmethod
    async def __setup_async(cls) -> AiAssistant:
        logger.info("__setup_async() start")
        ai_tools = AiTools()
        # await ai_tools.create_tool_async(ToolSettings(type=ToolType.BUILTIN, name="google-search", enabled=True))
        # await ai_tools.create_tool_async(
        #     RetrieverToolSettings.of_git_source(
        #         source_name="ai_code_assistant",
        #         clone_url="https://github.com/LongbowXXX/ai-code-assistant",
        #         branch="develop",
        #     )
        # )
        tools = await ai_tools.load_tools_async()

        ai_config = AiConfig(
            # chat_llm=LlmConfig(llm_provider="openai", llm_model="gpt-4o-2024-08-06"),
            chat_llm=LlmConfig(llm_provider="ollama", llm_model="llama3.1"),
            tools=tools,
        )
        return await AiAssistant.create_async(ai_config=ai_config)

    @property
    def system(self) -> str:
        system_message = self._ai_assistant.system
        return str(system_message.content) if system_message else ""

    @system.setter
    def system(self, system_prompt: str) -> None:
        new_message = SystemMessage(system_prompt)
        logger.info(f"Setting system message: {new_message}")
        self._ai_assistant.system = new_message

    def clear_history(self) -> None:
        self._ai_assistant.clear_history()

    def ask(self, sentence: str) -> Generator[str, None, None]:
        new_message = HumanMessage(sentence)
        ask_gen = self.__sync_ask(new_message)
        try:
            yield from ask_gen
        except StopIteration:
            # nothing to do
            pass

    def __sync_ask(self, message: HumanMessage) -> Generator[str, None, str]:
        gen = self.__ask_async(message)
        all_str = ""
        while True:
            try:
                assert self._loop
                str_value: str = self._loop.run_until_complete(gen.__anext__())
                yield str_value
                all_str += str_value
            except StopAsyncIteration:
                break
        return all_str

    async def __ask_async(self, message: HumanMessage) -> AsyncGenerator[str, None]:
        assert self._ai_assistant
        a_result = self._ai_assistant.ask_async(message)
        async for result in a_result:
            yield result
