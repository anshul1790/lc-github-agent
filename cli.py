from app.routes.agent_router import agent_executor

print("🤖 LangChain Agent Ready. Type 'exit' to quit.")
while True:
    user_input = input("🧑 You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    result = agent_executor.invoke({"input": user_input})
    print(f"🤖 Bot: {result['output']}")
