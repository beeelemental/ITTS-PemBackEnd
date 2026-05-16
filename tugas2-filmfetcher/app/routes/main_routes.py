from flask import Blueprint, render_template
from app.services.tmdb_service import TMDBService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    service = TMDBService()
    trending  = service.get_trending()[:10]
    popular   = service.get_popular()[:10]
    top_rated = service.get_top_rated()[:10]

    return render_template('index.html',
                           trending=trending,
                           popular=popular,
                           top_rated=top_rated,
                           image_base='https://image.tmdb.org/t/p/w500')

@main_bp.route('/about')
def about():
    return render_template('about.html')