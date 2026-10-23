from os import system

from  utils.model_loaders import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.arithamatic_op_tool import ArithamaticOpTool
from tools.currency_converter_tool import CurrencyConverterTool
from tools.weather_info_tool import WeatherInfoTool
from tools.expense_calculator_tool import CalculatorTool
from tools.place_seach_tool import PlaceSearchTool




class Graphbuilder:
    def __init__(self, model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        self.tools = []
        self.weather_tool = WeatherInfoTool()
        self.calculator_tool = CalculatorTool()
        self.arithamatic_tool = ArithamaticOpTool()
        self.currency_converter_tool = CurrencyConverterTool()
        self.place_search_tool = PlaceSearchTool()
        self.tools.extend([self.weather_tool, 
                           self.calculator_tool,
                           self.arithamatic_tool, 
                           self.currency_converter_tool, 
                           self.place_search_tool])   

        self.system_prompt = SYSTEM_PROMPT
        self.llm_tools=self.llm.with_tools(self.tools)


    def agent_function(self,state:MessagesState):
        """ main agent function that will be called by the graph"""
        user_question=state["messages"]
        input_question=[self.system_prompt]+user_question
        response=self.llm_tools.invoke(input_question)

        return {"messages": response}

    def build_graph(self):
        graph_builder=StateGraph(messages_state=MessagesState())
       

        graph_builder.add_node(self.agent_function, name="agent")
        graph_builder.add_edge(START, 'agent')
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge( 'tools',"agent", condition=tools_condition)
        graph_builder.add_node(END)
        self.graph=graph_builder.compile()

    def __call__(self, input_text):
        return self.build_graph()
        