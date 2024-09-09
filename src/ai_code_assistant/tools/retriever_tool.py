#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import logging
from os.path import basename

from langchain_community.document_loaders import GitLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.tools import BaseTool, create_retriever_tool
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ai_code_assistant.common.app_context import AppContext
from ai_code_assistant.common.path import remove_dir_contents
from ai_code_assistant.tools.interfaces import (
    RetrieverToolSettings,
    GitDocumentSourceSettings,
    PdfDocumentSourceSettings,
)

logger = logging.getLogger(basename(__name__))


class RetrieverTool:
    @classmethod
    async def create_tool_async(cls, tool_setting: RetrieverToolSettings, app_context: AppContext) -> BaseTool:
        logger.info(f"creating tool tool_setting={tool_setting}")
        source = tool_setting.source
        documents: list[Document]
        match source:
            case GitDocumentSourceSettings():
                # noinspection PyTypeChecker
                documents = await cls.__load_git_documents_async(tool_setting, source, app_context)
            case PdfDocumentSourceSettings():
                documents = await cls.__load_pdf_documents_async(source)
            case _:
                raise NotImplementedError(f"{source} is not supported.")
        return await cls.__create_tool_async(app_context, documents, tool_setting)

    @classmethod
    async def load_tool_async(cls, tool_settings: RetrieverToolSettings, app_context: AppContext) -> BaseTool:
        logger.info(f"Load tool tool_settings={tool_settings}")
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
    async def remove_tool_async(cls, app_context: AppContext, tool_settings: RetrieverToolSettings) -> None:
        logger.info(f"Remove tool tool_settings={tool_settings}")
        persistent_directory = app_context.db_dir / tool_settings.name
        remove_dir_contents(persistent_directory)
        repository_path = app_context.repository_dir / tool_settings.name
        remove_dir_contents(repository_path)

    @classmethod
    async def __load_git_documents_async(
        cls,
        tool_settings: RetrieverToolSettings,
        source: GitDocumentSourceSettings,
        app_context: AppContext,
    ) -> list[Document]:
        repo_path = app_context.repository_dir / tool_settings.name
        loader = GitLoader(
            clone_url=source.clone_url,
            repo_path=str(repo_path),
            branch=source.branch,
        )
        return await loader.aload()

    @classmethod
    async def __load_pdf_documents_async(
        cls,
        source: PdfDocumentSourceSettings,
    ) -> list[Document]:
        loader = PyPDFLoader(source.file_path)
        documents = await loader.aload()
        return RecursiveCharacterTextSplitter().split_documents(documents)

    @classmethod
    async def __create_tool_async(
        cls,
        app_context: AppContext,
        documents: list[Document],
        tool_settings: RetrieverToolSettings,
    ) -> BaseTool:
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
