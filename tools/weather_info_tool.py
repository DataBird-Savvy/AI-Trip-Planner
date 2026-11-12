import os
import sys
from typing import Optional, Any, Dict,List

from langchain.tools import tool
from dotenv import load_dotenv
from utils.weather_info import WeatherForecastTool
import json
from logger import logger
from exception import AITripPlannerException
class WeatherInfoTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()       

    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast tool"""
        @tool
        def get_current_weather(city: str) -> str:
            """Get current weather for a city"""
            try:
                weather_data = self.weather_service.get_current_weather(city)
                if weather_data:
                    temp = weather_data.get('main', {}).get('temp', 'N/A')
                    desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                    logger.info(f"Current weather in {city}: {temp}°C, {desc}")
                    return f"Current weather in {city}: {temp}°C, {desc}"
                return f"Could not fetch weather for {city}"
            except Exception as e:
                logger.error(f"Error occurred while fetching weather for {city}: {e}")
                raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())
            


        @tool
        def get_weather_forecast(location: str, days: int) -> str:
            """
            Get the weather forecast for a given location and number of days.
            Args:
                location (str): The location for which to get the weather forecast.
                days (int): The number of days for which to get the forecast.
            Returns:


                str: The weather forecast for the given location and number of days.

            """
            try:
                forecast_data = self.weather_service.get_forecast_weather(location, days)
                logger.info(f"Weather forecast data for {location} for the next {days} days: {forecast_data}")
                formated_forecast = self.weather_service.format_forecast_data(forecast_data)
                formated_forecast = json.loads(formated_forecast) if formated_forecast else {}
                logger.info(f"Formatted forecast data for {location} for the next {days} days: {formated_forecast}")
                if formated_forecast:
                    forecast_str = "Weather forecast in London for the next 5 days:\n"

                    for data in formated_forecast["data"]:
                        date = data["date"]
                        min_temp = data["min_temp"]
                        max_temp = data["max_temp"]
                        desc = data["description"]

                        forecast_str += (
                            f"{date}: Min {min_temp}, Max {max_temp}, "
                            f"{desc}\n"
                        )
                        

                logger.info(f"Weather forecast for {location} for the next {days} days: {forecast_str}")
                return forecast_str
            except Exception as e:
                raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())
                

        return [get_current_weather, get_weather_forecast]
            