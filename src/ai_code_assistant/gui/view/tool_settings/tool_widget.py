#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename
from typing import Callable

import mesop as me

from ai_code_assistant.gui.model.ai_assistant_model import AiAssistantModel
from ai_code_assistant.gui.tool_state import ToolState
from ai_code_assistant.llm.interfaces import LlmConfig

logger = logging.getLogger(basename(__name__))

# noinspection SpellCheckingInspection
_COLOR_CHAT_BUBBLE_EDITED = "#f2ebff"
_DEFAULT_PADDING = me.Padding.all(20)


_STYLE_MODAL_CONTAINER = me.Style(
    background="#fff",
    margin=me.Margin.symmetric(vertical="0", horizontal="auto"),
    width="min(800px, 80%)",
    box_sizing="content-box",
    height="80%",
    overflow_y="scroll",
    box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
)
_STYLE_INPUT_WIDTH = me.Style(width="100%")
_STYLE_MODAL_CONTENT = me.Style(margin=me.Margin.all(20))

_CONTENT_GROUP = me.Style(
    background="#fff",
    width="100%",
    margin=me.Margin.all(5),
    border=me.Border.all(me.BorderSide(width=2, color="gray", style="solid")),
    border_radius=10,
    padding=me.Padding.all(8),
)


def show_tool_widget() -> None:
    me.navigate("/tool_settings")


def hide_tool_widget() -> None:
    me.navigate("/")


def update_state_if_needed(ai_assistant: AiAssistantModel) -> None:
    state = me.state(ToolState)
    if not state.initialized:
        state.initialized = True
        state.llm_provider = ai_assistant.llm_config.llm_provider
        state.llm_model = ai_assistant.llm_config.llm_model


def tool_settings_ui(ai_assistant: Callable[[], AiAssistantModel]) -> None:
    update_state_if_needed(ai_assistant())
    state = me.state(ToolState)
    logger.info(f"tool_settings_ui() {state}")
    # Modal
    with me.box(style=_STYLE_MODAL_CONTAINER):
        with me.box(style=_STYLE_MODAL_CONTENT):
            with me.box(style=_CONTENT_GROUP):
                me.text("Chat LLM Provider")
                me.radio(
                    on_change=on_provider_changed,
                    options=[
                        me.RadioOption(label="OpenAI", value="openai"),
                        me.RadioOption(label="Amazon Bedrock", value="amazon_bedrock"),
                        me.RadioOption(label="Ollama", value="ollama"),
                    ],
                    value=state.llm_provider,
                )
                me.input(
                    label="Chat LLM Model",
                    appearance="outline",
                    style=_STYLE_INPUT_WIDTH,
                    value=state.llm_model,
                    on_blur=on_llm_model_blur,
                )
                me.button(
                    "Apply LLM Config",
                    color="primary",
                    type="flat",
                    on_click=lambda event: on_apply_llm_config(event, ai_assistant()),
                )

            with me.box(style=_CONTENT_GROUP):
                me.input(
                    label="Git Clone URL",
                    appearance="outline",
                    style=_STYLE_INPUT_WIDTH,
                    value=state.git_clone_url,
                    on_blur=on_clone_url_blur,
                )
                me.input(
                    label="Git Branch",
                    appearance="outline",
                    style=_STYLE_INPUT_WIDTH,
                    value=state.git_branch,
                    on_blur=on_branch_blur,
                )
                me.input(
                    label="Source Name (Only letters, numbers and _ are allowed.)",
                    appearance="outline",
                    style=_STYLE_INPUT_WIDTH,
                    value=state.git_source_name,
                    on_blur=on_source_name_blur,
                )
                me.button(
                    "Add Git Source for Retriever",
                    color="primary",
                    type="flat",
                    on_click=lambda event: on_add_git_source(event, ai_assistant()),
                )

            with me.box(style=_CONTENT_GROUP):
                me.text("Builtin-tools")
                me.button(
                    "Add Google Search",
                    color="primary",
                    type="flat",
                    on_click=lambda event: on_add_google_search(event, ai_assistant()),
                )

            with me.box(style=_CONTENT_GROUP):
                me.text(f"Enabled Tools: {len(ai_assistant().tools)}")

                for tool in ai_assistant().tools:
                    with me.box():
                        me.text(f"{tool.name}: [{tool.type}]")
                        me.button(
                            f"Remove {tool.name}",
                            key=tool.name,
                            on_click=lambda event: ai_assistant().remove_tool(event.key),
                        )

            me.button(
                "Exit Setting page",
                on_click=on_exit_settings,
            )


def on_clone_url_blur(e: me.InputBlurEvent) -> None:
    state = me.state(ToolState)
    state.git_clone_url = e.value


def on_source_name_blur(e: me.InputBlurEvent) -> None:
    state = me.state(ToolState)
    state.git_source_name = e.value


def on_branch_blur(e: me.InputBlurEvent) -> None:
    state = me.state(ToolState)
    state.git_branch = e.value


async def on_add_google_search(_: me.ClickEvent, assistant: AiAssistantModel) -> None:
    await assistant.add_google_search()


async def on_add_git_source(_: me.ClickEvent, assistant: AiAssistantModel) -> None:
    state: ToolState = me.state(ToolState)
    await assistant.add_git_source(state.git_source_name, state.git_clone_url, state.git_branch)
    # state.git_source_name = ""
    # state.git_clone_url = ""
    # state.git_branch = ""


async def on_apply_llm_config(_: me.ClickEvent, assistant: AiAssistantModel) -> None:
    state: ToolState = me.state(ToolState)
    await assistant.update_assistant(
        LlmConfig(
            llm_provider=state.llm_provider,  # type: ignore[arg-type]
            llm_model=state.llm_model,
        )
    )


def on_exit_settings(_: me.ClickEvent) -> None:
    hide_tool_widget()
    state = me.state(ToolState)
    state.initialized = False


def on_provider_changed(event: me.RadioChangeEvent) -> None:
    state = me.state(ToolState)
    state.llm_provider = event.value


def on_llm_model_blur(e: me.InputBlurEvent) -> None:
    state = me.state(ToolState)
    state.llm_model = e.value
