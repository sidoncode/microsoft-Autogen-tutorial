# AutoGen Two-Agent Quickstart

Two agents that collaborate on a simple pipeline:

- **Retriever** — fetches a Wikipedia article via the REST API
- **Summarizer** — condenses it into 3 bullet points

## Setup

```bash
# 1. Install dependencies
pip install pyautogen python-dotenv requests

# 2. Add your OpenAI key
cp .env.example .env
# then edit .env and replace sk-...your-key-here... with your real key

# 3. Run
python main.py
```

## Customise

Change the topic on the last line of `main.py`:

```python
topic = "Quantum computing"   # any Wikipedia article title
```
