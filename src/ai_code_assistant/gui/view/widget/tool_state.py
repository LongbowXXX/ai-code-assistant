#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php

import mesop as me


@me.stateclass
class ToolState:
    modal_shown: bool = False
    rewrite: str = ""
    preview_original: str = ""
    preview_rewrite: str = ""
