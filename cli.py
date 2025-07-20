from app.orchestrator.agent_router import get_agent

agent = get_agent()
# ========== RUN INTERACTIVE LOOP FOR LOCAL TESTING ==========
print("🤖 LangChain Agent Ready. Type 'exit' to quit.")
while True:
    user_input = input("🧑 You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    result = agent.invoke({"input": user_input})
    print(f"🤖 Bot: {result['output']}")
