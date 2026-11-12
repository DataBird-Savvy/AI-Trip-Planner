import pytest
import os
from dotenv import load_dotenv
from tools.weather_info_tool import WeatherInfoTool

load_dotenv()


@pytest.fixture
def weather_tool():

    if not os.getenv("OPENWEATHERMAP_API_KEY"):
        pytest.skip("OpenWeatherMap API key not found")

    return WeatherInfoTool()


def test_real_current_weather(weather_tool):

    search_tool = weather_tool.weather_tool_list[0]

    result = search_tool.invoke({
        "city": "Kozhikode"
    })

    print("\nReal API Response:", result)

    assert result is not None
    assert "Kozhikode" in result


def test_real_weather_forecast(weather_tool):

    search_tool = weather_tool.weather_tool_list[1]

    result = search_tool.invoke({
        "location": "Kozhikode",
        "days": 5
    })

    print("\nReal Forecast Response:", result)

    assert result is not None
    assert len(result) > 0