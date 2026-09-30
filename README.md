# 🤖 FreelanceOS: The Agentic Copilot

A multi-agent AI assistant for freelancers, built with **CrewAI**, **Google Gemini (free tier)** and **Streamlit**.
Paste a job post and four agents work in sequence:

| Agent | Output |
|---|---|
| 🔍 Lead Scout | Fit score, red flags, GO/NO-GO |
| ✍️ Proposal Architect | Personalized proposal |
| 📅 Project Manager | Milestones, timeline, risks |
| 💰 Finance Officer | Pricing, payment schedule, invoice draft |

## Project Structure
```
freelanceos/
├── app.py            # Streamlit UI
├── main.py           # Crew execution logic
├── agents.py         # 4 CrewAI agents
├── tasks.py          # 4 sequential tasks
├── requirements.txt
├── .env.example
└── README.md
```

## Run Locally
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then add your free Gemini key from https://aistudio.google.com/apikey
streamlit run app.py
```

## Deploy
Deploy free on Streamlit Community Cloud. Add `GEMINI_API_KEY = "your-key"` under **Advanced settings → Secrets**.

## Tech Stack
Python 3.10–3.12, CrewAI, Google Gemini (via LiteLLM), Streamlit, Pydantic.

## License
MIT
