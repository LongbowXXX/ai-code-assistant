#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from enum import Enum
from typing import Union, Literal

from pydantic import BaseModel, Field, ConfigDict


class ToolType(str, Enum):
    RETRIEVER = "retriever"
    BUILTIN = "builtin"


class GitDocumentSourceSettings(BaseModel):
    type: Literal["git"] = "git"
    clone_url: str
    branch: str


class PdfDocumentSourceSettings(BaseModel):
    type: Literal["pdf"] = "pdf"
    file_path: str


class ToolSettings(BaseModel):
    name: str
    type: ToolType
    enabled: bool


class ModelServiceType(str, Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"


class RetrieverToolSettings(ToolSettings):
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
