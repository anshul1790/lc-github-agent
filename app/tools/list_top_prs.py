import re
import requests
from langchain.tools import Tool

GITHUB_API = "https://api.github.com/repos"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "langchain-agent"
}

def _extract_owner_repo(url: str):
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)(?:/|$)", url.strip())
    return match.groups() if match else (None, None)

def _list_top_prs(repo_url: str, limit: int = 10) -> str:
    owner, repo = _extract_owner_repo(repo_url)
    if not owner or not repo:
        return "Invalid GitHub repo URL. Format: https://github.com/owner/repo"

    try:
        params = {
            "state": "open",
            "per_page": limit,
            "sort": "created",  # GitHub API doesn't support 'popularity' sort
            "direction": "desc"
        }
        res = requests.get(f"{GITHUB_API}/{owner}/{repo}/pulls", headers=HEADERS, params=params, timeout=5)
        if res.status_code != 200:
            return f"PR fetch failed: {res.status_code}"

        prs = res.json()
        if not prs:
            return "No open pull requests found."

        lines = [f"🚀 Top {len(prs)} Open PRs in {owner}/{repo}:"]
        for idx, pr in enumerate(prs, 1):
            lines.append(f"{idx}. #{pr['number']} - {pr['title']} (by @{pr['user']['login']})")
        return "\n".join(lines)

    except Exception as e:
        return f"Error retrieving PRs: {str(e)}"

list_top_prs = Tool(
    name="ListTopPRs",
    func=lambda url: _list_top_prs(url, limit=10),
    description="List top 10 open pull requests in a GitHub repo."
)

# Optional: CLI test
if __name__ == "__main__":
    print(_list_top_prs("https://github.com/openai/openai-python"))
