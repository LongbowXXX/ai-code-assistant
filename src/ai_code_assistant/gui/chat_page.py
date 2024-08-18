#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import time
from dataclasses import dataclass
from typing import Callable, Generator, Literal

import mesop as me
from mesop.component_helpers.style import ItemAlignmentValues

ChatUiRole = Literal["user", "assistant"]

_BOT_USER_DEFAULT = "mesop-bot"

_COLOR_BACKGROUND = me.theme_var("background")
_COLOR_CHAT_BUBBLE_YOU = me.theme_var("surface-container-low")
_COLOR_CHAT_BUBBLE_BOT = me.theme_var("secondary-container")

_DEFAULT_PADDING = me.Padding.all(20)
_DEFAULT_BORDER_SIDE = me.BorderSide(width="1px", style="solid", color=me.theme_var("secondary-fixed"))

_LABEL_BUTTON = "send"
_LABEL_BUTTON_IN_PROGRESS = "pending"
_LABEL_INPUT = "Enter your prompt"

_STYLE_APP_CONTAINER = me.Style(
    background=_COLOR_BACKGROUND,
    display="grid",
    height="100vh",
    grid_template_columns="repeat(1, 1fr)",
)
_STYLE_TITLE = me.Style(padding=me.Padding(left=10))
_STYLE_CHAT_BOX = me.Style(
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
_STYLE_CHAT_INPUT = me.Style(width="100%")
_STYLE_CHAT_INPUT_BOX = me.Style(padding=me.Padding(top=30), display="flex", flex_direction="row")
_STYLE_CHAT_BUTTON = me.Style(margin=me.Margin(top=8, left=8))
_STYLE_CHAT_BUBBLE_NAME = me.Style(
    font_weight="bold",
    font_size="13px",
    padding=me.Padding(left=15, right=15, bottom=5),
)
_STYLE_CHAT_BUBBLE_PLAINTEXT = me.Style(margin=me.Margin.symmetric(vertical=15))


def _make_style_chat_ui_container(has_title: bool) -> me.Style:  # type: ignore[no-any-unimported]
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


def _make_style_chat_bubble_wrapper(role: ChatUiRole) -> me.Style:  # type: ignore[no-any-unimported]
    align_items: ItemAlignmentValues = "end" if role == "user" else "start"  # type: ignore[no-any-unimported]
    return me.Style(
        display="flex",
        flex_direction="column",
        align_items=align_items,
    )


def _make_chat_bubble_style(role: ChatUiRole) -> me.Style:  # type: ignore[no-any-unimported]
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


@dataclass(kw_only=True)
class ChatUiMessage:
    role: ChatUiRole = "user"
    content: str = ""


@me.stateclass
class ChatState:
    input: str
    output: list[ChatUiMessage]
    in_progress: bool = False


def on_blur(e: me.InputBlurEvent) -> None:  # type: ignore[no-any-unimported]
    chat_state = me.state(ChatState)
    chat_state.input = e.value


def chat_ui(
    transform: Callable[[str, list[ChatUiMessage]], Generator[str, None, None] | str],
    *,
    title: str | None = None,
    bot_user: str = _BOT_USER_DEFAULT,
) -> None:
    """
    Renders the chat UI component.

    Args:
        transform: A function that processes the user input and returns the assistant's response.
        title: The title of the chat UI. Defaults to None.
        bot_user: The name of the bot user. Defaults to _BOT_USER_DEFAULT.
    """
    state = me.state(ChatState)

    def submit() -> Generator[None, None, None]:
        chat_state = me.state(ChatState)
        if chat_state.in_progress or not chat_state.input:
            return
        chat_input = chat_state.input
        chat_state.input = ""
        yield

        output = chat_state.output
        if output is None:
            output = []
        output.append(ChatUiMessage(role="user", content=chat_input))
        chat_state.in_progress = True
        yield

        me.scroll_into_view(key="scroll-to")
        time.sleep(0.15)
        yield

        start_time = time.time()
        output_message = transform(chat_input, chat_state.output)
        assistant_message = ChatUiMessage(role="assistant")
        output.append(assistant_message)
        chat_state.output = output

        for content in output_message:
            assistant_message.content += content
            if (time.time() - start_time) >= 0.25:
                start_time = time.time()
                yield
        chat_state.in_progress = False
        me.focus_component(key=f"input-{len(chat_state.output)}")
        yield

    def on_click_submit(_: me.ClickEvent) -> Generator[None, None, None]:  # type: ignore[no-any-unimported]
        yield from submit()

    def toggle_theme(_: me.ClickEvent) -> None:  # type: ignore[no-any-unimported]
        if me.theme_brightness() == "light":
            me.set_theme_mode("dark")
        else:
            me.set_theme_mode("light")

    with me.box(style=_STYLE_APP_CONTAINER):
        with me.content_button(
            type="icon",
            style=me.Style(position="absolute", right=4, top=8),
            on_click=toggle_theme,
        ):
            me.icon("light_mode" if me.theme_brightness() == "dark" else "dark_mode")
        with me.box(style=_make_style_chat_ui_container(bool(title))):
            if title:
                me.text(title, type="headline-5", style=_STYLE_TITLE)
            with me.box(style=_STYLE_CHAT_BOX):
                for msg in state.output:
                    with me.box(style=_make_style_chat_bubble_wrapper(msg.role)):
                        if msg.role == "assistant":
                            me.markdown(bot_user, style=_STYLE_CHAT_BUBBLE_NAME)
                        with me.box(style=_make_chat_bubble_style(msg.role)):
                            if msg.role == "user":
                                me.markdown(msg.content, style=_STYLE_CHAT_BUBBLE_PLAINTEXT)
                            else:
                                me.markdown(msg.content)

                if state.in_progress:
                    with me.box(key="scroll-to", style=me.Style(height=300)):
                        pass

            with me.box(style=_STYLE_CHAT_INPUT_BOX):
                with me.box(style=me.Style(flex_grow=1)):
                    me.textarea(
                        label=_LABEL_INPUT,
                        # Workaround: update key to clear input.
                        key=f"input-{len(state.output)}",
                        on_blur=on_blur,
                        style=_STYLE_CHAT_INPUT,
                    )
                with me.content_button(
                    color="primary",
                    type="flat",
                    disabled=state.in_progress,
                    on_click=on_click_submit,
                    style=_STYLE_CHAT_BUTTON,
                ):
                    me.icon(_LABEL_BUTTON_IN_PROGRESS if state.in_progress else _LABEL_BUTTON)
