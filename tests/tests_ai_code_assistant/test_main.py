#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from pathlib import Path

import pytest
from flask.cli import load_dotenv
from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.document_loaders import GitLoader
from langchain_community.vectorstores import Chroma
from langchain_core.tools import create_retriever_tool
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from ai_code_assistant.common.path import APPLICATION_DB_DIR, APPLICATION_REPOSITORY_DIR
from ai_code_assistant.main import main


@pytest.mark.skip(reason="needs openai api key")
@pytest.mark.asyncio
async def test_main() -> None:
    await main()


@pytest.mark.skip(reason="needs openai api key")
def test_sandbox() -> None:
    print(APPLICATION_DB_DIR)
    print(APPLICATION_REPOSITORY_DIR)
    load_dotenv()
    repo_path = Path(APPLICATION_REPOSITORY_DIR, "ai-code-assistant").resolve()
    loader = GitLoader(
        clone_url="https://github.com/LongbowXXX/ai-code-assistant",
        repo_path=str(repo_path),
        branch="develop",
    )
    documents = loader.load()
    # for document in documents:
    #     print(document)
    vector_store: VectorStore = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
        collection_name="ai-code-assistant-repo",
        persist_directory=str(APPLICATION_DB_DIR),
    )

    retriever = vector_store.as_retriever()
    tool = create_retriever_tool(
        retriever,
        "search_ai_code_assistant",
        "Searches and returns the source code in the ai-code-assistant repository.",
    )
    prompt = hub.pull("hwchase17/openai-tools-agent")
    llm = ChatOpenAI(temperature=0, model="gpt-4o-2024-08-06", verbose=True)
    agent = create_openai_tools_agent(llm, [tool], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[tool], verbose=True)  # type: ignore[arg-type]
    result = agent_executor.invoke({"input": "Please explain main.py in ai-code-assistant."})
    print(f"output={result['output']}")
