#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

from ai_code_assistant.tools.interfaces import ModelServiceType


def create_embedding(embedding_model: str, model_service: ModelServiceType) -> Embeddings:
    """
    Creates an embedding instance based on the provided model and service type.

    Args:
        embedding_model: The name of the embedding model to use.
        model_service: The type of model service (e.g., OPENAI, OLLAMA).

    Returns:
        An instance of the Embeddings class.

    Raises:
        NotImplementedError: If the model service type is not supported.
    """
    if model_service == ModelServiceType.OPENAI:
        return OpenAIEmbeddings(model=embedding_model)
    elif model_service == ModelServiceType.OLLAMA:
        return OllamaEmbeddings(model=embedding_model)
    else:
        raise NotImplementedError(f"{model_service} is not supported.")
