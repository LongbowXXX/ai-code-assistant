#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import asyncio
import logging
import os
import tempfile
from os.path import basename
from typing import Generator, AsyncGenerator

from langchain_core.messages import SystemMessage, HumanMessage

from ai_code_assistant.assistant.assistant import AiAssistant
from ai_code_assistant.assistant.interfaces import AiConfig
from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.llm.interfaces import LlmConfig
from ai_code_assistant.tools.ai_tools import AiTools
from ai_code_assistant.tools.interfaces import ToolSettings, RetrieverToolSettings, ToolType

logger = logging.getLogger(basename(__name__))


class AiAssistantModel:
    """
    AiAssistantModel is responsible for managing the AI assistant, tools, and LLM configuration.
    """

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
        """
        Initializes the AiAssistantModel.

        Args:
            ai_assistant: The AI assistant instance.
            ai_tools: The AI tools instance.
            llm_config: The LLM configuration.
            loop: The event loop.
            app_context: The application context.
        """
        super().__init__()
        self._ai_assistant = ai_assistant
        self._ai_tools = ai_tools
        self._llm_config = llm_config
        self._loop = loop
        self._app_context = app_context

    @classmethod
    async def create(cls, app_context: AppContext) -> "AiAssistantModel":
        """
        Creates an instance of AiAssistantModel.

        Args:
            app_context: The application context.

        Returns:
            The created AiAssistantModel instance.
        """
        llm_config = LlmConfig.load_from_file(app_context.data_dir)
        ai_tools = AiTools(app_context)
        assistant = await cls.__create_ai_assistant(ai_tools, llm_config)
        loop = asyncio.new_event_loop()
        return AiAssistantModel(assistant, ai_tools, llm_config, loop, app_context)

    @classmethod
    async def __create_ai_assistant(cls, ai_tools: AiTools, llm_config: LlmConfig) -> AiAssistant:
        logger.info("__create_ai_assistant() start")

        tools = await ai_tools.load_tools_async()

        for tool in tools:
            logger.info(f"__create_ai_assistant(): Loaded tool {tool.tool_settings.name}")

        ai_config = AiConfig(
            chat_llm=llm_config,
            tools=tools,
        )
        return await AiAssistant.create_async(ai_config=ai_config)

    @property
    def tools(self) -> list[ToolSettings]:
        """
        Gets the list of tool settings.

        Returns:
            The list of tool settings.
        """
        return [ai_tool.tool_settings for ai_tool in self._ai_assistant.ai_config.tools]

    @property
    def llm_config(self) -> LlmConfig:
        """
        Gets the LLM configuration.

        Returns:
            The LLM configuration.
        """
        return self._llm_config

    async def remove_tool(self, tool_name: str) -> ToolSettings:
        """
        Removes a tool by name.

        Args:
            tool_name: The name of the tool to remove.

        Returns:
            The settings of the removed tool.
        """
        removed = await self._ai_tools.remove_tool_setting(tool_name)
        await self.update_assistant(self._llm_config)
        return removed

    async def add_google_search(self) -> None:
        """
        Adds the Google Search tool.
        """
        await self._ai_tools.create_tool_async(ToolSettings(type=ToolType.BUILTIN, name="google-search", enabled=True))
        await self.update_assistant(self._llm_config)

    async def add_pdf_source(self, source_name: str, content: bytes) -> None:
        """
        Adds a PDF source tool.

        Args:
            source_name: The name of the PDF source.
            content: The content of the PDF file.
        """
        file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        file.write(content)
        file.close()
        file_path = file.name
        logger.info(f"add_pdf_source() : {source_name} : {file_path}")
        await self._ai_tools.create_tool_async(
            RetrieverToolSettings.of_pdf_source(source_name=source_name, file_path=file_path)
        )
        await self.update_assistant(self._llm_config)
        os.unlink(file_path)

    async def add_git_source(self, source_name: str, clone_url: str, branch: str) -> None:
        """
        Adds a Git source tool.

        Args:
            source_name: The name of the Git source.
            clone_url: The URL to clone the repository from.
            branch: The branch to clone.
        """
        await self._ai_tools.create_tool_async(
            RetrieverToolSettings.of_git_source(
                source_name=source_name,
                clone_url=clone_url,
                branch=branch,
            )
        )
        await self.update_assistant(self._llm_config)

    async def update_assistant(self, llm_config: LlmConfig) -> None:
        """
        Updates the AI assistant with a new LLM configuration.

        Args:
            llm_config: The new LLM configuration.
        """
        logger.info(f"update_assistant() : {llm_config}")
        self._llm_config = llm_config
        llm_config.save_to_file(self._app_context.data_dir)
        self._ai_assistant = await self.__create_ai_assistant(self._ai_tools, llm_config)

    @property
    def system(self) -> str:
        """
        Gets the system message.

        Returns:
            str: The system message content.
        """
        system_message = self._ai_assistant.system
        return str(system_message.content) if system_message else ""

    @system.setter
    def system(self, system_prompt: str) -> None:
        """
        Sets the system message.

        Args:
            system_prompt: The new system message content.
        """
        new_message = SystemMessage(system_prompt)
        logger.info(f"Setting system message: {new_message}")
        self._ai_assistant.system = new_message

    def clear_history(self) -> None:
        """
        Clears the message history.
        """
        self._ai_assistant.clear_history()

    def ask(self, sentence: str) -> Generator[str, None, None]:
        """
        Asks a question to the AI assistant.

        Args:
            sentence: The question to ask.

        Returns:
            The response from the AI assistant.
        """
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
