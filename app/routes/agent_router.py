# routes/github_chat.py
import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter, Request
from app.agent.github_agent import GitHubAgent

router = APIRouter()
agent = GitHubAgent(thread_id="api-session")

@router.post("/chat")
async def chat_with_agent(request: Request):
    logger.info("Received chat request")
    data = await request.json()
    user_input = data.get("message", "")
    response = agent.chat(user_input)
    return {"response": response}
