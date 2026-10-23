from collections import defaultdict
import json
import os
from typing import Optional, Any, dict,List
from langchain.tools import tools

import requests
import json

class WeatherForecastTool:
    def __init__(self):
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geourl="https://api.openweathermap.org/geo/1.0/direct"

    def get_current_weather(self, place:str):
        """Get current weather using coordinates."""
        try:
            geo_url=f"{self.geourl}"

            geo_params = {
                "q": place,
                "appid": self.api_key}
            
            geo_response = requests.get(geo_url, params=geo_params, timeout=10)
            geo_response.raise_for_status()
            geo_data = geo_response.json()[0]  # Get the first result
            base_url = f"{self.base_url}/weather"
        
        
            params = {
                "lat": geo_data["lat"],
                "lon": geo_data["lon"],
                "appid": self.api_key,
                "units": "metric",
            }

            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status() 

            return response.json() if response.status_code == 200 else {}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")

    def get_forecast_weather(self, place:str, days:int):
        """Get weather forecast of a place"""
        cnt=days*8  # OpenWeatherMap provides data in 3-hour intervals, so 8 intervals per day
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": place,
                "appid": self.api_key,
                "cnt": cnt,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            raise e

    def format_forecast_data(forecast_data):
        """Format the forecast data into a more readable structure."""
        daily = defaultdict(list)
        
        for forecast in forecast_data.get("list", []):
            date = forecast.get('dt_txt', 'N/A').split(' ')[0]  # Get only the date part
            daily[date].append(forecast)

        result = {
            "forecast": []
        }
        for date, forecasts in daily.items():
            temps = [f.get('main', {}).get('temp', 'N/A') for f in forecasts]
            descriptions = [f.get('weather', [{}])[0].get('description', 'N/A') for f in forecasts]
            description=max(set(descriptions), key=descriptions.count)  # Most common description

            result["forecast"].append({
                "date": date,
                "min_temp": f'{min(temps) if temps else None}°C',
                "max_temp": f'{max(temps) if temps else None}°C',
                "description": description
            })
        return json.dumps(result, indent=2, ensure_ascii=False)