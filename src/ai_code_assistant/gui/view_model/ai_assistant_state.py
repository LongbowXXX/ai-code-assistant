#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import asyncio
from dataclasses import dataclass, field
from typing import Optional, Generator, AsyncGenerator, Literal

import mesop as me
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

from ai_code_assistant.assistant.assistant import AiAssistant
from ai_code_assistant.assistant.interfaces import AiConfig
from ai_code_assistant.llm.interfaces import LlmConfig
from ai_code_assistant.tools.interfaces import ToolSettings

ChatRole = Literal["user", "assistant"]


@dataclass(kw_only=True)
class ChatMessage:
    """Chat message metadata."""

    role: ChatRole = "user"
    content: str = ""


@me.stateclass
class AiAssistantState:
    input: str
    history: list[ChatMessage] = field(default_factory=list)
    in_progress: bool = False


class AiAssistantViewModel:
    _ai_assistant: Optional[AiAssistant] = None
    _loop: Optional[asyncio.AbstractEventLoop] = None
    _ai_assistant_state: Optional[AiAssistantState] = None

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def setup_assistant_if_needed(self, ai_assistant_state: AiAssistantState) -> None:
        self._ai_assistant_state = ai_assistant_state
        if self._ai_assistant:
            return

        ai_config = AiConfig(
            chat_llm=LlmConfig(llm_provider="openai", llm_model="gpt-4o"),
            tools=[ToolSettings(name="google_search")],
        )
        assistant = AiAssistant.create(ai_config=ai_config)
        assistant.system = SystemMessage('You are a cat beast-man. Please add "nya" to the end of your sentences.')
        self._ai_assistant = assistant
        self._loop = asyncio.new_event_loop()

    def ask(self) -> Generator[str, None, None]:
        assert self._ai_assistant_state
        self._ai_assistant_state.in_progress = True
        new_message = HumanMessage(self._ai_assistant_state.input)
        self._ai_assistant_state.history.append(self.__langchain_message_to_chat_message(new_message))
        ask_gen = self.__sync_ask(new_message)
        try:
            yield from ask_gen
        except StopIteration as error:
            self._ai_assistant_state.history.append(ChatMessage(role="assistant", content=str(error.value)))
        self._ai_assistant_state.in_progress = False
        self._ai_assistant_state.input = ""

    def __sync_ask(self, message: HumanMessage) -> Generator[str, None, str]:
        gen = self.__a_ask(message)
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

    async def __a_ask(self, message: HumanMessage) -> AsyncGenerator[str, None]:
        assert self._ai_assistant
        a_result = self._ai_assistant.a_ask(message)
        async for result in a_result:
            yield result

    @staticmethod
    def __langchain_message_to_chat_message(message: BaseMessage) -> ChatMessage:
        match message:
            case SystemMessage():
                return ChatMessage(role="assistant", content=str(message.content))
            case HumanMessage():
                return ChatMessage(role="user", content=str(message.content))
            case _:
                raise ValueError(f"Unexpected message type: {type(message)}")
