from fastapi import APIRouter, HTTPException
from app.agent.github_agent import execute_agent_flow
from app.schema import PromptRequest

# Create router
router = APIRouter()

# Instantiate the agent once so it doesn't reload each request
agent_executor, prompt_template = execute_agent_flow()


@router.post("/agent/ask")
async def ask_agent(request: PromptRequest):
    """
        Endpoint to query the GitHub agent.
        Expects: {"project_name": "...", "pr_number": "...", "issue_number": "..."}
    """
    if not request.project_name and not request.pr_number and not request.issue_number:
        raise HTTPException(status_code=400, detail="At least one of project_name, pr_number, or issue_number is required")

    # Format the prompt dynamically
    formatted_prompt = prompt_template.format_prompt(
        project_name=request.project_name or "",
        pr_number=request.pr_number or "",
        issue_number=request.issue_number or ""
    )

    # Invoke agent
    result = agent_executor.invoke(
        input={"input": formatted_prompt}
    )

    return {"output": result["output"]}
