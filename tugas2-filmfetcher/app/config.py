import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'filmfetcher-dev-key')
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_W500 = 'https://image.tmdb.org/t/p/w500'
    TMDB_IMAGE_W185 = 'https://image.tmdb.org/t/p/w185'
    TMDB_IMAGE_ORIGINAL = 'https://image.tmdb.org/t/p/original'