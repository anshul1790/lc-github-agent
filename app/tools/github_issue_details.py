import re
import requests
from langchain.tools import Tool

GITHUB_API = "https://api.github.com/repos"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "langchain-agent"
}

def _github_issue_details(issue_url: str) -> str:
    """
    Fetch details of a GitHub issue.
    Supports:
    - https://github.com/owner/repo/issues/123
    - https://github.com/owner/repo#123
    """
    match = re.match(r"https?://github\.com/([^/]+)/([^/#]+)(?:/issues/|#)(\d+)", issue_url.strip())
    if not match:
        return "Invalid format. Use: https://github.com/owner/repo/issues/123 or https://github.com/owner/repo#123"

    owner, repo, issue_number = match.groups()
    try:
        res = requests.get(f"{GITHUB_API}/{owner}/{repo}/issues/{issue_number}", headers=HEADERS, timeout=5)
        if res.status_code != 200:
            return f"Issue fetch failed: {res.status_code}"

        data = res.json()
        return (
            f"🪪 Issue #{data.get('number')}: {data.get('title', 'No title')}\n"
            f"🔗 URL: {data.get('html_url')}\n"
            f"📝 Description:\n{data.get('body', 'No description')[:1000]}"
        )
    except Exception as e:
        return f"Error retrieving issue: {str(e)}"

github_issue_details = Tool(
    name="GitHubIssueDetails",
    func=_github_issue_details,
    description="Fetch metadata and description of a GitHub issue from its URL."
)

# Optional: CLI test
if __name__ == "__main__":
    print(_github_issue_details("https://github.com/openai/openai-python/issues/2544"))