import binascii

from flask import Flask, url_for
from flask import render_template
from db_classes import *
import urllib.parse

app = Flask(__name__)


@app.route('/')
@app.route('/index/<int:page>')
def main_page(page=1):
    films = Film.get_page(page)
    films_count = Film.get_film_count()
    pages_count = films_count // 20 + 1

    genres = Genre.get_all_genres()

    return render_template('index.html',
                           films=films,
                           len=films_count,
                           genres=genres,
                           p_count=pages_count,
                           page=page)


@app.route('/film/<int:id>')
def film_profile(id):
    film = Film.get_by_id(id)
    actors = film.get_actors()
    studios = film.get_studios()
    genres = film.get_genres()
    countries = film.get_countries()

    return render_template('film.html',
                           film=film,
                           actors=actors,
                           studios=studios,
                           genres=genres,
                           countries=countries)


@app.route('/actor/<int:id>')
def actor_profile(id):
    actor = Actor.get_by_id(id)
    films = actor.get_films()
    countries = actor.get_countries()
    gender = Gender.get_by_id(actor.genderId)

    return render_template('actor.html',
                           films=films,
                           actor=actor,
                           countries=countries,
                           gender=gender)


@app.route('/studio/<int:id>')
def studio_profile(id):
    studio = Studio.get_by_id(id)
    films = studio.get_films()

    return render_template('studio.html',
                           films=films,
                           studio=studio)


@app.route('/genre/<int:id>')
def genre_page(id):
    genre = Genre.get_by_id(id)
    films = genre.get_films()

    return render_template('genre.html',
                           films=films,
                           genre=genre)


@app.route('/country/<int:id>')
def country_page(id):
    country = Country.get_by_id(id)
    films = country.get_films()
    actors = country.get_actors()

    return render_template('country.html',
                           films=films,
                           country=country,
                           actors=actors)


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
    app.run()
