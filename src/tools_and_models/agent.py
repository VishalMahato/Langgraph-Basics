
from langgraph.graph import StateGraph, START, END
from langchain.messages import HumanMessage
from state import MessagesState
from node import llm_call, tool_node
from edge import should_continue
from IPython.display import Image, display



# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
# graph wiring
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", "llm_call", END]  
)
agent_builder.add_edge("tool_node", "llm_call")



# Compile the agent
agent = agent_builder.compile()

# Show the agent

png = agent.get_graph(xray=True).draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png)

print("✅ Saved graph.png — open it from VS Code Explorer")
# Invoke
# user_query=  input("> ")
messages = agent.invoke({"messages": [], "llm_calls": 0, "should_end": False})
for m in messages["messages"]:
    m.pretty_print()