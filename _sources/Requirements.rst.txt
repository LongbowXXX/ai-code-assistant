Requirements
=================

Create an app/IDE plugin that assists with coding using LLM.

- Assist in implementing source code
   - TODO, FIXME implementation
   - Code explanation
   - Add comments
   - Create tests
   - Improve code
   - Code review
- Select the source code to be advised
- Refer to other files during advice
   - Embed source code and enable search by cosine similarity
   - Refer to related files by class name, function name, etc.
   - Specify files to refer to explicitly
- Refer to non-source code files
   - web site
   - pdf files
   - image files
- Understand usage fees
   - Know the number of tokens for Chat/Embedding
   - Set a table for token/fee conversion
   - Use free models available on Ollama
- Use Python for the core part of the app to keep up with the evolution of LLM
   - Can be used as a coding assistant app with Python alone
- Can be used as an IDE plugin
   - Target IntelliJ/PyCharm
      - The implementation language of the IntelliJ/PyCharm plugin is Kotlin
      - To call Python from Kotlin, the core on the Python side supports CLI
      - Call CLI from the plugin
- Select the LLM to use
   - OpenAI
   - Amazon Bedrock Claude3
   - Google Gemini Pro
   - Ollama
- Support advanced responses using multiple LLMs in an ensemble
