from fastapi import APIRouter, HTTPException
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from app.client.openai_client import get_openai_llm
from app.tools.github_describe_repo import github_describe_repo
from app.tools.github_issue_details import github_issue_details
import pytz
from datetime import datetime
from app.schema import PromptRequest

router = APIRouter()

def get_weather(location: str) -> str:
    return f"The current weather in {location} is sunny and 30°C."

def get_current_time(timezone: str) -> str:
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return now.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return str(e)

def calculate(expression: str) -> str:
    try:
        # For production, use a safe math parser!
        import numexpr
        result = numexpr.evaluate(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

tools = [
    Tool(
        name="Weather Tool",
        func=get_weather,
        description="Use this to get current weather. Input should be a city like 'Delhi'."
    ),
    Tool(
        name="Time Tool",
        func=get_current_time,
        description="Use this to get current time in a timezone. Input should be a timezone like 'Asia/Kolkata'."
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="Use this to do math calculations. Input should be a math expression like '2 + 3 * 4'."
    ),
    github_describe_repo,
    github_issue_details
]

def get_agent():
    llm = get_openai_llm()
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True,
    )
    return agent

@router.post("/agent/ask")
async def ask_agent(request: PromptRequest):
    user_input = request.input
    if not user_input:
        raise HTTPException(status_code=400, detail="Missing input")
    agent = get_agent()
    result = agent.invoke({"input": user_input})
    return {"output": result["output"]}