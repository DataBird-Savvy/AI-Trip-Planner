import sys

from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import Graphbuilder
import os
from logger import logger
from exception import AITripPlannerException



app=FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_travel_request(query: QueryRequest):
    try:
        logger.info(f"Received query: {query.query}")
        print(f"Received query: {query}")
        graph=Graphbuilder(model_provider="groq")
        react_app=graph()

        # png_graph = react_app.get_graph().draw_mermaid_png()
        # with open("my_graph.png", "wb") as f:
        #     f.write(png_graph)

        # print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
       
        messages = {
            "messages": [
                {"role": "user", "content": query.query}
            ]
        }


        output = react_app.invoke(messages)
        logger.info(f"Output from graph: {output}")
                
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output}



    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())


def main():
    print("Hello from ai-trip-planner!")


if __name__ == "__main__":
    main()
