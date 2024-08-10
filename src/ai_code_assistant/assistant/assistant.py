#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename
from typing import AsyncIterator

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

from ai_code_assistant.assistant.interfaces import AiConfig
from ai_code_assistant.llm.llm import AiLlms
from ai_code_assistant.tools.tools import AiTools

logger = logging.getLogger(basename(__name__))


class AiAssistant:

    @staticmethod
    def create(*, ai_config: AiConfig, ai_llms: AiLlms = AiLlms(), ai_tools: AiTools = AiTools()) -> 'AiAssistant':
        llm = ai_llms.create_llm(llm_config=ai_config.chat_llm)
        tools = ai_tools.create_tools(ai_config.tools)
        agent = create_react_agent(llm, tools)

        return AiAssistant(agent)

    def __init__(self, agent: CompiledGraph):
        self._agent = agent

    async def a_ask(self, message: HumanMessage) -> AsyncIterator[str]:
        system = SystemMessage("あなたは猫の獣人です。語尾にニャをつけてください。")
        stream_response = self._agent.astream_events(
            {"messages": [system, message]}, version="v1", stream_mode="updates"
        )

        # for step in app.stream({"messages": [("human", query)]}, stream_mode="updates"):
        #     print(step)

        async for event in stream_response:
            # logger.info(f"ask(): event={event}")
            kind = event["event"]
            if kind == "on_chain_start":
                if (
                        event["name"] == "agent"
                ):  # matches `.with_config({"run_name": "Agent"})` in agent_executor
                    yield "\n"
                    yield (
                        f"Starting agent: {event['name']} "
                        f"with input: {event['data'].get('input')}"
                    )
                    yield "\n"
            elif kind == "on_chain_end":
                if (
                        event["name"] == "agent"
                ):  # matches `.with_config({"run_name": "Agent"})` in agent_executor
                    yield "\n"
                    yield (
                        f"Done agent: {event['name']} "
                        # f"with output: {event['data'].get('output')['messages'][0]['content']}"
                    )
                    yield "\n"
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Empty content in the context of OpenAI means
                    # that the model is asking for a tool to be invoked.
                    # So we only print non-empty content
                    yield content
            elif kind == "on_tool_start":
                yield "\n"
                yield (
                    f"Starting tool: {event['name']} "
                    f"with inputs: {event['data'].get('input')}"
                )
                yield "\n"
            elif kind == "on_tool_end":
                yield "\n"
                yield (
                    f"Done tool: {event['name']} "
                    f"with output: {event['data'].get('output')}"
                )
                yield "\n"
