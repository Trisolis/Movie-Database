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
        # Call API request function
        url = f"{self.base_url}/search/movie"
        params = {"query": query, "api_key": self.key}
        data = self._get_data(url, params)

        if not data:
            return []

        return [
            {
            "tmdb_id": movie["id"],
            "title": movie["title"],
            "vote_average": movie.get("vote_average"),
            "vote_count": movie.get("vote_count"),
            "poster_path": movie.get("poster_path"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date")
            }
            for movie in data["results"]
        ]

    # Calls movie details endpoint and returns specific details needed for movie pages
    def get_movie_details(self, tmdb_id):
        # Call API request function
        url = f"{self.base_url}/movie/{tmdb_id}"
        params = {"api_key": self.key}
        data = self._get_data(url, params)

        if not data:
            return None

        return {
            "tmdb_id": data["id"],
            "title": data["title"],
            "vote_average": data.get("vote_average"),
            "vote_count": data.get("vote_count"),
            "poster_path": data.get("poster_path"),
            "overview": data.get("overview"),
            "release_date": data.get("release_date"),
            "runtime": data.get("runtime"),
            "tagline": data.get("tagline"),
            "original_language": data.get("original_language"),
            "revenue": data.get("revenue"),
            "genres": data.get("genres"),
            "origin_country": data.get("origin_country")
        }

    # Hits popular movies endpoint and returns a list with cursory details
    def get_popular(self):
        # Call API request function
        url = f"{self.base_url}/movie/popular"
        params = {"api_key": self.key}
        data = self._get_data(url, params)

        if not data:
            return []

        return [
            {
            "tmdb_id": movie["id"],
            "title": movie["title"],
            "vote_average": movie.get("vote_average"),
            "vote_count": movie.get("vote_count"),
            "poster_path": movie.get("poster_path"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date")
            }
            for movie in data["results"]
        ]