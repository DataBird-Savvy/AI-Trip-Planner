
from langchain.tools import tool

class ArithamaticOperationTool:
    def __init__(self):
        pass

    @tool
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers"""
        return a * b

    @tool
    def add(self, a: float, b: float) -> float:
        """Add two numbers"""
        return a + b

  
    