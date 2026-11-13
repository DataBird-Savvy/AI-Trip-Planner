import os
import sys
from utils.currency_converter import CurrencyConverter
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv
from logger import logger
from exception import AITripPlannerException
load_dotenv()
class CurrencyConverterTool:
    def __init__(self):
      
        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
        self.currency_service = CurrencyConverter(self.api_key)
        self.currency_converter_tool_list = self._setup_tools()
        

    def _setup_tools(self) -> List:
        """Setup all tools for the currency converter tool"""
        @tool
        def convert_currency(amount:float, from_currency:str, to_currency:str):
            """Convert amount from one currency to another"""
            try:
                result= self.currency_service.convert_currency(amount, from_currency, to_currency)
                logger.info("Currency conversion result: {} {} to {} = {}".format(amount, from_currency, to_currency, result))
                print(f"Currency conversion result: {amount} {from_currency} to {to_currency} = {result}")
                return result
            except Exception as e:
              logger.error(f"Error in currency conversion tool: {e}")
              print(f"Error in currency conversion tool: {e}")
             

        logger.info("Converter tool setup complete with tools: convert_currency")
        return [convert_currency]