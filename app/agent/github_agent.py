from langchain import hub
# from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent

from app.tools.search_github_repo import search_github_repo
from app.tools.github_describe_repo import github_describe_repo
from app.tools.github_issue_details import github_issue_details
from app.tools.github_pr_details import github_pr_details
from app.tools.list_top_issues import list_top_issues
from app.tools.list_top_prs import list_top_prs

from app.context.custom_context import RepoContextMemory


from dotenv import load_dotenv
load_dotenv()

def execute_agent_flow():
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o-mini",
    )

    # This prompt_template is for formatting user input if you want,
    # but DO NOT pass this to create_react_agent as its prompt!
    prompt_template = PromptTemplate(
        template="""Given the project name {project_name},
                    I want you to get me the GitHub repository link for that project and remember the project name for later conversation.
                    Whenever the user asks about the project, use the remembered project name.
                    When the user provides {pr_number}, use relevant tools to get the details of the pull request.
                    When the user provides {issue_number}, use relevant tools to get the details of the issue.""",
        input_variables=["project_name", "pr_number", "issue_number"]
    )

    tools_for_agent = [
        search_github_repo,
        github_describe_repo,
        github_issue_details,
        github_pr_details,
        list_top_issues,
        list_top_prs
    ]

    # Use the official React agent prompt, which has all needed variables
    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt,  # use default react prompt here!
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
        handle_parsing_errors=True,
    )

    # Return both for usage:
    # - agent_executor: to handle the conversation & tool calls
    # - prompt_template: optionally to format inputs or as a guide for input parsing
    return agent_executor, prompt_template
