from fastapi import FastAPI
from app.routes.agent_router import router as agent_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="MCP LC Agent",
    description="LangChain-powered agent API",
    version="1.0.0"
)
# Mount static files at /static
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Serve index.html manually at root
from fastapi.responses import FileResponse

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

# Include your agent router
app.include_router(agent_router)
