import streamlit as st
import pandas as pd

from graph.builder import build_graph
from tools.vectorStore import populate_vector_store


populate_vector_store()
graph = build_graph()

st.set_page_config(page_title="Travel Assistant", layout="wide")
st.title(" Travel Assistant")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "session-1"

if "last_city" not in st.session_state:
    st.session_state.last_city = None

city_input = st.text_input("Enter a city:", placeholder="Tokyo, Paris, Kyoto...")

# reuse last city if input is empty (for follow-up queries)
resolved = city_input.strip() or st.session_state.last_city

if st.button("Go") and resolved:
    with st.spinner(f"Looking up {resolved}..."):
        config = {"configurable": {"thread_id": st.session_state.thread_id}}

        state = {
            "user_query": city_input,
            "city": resolved,
            "route": None,
            "city_summary": None,
            "weather_forecast": None,
            "image_urls": None,
            "messages": [],
            "final_output": None,
        }

        try:
            result = graph.invoke(state, config=config)
            st.session_state.last_city = resolved

            output = result.get("final_output", {})

            col1, col2 = st.columns([1.5, 1])

            with col1:
                st.subheader(resolved.title())
                st.write(output.get("city_summary", "couldn't load summary"))

                facts = output.get("fun_facts", [])
                if facts:
                    st.subheader("Fun Facts")
                    for f in facts:
                        st.markdown(f"• {f}")

                bttv = output.get("best_time_to_visit", "")
                if bttv:
                    st.info(f"Best time to visit: {bttv}")

            with col2:
                st.subheader("Forecast")
                forecast = output.get("weather_forecast", [])
                if forecast:
                    df = pd.DataFrame(forecast).set_index("day")[["high", "low"]]
                    st.line_chart(df)
                else:
                    st.write("no forecast data")

            imgs = output.get("image_urls", [])
            if imgs:
                st.subheader("Photos")
                cols = st.columns(min(3, len(imgs)))
                for i, url in enumerate(imgs[:3]):
                    with cols[i]:
                        st.image(url, use_container_width=True)

            st.sidebar.write(f"route: **{result.get('route', '?')}**")
            if st.session_state.last_city:
                st.sidebar.write(f"last city: {st.session_state.last_city}")
        except Exception as e:
            st.error(f"something went wrong: {e}")
