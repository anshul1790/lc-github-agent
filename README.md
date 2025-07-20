# MCP LangChain Agent

A modular, production-ready Python project for building conversational AI agents using [LangChain](https://python.langchain.com/), [OpenAI](https://platform.openai.com/), and FastAPI.  
This agent can answer questions, fetch GitHub repository and issue details, additionally - perform calculations, provide weather info, and more.

---

## 🚀 Features

- **Conversational agent** powered by OpenAI LLMs (GPT-4, GPT-4o, etc.)
- **GitHub tools**: Get repository stats and issue details
- **Calculator**: Safe math expression evaluation
- **Weather & Time tools**: Demo endpoints for extensibility
- **FastAPI**: Production-ready API server
- **Modular structure**: Easy to extend with new tools

---

## 📁 Project Structure

```
app/
  main.py                # FastAPI entrypoint
  schema.py              # Pydantic models
  client/
    openai_client.py     # OpenAI LLM setup
  orchestrator/
    agent_router.py      # Agent logic & API endpoints
  tools/
    github_describe_repo.py
    github_issue_details.py
    ... (add more tools here)
requirements.txt
.env                     # Your OpenAI API key and other secrets
.gitignore
README.md
```

---

## ⚙️ Setup

1. **Clone the repo**
    ```sh
    git clone <your-repo-url>
    cd mcp-lc-agent
    ```

2. **Create and activate a virtual environment**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your `.env` file**
    ```
    OPENAI_API_KEY=...
    ```

5. **Run the FastAPI server**
    ```sh
    uvicorn app.main:app --reload
    ```

---

## 🛠️ Usage

### **API Endpoint**

- **POST** `/agent/ask`
    - **Request body:**  
      ```json
      { "input": "What is the current weather in Delhi?" }
      ```
    - **Response:**  
      ```json
      { "output": "The current weather in Delhi is sunny and 30°C." }
      ```

### **Supported Prompts**

- "Describe https://github.com/openai/openai-python"
- "Show details for https://github.com/openai/openai-python/issues/123"
- "What is 2 + 3 * 4?"
- "What time is it in Asia/Kolkata?"
- "What is the current weather in Delhi?"

