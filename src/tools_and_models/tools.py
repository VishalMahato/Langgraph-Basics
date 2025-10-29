from langchain.tools import tool

# Define tools 
@tool
def multiply(a: int, b: int)-> int:
    """Multiply 'a' and 'b'."""
    
    return a * b 



@tool
def divide(a: int, b: int) -> str:
    """Divide 'a' by 'b'. Returns a string with either result or an error message."""
    
    if b == 0:
        return "Error: Cannot divide by zero. Please provide a non-zero divisor."
    return str(a / b)



@tool
def add(a: int, b: int)-> int:
    """add 'a' and 'b'."""
    
    return a + b 


# now add the tools to the llm
tools= [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}




     