# main.py — AutoGen Two-Agent Project
# Agent 1 (Retriever): fetches a Wikipedia article
# Agent 2 (Summarizer): summarizes it into 3 bullet points

import os
import requests
from dotenv import load_dotenv
import autogen

# ── Load API key from .env ─────────────────────────────────────────────────────
load_dotenv()

# ── LLM config ────────────────────────────────────────────────────────────────
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ]
}

# ── Tool: fetch a Wikipedia summary ───────────────────────────────────────────
def get_wikipedia(topic: str) -> str:
    """Fetch the Wikipedia summary for a given topic."""
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")
    response = requests.get(url, timeout=8)
    if response.status_code != 200:
        return f"Could not fetch '{topic}' (HTTP {response.status_code})"
    data = response.json()
    return data.get("extract", "No content found.")[:800]


# ── Agent 1: Retriever ────────────────────────────────────────────────────────
retriever = autogen.AssistantAgent(
    name="Retriever",
    system_message=(
        "You are a data retrieval specialist. "
        "When given a topic, call the get_wikipedia tool and return the raw text. "
        "Do not add any commentary — return only the fetched text."
    ),
    llm_config=llm_config,
)

# ── Agent 2: Summarizer ───────────────────────────────────────────────────────
summarizer = autogen.AssistantAgent(
    name="Summarizer",
    system_message=(
        "You are a concise summarizer. "
        "Given raw text, write exactly 3 bullet points capturing the key facts. "
        "Keep each bullet under 20 words. "
        "After the bullet points, write TERMINATE on a new line."
    ),
    llm_config=llm_config,
)

# ── Proxy — orchestrates the pipeline ────────────────────────────────────────
proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda m: "TERMINATE" in m.get("content", ""),
    code_execution_config=False,
)

# Register the Wikipedia tool
retriever.register_for_llm(description="Fetch a Wikipedia article summary for a given topic.")(get_wikipedia)
proxy.register_for_execution(name="get_wikipedia")(get_wikipedia)

# ── Group chat: Retriever → Summarizer ────────────────────────────────────────
chat = autogen.GroupChat(
    agents=[proxy, retriever, summarizer],
    messages=[],
    max_round=6,
    speaker_selection_method="round_robin",
)

manager = autogen.GroupChatManager(groupchat=chat, llm_config=llm_config)

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    topic = "Artificial intelligence"   # ← change this to any Wikipedia topic

    proxy.initiate_chat(
        manager,
        message=(
            f"Retrieve the Wikipedia article for '{topic}' "
            "and then summarize it in 3 bullet points."
        ),
    )
