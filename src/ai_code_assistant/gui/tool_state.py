#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import mesop as me


@me.stateclass
class ToolState:
    initialized: bool = False
    clone_url: str = ""
    llm_provider: str = ""
    llm_model: str = ""
