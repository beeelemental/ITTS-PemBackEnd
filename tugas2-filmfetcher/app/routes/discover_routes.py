from flask import Blueprint, render_template, request, jsonify, Response
from app.services.tmdb_service import TMDBService
from app.services.export_service import export_movies_csv

discover_bp = Blueprint('discover', __name__)

@discover_bp.route('/discover')
def discover():
    service    = TMDBService()
    genres     = service.get_genres()

    genre_ids    = request.args.getlist('genres')
    actor_id     = request.args.get('actor_id', '')
    actor_name   = request.args.get('actor_name', '')
    release_from = request.args.get('release_from', '')
    release_to   = request.args.get('release_to', '')
    rating_min   = request.args.get('rating_min', '')
    sort_by      = request.args.get('sort_by', 'popularity.desc')
    is_search    = request.args.get('search', '')

    movies = []
    total  = 0

    if is_search:
        params = {'sort_by': sort_by}
        if genre_ids:
            params['with_genres'] = ','.join(genre_ids)
        if actor_id:
            params['with_cast'] = actor_id
        if release_from:
            params['primary_release_date.gte'] = f"{release_from}-01-01"
        if release_to:
            params['primary_release_date.lte'] = f"{release_to}-12-31"
        if rating_min and float(rating_min) > 0:
            params['vote_average.gte'] = rating_min

        result = service.discover_movies(params)
        movies = result.get('results', [])
        total  = result.get('total_results', 0)

    return render_template('discover.html',
                           genres=genres,
                           movies=movies,
                           total=total,
                           image_base='https://image.tmdb.org/t/p/w500',
                           selected_genres=genre_ids,
                           actor_id=actor_id,
                           actor_name=actor_name,
                           release_from=release_from,
                           release_to=release_to,
                           rating_min=rating_min,
                           sort_by=sort_by,
                           query_string=request.query_string.decode('utf-8'))

@discover_bp.route('/api/search-actor')
def search_actor():
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    service = TMDBService()
    return jsonify(service.search_actor(query))

@discover_bp.route('/export')
def export_csv():
    service      = TMDBService()
    genre_ids    = request.args.getlist('genres')
    actor_id     = request.args.get('actor_id', '')
    release_from = request.args.get('release_from', '')
    release_to   = request.args.get('release_to', '')
    rating_min   = request.args.get('rating_min', '')
    sort_by      = request.args.get('sort_by', 'popularity.desc')

    params = {'sort_by': sort_by}
    if genre_ids:
        params['with_genres'] = ','.join(genre_ids)
    if actor_id:
        params['with_cast'] = actor_id
    if release_from:
        params['primary_release_date.gte'] = f"{release_from}-01-01"
    if release_to:
        params['primary_release_date.lte'] = f"{release_to}-12-31"
    if rating_min and float(rating_min) > 0:
        params['vote_average.gte'] = rating_min

    result   = service.discover_movies(params)
    movies   = result.get('results', [])
    csv_data = export_movies_csv(movies)

    return Response(
        csv_data,
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=filmfetcher_results.csv'
        }
    )