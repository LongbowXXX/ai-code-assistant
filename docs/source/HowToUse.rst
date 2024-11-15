How To Use
=================

Code implementation assistance by LLM.

Requirements
------------

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

Setup
-----

1. Install Ollama.
    - https://ollama.com/
    - Install models: llama3.1, bge-m3
2. Setup google custom search.
    - `Custom Search API <https://developers.google.com/custom-search/v1/overview>`_
3. Setup AWS Amazon Bedrock.
    - `Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html>`_
4. Copy .env.example to .env and set the environment variables in the .env file.

Demo
----
.. figure:: ./images/00_AiCodeAssistant_Demo.mp4
   :class: controls

Installation
------------

.. code-block:: bash

   $ pip install -e .
   $ pip install -e .[dev]

Run Web GUI
-----------

.. code-block:: bash

   $ mesop src/ai_code_assistant/gui/gui_app.py

Running server on http://localhost:32123

mypy
----

.. code-block:: bash

   $ mypy . --no-incremental

flake8
------

.. code-block:: bash

   $ flake8 --statistics

black
-----

.. code-block:: bash

   $ black .

pytest
------

.. code-block:: bash

   $ pytest --html=build/reports/test/result/report.html --cov --cov-report=html:build/reports/test/coverage --cov-report=term