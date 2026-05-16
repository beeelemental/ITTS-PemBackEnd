import csv
import io

def export_movies_csv(movies):
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow([
        'Title', 'Release Year', 'Rating',
        'Vote Count', 'Popularity', 'Overview'
    ])

    for movie in movies:
        release_year = (
            movie.get('release_date', '')[:4]
            if movie.get('release_date') else 'N/A'
        )
        writer.writerow([
            movie.get('title', 'N/A'),
            release_year,
            round(movie.get('vote_average', 0), 1),
            movie.get('vote_count', 0),
            round(movie.get('popularity', 0), 2),
            movie.get('overview', 'N/A')
        ])

    output.seek(0)
    return output.getvalue()


def export_reviews_csv(movie_title, reviews):
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow(['Movie', 'Author', 'Rating', 'Date', 'Review'])

    for r in reviews:
        rating = 'N/A'
        if r.get('author_details') and r['author_details'].get('rating'):
            rating = r['author_details']['rating']
        writer.writerow([
            movie_title,
            r.get('author', 'N/A'),
            rating,
            r.get('created_at', '')[:10] if r.get('created_at') else 'N/A',
            r.get('content', 'N/A')
        ])

    output.seek(0)
    return output.getvalue()