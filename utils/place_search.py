from langchain_tavily import TavilySearch
import requests
import time

from functools import lru_cache


class OpenStreetMapPlaceSearch:

    def __init__(self):
        self.nominatim_url = (
            "https://nominatim.openstreetmap.org/search"
        )

        self.overpass_url = (
            "https://overpass-api.de/api/interpreter"
        )

        self.session = requests.Session()

        # Replace with your actual contact email.
        self.session.headers.update({
            "User-Agent": "AITripPlanner/1.0 (jiyabmh@gmail.com)"
        })

        self.last_geocode_request = 0

    @lru_cache(maxsize=128)
    def _get_coordinates(self, place: str):
        """Convert city name into latitude and longitude."""

        elapsed = time.monotonic() - self.last_geocode_request

        if elapsed < 1:
            time.sleep(1 - elapsed)

        response = self.session.get(
            self.nominatim_url,
            params={
                "q": place,
                "format": "jsonv2",
                "limit": 1
            },
            timeout=20
        )

        self.last_geocode_request = time.monotonic()

        response.raise_for_status()

        results = response.json()

        if not results:
            raise ValueError(f"Location not found: {place}")

        return float(results[0]["lat"]), float(results[0]["lon"])

    def _search_places(self, place: str, filters: list) -> dict:
        """Search places using OpenStreetMap Overpass API."""

        latitude, longitude = self._get_coordinates(place)

        query_parts = []

        for key, value in filters:
            query_parts.append(
                f'nwr(around:10000,{latitude},{longitude})'
                f'["{key}"~"{value}"];'
            )

        query = (
            "[out:json][timeout:30];"
            "(" + "".join(query_parts) + ");"
            "out center tags 30;"
        )

        response = self.session.post(
            self.overpass_url,
            data={"data": query},
            timeout=60
        )

        response.raise_for_status()

        elements = response.json().get("elements", [])

        places = []

        for item in elements:
            tags = item.get("tags", {})

            # Ignore places without names.
            if not tags.get("name"):
                continue

            center = item.get("center", {})

            places.append({
                "name": tags.get("name"),
                "address": tags.get("addr:full")
                           or tags.get("addr:street"),
                "latitude": item.get("lat", center.get("lat")),
                "longitude": item.get("lon", center.get("lon")),
                "category": tags.get("tourism")
                            or tags.get("amenity")
                            or tags.get("leisure")
                            or tags.get("public_transport"),
                "website": tags.get("website"),
                "phone": tags.get("phone"),
                "osm_type": item.get("type"),
                "osm_id": item.get("id")
            })

        return {
            "location": place,
            "source": "OpenStreetMap",
            "results": places
        }

    # 1. Attractions

    def search_attractions(self, place: str) -> dict:
        return self._search_places(
            place,
            [
                ("tourism", "attraction|museum|gallery"),
                ("historic", ".*"),
                ("leisure", "park")
            ]
        )

    # 2. Restaurants

    def search_restaurants(self, place: str) -> dict:
        return self._search_places(
            place,
            [
                ("amenity", "restaurant|cafe|fast_food")
            ]
        )

    # 3. Activities

    def search_activity(self, place: str) -> dict:
        return self._search_places(
            place,
            [
                ("leisure", "sports_centre|water_park|amusement_arcade"),
                ("sport", ".*"),
                ("tourism", "theme_park|zoo")
            ]
        )

    # 4. Transportation

    def search_transportation(self, place: str) -> dict:
        return self._search_places(
            place,
            [
                ("amenity", "bus_station|taxi"),
                ("railway", "station|halt"),
                ("public_transport", "station|platform")
            ]
        )

    # 5. Hotels

    def search_hotels(self, place: str) -> dict:
        return self._search_places(
            place,
            [
                ("tourism", "hotel|hostel|motel|guest_house")
            ]
        )





class TavilyPlaceSearch:

    def __init__(self):
        self.tavily_search_tool = TavilySearch(max_results=3)

    def _search(self, query: str) -> dict:
        return self.tavily_search_tool.invoke({
            "query": query
        })

    def tavily_search_attractions(self, place: str) -> dict:
        return self._search(f"top attractions in {place}")

    def tavily_search_restaurants(self, place: str) -> dict:
        return self._search(f"best restaurants in {place}")

    def tavily_search_activity(self, place: str) -> dict:
        return self._search(f"activities to do in {place}")

    def tavily_search_transportation(self, place: str) -> dict:
        return self._search(f"transportation options in {place}")

    def tavily_search_hotels(self, place: str) -> dict:
        return self._search(f"best hotels in {place}")
