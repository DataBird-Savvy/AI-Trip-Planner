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
        def convert_amount(amount:float, from_currency:str, to_currency:str):
            """Convert amount from one currency to another

            Args:
                amount (float): The amount to convert
                from_currency (str): The currency code to convert from
                to_currency (str): The currency code to convert to  
            Returns:
                float: The converted amount
            """
            
            try:
                result= self.currency_service.convert_currency(amount, from_currency, to_currency)
                logger.info("Currency conversion result: {} {} to {} = {}".format(amount, from_currency, to_currency, result))
                print(f"Currency conversion result: {amount} {from_currency} to {to_currency} = {result}")
                return result
            except Exception as e:
              logger.error(f"Error in currency conversion tool: {e}")
              print(f"Error in currency conversion tool: {e}")
             

        logger.info("Converter tool setup complete with tools: convert_amount")
        return [convert_amount]


if __name__ == "__main__":
    # Example usage of the CurrencyConverterTool
    converter_tool = CurrencyConverterTool()
    amount = 100.0
    from_currency = "USD"
    to_currency = "INR"
    result = converter_tool.currency_converter_tool_list[0].invoke({"amount": amount, "from_currency": from_currency, "to_currency": to_currency})
    print(f"Converted amount: {result}")
    for t in converter_tool.currency_converter_tool_list:
        print(f"Tool name: {t.name}, description: {t.description}, args schema: {t.args_schema.model_json_schema()}")