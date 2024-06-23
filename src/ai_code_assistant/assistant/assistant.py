#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
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

    def ask(self, message: HumanMessage) -> AIMessage:
        system = SystemMessage("あなたは猫の獣人です。語尾にニャをつけてください。")
        stream_response = self._agent.stream(
            {"messages": [system, message]}, stream_mode="updates"
        )

        # for step in app.stream({"messages": [("human", query)]}, stream_mode="updates"):
        #     print(step)

        for step in stream_response:
            logger.info(f"ask(): step={step}")
        return AIMessage("Hello Bob!")
