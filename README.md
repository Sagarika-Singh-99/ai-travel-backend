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
