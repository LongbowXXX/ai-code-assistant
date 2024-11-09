#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

LLM_PROVIDER = Literal["openai", "amazon_bedrock", "ollama"]

OPENAI_CHAT_MODEL = Literal["gpt-4o"]


class LlmConfig(BaseModel):
    llm_provider: LLM_PROVIDER = "ollama"
    llm_model: str = "llama3.1"
    # llm_provider: LLM_PROVIDER = "openai"
    # llm_model: str = "gpt-4o-2024-08-06"

    @staticmethod
    def load_from_file(dir_path: Path) -> "LlmConfig":
        file = dir_path / "llm_config.json"
        if file.exists():
            return LlmConfig.model_validate_json(file.read_text(encoding="utf-8"))
        return LlmConfig()

    def save_to_file(self, dir_path: Path) -> None:
        file = dir_path / "llm_config.json"
        file.write_text(self.model_dump_json(), encoding="utf-8")
