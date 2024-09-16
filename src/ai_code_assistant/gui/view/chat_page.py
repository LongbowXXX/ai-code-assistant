#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import time
from typing import Callable, Generator, Any

import mesop as me
from mesop import ClickEvent
from mesop.component_helpers.style import ItemAlignmentValues

from ai_code_assistant.gui.view.chat_state import ChatUiRole, ChatState, ChatUiMessage
from ai_code_assistant.gui.view.page_header import page_header
from ai_code_assistant.gui.view.widget.tool_widget import tool_widget, is_tool_widget_open

_COLOR_BACKGROUND = me.theme_var("background")
_COLOR_CHAT_BUBBLE_YOU = me.theme_var("surface-container-low")
_COLOR_CHAT_BUBBLE_BOT = me.theme_var("secondary-container")

_DEFAULT_PADDING = me.Padding.all(20)
_DEFAULT_BORDER_SIDE = me.BorderSide(width="1px", style="solid", color=me.theme_var("secondary-fixed"))
_DEFAULT_BORDER = me.Border.all(me.BorderSide(color="#e0e0e0", width=1, style="solid"))
_LABEL_BUTTON = "send"
_LABEL_BUTTON_IN_PROGRESS = "pending"
_LABEL_USER_INPUT = "Enter your prompt"
_LABEL_SYSTEM_PROMPT = "Enter your system prompt"

_STYLE_APP_CONTAINER = me.Style(
    background=_COLOR_BACKGROUND,
    display="grid",
    height="100vh",
    grid_template_columns="repeat(1, 1fr)",
)
_STYLE_TITLE = me.Style(padding=me.Padding(left=10))
_STYLE_CHAT_HISTORY_BOX = me.Style(
    height="100%",
    overflow_y="scroll",
    padding=_DEFAULT_PADDING,
    margin=me.Margin(bottom=20),
    border_radius="10px",
    border=me.Border(
        left=_DEFAULT_BORDER_SIDE,
        right=_DEFAULT_BORDER_SIDE,
        top=_DEFAULT_BORDER_SIDE,
        bottom=_DEFAULT_BORDER_SIDE,
    ),
)
_STYLE_CHAT_USER_INPUT = me.Style(width="100%")
_STYLE_CHAT_SYSTEM_PROMPT = me.Style(width="100%")
_STYLE_CHAT_USER_INPUT_BOX = me.Style(padding=me.Padding(top=30), display="flex", flex_direction="row")
_STYLE_CHAT_SYSTEM_PROMPT_BOX = me.Style(padding=me.Padding(top=30), display="flex", flex_direction="row")
_STYLE_CHAT_SEND_BUTTON = me.Style(margin=me.Margin(top=8, left=8))
_STYLE_CHAT_BUBBLE_NAME = me.Style(
    font_weight="bold",
    font_size="13px",
    padding=me.Padding(left=15, right=15, bottom=5),
)
_STYLE_CHAT_BUBBLE_PLAINTEXT = me.Style(margin=me.Margin.symmetric(vertical=15))


def _make_style_chat_ui_container(has_title: bool) -> me.Style:
    return me.Style(
        display="grid",
        grid_template_columns="repeat(1, 1fr)",
        grid_template_rows="1fr 14fr 1fr" if has_title else "5fr 1fr",
        margin=me.Margin.symmetric(vertical=0, horizontal="auto"),
        width="min(1024px, 100%)",
        height="100vh",
        background=_COLOR_BACKGROUND,
        box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
        padding=me.Padding(top=20, left=20, right=20),
    )


def _make_style_chat_bubble_wrapper(role: ChatUiRole) -> me.Style:
    align_items: ItemAlignmentValues = "end" if role == "user" else "start"
    return me.Style(
        display="flex",
        flex_direction="column",
        align_items=align_items,
    )


def _make_chat_bubble_style(role: ChatUiRole) -> me.Style:
    background = _COLOR_CHAT_BUBBLE_YOU if role == "user" else _COLOR_CHAT_BUBBLE_BOT
    return me.Style(
        width="80%",
        font_size="16px",
        line_height="1.5",
        background=background,
        border_radius="15px",
        padding=me.Padding(right=15, left=15, bottom=3),
        margin=me.Margin(bottom=10),
        border=me.Border(
            left=_DEFAULT_BORDER_SIDE,
            right=_DEFAULT_BORDER_SIDE,
            top=_DEFAULT_BORDER_SIDE,
            bottom=_DEFAULT_BORDER_SIDE,
        ),
    )


def on_user_input_blur(e: me.InputBlurEvent) -> None:
    chat_state = me.state(ChatState)
    chat_state.user_input = e.value


def on_system_prompt_blur(e: me.InputBlurEvent) -> None:
    chat_state = me.state(ChatState)
    chat_state.system_prompt = e.value


