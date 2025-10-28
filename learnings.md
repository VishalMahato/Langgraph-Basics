### 📌 Virtual Environment Path Dependency

**Date:** 2025-10-28  
**Topic / Area:** Python Virtual Environments

**What I learned:**  
A `.venv` stores absolute paths to the folder where it was created. If I rename or move the project folder, the virtual environment still looks for the old path and breaks when running Python or `pip`.

**Common Error Example:**
Fatal error in launcher: Unable to create process using ...

**How to fix:**
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt


**Takeaway:**  
Renaming or moving the project folder after creating a venv usually means recreating the venv.


### 🧩 LangGraph Basics: StateGraph, Nodes, Edges, Start/End, Compile & Invoke

**StateGraph:**  
The structure that defines how information (state) flows between different steps (nodes) in the graph. Think of it as the blueprint of your chatbot workflow.

**Nodes:**  
Each node is a function or component that takes the current state and returns updated state. Nodes are like action points (e.g., call an LLM, search a tool, update memory).

**Edges:**  
Edges define the order of execution. They connect nodes and tell the graph:  
“After finishing this node, go to that node.”

**START and END:**  
Special markers that define the flow entry and exit points.
- `START` is where the graph begins executing.
- `END` is where the graph finishes.

**graph.compile():**  
Takes the blueprint (StateGraph with nodes and edges) and builds a runnable graph.  
Without compiling, the graph has structure but can’t execute.

**graph.invoke():**  
Runs the compiled graph with an initial state.  
You provide input (like user messages), and the graph processes through all connected nodes until it reaches END.
