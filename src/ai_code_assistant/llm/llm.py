#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from langchain_aws import ChatBedrock
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from ai_code_assistant.llm.interfaces import LlmConfig


class AiLlms:
    def create_llm(self, llm_config: LlmConfig) -> BaseChatModel:
        model: BaseChatModel
        match llm_config.llm_provider:
            case "openai":
                model = ChatOpenAI(model=llm_config.llm_model)
            case "amazon_bedrock":
                model = ChatBedrock(model=llm_config.llm_model)
            case "ollama":
                model = ChatOllama(model=llm_config.llm_model)
            case _:
                raise NotImplementedError(f"{llm_config.llm_provider} is not supported.")
        return model
