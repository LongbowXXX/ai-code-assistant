#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php

import mesop as me


@me.stateclass
class ToolState:
    """
    Represents the state of the tool settings.

    Attributes:
        initialized: Indicates if the tool has been initialized.
        git_clone_url: The URL of the Git repository to clone.
        git_branch: The branch of the Git repository to use.
        git_source_name: The name of the source for the Git repository.
        pdf_source_name: The name of the source for PDF files.
        llm_provider: The provider of the large language model (LLM).
        llm_model: The specific model of the LLM to use.
    """

    initialized: bool = False
    git_clone_url: str = "https://github.com/LongbowXXX/ai-code-assistant"
    git_branch: str = "develop"
    git_source_name: str = "ai_code_assistant"
    pdf_source_name: str = ""
    llm_provider: str = ""
    llm_model: str = ""
