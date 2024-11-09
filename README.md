# ai-code-assistant
Code implementation assistance by LLM.

## Requirements
- Python 3.11
- Ollama v0.3.14  
  - not compatible with 0.4.0. Please install 0.3.14
  - Python ollama package(0.3.3) is not compatible with 0.4.0. (2024/11/09)
  - Using models
    - llama3.1 (ChatModel)
    - bge-m3 (EmbeddingModel)
  - Ollama download link: https://ollama.com/
  - Ollama quick start guide: https://github.com/ollama/ollama/blob/main/README.md#quickstart
- RAG (Retrieval Augmented Generation)
  - To use RAG, you need to use a model that supports Tool Calling.
  - https://python.langchain.com/docs/integrations/chat/

## Installation
```
$ pip install -e .
$ pip install -e .[dev]
```

## Run Web GUI
```
$ mesop src/ai_code_assistant/gui/gui_app.py
```
Running server on http://localhost:32123

## mypy
```
$ mypy . --no-incremental
```
## flake8
```
$ flake8 --statistics
```
## black
```
$ black .
```

## pytest
```
$ pytest --html=build/reports/test/result/report.html --cov --cov-report=html:build/reports/test/coverage --cov-report=term
```
