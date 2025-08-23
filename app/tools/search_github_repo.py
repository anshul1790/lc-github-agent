from langchain.tools import Tool
from langchain_tavily import TavilySearch

def _search_github_repo_link(name: str) -> str:
    """Search GitHub repository link by name using Tavily Search."""
    search = TavilySearch()
    response = search.run(f"{name}")
    return f"Final Answer:\n{response}"

search_github_repo = Tool(
    name="SearchGitHubRepo",
    func=_search_github_repo_link,
    description="Find GitHub repository link by name"
)
