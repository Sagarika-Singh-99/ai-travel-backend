from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from weather_tool import get_weather
from budget_tool import estimate_budget
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

search_tool = TavilySearch(
    max_results=5,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

@tool
def weather_tool(destination: str, days: int) -> str:
    """
    Use this tool to get the weather forecast for a travel destination.
    Input should be the city name and number of days.
    Always use this tool when planning a trip itinerary.
    """
    return get_weather(destination, days)

@tool
def budget_tool(destination: str, days: int, vibe: str) -> str:
    """
    Use this tool to estimate the travel budget for a trip.
    Input should be the city name, number of days, and travel vibe.
    Always use this tool when planning a trip itinerary.
    """
    return estimate_budget(destination, days, vibe)

agent = create_react_agent(
    model=llm,
    tools=[search_tool, weather_tool, budget_tool]
)

def build_prompt(destination: str, days: int, vibe: str, currency: str) -> str:
    return f"""
    You are an expert travel planner. Plan a detailed {days}-day {vibe} trip to {destination}.

    Follow these steps:
    1. Use the weather_tool to get the weather forecast for {destination} for {days} days
    2. Use the budget_tool to estimate the budget for {destination} for {days} days with {vibe} vibe
    3. Search for the top attractions and experiences in {destination} for a {vibe} traveler
    4. Search for the best local food and restaurants in {destination}
    5. Search for practical travel tips for {destination} (transport, safety, culture)
    6. Based on all your research, write a detailed day-by-day itinerary

    IMPORTANT: Show ALL prices and budget estimates in {currency} currency.

    Format your response as:

    ## 🌍 {days}-Day {vibe.title()} Trip to {destination}

    ### 🌤️ Weather Forecast
    (summarize the weather for each day based on the weather_tool results)

    ### 💰 Estimated Budget
    (use the budget_tool results — show daily and total cost breakdown in {currency})

    ### 📅 Day-by-Day Itinerary

    **Day 1: [Theme for the day]**
    - Morning: ...
    - Afternoon: ...
    - Evening: ...

    (continue for all {days} days)

    ### 💡 Travel Tips
    (3-5 practical tips)
    """

def run_agent(destination: str, days: int, vibe: str, currency: str = "USD") -> str:
    prompt = build_prompt(destination, days, vibe, currency)
    result = agent.invoke({
        "messages": [{"role": "user", "content": prompt}]
    })
    return result["messages"][-1].content

def stream_agent(destination: str, days: int, vibe: str, currency: str = "USD"):
    prompt = build_prompt(destination, days, vibe, currency)

    for chunk, metadata in agent.stream(
        {"messages": [{"role": "user", "content": prompt}]},
        stream_mode="messages"
    ):
        if metadata.get("langgraph_node") != "agent":
            continue
        content = chunk.content
        if not content:
            continue
        if isinstance(content, list):
            continue
        if getattr(chunk, "tool_calls", None):
            continue
        yield content
