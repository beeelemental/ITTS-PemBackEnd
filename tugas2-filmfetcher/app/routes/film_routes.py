from flask import Blueprint, render_template, abort, Response
from app.services.tmdb_service import TMDBService
from app.services.export_service import export_reviews_csv

film_bp = Blueprint('film', __name__)

@film_bp.route('/film/<int:movie_id>')
def film_detail(movie_id):
    service = TMDBService()
    movie   = service.get_movie_detail(movie_id)

    if not movie:
        abort(404)

    reviews = service.get_movie_reviews(movie_id)

    return render_template('reviews.html',
                           movie=movie,
                           reviews=reviews,
                           image_base='https://image.tmdb.org/t/p/w500',
                           image_original='https://image.tmdb.org/t/p/original')

@film_bp.route('/film/<int:movie_id>/export-reviews')
def export_reviews(movie_id):
    service = TMDBService()
    movie   = service.get_movie_detail(movie_id)
    reviews = service.get_movie_reviews(movie_id)

    title    = movie.get('title', f'movie_{movie_id}') if movie else f'movie_{movie_id}'
    csv_data = export_reviews_csv(title, reviews)

    return Response(
        csv_data,
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=reviews_{movie_id}.csv'
        }
    )