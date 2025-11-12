from dotenv import load_dotenv
load_dotenv()

# ✅ use modern message classes
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain.chat_models import init_chat_model
from tools import tools, tools_by_name

SYSTEM_PROMPT = """You are a helpful assistant that performs arithmetic.
Rules:
1) Apply normal operator precedence.
2) If you need a tool, call AT MOST ONE tool per assistant turn.
3) After you receive the tool result, you may decide the next step."""

model = init_chat_model(model="gpt-4.1-nano", model_provider="openai", max_tokens=1000,  parallel_tool_calls=False, )
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

   
    if msgs and isinstance(msgs[-1], AIMessage) and getattr(msgs[-1], "tool_calls", None):
        return {"messages": [], "llm_calls": state.get("llm_calls", 0), "should_end": False}

    # collect user input only if the last message wasn't a tool result
    last_is_tool = bool(msgs) and isinstance(msgs[-1], ToolMessage)
    if not last_is_tool:
        user_query = input("ask > ")
        human = HumanMessage(content=user_query)
        new_msgs.append(human)

        if user_wants_end(user_query):
            goodbye = AIMessage(content="Closing the chat. Have a great day!")
            print(goodbye.content, flush=True)
            new_msgs.append(goodbye)
            return {"messages": new_msgs, "llm_calls": state.get("llm_calls", 0), "should_end": True}

    # Only prepend the system message on the first LLM turn
    prompt = ([SystemMessage(content=SYSTEM_PROMPT)] if not msgs else []) + msgs + new_msgs

    ai = model_with_tools.invoke(prompt)
    new_msgs.append(ai)

    try:
        print(ai.content, flush=True)
    except Exception:
        pass

    return {"messages": new_msgs, "llm_calls": state.get("llm_calls", 0) + 1, "should_end": False}

def tool_node(state: dict):
    """Respond to ALL tool calls in the last assistant message (API requirement)."""
    ai_msg = state["messages"][-1]
    tool_calls = getattr(ai_msg, "tool_calls", None)
    if not tool_calls:
        return {"messages": []}

    tool_msgs = []
    for tc in tool_calls:
        tool = tools_by_name[tc["name"]]
        observation = tool.invoke(tc["args"])
        tool_msgs.append(
            ToolMessage(
                content=str(observation),     
                tool_call_id=tc["id"],        
                name=tc["name"],              
            )
        )
    return {"messages": tool_msgs}
