# github_agent.py

from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain.chains.summarize import load_summarize_chain
from tiktoken import encoding_for_model

from app.client.openai_client import get_openai_llm
from app.tools.search_github_repo import search_github_repo
from app.tools.github_describe_repo import github_describe_repo
from app.tools.github_issue_details import github_issue_details
from app.tools.github_pr_details import github_pr_details
from app.tools.list_top_issues import list_top_issues
from app.tools.list_top_prs import list_top_prs
from app.tools.github_pr_review import github_review_pr
from app.tools.github_issue_review import github_issue_fixer

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

class GitHubAgent:
    def __init__(self, thread_id: str = "default-thread"):
        self.thread_id = thread_id
        self.max_tokens = 2000
        self.encoder = encoding_for_model("gpt-3.5-turbo")

        self.llm = get_openai_llm()
        self.summarizer_llm = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo")

        self.tools = [
            search_github_repo,
            github_describe_repo,
            github_issue_details,
            github_pr_details,
            list_top_issues,
            list_top_prs,
            github_review_pr,
            github_issue_fixer
        ]

        self.react_prompt = hub.pull("hwchase17/react")
        self.agent = create_react_agent(self.llm, self.tools, self.react_prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
        )

        self.summary_chain = load_summarize_chain(
            self.summarizer_llm,
            chain_type="map_reduce",
            verbose=False,
        )

        self.memory = MemorySaver()
        self.app = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(state_schema=MessagesState)
        workflow.add_node("summarize", self._summarize_old_messages)
        workflow.add_node("agent", self._safe_call_agent)
        workflow.add_edge(START, "summarize")
        workflow.add_edge("summarize", "agent")
        return workflow.compile(checkpointer=self.memory)

    def _summarize_old_messages(self, state: MessagesState):
        messages = state["messages"]
        total_tokens = sum(len(self.encoder.encode(m.content)) for m in messages)
        logger.info("Summarizing messages: %d tokens", total_tokens)

        if total_tokens < self.max_tokens:
            return {"messages": messages}

        summary = self.summary_chain.invoke({"input": messages})["output"]
        logger.info("Summary generated: %s", summary[:100])
        new_history = messages[-5:] + [AIMessage(content=summary)]
        return {"messages": new_history}

    def _call_agent(self, state: MessagesState):
        logger.info("Calling agent with %d messages", len(state["messages"]))
        response = self.agent_executor.invoke({"input": state["messages"]})
        output = response.get("output", "").strip()
        logger.info("Agent response: %s", output[:100])
        return {"messages": state["messages"] + [AIMessage(content=output)]}

    def _safe_call_agent(self, state: MessagesState):
        try:
            result = self._call_agent(state)
            last_msg = result["messages"][-1].content.strip()

            if not last_msg or "I don't know" in last_msg.lower():
                fallback = AIMessage(
                    content="🤔 I'm not sure how to help with that yet, but I'm learning every day. Could you rephrase or ask something else?")
                return {"messages": state["messages"] + [fallback]}

            return result

        except Exception as e:
            logger.error("Agent call failed: %s", str(e), exc_info=True)
            err = AIMessage(content=f"⚠️ Oops, something went wrong: {e}")
            return {"messages": state["messages"] + [err]}

    def get_history(self) -> list[str]:
        """Returns the current message history as plain text."""
        history = self.memory.get(self.thread_id)
        if not history:
            return []
        return [f"{msg.type}: {msg.content}" for msg in history["messages"]]

    def chat(self, user_input: str):
        logger.info("Received user input: %s", user_input)
        initial_state = {"messages": [HumanMessage(content=user_input)]}
        result = self.app.invoke(
            initial_state,
            config={"configurable": {"thread_id": self.thread_id}},
        )
        return result["messages"][-1].content
