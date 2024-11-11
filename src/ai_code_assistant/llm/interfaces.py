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
    """
    Configuration class for the Language Model (LLM).

    Attributes:
        llm_provider: The provider of the language model. Default is 'ollama'.
        llm_model: The specific model of the language model. Default is 'llama3.1'.
    """

    llm_provider: LLM_PROVIDER = "ollama"
    llm_model: str = "llama3.1"
    # llm_provider: LLM_PROVIDER = "openai"
    # llm_model: str = "gpt-4o-2024-08-06"

    @staticmethod
    def load_from_file(dir_path: Path) -> "LlmConfig":
        """
        Loads the LLM configuration from a JSON file.

        Args:
            dir_path: The directory path where the configuration file is located.

        Returns:
            The loaded LLM configuration.
        """
        file = dir_path / "llm_config.json"
        if file.exists():
            return LlmConfig.model_validate_json(file.read_text(encoding="utf-8"))
        return LlmConfig()

    def save_to_file(self, dir_path: Path) -> None:
        """
        Saves the LLM configuration to a JSON file.

        Args:
            dir_path: The directory path where the configuration file will be saved.
        """
        file = dir_path / "llm_config.json"
        file.write_text(self.model_dump_json(), encoding="utf-8")
