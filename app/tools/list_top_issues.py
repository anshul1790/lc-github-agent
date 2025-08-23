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

def _list_top_issues(repo_url: str, limit: int = 10) -> str:
    owner, repo = _extract_owner_repo(repo_url)
    if not owner or not repo:
        return "Invalid GitHub repo URL. Format: https://github.com/owner/repo"

    try:
        params = {
            "state": "open",
            "per_page": limit,
            "sort": "comments",
            "direction": "desc"
        }
        res = requests.get(f"{GITHUB_API}/{owner}/{repo}/issues", headers=HEADERS, params=params, timeout=5)
        if res.status_code != 200:
            return f"Issue fetch failed: {res.status_code}"

        issues = [i for i in res.json() if "pull_request" not in i]
        if not issues:
            return "No open issues found."

        lines = [f"🔥 Top {len(issues)} Open Issues in {owner}/{repo}:"]
        for idx, issue in enumerate(issues, 1):
            lines.append(f"{idx}. #{issue['number']} - {issue['title']} ({issue['comments']} comments)")
        return "\n".join(lines)

    except Exception as e:
        return f"Error retrieving issues: {str(e)}"

list_top_issues = Tool(
    name="ListTopIssues",
    func=lambda url: _list_top_issues(url, limit=10),
    description="List top 10 open issues in a GitHub repo, sorted by comment count."
)

# Optional: CLI test
if __name__ == "__main__":
    print(_list_top_issues("https://github.com/openai/openai-python"))
