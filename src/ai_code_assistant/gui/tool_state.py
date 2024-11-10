#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import mesop as me


@me.stateclass
class ToolState:
    initialized: bool = False
    git_clone_url: str = "https://github.com/LongbowXXX/ai-code-assistant"
    git_branch: str = "develop"
    git_source_name: str = "ai_code_assistant"
    llm_provider: str = ""
    llm_model: str = ""
