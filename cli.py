# cli.py
from app.agent.github_agent import GitHubAgent

agent = GitHubAgent(thread_id="cli-session")

print("🤖 GitHub Agent Ready. Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        break
    response = agent.chat(user_input)
    print("Bot:", response)
