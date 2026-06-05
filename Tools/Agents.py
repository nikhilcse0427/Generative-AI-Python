from dotenv import load_dotenv
load_dotenv()

import os
import requests
from rich import print

from tavily import TavilyClient

from langchain.tools import tool
from langchain_mistralai import ChatMistralAI

from langchain_core.messages import (
    HumanMessage,
    ToolMessage
)

# ==================================================
# API KEYS
# ==================================================

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

# ==================================================
# TAVILY CLIENT
# ==================================================

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ==================================================
# WEATHER TOOL
# ==================================================

@tool
def get_weather(city: str) -> str:
    """
    Get current weather of a city.
    """

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={OPEN_WEATHER_API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return f"Weather Error: {data.get('message')}"

    return f"""
City: {data['name']}
Country: {data['sys']['country']}
Temperature: {data['main']['temp']}°C
Feels Like: {data['main']['feels_like']}°C
Humidity: {data['main']['humidity']}%
Condition: {data['weather'][0]['description']}
"""

# ==================================================
# NEWS TOOL
# ==================================================

@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""

    response = tavily_client.search(
        query=f"latest breaking news in {city}",
        search_depth="advanced",
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_text = ""

    for i, item in enumerate(results, 1):

        news_text += f"""
News {i}
Title: {item.get('title')}
URL: {item.get('url')}
Summary: {item.get('content', 'No summary')}

"""

    return news_text
# ==================================================
# MODEL
# ==================================================

llm = ChatMistralAI(
    model="mistral-small-2506"
)

# Bind tools
llm_with_tools = llm.bind_tools(
    [get_weather, get_news]
)

# Tool lookup dictionary
tools = {
    "get_weather": get_weather,
    "get_news": get_news
}

# ==================================================
# CHAT LOOP
# ==================================================

messages = []

print("[bold green]AI Agent Started[/bold green]")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append(
        HumanMessage(content=user_input)
    )

    while True:

        result = llm_with_tools.invoke(messages)

        messages.append(result)

        # No tool needed
        if not result.tool_calls:

            print("\n[bold cyan]AI:[/bold cyan]")
            print(result.content)
            print()

            break

        # Execute tool calls
        for tool_call in result.tool_calls:

            tool_name = tool_call["name"]

            print(
                f"\n[yellow]Tool Requested:[/yellow] {tool_name}"
            )

            approval = input(
                "Approve tool execution? (yes/no): "
            )

            if approval.lower() != "yes":

                messages.append(
                    ToolMessage(
                        content="Tool execution denied by user.",
                        tool_call_id=tool_call["id"]
                    )
                )

                continue

            selected_tool = tools[tool_name]

            tool_result = selected_tool.invoke(
                tool_call["args"]
            )

            print(
                "\n[green]Tool Executed Successfully[/green]"
            )

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )