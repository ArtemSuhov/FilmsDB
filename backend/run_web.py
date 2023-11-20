import binascii

from flask import Flask
from flask import render_template
from db_classes import *

from kinopoisk.movie import Movie

app = Flask(__name__)

@app.route('/search/<s>')
def search_page(s):
    all_films = Film.get_all_films()
    films = []
    s = s.replace("%","\\").encode('utf-8').decode('unicode-escape')

    for film in all_films:
        if film.name.find(s) > 0:
            films.append(film)

    return render_template('search.html', title=s, films=films)


@app.route('/')
def main_page():
    films = Film.get_all_films()
    genres = Genre.get_all_genres()

    return render_template('index.html', films=films, len=len(films), genres=genres)


# movie_list = Movie.objects.search(film.name)
# movie = Movie(id=movie_list[0].id)
# movie.get_content('main_page')

@app.route('/film/<int:id>')
def film_profile(id):
    film = Film.get_by_id(id)
    actors = film.get_actors()
    studios = film.get_studios()
    genres = film.get_genres()
    countries = film.get_countries()

    return render_template('film.html', title=film.name, film=film, actors=actors, studios=studios, genres=genres,
                           countries=countries)


@app.route('/actor/<int:id>')
def actor_profile(id):
    actor = Actor.get_by_id(id)
    films = actor.get_films()
    countries = actor.get_countries()
    gender = Gender.get_by_id(actor.genderId)

    return render_template('actor.html', title=actor.name + " " + actor.surname, films=films, actor=actor,
                           countries=countries, gender=gender)


@app.route('/studio/<int:id>')
def studio_profile(id):
    studio = Studio.get_by_id(id)
    films = studio.get_films()

    return render_template('studio.html', title=studio.name, films=films, studio=studio)


@app.route('/genre/<int:id>')
def genre_page(id):
    genre = Genre.get_by_id(id)
    films = genre.get_films()

    return render_template('genre.html', title=genre.name, films=films, genre=genre)


@app.route('/country/<int:id>')
def country_page(id):
    country = Country.get_by_id(id)
    films = country.get_films()
    actors = country.get_actors()

    return render_template('country.html', title=country.name, films=films, country=country, actors=actors)


if __name__ == '__main__':
    app.run()
