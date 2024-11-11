Memo for development
====================

LangChain
---------

- RAG Tutorial
   - https://python.langchain.com/v0.2/docs/tutorials/rag/

- Agent Tutorial
   - https://python.langchain.com/v0.2/docs/tutorials/agents/

- Git
   - load document from git.
      - https://python.langchain.com/v0.2/docs/integrations/document_loaders/git/
      - https://python.langchain.com/v0.2/docs/integrations/document_loaders/github/
   - personal access token
      - https://github.com/settings/tokens?type=beta
      - https://python.langchain.com/v0.2/docs/integrations/tools/github/

- VectorStore
   - https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/
   - https://python.langchain.com/v0.2/docs/how_to/vectorstore_retriever/

- SQLite
   - https://python.langchain.com/v0.2/docs/integrations/memory/sqlite/

- streaming token
   - https://python.langchain.com/v0.2/docs/tutorials/agents/#streaming-tokens

LangServe
---------

- custom streaming
   - https://github.com/langchain-ai/langserve/blob/main/examples/agent_custom_streaming/server.py

Ollama
------

- Embedding
   - https://ollama.com/blog/embedding-models

- Models that support Japanese   
  ::
  
    ollama pull bge-m3

- Call Ollama API
  ::
  
    curl -k http://localhost:11434/v1/embeddings -H "Content-Type: application/json" -d '{"input": "Weather","model": "bge-m3"}'

- langchain ollama embedding  
  https://python.langchain.com/docs/integrations/text_embedding/ollama/

Amazon Bedrock
--------------

- Session Token
   - https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/sts_example_sts_GetSessionToken_section.html

GUI
---

- Google Mesop
   - https://github.com/google/mesop
   - https://google.github.io/mesop/
   - https://google.github.io/mesop/demo/
   - https://google.github.io/mesop/guides/deployment/

Python Documentations
---------------------

- Install sphinx.
  ::
  
    pip install sphinx sphinx-rtd-theme myst-parser sphinxcontrib-mermaid

- Create sphinx project.
  ::
  
    sphinx-quickstart

- Build document
  ::
  
    make.bat html

- Create API documentation
  ::
  
    sphinx-apidoc -f -o ./source/api ./src