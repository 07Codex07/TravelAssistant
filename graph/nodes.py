import json
import concurrent.futures
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from groq import Groq

from tools.vectorStore import query_vector_store
from tools.webSearch import mock_web_search
from tools.weather import get_weather_forecast
from tools.images import get_city_images


client = Groq()

# tool schema for the manual tool-call node
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "Get weather forecast for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }
]


def router_node(state):
    city = state["city"].lower()
    found, summary = query_vector_store(city)
    if found:
        return {**state, "route": "rag", "city_summary": summary}
    return {**state, "route": "web"}


def rag_lookup(state):
    return state


def search_web(state):
    # if city is not in local db, it falls back to search
    result = mock_web_search(state["city"])
    return {**state, "city_summary": result}


def fetch_extras(state):
    city = state["city"]
    with concurrent.futures.ThreadPoolExecutor() as pool:
        w = pool.submit(get_weather_forecast, city)
        imgs = pool.submit(get_city_images, city)
        weather = w.result()
        images = imgs.result()
    return {**state, "weather_forecast": weather, "image_urls": images}


def manual_tool_node(state):
    #llm decides what tool to call rather than hardcoding
    resp = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": f"Get the weather for {state['city']}"}
        ],
        tools=TOOLS,
        tool_choice="auto",
    )

    msg = resp.choices[0].message

    if msg.tool_calls:
        for call in msg.tool_calls:
            fn = call.function.name
            args = json.loads(call.function.arguments)
            if fn == "get_weather_forecast":
                result = get_weather_forecast(args["city"])
                return {**state, "weather_forecast": result}

    return {**state, "weather_forecast": get_weather_forecast(state["city"])}


def finalize_response(state):
    prompt = f"""
Turn this into cleaner travel info.

City: {state['city']}

Raw info:
{state['city_summary']}

Return JSON with:
city_summary
fun_facts
best_time_to_visit

JSON only.
"""
    # Sometimes llm response with wrong output format, to correct this, we force the llm to give the output in json format
    try:
        resp = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        llm_out = json.loads(resp.choices[0].message.content)
    except Exception:
        llm_out = {}
    return {**state, "final_output": {
        "city_summary": llm_out.get("city_summary", state["city_summary"]),
        "fun_facts": llm_out.get("fun_facts", []),
        "best_time_to_visit": llm_out.get("best_time_to_visit", ""),
        "weather_forecast": state.get("weather_forecast", []),
        "image_urls": state.get("image_urls", []),
    }}
