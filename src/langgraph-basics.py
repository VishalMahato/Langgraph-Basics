from langgraph.graph import StateGraph, MessagesState, START, END


def mock_llm(state: MessagesState):
    print({"messages": [{"role": "ai", "content": "hello world"}]})
    return {"messages": [{"role": "ai", "content": "hello world"}]}

# cadding initial state to the graph
graph = StateGraph(MessagesState)

# adding a node to the graph
graph.add_node(mock_llm)

#deciding its flow 
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)

#compiling it  
graph = graph.compile()

# creating a state 
message_state = {"messages": [{"role": "user", "content": "hi!"}]}

# running/Invoking a graph
graph.invoke(message_state)

