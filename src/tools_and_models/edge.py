from typing import Literal
from state import MessagesState
from langgraph.graph import END

def should_continue(state: MessagesState) -> Literal["tool_node", "llm_call", END]:
    # If user asked to end, stop immediately
    if state.get("should_end"):
        return END

    last = state["messages"][-1]

    # If the LLM made tool calls, go to tool node
    if getattr(last, "tool_calls", None):
        return "tool_node"

    # Otherwise, loop back to llm_call for the next user turn
    return "llm_call"
