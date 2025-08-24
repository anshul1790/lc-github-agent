# MCP LangChain Agent

A modular, Python project for building conversational AI agents using [LangChain](https://python.langchain.com/), [OpenAI](https://platform.openai.com/), and FastAPI.  
This agent can answer questions, fetch GitHub repository and issue details, additionally - perform calculations, provide weather info, and more.

---

## 🚀 Features

- **Conversational agent** powered by OpenAI LLMs (GPT-4, GPT-4o, etc.)
- **Advanced GitHub Integration**:
  - Repository description and search
  - Issue tracking and review
  - PR details and review capabilities
  - List top issues and PRs
- **FastAPI**: Production-ready API server
- **Modular structure**: Easy to extend with new tools

---

## 📁 Project Structure

```
app/
├── agent/
│   └── github_agent.py      # GitHub agent implementation
├── client/
│   └── openai_client.py     # OpenAI LLM setup
├── routes/
│   └── agent_router.py      # API routing and endpoints
└── tools/
    ├── github_describe_repo.py
    ├── github_issue_details.py
    ├── github_issue_review.py
    ├── github_pr_details.py
    ├── github_pr_review.py
    ├── list_top_issues.py
    ├── list_top_prs.py
    └── search_github_repo.py

static/                      # Static assets
cli.py                      # CLI interface
main.py                     # Application entrypoint
requirements.txt            # Project dependencies
```

---

## ⚙️ Setup

1. **Clone the repo**
    ```sh
    git clone <your-repo-url>
    cd lc-github-agent
    ```

2. **Create and activate a virtual environment**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following required variables:
   ```env
   # Required OpenAI API Configuration
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo

   LANGCHAIN_API_KEY=your_api_key_here
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_PROJECT=personal-learning

   # Optional Configuration
   PORT=8000  # Default port for the FastAPI server
   HOST=0.0.0.0  # Default host
   ```

   To get these credentials:
   - Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a GitHub token with repo access from [GitHub Settings](https://github.com/settings/tokens)
   - Get your LangChain API key from [LangChain](https://langchain.com/)

---

## 🚀 Running the Application

You can run the application in three ways:

1. **Using CLI Interface (Recommended for testing)**
   ```sh
   python cli.py
   ```
   This will start the interactive CLI mode where you can directly chat with the agent.

2. **Using FastAPI Development Server**
   ```sh
   python main.py
   ```
   This will start the server on http://localhost:8000

3. **Using Uvicorn with Hot Reload (Recommended for development)**
   ```sh
   uvicorn main:app --reload --port 8000
   ```
   This will start the server with hot reload enabled, which means any changes you make to the code will automatically restart the server.

Once the server is running, you can:
- Access the API documentation at `http://localhost:8000/docs`
- Access the alternative documentation at `http://localhost:8000/redoc`
- Use the web interface at `http://localhost:8000`

### Making API Requests

You can test the API using curl or any API client:

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Describe the repository tensorflow/tensorflow"}'
```

Or use the provided `ask-agent.http` file if you're using VS Code with the REST Client extension.

---

## 📚 Available Tools

- **Repository Tools**
  - `github_describe_repo`: Get detailed repository information
  - `search_github_repo`: Search for GitHub repositories

- **Issue Management**
  - `github_issue_details`: Get detailed issue information
  - `github_issue_review`: Review GitHub issues
  - `list_top_issues`: List top issues in a repository

- **PR Management**
  - `github_pr_details`: Get PR details
  - `github_pr_review`: Review pull requests
  - `list_top_prs`: List top pull requests

---

## 📝 License

This project is open source and available under the MIT License.


## 🙌 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.