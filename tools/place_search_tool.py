import os
from utils.place_search import OpenStreetMapPlaceSearch, TavilyPlaceSearch
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv
from logger import logger
from exception import AITripPlannerException
class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.osm_search = OpenStreetMapPlaceSearch()
        self.tavily_search = TavilyPlaceSearch()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool
        Args:
            place (str): The place to search for
        Returns:
            List: A list of tools for place search
        """
        @tool
        def search_attractions(place:str) -> str:
            """Search attractions of a place
            Args:
                place (str): The place to search for
            Returns:
                str: A string containing the attractions of the place
            """
            try:
                attraction_result = self.osm_search.search_attractions(place)
                if attraction_result:
                    logger.info("attraction_result: {}".format(attraction_result))
                    print(f"attraction_result: {attraction_result}")
                    return f"Following are the attractions of {place} as suggested by OpenStreetMap: {attraction_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_attractions(place)
                logger.info("tavily_result: {}".format(tavily_result))
                print(f"tavily_result: {tavily_result}")
                return f"OpenStreetMap cannot find the details due to {e}. \nFollowing are the attractions of {place} by Tavily: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        @tool
        def search_restaurants(place:str) -> str:
            """Search restaurants of a place

            Args:
                place (str): The place to search for

            Returns:
                str: A string containing the restaurants of the place
            """
            try:
                restaurants_result = self.osm_search.search_restaurants(place)
                if restaurants_result:
                    logger.info("restaurants_result: {}".format(restaurants_result))
                    print(f"restaurants_result: {restaurants_result}")
                    return f"Following are the restaurants of {place} as suggested by OpenStreetMap: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_restaurants(place)
                logger.info("tavily_result: {}".format(tavily_result))
                print(f"tavily_result: {tavily_result}")
                return f"OpenStreetMap cannot find the details due to {e}. \nFollowing are the restaurants of {place} by Tavily: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        @tool
        def search_activities(place:str) -> str:
            """Search activities of a place

            Args:
                place (str): The place to search for

            Returns:
                str: A string containing the activities of the place
            """
            try:
                activities_result = self.osm_search.search_activities(place)
                if activities_result:
                    logger.info("activities_result: {}".format(activities_result))
                    print(f"activities_result: {activities_result}")
                    return f"Following are the activities in and around {place} as suggested by OpenStreetMap: {activities_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_activity(place)
                logger.info("tavily_result: {}".format(tavily_result))
                print(f"tavily_result: {tavily_result}")
                return f"OpenStreetMap cannot find the details due to {e}. \nFollowing are the activities of {place} by Tavily: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        @tool
        def search_transportation(place:str) -> str:
            """Search transportation of a place

            Args:
                place (str): The place to search for

            Returns:
                str: A string containing the transportation options of the place
            """
            try:
                transportation_result = self.osm_search.search_transportation(place)
                if transportation_result:
                    logger.info("transportation_result: {}".format(transportation_result))
                    print(f"transportation_result: {transportation_result}")
                    return f"Following are the modes of transportation available in {place} as suggested by OpenStreetMap: {transportation_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
                logger.info("tavily_result: {}".format(tavily_result))
                print(f"tavily_result: {tavily_result}")
                return f"OpenStreetMap cannot find the details due to {e}. \nFollowing are the modes of transportation available in {place} by Tavily: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        return [search_attractions, search_restaurants, search_activities, search_transportation]