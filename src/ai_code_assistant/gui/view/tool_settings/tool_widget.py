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

_STYLE_PREVIEW_CONTAINER = me.Style(
    display="grid",
    grid_template_columns="repeat(2, 1fr)",
)

_STYLE_PREVIEW_ORIGINAL = me.Style(color="#777", padding=_DEFAULT_PADDING)

_STYLE_PREVIEW_REWRITE = me.Style(background=_COLOR_CHAT_BUBBLE_EDITED, padding=_DEFAULT_PADDING)


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
            with me.box():
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
            me.input(
                label="Clone URL",
                appearance="outline",
                style=_STYLE_INPUT_WIDTH,
                value=state.clone_url,
                on_blur=on_clone_url_blur,
            )

            with me.box():
                me.button(
                    "Submit Rewrite",
                    color="primary",
                    type="flat",
                    on_click=lambda event: on_click_submit_rewrite(event, ai_assistant()),
                )
                me.button(
                    "Cancel",
                    on_click=on_click_cancel_rewrite,
                )
            with me.box(style=_STYLE_PREVIEW_CONTAINER):
                with me.box(style=_STYLE_PREVIEW_ORIGINAL):
                    me.text("Original Message", type="headline-6")

                with me.box(style=_STYLE_PREVIEW_REWRITE):
                    me.text("Preview Rewrite", type="headline-6")


def on_clone_url_blur(e: me.InputBlurEvent) -> None:
    state = me.state(ToolState)
    state.clone_url = e.value


async def on_click_submit_rewrite(_: me.ClickEvent, assistant: AiAssistantModel) -> None:
    """Submits rewrite message."""
    state: ToolState = me.state(ToolState)
    await assistant.update_assistant(
        LlmConfig(
            llm_provider=state.llm_provider,  # type: ignore[arg-type]
            llm_model=state.llm_model,
        )
    )
    hide_tool_widget()
    state = me.state(ToolState)
    state.initialized = False


def on_click_cancel_rewrite(_: me.ClickEvent) -> None:
    """Hides rewrite modal."""
    hide_tool_widget()
    state = me.state(ToolState)
    state.initialized = False


def on_provider_changed(event: me.RadioChangeEvent) -> None:
    state = me.state(ToolState)
    state.llm_provider = event.value


def on_llm_model_blur(e: me.InputBlurEvent) -> None:
    state = me.state(ToolState)
    state.llm_model = e.value
