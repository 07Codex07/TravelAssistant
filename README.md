# Travel Assistant

A LangGraph-based travel assistant that pulls together city info,
weather, and photos into a Streamlit UI.

Built as part of an AI engineering assignment.

## How it works

The graph has a router that first checks a local vector store (ChromaDB)
for the queried city. If it finds a close enough match it uses that,
otherwise it falls back to a mock web search. Either way the result
feeds into a parallel fetch step that grabs weather and images at the
same time using ThreadPoolExecutor. A final LLM call (Groq/Llama3)
cleans up the raw info and returns structured JSON that the UI renders.

Used MemorySaver as a checkpointer so city context persists within a
session - if you search Tokyo then ask a follow-up without typing again
it reuses the last city.

Also implemented a manual tool-call node (manual_tool_node in nodes.py)
that parses the LLM's raw tool_calls payload and dispatches the function
manually, rather than using LangGraph's prebuilt ToolNode.

## Stack

- LangGraph for orchestration
- Groq (llama3-70b) for LLM calls
- ChromaDB + sentence-transformers for local vector search
- Streamlit for the UI

## How to run it

```bash
export GROQ_API_KEY=your_key_here
pip install -r requirements.txt
streamlit run app.py
```

graph.png is auto-generated on first run.
