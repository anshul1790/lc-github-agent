from langchain.tools import tool
import requests
import re

@tool
def github_issue_details(repo_url_and_issue: str) -> str:
    """
    Get detailed information about a specific GitHub issue, including title, description, and URL.
    Accepts either 'https://github.com/owner/repo/issues/123' or 'https://github.com/owner/repo#123'
    """
    # Accept both formats
    match = re.match(
        r"https?://github\.com/([^/]+)/([^/]+)(?:/issues/|#)(\d+)", 
        repo_url_and_issue.strip()
    )
    if not match:
        return "Final Answer:\n❌ Invalid format. Use format like https://github.com/owner/repo/issues/123 or https://github.com/owner/repo#123"

    owner, repo, issue_number = match.group(1), match.group(2), match.group(3)
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "langchain-agent"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Final Answer:\n❌ Failed to fetch issue details: {response.status_code} - {response.text}"

        issue = response.json()
        return (
            f"Final Answer:\n"
            f"🧾 Issue #{issue['number']}: {issue['title']}\n"
            f"📄 Description: {issue.get('body', 'No description')[:1000]}\n"
            f"📎 URL: {issue['html_url']}"
        )

    except Exception as e:
        return f"Final Answer:\n❌ Error: {str(e)}"