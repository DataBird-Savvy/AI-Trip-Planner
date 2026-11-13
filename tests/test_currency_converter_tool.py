import pytest
from utils.currency_converter import CurrencyConverter
import os
from dotenv import load_dotenv
load_dotenv()
assert os.environ.get("EXCHANGE_RATE_API_KEY") is not None, "EXCHANGE_RATE_API_KEY environment variable is not set."


def test_real_currency_conversion():

    result = CurrencyConverter(
        api_key=os.environ.get("EXCHANGE_RATE_API_KEY")
    ).convert_currency(amount=100.0, from_currency="USD", to_currency="INR")
    print("API Key:", os.environ.get("EXCHANGE_RATE_API_KEY"))
   
   

    print("Converted amount:", result)