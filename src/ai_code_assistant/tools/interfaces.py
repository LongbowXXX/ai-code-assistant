#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from enum import Enum

from pydantic import BaseModel


class ToolType(str, Enum):
    RETRIEVER = "retriever"
    BUILTIN = "builtin"


class DocumentSourceType(str, Enum):
    GIT = "git"


class DocumentSourceSettings(BaseModel):
    type: DocumentSourceType


class GitDocumentSourceSettings(DocumentSourceSettings):
    clone_url: str
    branch: str


class ToolSettings(BaseModel):
    name: str
    type: ToolType
    enabled: bool


class RetrieverToolSettings(ToolSettings):
    description: str
    embedding_model: str
    source: DocumentSourceSettings
