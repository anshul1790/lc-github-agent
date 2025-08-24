import re
import requests

from langchain.tools import Tool
from langchain.schema import HumanMessage

from app.client.openai_client import get_openai_llm

GITHUB_API = "https://api.github.com/repos"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "langchain-agent"
}

# initialize your OpenAI-backed LLM
llm = get_openai_llm()

def _github_issue_fixer(issue_url: str) -> str:
    """
    Given a GitHub issue URL, fetch its details and ask the LLM
    to propose 2–3 concrete ways to fix it (with code examples).
    """
    # 1. Validate & parse URL
    match = re.match(
        r"https?://github\.com/([^/]+)/([^/#]+)(?:/issues/|#)(\d+)",
        issue_url.strip()
    )
    if not match:
        return (
            "Invalid issue URL. "
            "Use https://github.com/owner/repo/issues/123 or https://github.com/owner/repo#123"
        )

    owner, repo, issue_number = match.groups()

    # 2. Fetch issue data from GitHub API
    try:
        res = requests.get(
            f"{GITHUB_API}/{owner}/{repo}/issues/{issue_number}",
            headers=HEADERS,
            timeout=5
        )
        if res.status_code != 200:
            return f"Failed to fetch issue: {res.status_code}"
        issue = res.json()
    except Exception as e:
        return f"Error retrieving issue: {e}"

    title = issue.get("title", "<no title>")
    body = issue.get("body", "").strip() or "<no description>"

    # 3. Build prompt for the LLM
    prompt = (f"""
            You are an experienced software engineer. The following GitHub issue describes a bug or missing feature:
            
            Issue Title: {title}
            
            Issue Description:
            {body}
            
            Please suggest 2–3 distinct ways to fix or address this issue. For each suggestion:
            - Give a brief rationale.
            - Provide a code snippet or pseudo-code if applicable.
            """
            .strip())

    # 4. Invoke the LLM via invoke() instead of __call__()
    try:
        messages = [HumanMessage(content=prompt)]
        llm_result = llm.invoke(messages)
        # extract the first generation's message
        return llm_result.content
        # return generation.message.content.strip()
    except Exception as e:
        return f"Error generating fix suggestions: {e}"

# 5. Wrap as a LangChain Tool
github_issue_fixer = Tool(
    name="GitHubIssueFixer",
    func=_github_issue_fixer,
    description=(
        "Given a GitHub issue URL, fetch the issue details and suggest 2–3 concrete "
        "fixes or improvements, including rationale and optional code snippets."
    )
)

# Optional CLI test
if __name__ == "__main__":
    print(
        _github_issue_fixer(
            "https://github.com/openai/openai-python/issues/2580"
        )
    )
