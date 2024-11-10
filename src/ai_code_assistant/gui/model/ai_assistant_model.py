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
from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.llm.interfaces import LlmConfig
from ai_code_assistant.tools.ai_tools import AiTools
from ai_code_assistant.tools.interfaces import ToolSettings

logger = logging.getLogger(basename(__name__))


class AiAssistantModel:
    _ai_assistant: AiAssistant
    _ai_tools: AiTools
    _llm_config: LlmConfig
    _loop: asyncio.AbstractEventLoop
    _app_context: AppContext

    def __init__(
        self,
        ai_assistant: AiAssistant,
        ai_tools: AiTools,
        llm_config: LlmConfig,
        loop: asyncio.AbstractEventLoop,
        app_context: AppContext,
    ) -> None:
        super().__init__()
        self._ai_assistant = ai_assistant
        self._ai_tools = ai_tools
        self._llm_config = llm_config
        self._loop = loop
        self._app_context = app_context

    @classmethod
    async def create(cls, app_context: AppContext) -> "AiAssistantModel":
        llm_config = LlmConfig.load_from_file(app_context.data_dir)
        ai_tools = AiTools(app_context)
        assistant = await cls.__create_ai_assistant(ai_tools, llm_config)
        loop = asyncio.new_event_loop()
        return AiAssistantModel(assistant, ai_tools, llm_config, loop, app_context)

    @classmethod
    async def __create_ai_assistant(cls, ai_tools: AiTools, llm_config: LlmConfig) -> AiAssistant:
        logger.info("__create_ai_assistant() start")
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
            chat_llm=llm_config,
            tools=tools,
        )
        return await AiAssistant.create_async(ai_config=ai_config)

    @property
    def tools(self) -> list[ToolSettings]:
        return [ai_tool.tool_settings for ai_tool in self._ai_assistant.ai_config.tools]

    @property
    def llm_config(self) -> LlmConfig:
        return self._llm_config

    async def remove_tool(self, tool_name: str) -> ToolSettings:
        removed = await self._ai_tools.remove_tool_setting(tool_name)
        await self.update_assistant(self._llm_config)
        return removed

    async def update_assistant(self, llm_config: LlmConfig) -> None:
        self._llm_config = llm_config
        llm_config.save_to_file(self._app_context.data_dir)
        self._ai_assistant = await self.__create_ai_assistant(self._ai_tools, llm_config)

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
