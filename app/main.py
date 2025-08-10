from fastapi import FastAPI
from app.routes.agent_router import router as agent_router

def call_fastapi():
    app = FastAPI(
        title="MCP LC Agent",
        description="LangChain-powered agent API",
        version="1.0.0"
    )

    app.include_router(agent_router)


if __name__ == "__main__":
    call_fastapi()
