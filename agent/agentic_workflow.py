from os import system
import sys

from  utils.model_loaders import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.arithamatic_op_tool import ArithamaticOperationTool
from tools.currency_converter_tool import CurrencyConverterTool
from tools.weather_info_tool import WeatherInfoTool
from tools.expense_calculator_tool import CalculatorTool
from tools.place_search_tool import PlaceSearchTool
from logger import logger
from exception import AITripPlannerException



class Graphbuilder:
    def __init__(self, model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        self.tools = []
        self.weather_tool = WeatherInfoTool()
        self.calculator_tool = CalculatorTool()
        self.arithamatic_tool = ArithamaticOperationTool()
        self.currency_converter_tool = CurrencyConverterTool()
        self.place_search_tool = PlaceSearchTool()
        self.tools.extend([*self.weather_tool.weather_tool_list, 
                           *self.calculator_tool.calculator_tool_list,
                           *self.arithamatic_tool.arithamatic_tool_list, 
                           *self.currency_converter_tool.currency_converter_tool_list, 
                           *self.place_search_tool.place_search_tool_list])   

        self.system_prompt = SYSTEM_PROMPT
        logger.info("tools loaded successfully: {}".format([tool.name for tool in self.tools]))
        self.llm_tools = self.llm.bind_tools(self.tools)


    def agent_function(self,state:MessagesState):
        """ main agent function that will be called by the graph"""
        try:
            user_question=state["messages"]
            input_question=[self.system_prompt]+user_question
            response=self.llm_tools.invoke(input_question)
            logger.info("Agent function invoked with response: {}".format(response))

            return {"messages": response}
        except Exception as e:
            logger.error(f"Error occurred in agent function: {e}")
            raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())  

    def build_graph(self):
        """Build the graph for the agent"""
        try:
            graph_builder = StateGraph(MessagesState)
        

            graph_builder.add_node("agent", self.agent_function)
            graph_builder.add_node("tools", ToolNode(tools=self.tools))

            graph_builder.add_edge(START, 'agent')
            graph_builder.add_conditional_edges('agent', tools_condition)
            graph_builder.add_edge('tools', 'agent')
           
            self.graph=graph_builder.compile()
            return self.graph
        except Exception as e:
            logger.error(f"Error occurred while building the graph: {e}")
            raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())

    def __call__(self):
        return self.build_graph()
        