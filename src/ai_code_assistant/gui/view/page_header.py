#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from dataclasses import fields

import mesop as me

from ai_code_assistant.gui.view.widget.tool_widget import show_tool_widget


@me.content_component  # type: ignore[misc]
def page_header(title: str) -> None:
    with me.box(style=me.Style(margin=me.Margin(bottom=15))):
        # Two section basic header.
        with header():
            with header_section():
                me.text(title, type="headline-6", style=me.Style(margin=me.Margin(bottom=0)))

            with header_section():
                me.button("Tool", on_click=lambda _: show_tool_widget())


@me.content_component  # type: ignore[misc]
def header(
    *,
    style: me.Style | None = None,
) -> None:
    """Creates a simple header component.

    Args:
      style: Override the default styles, such as background color, etc.
    """
    is_mobile = me.viewport_size().width < 640
    default_flex_style = _DEFAULT_MOBILE_FLEX_STYLE if is_mobile else _DEFAULT_FLEX_STYLE

    # The style override is a bit hacky here since we apply the override styles to both
    # boxes here which could cause problems depending on what styles are added.
    with me.box(style=merge_styles(_DEFAULT_STYLE, style)):
        with me.box(style=merge_styles(default_flex_style, style)):
            me.slot()


@me.content_component  # type: ignore[misc]
def header_section() -> None:
    """Adds a section to the header."""
    with me.box(style=me.Style(display="flex", gap=5)):
        me.slot()


def merge_styles(default: me.Style, overrides: me.Style | None = None) -> me.Style:
    """Merges two styles together.

    Args:
      default: The starting style
      overrides: Any set styles will override styles in default
    """
    if not overrides:
        overrides = me.Style()

    default_fields = {field.name: getattr(default, field.name) for field in fields(me.Style)}
    override_fields = {
        field.name: getattr(overrides, field.name)
        for field in fields(me.Style)
        if getattr(overrides, field.name) is not None
    }

    return me.Style(**default_fields | override_fields)


_DEFAULT_STYLE = me.Style(
    background=me.theme_var("surface-container"),
    border=me.Border.symmetric(
        vertical=me.BorderSide(
            width=1,
            style="solid",
            color=me.theme_var("outline-variant"),
        )
    ),
    padding=me.Padding.all(10),
)

_DEFAULT_FLEX_STYLE = me.Style(
    align_items="center",
    display="flex",
    gap=5,
    justify_content="space-between",
)

_DEFAULT_MOBILE_FLEX_STYLE = me.Style(
    align_items="center",
    display="flex",
    flex_direction="column",
    gap=12,
    justify_content="center",
)
