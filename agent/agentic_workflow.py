from os import system

from  utils.model_loaders import load_model
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition


class Graphbuilder:
    def __init__(self):
        self.tools = {
            # "weather": WeatherTool(),
            # "flight": FlightTool(),
            # "hotel": HotelTool(),
            # "restaurant": RestaurantTool(),
        }
        self.system_prompt = SYSTEM_PROMPT


    def agent_function(self,state:MessagesState):
        """ main agent function that will be called by the graph"""
        user_question=state["messages"]
        input_question=[self.system_prompt]+user_question
        response=self.llm_with_tools.invoke(input_question)

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
        