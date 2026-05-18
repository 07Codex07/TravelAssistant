from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from graph.state import TravelState
from graph.nodes import router_node, rag_lookup, search_web, fetch_extras, finalize_response
from graph.router import route_decision


def build_graph():
    g = StateGraph(TravelState)

    g.add_node("router", router_node)
    g.add_node("rag", rag_lookup)
    g.add_node("web_search", search_web)
    g.add_node("fetch_extras", fetch_extras)
    g.add_node("finalize", finalize_response)

    g.set_entry_point("router")

    g.add_conditional_edges(
        "router",
        route_decision,
        {"rag": "rag", "web": "web_search"}
    )

    g.add_edge("rag", "fetch_extras")
    g.add_edge("web_search", "fetch_extras")
    g.add_edge("fetch_extras", "finalize")
    g.add_edge("finalize", END)

    memory = MemorySaver()
    compiled = g.compile(checkpointer=memory)

    # save graph image for readme
    try:
        with open("graph.png", "wb") as f:
            f.write(compiled.get_graph().draw_mermaid_png())
    except Exception:
        pass
    return compiled
