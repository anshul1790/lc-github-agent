import requests
import re
from langchain.tools import Tool

def _extract_owner_repo(url: str):
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)(?:/|$)", url.strip())
    if not match:
        return None, None
    return match.groups()

def _list_top_issues(repo_url: str, limit: int = 10) -> str:
    owner, repo = _extract_owner_repo(repo_url)
    if not owner or not repo:
        return "Final Answer:\n Invalid GitHub repo URL."

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "langchain-agent"
    }
    params = {"state": "open", "per_page": limit, "sort": "comments", "direction": "desc"}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return f"Final Answer:\n Failed to fetch issues: {response.status_code} - {response.text}"

        issues = [i for i in response.json() if "pull_request" not in i]  # Exclude PRs
        result = "Final Answer:\n Top Issues:\n"
        for i, issue in enumerate(issues, 1):
            result += f"{i}. #{issue['number']} - {issue['title']} (comments: {issue['comments']})\n"
        return result.strip()
    except Exception as e:
        return f"Final Answer:\n Error: {str(e)}"

list_top_issues = Tool(
    name="ListTopIssues",
    func=lambda url: _list_top_issues(url, limit=10),
    description="List top 10 open issues in a GitHub repo sorted by comment count."
)

if __name__ == "__main__":
    # Example usage
    print(_list_top_issues("https://github.com/openai/openai-python"))
