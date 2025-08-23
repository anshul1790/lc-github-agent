import re
import requests
from langchain.tools import Tool

GITHUB_API = "https://api.github.com/repos"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "langchain-agent"
}

def _github_pr_details(pr_url: str) -> str:
    """
    Fetch metadata for a GitHub Pull Request.
    Supports:
    - https://github.com/owner/repo/pull/123
    - https://github.com/owner/repo/pulls/123
    """
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)/(?:pull|pulls)/(\d+)", pr_url.strip())
    if not match:
        return "Invalid PR URL format. Use: https://github.com/owner/repo/pull/123"

    owner, repo, pr_number = match.groups()
    try:
        res = requests.get(f"{GITHUB_API}/{owner}/{repo}/pulls/{pr_number}", headers=HEADERS, timeout=5)
        if res.status_code != 200:
            return f"PR fetch failed: {res.status_code}"

        data = res.json()
        return (
            f"🔀 PR #{data.get('number')}: {data.get('title', 'No title')}\n"
            f"🔗 URL: {data.get('html_url')}\n"
            f"📝 Description:\n{data.get('body', 'No description')[:1000]}"
        )
    except Exception as e:
        return f"Error retrieving PR: {str(e)}"

github_pr_details = Tool(
    name="GitHubPRDetails",
    func=_github_pr_details,
    description="Fetch metadata and description of a GitHub Pull Request from its URL."
)

# Optional: CLI test
if __name__ == "__main__":
    print(_github_pr_details("https://github.com/openai/openai-python/pull/2543"))