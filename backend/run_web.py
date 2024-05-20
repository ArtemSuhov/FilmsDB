import binascii
import urllib

from flask import Flask, render_template, request
from db_classes import *

app = Flask(__name__)

# Route to display the main page with a paginated list of films
@app.route('/')
@app.route('/index/<int:page>')
def main_page(page=1):
    try:
        films = Film.get_page(page)
        films_count = Film.get_film_count()
        pages_count = (films_count + PAGE_SIZE - 1) // PAGE_SIZE  # Calculate the number of pages
        genres = Genre.get_all_genres()
        return render_template('index.html', films=films, len=films_count, genres=genres, p_count=pages_count, page=page)
    except Exception as e:
        return render_template('error.html', message=str(e))

# Route to display details about a specific film
@app.route('/film/<int:id>')
def film_profile(id):
    try:
        film = Film.get_by_id(id)
        actors = film.get_actors()
        studios = film.get_studios()
        genres = film.get_genres()
        countries = film.get_countries()
        return render_template('film.html', film=film, actors=actors, studios=studios, genres=genres, countries=countries)
    except Exception as e:
        return render_template('error.html', message=str(e))

# Route to display details about a specific actor
@app.route('/actor/<int:id>')
def actor_profile(id):
    try:
        actor = Actor.get_by_id(id)
        films = actor.get_films()
        countries = actor.get_countries()
        gender = Gender.get_by_id(actor.genderId)
        return render_template('actor.html', films=films, actor=actor, countries=countries, gender=gender)
    except Exception as e:
        return render_template('error.html', message=str(e))

# Route to display details about a specific studio
@app.route('/studio/<int:id>')
def studio_profile(id):
    try:
        studio = Studio.get_by_id(id)
        films = studio.get_films()
        return render_template('studio.html', films=films, studio=studio)
    except Exception as e:
        return render_template('error.html', message=str(e))

# Route to display a list of films belonging to a specific genre
@app.route('/genre/<int:id>')
def genre_page(id):
    try:
        genre = Genre.get_by_id(id)
        films = genre.get_films()
        return render_template('genre.html', films=films, genre=genre)
    except Exception as e:
        return render_template('error.html', message=str(e))

# Route to display a list of films and actors associated with a specific country
@app.route('/country/<int:id>')
def country_page(id):
    try:
        country = Country.get_by_id(id)
        films = country.get_films()
        actors = country.get_actors()
        return render_template('country.html', films=films, country=country, actors=actors)
    except Exception as e:
        return render_template('error.html', message=str(e))

@app.route('/filter')
def filter():
    all_genres = Genre.get_all_genres()
    all_countries = Country.get_all_countries()
    return render_template('filter.html', all_genres=all_genres, all_countries=all_countries, page=1)

@app.route('/filtered_films', methods=['GET'])
def filtered_films():
    all_genres = Genre.get_all_genres()
    all_countries = Country.get_all_countries()
    genres = request.args.getlist('genres')
    min_rating = float(request.args.get('min_rating', 0))
    countries = request.args.getlist('countries')

    filtered_films = Studio.filter_films(genres, min_rating, countries)


    return render_template('filter.html', filtered_films=filtered_films, all_genres=all_genres, all_countries=all_countries, page=1)

@app.route('/genre/<genre>/search/<s>')
@app.route('/search/<s>')
@app.route('/search/')
def search_page(genre="", s=""):
    films_count = Film.get_film_count()
    pages_count = films_count // 20 + 1
    all_films = []

    for i in range(pages_count):
        all_films.extend(Film.get_page(i))

    films = []

    s = (s.replace("%", "\\")
         .encode('utf-8')
         .decode('unicode-escape'))


    for film in all_films:
        genres = []
        for genre_bd in film.get_genres():
            genres.append(genre_bd.name)

        if film.name.find(s) > 0 and (genre in genres or genre == ""):
            films.append(film)

    return render_template('search.html',
                           title=s,
                           films=films)

if __name__ == '__main__':
    app.run(debug=True)
