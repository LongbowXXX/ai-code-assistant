Software Design
=================================

This document describes the design of the AI code assistant software.

Overview
--------

.. mermaid::

   graph TD
       subgraph "IDE Plugin" ["IDE Plugin (kotlin)"]
           code_assistant["code_assistant (IntelliJ IDEA)"]
       end

       subgraph "Front End" ["Front End (python)"]
           cli["Web API (FastAPI)"]
           gui["gui (google mesop)"]
       end

       subgraph "Core Logic" ["Core Logic (python)"]
           assistant["assistant"]
       end

       subgraph "LangChain" ["LangChain (python)"]
           langchain["langchain"]
       end

       gui --> assistant
       cli --> assistant
       code_assistant -.-> cli
       assistant --> langchain

Core Logic
----------

This section describes the design of the core logic of the AI assistant.

.. mermaid::

   classDiagram
     class AiConfig {
     }

     class LlmConfig {
     }

     class ToolSettings {
     }

     class RetrieverToolSettings {
     }

     class AiAssistant {
       system()
       ask_async()
     }
     note for AiAssistant "The AiAssistant class is the main class\n of the AI assistant system."

     class AiTools {
        load_tools_async()
        create_tool_async()
        remove_tool_async()
     }
     note for AiTools "The AiTools class manages\n the tools used by the AI assistant."

     class AiLlms {
        create_llm()
     }

     class ToolSettingsManager {
        load_tool_settings()
        save_tool_setting()
        remove_tool_setting()
     }

     class RetrieverTool {
        load_tools_async()
        create_tool_async()
        remove_tool_async()
     }

    AiAssistant --> AiConfig : "1"
    AiAssistant ..> AiTools
    AiTools *--> ToolSettingsManager : "1"
    AiTools --> RetrieverTool
    AiAssistant ..> AiLlms
    AiConfig *--> LlmConfig : "1"
    AiConfig *--> ToolSettings : "0..*"
    RetrieverToolSettings --|> ToolSettings
