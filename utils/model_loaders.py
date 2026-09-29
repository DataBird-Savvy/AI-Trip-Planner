import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

class ConfigLoader:
    def __init__(self):
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]

    
class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        print("LLM loading...")

        groq_llm = ChatGroq(
            model=self.config["llm"]["groq"]["model_name"],
            api_key=os.getenv("GROQ_API_KEY")
        ).with_retry(stop_after_attempt=3)

        openai_llm = ChatOpenAI(
            model=self.config["llm"]["openai"]["model_name"],
            api_key=os.getenv("OPENAI_API_KEY")
        ).with_retry(stop_after_attempt=3)

        if self.model_provider == "groq":
            return groq_llm.with_fallbacks([openai_llm])

        elif self.model_provider == "openai":
            return openai_llm.with_fallbacks([groq_llm])