
import os
import requests
from dotenv import load_dotenv

load_dotenv()

import os
import requests

class CurrencyConverter:

    def __init__(self):
        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
        self.base_url = "https://api.exchangerate.host/convert"

    def convert_currency(
        self,
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> float:

        params = {
            "access_key": self.api_key,
            "from": from_currency,
            "to": to_currency,
            "amount": amount
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get("success"):
            result = data["result"]

            print(
                f"{amount} {from_currency} = "
                f"{result:.2f} {to_currency}"
            )

            print(f"Rate used: {data['info']['quote']}")

            
            return result
        else:
            print(f"Error: {data.get('error', {}).get('info', 'Conversion failed')}")

        