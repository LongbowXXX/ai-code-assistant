Software Specification
======================

1. Overview
-----------

This software provides an application and an IDE plugin that assist with coding using LLM (Large Language Model). The goal is to offer various support to users during coding, implementing the following features.

2. Functional Requirements
---------------------------

2.1 Coding Assistant Features

- **TODO, FIXME Implementation Assistance**
   - Detect TODO and FIXME comments and suggest implementation ideas.
- **Code Explanation**
   - Provide explanations for selected source code.
- **Comment Addition**
   - Automatically generate appropriate comments for the source code.
- **Test Creation**
   - Automatically generate unit tests and other test cases for the source code.
- **Code Improvement**
   - Suggest improvements for existing code.
- **Code Review**
   - Review the source code and point out improvements and potential issues.

2.2 Source Code Selection

- **Selectable Source Code for Advice**
   - Provide an interface for users to select the source code they want advice on.

2.3 Reference Function for Other Files

- **File Reference**
   - Embed the source code and search for related files using cosine similarity.
   - Automatically reference related files by class name and function name.
   - Allow explicit specification of reference files.
   - Reference files other than source code.
      - Websites
      - PDF files
      - Image files

2.4 Visualization of Usage Fees

- **Display Token Count**
   - Display the token count for Chat and Embedding.
- **Fee Conversion Table Setting**
   - Provide a function to set a table for converting token count to fees.

3. Technical Requirements
--------------------------

3.1 Core Part

- **Python**
   - Implement the core part of the coding assistance application in Python.
   - Make the application usable as a standalone Python application.

3.2 IDE Plugin

- **Target IDE**
   - Provide plugins for IntelliJ and PyCharm.
   - Implement the plugin in Kotlin.
   - Ensure the Python core can be called from Kotlin, with the core supporting CLI.
   - Provide functionality by calling the CLI from the plugin.

3.3 LLM Selection

- **Supported LLMs**
   - Allow selection of the LLM to use.
      - OpenAI
      - Amazon Bedrock Claude3
      - Google Gemini Pro
      - Ollama
- **Ensemble Response**
   - Provide advanced responses using an ensemble of multiple LLMs.

4. Non-functional Requirements
-------------------------------

4.1 Usability

- **Intuitive Interface**
   - Provide a UI/UX that users can operate intuitively.

4.2 Performance

- **Response Time**
   - Optimize the response time of the coding assistance features to not hinder user work.

4.3 Maintainability

- **Adaptation to LLM Evolution**
  - Design the core part in Python to flexibly adapt to the evolution of LLMs.

5. Supplementary Information
-----------------------------

5.1 Interface

- **GUI**
   - Provide a GUI that integrates features such as source code selection, file reference, and fee display.

5.2 Documentation

- **User Manual**
   - Provide a user manual that includes installation steps, usage methods, and FAQs.
- **Developer Documentation**
   - Provide technical documentation that includes API specifications for the core part and plugin development methods.