import requests
import re
import base64
from langchain.tools import Tool

def _extract_owner_repo(url: str):
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)(?:/|$)", url.strip())
    if not match:
        return None, None
    return match.groups()

def _fetch_readme(owner: str, repo: str) -> str:
    """Fetch the README.md content from the GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "langchain-agent"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "README not found or failed to fetch."
        data = response.json()
        # README content is Base64 encoded
        content = base64.b64decode(data.get("content", "")).decode("utf-8", errors="ignore")
        return content.strip() if content else "README file is empty."
    except Exception as e:
        return f"Error fetching README: {str(e)}"

def _describe_repo(repo_url: str) -> str:
    owner, repo = _extract_owner_repo(repo_url)
    if not owner or not repo:
        return "Final Answer:\n Invalid GitHub repo URL. Use https://github.com/owner/repo"

    repo_info_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "langchain-agent"
    }

    try:
        # Fetch repo metadata
        response = requests.get(repo_info_url, headers=headers)
        if response.status_code != 200:
            return f"Final Answer:\n Failed to fetch repo info: {response.status_code} - {response.text}"
        response_data = response.json()

        # Fetch README.md
        readme_content = _fetch_readme(owner, repo)

        return (
            f"Final Answer:\n"
            f"📦 Repository: {response_data.get('full_name', 'N/A')}\n"
            f"📝 Description: {response_data.get('description', 'No description') or 'No description'}\n"
            f"🐛 Open Issues: {response_data.get('open_issues_count', 0)}\n\n"
            f"📖 Detailed:\n{'-'*40} \n{readme_content[:5000]}"
        )
    except Exception as e:
        return f"Final Answer:\n Error: {str(e)}"

github_describe_repo = Tool(
    name="DescribeGitHubRepo",
    func=_describe_repo,
    description="Summarize a GitHub repository from its URL (stars, forks, description, open issues, README.md)."
)

if __name__ == "__main__":
    # Example usage
    print(_describe_repo("https://github.com/openai/openai-python"))