def chat_ui(
    transform: Callable[[str, str, list[ChatUiMessage]], Generator[str, None, None] | str],
    *,
    title: str,
    bot_user: str,
) -> None:
    """
    Renders the chat UI component.

    Args:
        transform: A function that processes the user input and returns the assistant's response.
        title: The title of the chat UI.
        bot_user: The name of the bot user.
    """

    def submit() -> Generator[None, None, None]:
        chat_state = me.state(ChatState)
        if chat_state.in_progress or not chat_state.user_input:
            return
        chat_input = chat_state.user_input
        chat_system_prompt = chat_state.system_prompt
        chat_state.user_input = ""
        yield

        output = chat_state.chat_history
        if output is None:
            output = []
        output.append(ChatUiMessage(role="user", content=chat_input))
        chat_state.in_progress = True
        yield

        me.scroll_into_view(key="scroll-to")
        time.sleep(0.15)
        yield

        start_time = time.time()
        output_message = transform(chat_input, chat_system_prompt, chat_state.chat_history)
        assistant_message = ChatUiMessage(role="assistant")
        output.append(assistant_message)
        chat_state.chat_history = output

        for content in output_message:
            assistant_message.content += content
            if (time.time() - start_time) >= 0.25:
                start_time = time.time()
                yield
        chat_state.in_progress = False
        me.focus_component(key=f"input-{len(chat_state.chat_history)}")
        yield

    def on_click_submit(_: me.ClickEvent) -> Generator[None, None, None]:
        yield from submit()

    def toggle_theme(_: me.ClickEvent) -> None:
        if me.theme_brightness() == "light":
            me.set_theme_mode("dark")
        else:
            me.set_theme_mode("light")

    __chat_screen(title=title, bot_user=bot_user, on_click_theme=toggle_theme, on_click_submit=on_click_submit)


def __chat_screen(
    *,
    title: str,
    bot_user: str,
    on_click_theme: Callable[[ClickEvent], Any],
    on_click_submit: Callable[[ClickEvent], Any],
) -> None:
    chat_state = me.state(ChatState)
    with me.box(style=_STYLE_APP_CONTAINER):
        with me.content_button(
            type="icon",
            style=me.Style(position="absolute", right=4, top=8),
            on_click=on_click_theme,
        ):
            me.icon("light_mode" if me.theme_brightness() == "dark" else "dark_mode")

        if is_tool_widget_open():
            with tool_widget():
                me.slot()

        with me.box(style=_make_style_chat_ui_container(bool(title))):

            with page_header(title):
                me.slot()

            with me.box(style=_STYLE_CHAT_HISTORY_BOX):
                for msg in chat_state.chat_history:
                    with me.box(style=_make_style_chat_bubble_wrapper(msg.role)):
                        if msg.role == "assistant":
                            me.markdown(bot_user, style=_STYLE_CHAT_BUBBLE_NAME)
                        with me.box(style=_make_chat_bubble_style(msg.role)):
                            if msg.role == "user":
                                me.markdown(msg.content, style=_STYLE_CHAT_BUBBLE_PLAINTEXT)
                            else:
                                me.markdown(msg.content)

                if chat_state.in_progress:
                    with me.box(key="scroll-to", style=me.Style(height=300)):
                        pass
            with tab_box(header="System Prompt", key="system_prompt_tab"):
                with me.box(style=_STYLE_CHAT_SYSTEM_PROMPT_BOX):
                    with me.box(style=me.Style(flex_grow=1)):
                        me.textarea(
                            label=_LABEL_SYSTEM_PROMPT,
                            on_blur=on_system_prompt_blur,
                            style=_STYLE_CHAT_SYSTEM_PROMPT,
                            rows=3,
                            value=chat_state.system_prompt,
                        )
            with me.box(style=_STYLE_CHAT_USER_INPUT_BOX):
                with me.box(style=me.Style(flex_grow=1)):
                    me.textarea(
                        label=_LABEL_USER_INPUT,
                        # Workaround: update key to clear input.
                        key=f"input-{len(chat_state.chat_history)}",
                        on_blur=on_user_input_blur,
                        style=_STYLE_CHAT_USER_INPUT,
                    )
                with me.content_button(
                    color="primary",
                    type="flat",
                    disabled=chat_state.in_progress,
                    on_click=on_click_submit,
                    style=_STYLE_CHAT_SEND_BUTTON,
                ):
                    me.icon(_LABEL_BUTTON_IN_PROGRESS if chat_state.in_progress else _LABEL_BUTTON)


@me.content_component  # type: ignore[misc]
def tab_box(*, header: str, key: str) -> None:
    """Collapsible tab box"""
    state = me.state(ChatState)
    tab_open = getattr(state, key)
    with me.box(style=me.Style(width="100%", margin=me.Margin(bottom=20))):
        # Tab Header
        with me.box(
            key=key,
            on_click=on_click_tab_header,
            style=me.Style(padding=_DEFAULT_PADDING, border=_DEFAULT_BORDER),
        ):
            with me.box(style=me.Style(display="flex")):
                me.icon(icon="keyboard_arrow_down" if tab_open else "keyboard_arrow_right")
                me.text(
                    header,
                    style=me.Style(line_height="24px", margin=me.Margin(left=5), font_weight="bold"),
                )
        # Tab Content
        with me.box(
            style=me.Style(
                padding=_DEFAULT_PADDING,
                border=_DEFAULT_BORDER,
                display="block" if tab_open else "none",
            )
        ):
            me.slot()


def on_click_tab_header(e: me.ClickEvent) -> None:
    """Open and closes tab content."""
    state = me.state(ChatState)
    setattr(state, e.key, not getattr(state, e.key))
