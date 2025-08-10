import requests
import re
from langchain.tools import Tool

def _extract_owner_repo(url: str):
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)(?:/|$)", url.strip())
    if not match:
        return None, None
    return match.groups()

def _list_top_prs(repo_url: str, limit: int = 10) -> str:
    owner, repo = _extract_owner_repo(repo_url)
    if not owner or not repo:
        return "Final Answer:\n Invalid GitHub repo URL."

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "langchain-agent"
    }
    params = {"state": "open", "per_page": limit, "sort": "popularity", "direction": "desc"}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return f"Final Answer:\n Failed to fetch PRs: {response.status_code} - {response.text}"

        prs = response.json()
        result = "Final Answer:\n Top Pull Requests:\n"
        for i, pr in enumerate(prs, 1):
            result += f"{i}. #{pr['number']} - {pr['title']} (by {pr['user']['login']})\n"
        return result.strip()
    except Exception as e:
        return f"Final Answer:\n Error: {str(e)}"

list_top_prs = Tool(
    name="ListTopPRs",
    func=lambda url: _list_top_prs(url, limit=10),
    description="List top 10 open PRs in a GitHub repo."
)

if __name__ == "__main__":
    # Example usage
    print(_list_top_prs("https://github.com/openai/openai-python"))
