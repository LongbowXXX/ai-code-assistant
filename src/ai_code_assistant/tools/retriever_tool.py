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

from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.tools.interfaces import RetrieverToolSettings, GitDocumentSourceSettings

logger = logging.getLogger(basename(__name__))


class RetrieverTool:
    @classmethod
    async def create_tool_async(cls, tool_setting: RetrieverToolSettings, app_context: AppContext) -> BaseTool:
        logger.info(f"Creating tool tool_setting={tool_setting}")
        source = tool_setting.source
        tool: BaseTool
        match source:
            case GitDocumentSourceSettings():
                # noinspection PyTypeChecker
                tool = await cls.__create_git_tool_async(tool_setting, source, app_context)
            case _:
                raise NotImplementedError(f"{source} is not supported.")
        return tool

    @classmethod
    async def load_tool_async(cls, tool_setting: RetrieverToolSettings, app_context: AppContext) -> BaseTool:
        logger.info(f"Load tool tool_setting={tool_setting}")
        source = tool_setting.source
        tool: BaseTool
        match source:
            case GitDocumentSourceSettings():
                # noinspection PyTypeChecker
                tool = await cls.__load_git_tool_async(tool_setting, app_context)
            case _:
                raise NotImplementedError(f"{source} is not supported.")
        return tool

    @classmethod
    async def __load_git_tool_async(cls, tool_settings: RetrieverToolSettings, app_context: AppContext) -> BaseTool:
        persistent_directory = app_context.db_dir / tool_settings.name
        vector_store: VectorStore = Chroma(
            collection_name=tool_settings.name,
            persist_directory=str(persistent_directory),
            embedding_function=OpenAIEmbeddings(model=tool_settings.embedding_model),
        )
        retriever = vector_store.as_retriever()
        tool = create_retriever_tool(
            retriever,
            tool_settings.name,
            tool_settings.description,
        )
        return tool

    @classmethod
    async def __create_git_tool_async(
        cls,
        tool_settings: RetrieverToolSettings,
        source: GitDocumentSourceSettings,
        app_context: AppContext,
    ) -> BaseTool:
        repo_path = app_context.repository_dir / tool_settings.name
        loader = GitLoader(
            clone_url=source.clone_url,
            repo_path=str(repo_path),
            branch=source.branch,
        )
        documents = await loader.aload()
        persistent_directory = app_context.db_dir / tool_settings.name
        vector_store: VectorStore = await Chroma.afrom_documents(
            documents=documents,
            embedding=OpenAIEmbeddings(model=tool_settings.embedding_model),
            collection_name=tool_settings.name,
            persist_directory=persistent_directory,
        )

        retriever = vector_store.as_retriever()
        tool = create_retriever_tool(
            retriever,
            tool_settings.name,
            tool_settings.description,
        )
        return tool
