#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename

from langchain_community.document_loaders import GitLoader
from langchain_community.vectorstores import Chroma
from langchain_core.tools import BaseTool, create_retriever_tool
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings

from ai_code_assistant.tools.interfaces import RetrieverToolSettings, GitDocumentSource

logger = logging.getLogger(basename(__name__))


class RetrieverTool:
    @classmethod
    async def create_tool_async(cls, tool_setting: RetrieverToolSettings) -> BaseTool:
        logger.info(f"Creating tool tool_setting={tool_setting}")
        source = tool_setting.source
        tool: BaseTool
        match source:
            case GitDocumentSource():
                # noinspection PyTypeChecker
                tool = await cls.create_git_tool_async(tool_setting, source)
            case _:
                raise NotImplementedError(f"{source} is not supported.")
        return tool

    @classmethod
    async def create_git_tool_async(cls, tool_settings: RetrieverToolSettings, source: GitDocumentSource) -> BaseTool:
        loader = GitLoader(
            clone_url=source.clone_url,
            repo_path=source.repo_path,
            branch=source.branch,
        )
        documents = await loader.aload()
        vector_store: VectorStore = await Chroma.afrom_documents(
            documents=documents,
            embedding=OpenAIEmbeddings(model=tool_settings.embedding_model),
            collection_name=tool_settings.collection_name,
            persist_directory=tool_settings.persist_directory,
        )

        retriever = vector_store.as_retriever()
        tool = create_retriever_tool(
            retriever,
            tool_settings.name,
            tool_settings.description,
        )
        return tool
