from fastapi import FastAPI
from app.orchestrator.agent_router import router as agent_router

app = FastAPI(
    title="MCP LC Agent",
    description="LangChain-powered agent API",
    version="1.0.0"
)

app.include_router(agent_router)
