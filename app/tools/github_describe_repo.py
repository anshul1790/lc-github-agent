# app/tools/github_repo_info.py

import json
import requests
import re

from pydantic import BaseModel
from langchain.tools import Tool

GITHUB_API_BASE = "https://api.github.com"

class GithubSchemaInput(BaseModel):
    repo_url: str

# GitHub repo info tool
def extract_owner_repo(url: str):
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)(?:/|$)", url.strip())
    if not match:
        return None, None
    return match.group(1), match.group(2)

def _describe_repo(repo_url: str) -> str:
    owner, repo = extract_owner_repo(repo_url)
    if not owner or not repo:
        return "Final Answer:\n❌ Invalid GitHub repo URL. Please provide a URL like https://github.com/owner/repo"


    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "langchain-agent"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Final Answer:\n❌ Failed to fetch repo info: {response.status_code} - {response.text}"

        data = response.json()

        summary_payload = (
            f"📦 Repository: {data.get('full_name', 'N/A')}\n"
            f"📝 Description: {data.get('description', 'No description') or 'No description'}\n"
            f"⭐ Stars: {data.get('stargazers_count', 0)}\n"
            f"🍴 Forks: {data.get('forks_count', 0)}\n"
            f"🐛 Open Issues: {data.get('open_issues_count', 0)}"
        )
        return f"Final Answer:\n{summary_payload}"

    except Exception as e:
        return f"Final Answer:\n❌ Error: {str(e)}"

github_describe_repo = Tool(
    name="DescribeGitHubRepo",
    func=_describe_repo,
    description="Use when the user provides a GitHub repository URL to get summary stats."
)