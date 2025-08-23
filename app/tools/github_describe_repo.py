import requests
import re
import base64
from langchain.tools import Tool

GITHUB_API = "https://api.github.com/repos"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "langchain-agent"
}

def _extract_owner_repo(url: str):
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)(?:/|$)", url.strip())
    return match.groups() if match else (None, None)

def _fetch_readme(owner: str, repo: str) -> str:
    try:
        res = requests.get(f"{GITHUB_API}/{owner}/{repo}/readme", headers=HEADERS, timeout=5)
        if res.status_code != 200:
            return "README not available."
        content = base64.b64decode(res.json().get("content", "")).decode("utf-8", errors="ignore")
        return content.strip()[:1000] or "README is empty."
    except Exception:
        return "Error retrieving README."

def _describe_repo(repo_url: str) -> str:
    owner, repo = _extract_owner_repo(repo_url)
    if not owner or not repo:
        return "Invalid GitHub URL. Format: https://github.com/owner/repo"

    try:
        res = requests.get(f"{GITHUB_API}/{owner}/{repo}", headers=HEADERS, timeout=5)
        if res.status_code != 200:
            return f"Repo info fetch failed: {res.status_code}"
        data = res.json()
        readme = _fetch_readme(owner, repo)

        return (
            f"📦 Repo: {data.get('full_name', 'N/A')}\n"
            f"📝 Description: {data.get('description') or 'No description'}\n"
            f"🐛 Open Issues: {data.get('open_issues_count', 0)}\n"
            f"📖 README Preview:\n{'-'*30}\n{readme}"
        )
    except Exception as e:
        return f"Unexpected error: {str(e)}"

github_describe_repo = Tool(
    name="DescribeGitHubRepo",
    func=_describe_repo,
    description="Summarize a GitHub repository from its URL. Includes metadata and README preview."
)

# Optional: CLI test
if __name__ == "__main__":
    print(_describe_repo("https://github.com/openai/openai-python"))
