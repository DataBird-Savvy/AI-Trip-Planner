
import sys

from langchain.tools import tool
from exception import AITripPlannerException

class ArithamaticOperationTool:
    def __init__(self):
        self.arithamatic_tool_list = self._setup_tools()

    def _setup_tools(self):

        @tool
        def multiply(self, a: float, b: float) -> float:
            """Multiply two numbers"""
            
            try:
                return a * b
            except Exception as e:
                raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())

        @tool
        def add(self, a: float, b: float) -> float:
            """Add two numbers"""
            try:
                return a + b
            except Exception as e:
                raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())

        return [multiply, add]

    