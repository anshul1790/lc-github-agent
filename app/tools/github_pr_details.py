import requests
import re
from langchain.tools import Tool

def _github_pr_details(pr_url: str) -> str:
    """
    Get detailed information about a specific GitHub Pull Request.
    Accepts formats like:
    - https://github.com/owner/repo/pulls/123
    """
    match = re.match(
        r"https?://github\.com/([^/]+)/([^/]+)/(?:pull|pulls)/(\d+)",
        pr_url.strip()
    )
    if not match:
        return "Final Answer:\n Invalid PR URL format. Use https://github.com/owner/repo/pull/123"

    owner, repo, pr_number = match.groups()
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "langchain-agent"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Final Answer:\n Failed to fetch PR details: {response.status_code} - {response.text}"

        pr_data = response.json()
        return (
            f"Final Answer:\n"
            f"PR Number #{pr_data['number']}\n"
            f"Title #{pr_data['title']}\n"
            f"URL: {pr_data['url']}\n"
            f"details: {pr_data.get('body', 'No description')[:2000]}\n"
        )
    except Exception as e:
        return f"Final Answer:\n Error: {str(e)}"

github_pr_details = Tool(
    name="GitHubPRDetails",
    func=_github_pr_details,
    description="Get details of a GitHub Pull Request from its URL."
)

if __name__ == "__main__":
    print(_github_pr_details("https://github.com/openai/openai-python/pull/2543"))