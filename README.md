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

##

<img width="791" height="356" alt="image" src="https://github.com/user-attachments/assets/218155f7-8822-4063-b323-27c75dccf584" />

</br>

<img width="767" height="228" alt="image" src="https://github.com/user-attachments/assets/91624c37-9f13-49d5-9b03-6e24b248b44c" />

