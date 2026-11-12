
import pytest
from unittest.mock import patch
from tools.place_search_tool import PlaceSearchTool


# Fixture: Create PlaceSearchTool with mocked external services
@pytest.fixture
def place_tool():

    with patch("tools.place_search_tool.OpenStreetMapPlaceSearch"), \
         patch("tools.place_search_tool.TavilyPlaceSearch"):

        tool = PlaceSearchTool()

        return tool


# 1. Test whether all tools are registered
def test_tools_registered(place_tool):

    assert len(place_tool.place_search_tool_list) == 4

    tool_names = [
        t.name for t in place_tool.place_search_tool_list
    ]

    print("\nRegistered tools:", tool_names)

    assert "search_attractions" in tool_names
    assert "search_restaurants" in tool_names
    assert "search_activities" in tool_names
    assert "search_transportation" in tool_names


# 2. Test attraction search using OSM
def test_search_attractions_success(place_tool):

    place_tool.osm_search.search_attractions.return_value = (
        "Eiffel Tower, Louvre Museum"
    )

    search_tool = place_tool.place_search_tool_list[0]

    result = search_tool.invoke({"place": "Paris"})

    print("\nAttraction Search Result:", result)

    assert "Eiffel Tower" in result
    assert "Louvre Museum" in result

    place_tool.osm_search.search_attractions.assert_called_once_with(
        "Paris"
    )

    place_tool.tavily_search.tavily_search_attractions.assert_not_called()


# 3. Test attraction fallback using Tavily
def test_search_attractions_fallback(place_tool):

    place_tool.osm_search.search_attractions.side_effect = Exception(
        "OSM API error"
    )

    place_tool.tavily_search.tavily_search_attractions.return_value = (
        "Eiffel Tower, Louvre Museum"
    )

    search_tool = place_tool.place_search_tool_list[0]

    result = search_tool.invoke({"place": "Paris"})

    print("\nAttraction Fallback Result:", result)

    assert "Eiffel Tower" in result

    place_tool.osm_search.search_attractions.assert_called_once_with(
        "Paris"
    )

    place_tool.tavily_search.tavily_search_attractions.assert_called_once_with(
        "Paris"
    )


# 4. Test restaurant fallback using Tavily
def test_search_restaurants_fallback(place_tool):

    place_tool.osm_search.search_restaurants.side_effect = Exception(
        "OSM API error"
    )

    place_tool.tavily_search.tavily_search_restaurants.return_value = (
        "Restaurant A, Restaurant B"
    )

    search_tool = place_tool.place_search_tool_list[1]

    result = search_tool.invoke({"place": "Paris"})

    print("\nRestaurant Fallback Result:", result)

    assert "Restaurant A" in result
    assert "Restaurant B" in result

    place_tool.osm_search.search_restaurants.assert_called_once_with(
        "Paris"
    )

    place_tool.tavily_search.tavily_search_restaurants.assert_called_once_with(
        "Paris"
    )


# 5. Test activities fallback using Tavily
def test_search_activities_fallback(place_tool):

    place_tool.osm_search.search_activities.side_effect = Exception(
        "OSM API error"
    )

    place_tool.tavily_search.tavily_search_activity.return_value = (
        "Walking tour, Boat tour"
    )

    search_tool = place_tool.place_search_tool_list[2]

    result = search_tool.invoke({"place": "Paris"})

    print("\nActivities Fallback Result:", result)

    assert "Walking tour" in result
    assert "Boat tour" in result

    place_tool.osm_search.search_activities.assert_called_once_with(
        "Paris"
    )

    place_tool.tavily_search.tavily_search_activity.assert_called_once_with(
        "Paris"
    )


# 6. Test transportation fallback using Tavily
def test_search_transportation_fallback(place_tool):

    place_tool.osm_search.search_transportation.side_effect = Exception(
        "OSM API error"
    )

    place_tool.tavily_search.tavily_search_transportation.return_value = (
        "Bus, Metro, Train"
    )

    search_tool = place_tool.place_search_tool_list[3]

    result = search_tool.invoke({"place": "Paris"})

    print("\nTransportation Fallback Result:", result)

    assert "Bus" in result
    assert "Metro" in result

    place_tool.osm_search.search_transportation.assert_called_once_with(
        "Paris"
    )

    place_tool.tavily_search.tavily_search_transportation.assert_called_once_with(
        "Paris"
    )
