from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict, Annotated
from typing import List, Optional

class MessagesState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    llm_calls: int
    should_end: Optional[bool]
