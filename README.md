# 🤖 AI Travel Backend

The FastAPI + LangGraph agent backend for the AI Travel Planner app. Built with Python and deployed on Render.

## Purpose
Houses the core AI logic. Receives trip requests, runs a LangGraph ReAct agent powered by GPT-4o-mini,
calls weather and budget tools, searches the web via Tavily, and streams the generated
itinerary back token by token via SSE.

## 🌐 Live URL
[https://ai-travel-backend-khc0.onrender.com](https://ai-travel-backend-khc0.onrender.com)

## 📁 Repo Structure
```
ai-travel-backend/
├── agent.py                   # LangGraph ReAct agent, build_prompt, stream_agent
├── main.py                    # FastAPI app, TripRequest model, /plan-trip route
├── weather_tool.py            # Weather forecast tool (called by agent)
├── budget_tool.py             # Budget estimation tool (called by agent)
├── requirements.txt
└── .env                       # OPENAI_API_KEY, TAVILY_API_KEY (not committed)
```
## 🛠️ Tech Stack & Libraries

| Library | Purpose |
|---------|---------|
| FastAPI | Python web framework + SSE streaming |
| LangGraph | ReAct agent orchestration |
| LangChain OpenAI | GPT-4o-mini LLM integration |
| LangChain Tavily | Web search tool for real-time info |
| Pydantic | Request validation via BaseModel |
| python-dotenv | Environment variable management |
| uvicorn | ASGI server to run FastAPI |

## 📄 File Descriptions

| File | Description |
|------|-------------|
| `agent.py` | Core AI logic — defines the LangGraph ReAct agent, `build_prompt()` constructs the full trip planning prompt, `stream_agent()` streams tokens back, `run_agent()` for non-streaming use |
| `main.py` | FastAPI app entry point — defines `TripRequest` Pydantic model and `POST /plan-trip` route that returns a `StreamingResponse` |
| `weather_tool.py` | LangChain tool that fetches weather forecast for a destination — called automatically by the agent |
| `budget_tool.py` | LangChain tool that estimates trip budget based on destination, days, and vibe — called automatically by the agent |
| `requirements.txt` | All Python dependencies |
| `.env` | Stores `OPENAI_API_KEY` and `TAVILY_API_KEY` — never committed to Git |

## 🚀 Install & Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/Sagarika-Singh-99/ai-travel-backend.git
cd ai-travel-backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here

# 5. Start the server
uvicorn main:app --reload --port 8000
```

> The backend will run on http://localhost:8000
