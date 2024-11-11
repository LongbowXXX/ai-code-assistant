#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename
from typing import AsyncIterator, Optional

from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage, ToolMessage
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

from ai_code_assistant.assistant.interfaces import AiConfig
from ai_code_assistant.llm.llm import AiLlms

logger = logging.getLogger(basename(__name__))


class AiAssistant:
    """
    AiAssistant is responsible for managing the interaction with the AI agent,
    including sending messages and handling responses.
    """

    @staticmethod
    async def create_async(
        *,
        ai_config: AiConfig,
        ai_llms: AiLlms = AiLlms(),
    ) -> "AiAssistant":
        """
        Asynchronously creates an instance of AiAssistant.

        Args:
            ai_config: Configuration settings for the AI assistant.
            ai_llms: Instance of AiLlms for creating language models. Defaults to AiLlms().

        Returns:
            An instance of AiAssistant.
        """
        llm = ai_llms.create_llm(llm_config=ai_config.chat_llm)
        # AiTool to BaseTool
        base_tools = [ai_tool.tool for ai_tool in ai_config.tools]
        agent = create_react_agent(llm, base_tools)

        return AiAssistant(agent, ai_config)

    def __init__(self, agent: CompiledGraph, ai_config: AiConfig) -> None:
        """
        Initializes the AiAssistant instance.

        Args:
            agent: The AI agent used for processing messages.
            ai_config: Configuration settings for the AI assistant.
        """
        self._agent = agent
        self._ai_config = ai_config
        self._history: list[BaseMessage] = []

    @property
    def ai_config(self) -> AiConfig:
        """
        Gets the AI configuration settings.

        Returns:
            The AI configuration settings.
        """
        return self._ai_config

    @property
    def system(self) -> Optional[SystemMessage]:
        """
        Gets the current system message.

        Returns:
            The current system message if it exists, otherwise None.
        """
        filtered = [msg for msg in self._history if isinstance(msg, SystemMessage)]
        return filtered[-1] if filtered else None

    @system.setter
    def system(self, system: SystemMessage) -> None:
        """
        Gets the current system message.

        Returns:
            The current system message if it exists, otherwise None.
        """
        logger.info(f"Setting system message: {system}")
        # remove old system messages
        self._history = [msg for msg in self._history if not isinstance(msg, SystemMessage)]
        # add new system message to head
        self._history.insert(0, system)

    def clear_history(self) -> None:
        """
        Clears the message history, retaining the current system message if it exists.
        """
        logger.info("clear_history()")
        tmp_system = self.system
        self._history.clear()
        if tmp_system:
            self.system = tmp_system

    async def ask_async(self, message: HumanMessage) -> AsyncIterator[str]:
        """
        Asynchronously sends a message to the AI agent and yields the response.

        Args:
            message: The message to send to the AI agent.

        Yields:
            The response from the AI agent.
        """
        logger.info(f"ask(): message={message}")
        self._history.append(message)
        logger.info(f"ask(): history={self._history}")
        stream_response = self._agent.astream_events({"messages": self._history}, version="v2", stream_mode="updates")

        async for event in stream_response:
            logger.debug(f"ask(): event kind={event['event']}, name={event['name']}")
            kind = event["event"]
            if kind == "on_chain_start":
                if event["name"] == "agent":
                    logger.debug(f"Starting agent: {event['name']} with input: {event['data'].get('input')}")
            elif kind == "on_chain_end":
                if event["name"] == "agent":
                    output = event["data"].get("output")
                    if output:
                        for out_message in output["messages"]:
                            ai_message: AIMessage = out_message
                            self._history.append(ai_message)
                            if "tool_calls" in ai_message.additional_kwargs:
                                logger.info(f"Done agent tool calling: {event['name']} with output: {ai_message}")
                            elif (
                                "message" in ai_message.response_metadata
                                and "tool_calls" in ai_message.response_metadata["message"]
                            ):
                                logger.info(f"Done agent tool calling: {event['name']} with output: {ai_message}")
                            else:
                                logger.info(f"Done agent: {event['name']} with output: {ai_message}")
                    else:
                        logger.warning("Agent did not return any output")

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Empty content in the context of OpenAI means
                    # that the model is asking for a tool to be invoked.
                    # So we only print non-empty content
                    yield content
            elif kind == "on_tool_start":
                logger.debug(f"Starting tool: {event['name']} " f"with inputs: {event['data'].get('input')}")
            elif kind == "on_tool_end":
                output = event["data"].get("output")
                logger.info(f"Done tool: {event['name']} " f"with output: {output}")
                if isinstance(output, ToolMessage):
                    logger.info(f"Tool message: {output}")
                    self._history.append(output)
