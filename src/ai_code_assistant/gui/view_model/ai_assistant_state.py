#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import asyncio
from typing import Optional, Generator, AsyncGenerator

from langchain_core.messages import SystemMessage, HumanMessage

from ai_code_assistant.assistant.assistant import AiAssistant
from ai_code_assistant.assistant.interfaces import AiConfig
from ai_code_assistant.llm.interfaces import LlmConfig
from ai_code_assistant.tools.ai_tools import AiTools
from ai_code_assistant.tools.interfaces import ToolSettings, ToolType


class AiAssistantViewModel:
    _ai_assistant: Optional[AiAssistant] = None
    _loop: Optional[asyncio.AbstractEventLoop] = None

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def setup_assistant_if_needed(self, system_prompt: str) -> None:
        if self._ai_assistant:
            self._ai_assistant.system = SystemMessage(system_prompt)
            return
        assistant = asyncio.run(self.__setup_async())
        assistant.system = SystemMessage(system_prompt)
        self._ai_assistant = assistant
        self._loop = asyncio.new_event_loop()

    @classmethod
    async def __setup_async(cls) -> AiAssistant:
        ai_tools = AiTools()
        await ai_tools.create_tool_async(ToolSettings(type=ToolType.BUILTIN, name="google-search", enabled=True))
        tools = await ai_tools.load_tools_async()

        ai_config = AiConfig(
            chat_llm=LlmConfig(llm_provider="openai", llm_model="gpt-4o-2024-08-06"),
            tools=tools,
        )
        return await AiAssistant.create_async(ai_config=ai_config)

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
