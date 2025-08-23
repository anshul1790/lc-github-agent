# routes/github_chat.py
from fastapi import APIRouter, Request
from app.agent.github_agent import GitHubAgent

router = APIRouter()
agent = GitHubAgent(thread_id="api-session")

@router.post("/chat")
async def chat_with_agent(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    response = agent.chat(user_input)
    return {"response": response}
