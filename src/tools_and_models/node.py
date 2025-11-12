from dotenv import load_dotenv
load_dotenv()

from langchain.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain.chat_models import init_chat_model
from tools import tools, tools_by_name

SYSTEM_PROMPT = "You are a helpful assistant tasked with performing arithmetic on a set of inputs."


model = init_chat_model(model="gpt-4.1-nano",model_provider="openai", max_tokens=1000,)
model_with_tools = model.bind_tools(tools)



QUIT_PHRASES = {
    "quit", "exit", "close", "stop", "bye", "goodbye",
    "ok close the chat", "close the chat", "end chat", "finish"
}

def user_wants_end(text: str) -> bool:
    t = text.strip().lower()
    return any(p in t for p in QUIT_PHRASES)


def llm_call(state: dict):
    msgs = state.get("messages", [])
    new_msgs = []

    last_is_tool = bool(msgs) and isinstance(msgs[-1], ToolMessage)
    if not last_is_tool:
        user_query = input("ask > ")
        human = HumanMessage(content=user_query)
        new_msgs.append(human)

        if user_wants_end(user_query):
            goodbye = AIMessage(content="Closing the chat. Have a great day!")
            # print immediately so the user sees it before END
            print(goodbye.content, flush=True)
            new_msgs.append(goodbye)
            return {"messages": new_msgs, "llm_calls": state.get("llm_calls", 0), "should_end": True}

    ai = model_with_tools.invoke([SystemMessage(content=SYSTEM_PROMPT)] + msgs + new_msgs)
    new_msgs.append(ai)

    # print the model’s message right away
    try:
        print(ai.content, flush=True)
    except Exception:
        pass

    return {"messages": new_msgs, "llm_calls": state.get("llm_calls", 0) + 1, "should_end": False}
  
def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}