#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from enum import Enum
from typing import Union, Literal

from pydantic import BaseModel, Field, ConfigDict


class ToolType(str, Enum):
    """
    Enum representing the type of tool.

    Attributes:
        RETRIEVER: Represents a retriever tool.
        BUILTIN: Represents a built-in tool.
    """

    RETRIEVER = "retriever"
    BUILTIN = "builtin"


class GitDocumentSourceSettings(BaseModel):
    """
    Settings for a Git document source.

    Attributes:
        type: The type of the document source, always "git".
        clone_url: The URL to clone the Git repository from.
        branch: The branch of the Git repository to use.
    """

    type: Literal["git"] = "git"
    clone_url: str
    branch: str


class PdfDocumentSourceSettings(BaseModel):
    """
    Settings for a PDF document source.

    Attributes:
        type: The type of the document source, always "pdf".
        file_path: The file path to the PDF document.
    """

    type: Literal["pdf"] = "pdf"
    file_path: str


class ToolSettings(BaseModel):
    """
    Base settings for a tool.

    Attributes:
        name: The name of the tool.
        type: The type of the tool.
        enabled: Whether the tool is enabled.
    """

    name: str
    type: ToolType
    enabled: bool


class ModelServiceType(str, Enum):
    """
    Enum representing the type of model service.

    Attributes:
        OPENAI: Represents the OpenAI model service.
        OLLAMA: Represents the Ollama model service.
    """

    OPENAI = "openai"
    OLLAMA = "ollama"


class RetrieverToolSettings(ToolSettings):
    """
    Settings for a retriever tool.

    Attributes:
        description: A description of the retriever tool.
        embedding_model: The name of the embedding model to use.
        model_service: The type of model service.
        source: The document source settings.
        model_config: Configuration for the model.
    """

    description: str
    embedding_model: str
    model_service: ModelServiceType
    source: Union[GitDocumentSourceSettings, PdfDocumentSourceSettings] = Field(..., discriminator="type")

    model_config = ConfigDict(protected_namespaces=())

    @classmethod
    def of_pdf_source(
        cls,
        *,
        source_name: str,
        file_path: str,
        embed_model: str = "bge-m3",
        model_service: ModelServiceType = ModelServiceType.OLLAMA,
    ) -> "RetrieverToolSettings":
        """
        Creates a RetrieverToolSettings instance for a PDF document source.

        Args:
            source_name: The name of the source.
            file_path: The file path to the PDF document.
            embed_model: The name of the embedding model to use. Defaults to "bge-m3".
            model_service: The type of model service. Defaults to ModelServiceType.OLLAMA.

        Returns:
            The created RetrieverToolSettings instance.
        """
        return RetrieverToolSettings(
            name=source_name,
            type=ToolType.RETRIEVER,
            enabled=True,
            description=f"{source_name} PDF retriever",
            embedding_model=embed_model,
            model_service=model_service,
            source=PdfDocumentSourceSettings(
                type="pdf",
                file_path=file_path,
            ),
        )

    @classmethod
    def of_git_source(
        cls,
        *,
        source_name: str,
        clone_url: str,
        branch: str,
        embed_model: str = "bge-m3",
        model_service: ModelServiceType = ModelServiceType.OLLAMA,
    ) -> "RetrieverToolSettings":
        """
        Creates a RetrieverToolSettings instance for a Git document source.

        Args:
            source_name: The name of the source.
            clone_url: The URL to clone the Git repository from.
            branch: The branch of the Git repository to use.
            embed_model: The name of the embedding model to use. Defaults to "bge-m3".
            model_service: The type of model service. Defaults to ModelServiceType.OLLAMA.

        Returns:
            The created RetrieverToolSettings instance.
        """
        return RetrieverToolSettings(
            name=source_name,
            type=ToolType.RETRIEVER,
            enabled=True,
            description=f"{source_name} source code retriever",
            embedding_model=embed_model,
            model_service=model_service,
            source=GitDocumentSourceSettings(
                type="git",
                clone_url=clone_url,
                branch=branch,
            ),
        )
