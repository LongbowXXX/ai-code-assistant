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

    @staticmethod
    async def create_async(
        *,
        ai_config: AiConfig,
        ai_llms: AiLlms = AiLlms(),
    ) -> "AiAssistant":
        llm = ai_llms.create_llm(llm_config=ai_config.chat_llm)
        agent = create_react_agent(llm, ai_config.tools)

        return AiAssistant(agent)

    def __init__(self, agent: CompiledGraph):
        self._agent = agent
        self._history: list[BaseMessage] = []

    @property
    def system(self) -> Optional[SystemMessage]:
        filtered = [msg for msg in self._history if isinstance(msg, SystemMessage)]
        return filtered[-1] if filtered else None

    @system.setter
    def system(self, system: SystemMessage) -> None:
        logger.info(f"Setting system message: {system}")
        # remove old system messages
        self._history = [msg for msg in self._history if not isinstance(msg, SystemMessage)]
        # add new system message to head
        self._history.insert(0, system)

    def clear_history(self) -> None:
        logger.info("clear_history()")
        tmp_system = self.system
        self._history.clear()
        self.system = tmp_system

    async def ask_async(self, message: HumanMessage) -> AsyncIterator[str]:
        logger.info(f"ask(): message={message}")
        self._history.append(message)
        stream_response = self._agent.astream_events({"messages": self._history}, version="v1", stream_mode="updates")

        async for event in stream_response:
            # logger.info(f"ask(): event={event}")
            kind = event["event"]
            if kind == "on_chain_start":
                if event["name"] == "agent":
                    logger.info(f"Starting agent: {event['name']} with input: {event['data'].get('input')}")
            elif kind == "on_chain_end":
                if event["name"] == "agent":
                    output = event["data"].get("output")
                    if output:
                        ai_message: AIMessage = output["messages"][0]
                        if "tool_calls" in ai_message.additional_kwargs:
                            # don't save tool call messages
                            logger.info(f"Done agent tool calling: {event['name']} with output: {ai_message}")
                        else:
                            self._history.append(ai_message)
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
                logger.info(f"Starting tool: {event['name']} " f"with inputs: {event['data'].get('input')}")
            elif kind == "on_tool_end":
                output = event["data"].get("output")
                logger.info(f"Done tool: {event['name']} " f"with output: {output}")
                if isinstance(output, ToolMessage):
                    logger.info(f"Tool message: {output}")
                    # don't save tool messages
