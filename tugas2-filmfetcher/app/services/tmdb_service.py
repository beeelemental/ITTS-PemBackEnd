import requests
from flask import current_app

class TMDBService:

    def __init__(self):
        self.api_key = current_app.config['TMDB_API_KEY']
        self.base_url = current_app.config['TMDB_BASE_URL']

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def get_trending(self):
        data = self._get('/trending/movie/day')
        return data.get('results', []) if data else []

    def get_popular(self):
        data = self._get('/movie/popular')
        return data.get('results', []) if data else []

    def get_top_rated(self):
        data = self._get('/movie/top_rated')
        return data.get('results', []) if data else []

    def get_genres(self):
        data = self._get('/genre/movie/list')
        return data.get('genres', []) if data else []

    def search_actor(self, query):
        data = self._get('/search/person', {
            'query': query,
            'include_adult': False
        })
        results = data.get('results', []) if data else []
        return [
            {
                'id': r['id'],
                'name': r['name'],
                'photo': f"https://image.tmdb.org/t/p/w185{r['profile_path']}"
                         if r.get('profile_path') else None
            }
            for r in results[:8]
        ]

    def discover_movies(self, params=None):
        if params is None:
            params = {}
        data = self._get('/discover/movie', params)
        return data if data else {
            'results': [],
            'total_results': 0,
            'total_pages': 0
        }

    def get_movie_detail(self, movie_id):
        return self._get(f'/movie/{movie_id}')

    def get_movie_reviews(self, movie_id):
        data = self._get(f'/movie/{movie_id}/reviews')
        return data.get('results', []) if data else []