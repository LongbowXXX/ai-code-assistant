#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import pytest
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings


@pytest.mark.skip(reason="needs ollama server")
def test_ollama_embedding() -> None:
    embeddings = OllamaEmbeddings(
        model="bge-m3",
    )

    vectorstore = InMemoryVectorStore.from_texts(
        [
            "France",
            "Babe Ruth",
            "baseball player",
            "basketball player",
        ],
        embedding=embeddings,
    )

    retriever = vectorstore.as_retriever()

    retrieved_documents = retriever.invoke("Tell me about Babe Ruth")

    print(f"count={len(retrieved_documents)}")
    for doc in retrieved_documents:
        print(doc.page_content)
        print(doc)
