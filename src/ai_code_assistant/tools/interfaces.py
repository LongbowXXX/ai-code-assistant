#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from enum import Enum
from typing import Union, Literal

from pydantic import BaseModel, Field


class ToolType(str, Enum):
    RETRIEVER = "retriever"
    BUILTIN = "builtin"


class GitDocumentSourceSettings(BaseModel):
    type: Literal["git"]
    clone_url: str
    branch: str


class PdfDocumentSourceSettings(BaseModel):
    type: Literal["pdf"]
    file_path: str


class ToolSettings(BaseModel):
    name: str
    type: ToolType
    enabled: bool


class RetrieverToolSettings(ToolSettings):
    description: str
    embedding_model: str
    source: Union[GitDocumentSourceSettings, PdfDocumentSourceSettings] = Field(..., discriminator="type")
