import re
import requests
from langchain.tools import Tool

GITHUB_API = "https://api.github.com/repos"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "langchain-agent"
}
TIMEOUT = 5

PR_URL_RE = re.compile(
    r"https?://github\.com/([^/]+)/([^/]+)/(?:pull|pulls)/(\d+)"
)
ISSUE_REF_RE = re.compile(r"#(\d+)")

def _review_pr(pr_url: str) -> str:
    """
    Summarize a PR and emit a lightweight review checklist.
    Input: https://github.com/owner/repo/pull/123
    """
    m = PR_URL_RE.match(pr_url.strip())
    if not m:
        return "Invalid PR URL. Use: https://github.com/owner/repo/pull/123"

    owner, repo, pr_number = m.groups()

    # 1. Fetch PR metadata
    meta_res = requests.get(
        f"{GITHUB_API}/{owner}/{repo}/pulls/{pr_number}",
        headers=HEADERS, timeout=TIMEOUT
    )
    if meta_res.status_code != 200:
        return f"Failed to fetch PR: {meta_res.status_code}"
    pr = meta_res.json()

    # 2. Fetch list of changed files
    files_res = requests.get(
        f"{GITHUB_API}/{owner}/{repo}/pulls/{pr_number}/files",
        headers=HEADERS, timeout=TIMEOUT
    )
    if files_res.status_code != 200:
        return f"Failed to fetch PR files: {files_res.status_code}"
    files = files_res.json()

    # 3. Extract linked issues from PR body
    body = pr.get("body") or ""
    linked_issues = sorted(set(ISSUE_REF_RE.findall(body)))
    linked_str = (
        ", ".join(f"#{num}" for num in linked_issues)
        if linked_issues else "None"
    )

    # 4. Summarize changes
    total_adds = sum(f.get("additions", 0) for f in files)
    total_dels = sum(f.get("deletions", 0) for f in files)
    file_count = len(files)

    top_files = files[:5]
    files_summary = "\n".join(
        f"  • {f['filename']} (+{f['additions']}/−{f['deletions']})"
        for f in top_files
    )
    if file_count > 5:
        files_summary += f"\n  • ...and {file_count - 5} more files."

    # 5. Build review checklist
    checklist = [
        f"[ ] PR addresses issue(s): {linked_str}",
        "[ ] Code changes look focused and minimal",
        "[ ] Naming and style follow repo conventions",
        "[ ] Edge cases and error handling covered",
        "[ ] Tests added or updated for new behavior",
        "[ ] Documentation or README updates included",
        "[ ] No high-risk performance or security regressions",
        "[ ] CI passing and no merge conflicts"
    ]
    checklist_str = "\n".join(f"- {item}" for item in checklist)

    # 6. Final formatted output
    return (
        f"🔍 PR Review Summary\n"
        f"{'-'*20}\n"
        f"🔀 PR #{pr['number']}: {pr.get('title','<no title>')}\n"
        f"👤 Author: @{pr['user']['login']}\n"
        f"🔗 URL: {pr['html_url']}\n\n"
        f"📝 Description:\n{body.strip()[:300] or '<no description>'}\n\n"
        f"📎 Linked issues: {linked_str}\n"
        f"🗂️ Files changed: {file_count}   (+{total_adds}/−{total_dels})\n"
        f"{files_summary}\n\n"
        f"🛠️ Review Checklist\n"
        f"{checklist_str}"
    )

github_review_pr = Tool(
    name="GitHubPRReview",
    func=_review_pr,
    description=(
        "Fetches a GitHub PR, summarizes its intent and code changes, "
        "and emits a basic review checklist."
    )
)

# Optional CLI test
if __name__ == "__main__":
    url = "https://github.com/openai/openai-python/pull/2543"
    print(_review_pr(url))
