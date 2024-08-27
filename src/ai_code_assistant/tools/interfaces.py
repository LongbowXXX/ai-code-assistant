#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from dataclasses import dataclass
from typing import Literal


@dataclass
class ToolSettings:
    name: str


@dataclass
class DocumentSource:
    type: Literal["git"]


@dataclass
class GitDocumentSource(DocumentSource):
    repo_path: str
    clone_url: str | None
    branch: str


@dataclass
class RetrieverToolSettings(ToolSettings):
    description: str
    collection_name: str
    persist_directory: str
    embedding_model: str
    source: DocumentSource
