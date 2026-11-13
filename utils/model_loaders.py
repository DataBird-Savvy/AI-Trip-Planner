import os
import sys
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field,ConfigDict
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from exception import AITripPlannerException

load_dotenv()  

class ConfigLoader:
    def __init__(self):
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]

    
class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True) 

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
   
    
    def load_llm(self):

        print("LLM loading...")

        try:

            if self.model_provider == "groq":
                llm = ChatGroq(
                    model=self.config["llm"]["groq"]["model_name"],
                    api_key=os.getenv("GROQ_API_KEY") 
                )

                

                return llm

            elif self.model_provider == "openai":
                secondary_llm = ChatOpenAI(
                    model=self.config["llm"]["openai"]["model_name"],
                    api_key=os.getenv("OPENAI_API_KEY")
                )

                return secondary_llm
        except Exception as e:
            raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())