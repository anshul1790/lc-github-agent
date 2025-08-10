import sys

import requests
import re
from langchain.tools import Tool

def _github_issue_details(repo_url_and_issue: str) -> str:
    """
    Get detailed information about a specific GitHub issue.
    Accepts either:
    - https://github.com/owner/repo/issues/123
    - https://github.com/owner/repo#123
    """
    match = re.match(
        r"https?://github\.com/([^/]+)/([^/]+)(?:/issues/|#)(\d+)",
        repo_url_and_issue.strip()
    )
    if not match:
        return "Final Answer:\n Invalid format. Use https://github.com/owner/repo/issues/123 or https://github.com/owner/repo#123"

    owner, repo, issue_number = match.groups()
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "langchain-agent"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Final Answer:\n Failed to fetch issue details: {response.status_code} - {response.text}"

        issue_data = response.json()
        return (
            f"Final Answer:\n"
            f"Issue #{issue_data['number']}: {issue_data['title']}\n"
            f"URL: {issue_data['html_url']}\n"
            f"Description: {issue_data.get('body', 'No description')[:2000]}"
        )

    except Exception as e:
        return f"Final Answer:\n Error: {str(e)}"

github_issue_details = Tool(
    name="GitHubIssueDetails",
    func=_github_issue_details,
    description="Get details of a GitHub issue from its URL."
)

if __name__ == "__main__":
    # Example usage
    print(_github_issue_details("https://github.com/openai/openai-python/issues/2544"))