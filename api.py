import requests
from config import API_KEY

class API:
    def __init__(self):
        self.key = API_KEY
        self.base_url = "https://api.themoviedb.org/3"

    def _get_data(self, url, params):
        # Make API request
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            print("Could not connect to API.")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
            return None
        except requests.exceptions.Timeout:
            print("Request timed out.")
            return None

    # Hits search endpoint and returns list of movies + cursory details
    def search_movies(self, query):
        pass

    # Calls movie details endpoint and returns specific details needed for movie pages
    def get_movie_details(self, tmdb_id):
        pass

    # Hits popular movies endpoint and returns a list with cursory details
    def get_popular(self):
        # Call API request function
        url = f"{self.base_url}/data/2.5/movie/popular"
        params = {"pages": 5, "api_key": self.key}
        data = self._get_data(url, params)

        if not data:
            return []

        results = data["results"]

        return [
            {
            "tmdb_id": id,
            "title": movie["title"],
            "vote_average": movie["vote_average"],
            "vote_count": movie["vote_count"],
            "poster_path": movie["poster_path"],
            "overview": movie["overview"],
            "release_date": movie["release_date"]
            }
            for movie in data["results"]
        ]