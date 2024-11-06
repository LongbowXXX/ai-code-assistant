#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from dataclasses import dataclass
from typing import Literal

LLM_PROVIDER = Literal["openai", "amazon_bedrock", "ollama"]

OPENAI_CHAT_MODEL = Literal["gpt-4o"]


@dataclass
class LlmConfig:
    llm_provider: LLM_PROVIDER
    llm_model: str
