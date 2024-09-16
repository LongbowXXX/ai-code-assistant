#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import mesop as me

from ai_code_assistant.gui.view.widget.tool_state import ToolState

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
    state = me.state(ToolState)
    state.modal_shown = True


def hide_tool_widget() -> None:
    state = me.state(ToolState)
    state.modal_shown = False


def is_tool_widget_shown() -> bool:
    state = me.state(ToolState)
    return True if state.modal_shown else False


@me.content_component  # type: ignore[misc]
def tool_widget() -> None:
    state = me.state(ToolState)
    # Modal
    with me.box(style=_make_modal_background_style(state.modal_shown)):
        with me.box(style=_STYLE_MODAL_CONTAINER):
            with me.box(style=_STYLE_MODAL_CONTENT):
                me.textarea(
                    label="Rewrite",
                    style=_STYLE_INPUT_WIDTH,
                    value=state.rewrite,
                    on_input=on_rewrite_input,
                )
                with me.box():
                    me.button(
                        "Submit Rewrite",
                        color="primary",
                        type="flat",
                        on_click=on_click_submit_rewrite,
                    )
                    me.button(
                        "Cancel",
                        on_click=on_click_cancel_rewrite,
                    )
                with me.box(style=_STYLE_PREVIEW_CONTAINER):
                    with me.box(style=_STYLE_PREVIEW_ORIGINAL):
                        me.text("Original Message", type="headline-6")
                        me.markdown(state.preview_original)

                    with me.box(style=_STYLE_PREVIEW_REWRITE):
                        me.text("Preview Rewrite", type="headline-6")
                        me.markdown(state.preview_rewrite)


def on_rewrite_input(_: me.InputEvent) -> None:
    """Capture rewrite text input."""


def on_click_submit_rewrite(_: me.ClickEvent) -> None:
    """Submits rewrite message."""
    state = me.state(ToolState)
    state.modal_shown = False


def on_click_cancel_rewrite(_: me.ClickEvent) -> None:
    """Hides rewrite modal."""
    state = me.state(ToolState)
    state.modal_shown = False


def _make_modal_background_style(modal_open: bool) -> me.Style:
    """Makes style for modal background.

    Args:
      modal_open: Whether the modal is open.
    """
    return me.Style(
        display="block" if modal_open else "none",
        position="fixed",
        z_index=1000,
        width="100%",
        height="100%",
        overflow_x="auto",
        overflow_y="auto",
        background="rgba(0,0,0,0.4)",
    )
