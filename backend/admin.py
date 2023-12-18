from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from init import db
from db_classes import Film
from db_classes import Genre
from db_classes import Country
from db_classes import Actor
from kinopoisk_unofficial.request.staff.person_request import PersonRequest
import sys

api_client = KinopoiskApiClient("7a0fcfa4-0ad1-43d2-a148-e3dcb778d11c")


def add_film_kp(id_kp: int):
    request = FilmRequest(id_kp)
    response = api_client.films.send_film_request(request)

    films_count = Film.get_film_count()
    query = "INSERT INTO Films VALUES (?, ?, ?, ?, ?, ?)"
    film = response.film

    db.sql_do(query, [films_count + 1,
                      str(film.name_ru),
                      str(film.description),
                      1,
                      float(film.rating_kinopoisk),
                      film.year])

    for genre in film.genres:
        print(genre.genre)
        genre_bd = Genre.get_by_name(genre.genre)
        genre_id = None

        if genre_bd:
            genre_id = genre_bd.id

        if genre_id:
            query = "INSERT INTO FilmsGenres VALUES (?, ?)"

            db.sql_do(query, [films_count + 1, genre_id])
        else:
            query = "INSERT INTO Genres VALUES (?, ?)"
            genre_id = len(Genre.get_all_genres())
            db.sql_do(query, [genre_id + 1, genre.genre])

            query = "INSERT INTO FilmsGenres VALUES (?, ?)"

            db.sql_do(query, [films_count + 1, genre_id + 1])

    for country in film.countries:
        print(country.country)
        country_bd = Country.get_by_name(country.country)
        country_id = None

        if country_bd:
            country_id = country_bd.id

        if country_id:
            query = "INSERT INTO FilmsCountries VALUES (?, ?)"

            db.sql_do(query, [films_count + 1, country_id])
        else:
            query = "INSERT INTO Countries VALUES (?, ?)"
            country_id = len(Country.get_all_countries())
            db.sql_do(query, [country_id + 1, country.country])

            query = "INSERT INTO FilmsCountries VALUES (?, ?)"

            db.sql_do(query, [films_count + 1, country_id + 1])


def add_actor_kp(id_kp: int):
    request = PersonRequest(id_kp)
    response = api_client.staff.send_person_request(request)

    actors_count = Actor.get_actors_count()
    query = "INSERT INTO Actors VALUES (?, ?, ?, ?, ?, ?)"
    actor = response

    gender_id = 1
    if actor.sex.name == actor.sex.FEMALE:
        gender_id = 2

    db.sql_do(query,
              [actors_count + 1,
               actor.nameRu.split(" ")[1],
               actor.nameRu.split(" ")[0],
               "https://ru.wikipedia.org/",
               gender_id,
               actor.birthday])

    for film in actor.films:
        print(film.name_ru)
        film_bd = Film.get_by_name(film.name_ru)
        film_id = None

        if film_bd:
            film_id = film_bd.id

        if film_id:
            query = "INSERT INTO FilmsActors VALUES (?, ?)"

            db.sql_do(query, [film_id, actors_count + 1])

    country_bd = Country.get_by_name(actor.birthplace)
    country_id = None

    if country_bd:
        country_id = country_bd.id

    if country_id:
        query = "INSERT INTO ActorsCountries VALUES (?, ?)"

        db.sql_do(query, [actors_count + 1, country_id])
    else:
        query = "INSERT INTO Countries VALUES (?, ?)"
        country_id = len(Country.get_all_countries())
        db.sql_do(query, [country_id + 1, actor.birthplace])

        query = "INSERT INTO ActorsCountries VALUES (?, ?)"

        db.sql_do(query, [actors_count + 1, country_id + 1])


def del_film(id: int):
    query = "DELETE from Films where id = ?"
    db.sql_do(query, [id])

    query = "DELETE from FilmsCountries where idFilm = ?"
    db.sql_do(query, [id])

    query = "DELETE from FilmsGenres where idFilm = ?"
    db.sql_do(query, [id])

    query = "DELETE from FilmsActors where idFilm = ?"
    db.sql_do(query, [id])

    query = "DELETE from FilmsStudios where idFilm = ?"
    db.sql_do(query, [id])


def del_actor(id: int):
    query = "DELETE from Actors where id = ?"
    db.sql_do(query, [id])

    query = "DELETE from ActorsCountries where idActor = ?"
    db.sql_do(query, [id])

    query = "DELETE from FilmsActors where idActor = ?"
    db.sql_do(query, [id])


def add_film(id, name, description, budget, rating, dateFound):
    query = "INSERT INTO Films VALUES (?, ?, ?, ?, ?, ?)"
    db.sql_do(query, [id, name, description, budget, rating, dateFound])


def add_actor(id, surname, name, wikiLink, genderId, dateBirth):
    query = "INSERT INTO Actors VALUES (?, ?, ?, ?, ?, ?)"
    db.sql_do(query, [id, surname, name, wikiLink, genderId, dateBirth])


def edit_film(id, name=None, description=None, budget=None, rating=None, dateFound=None):
    if name:
        query = "Update Films set name = ? where id = ?"
        db.sql_do(query, [name, id])
    if description:
        query = "Update Films set description = ? where id = ?"
        db.sql_do(query, [description, id])
    if budget:
        query = "Update Films set budget = ? where id = ?"
        db.sql_do(query, [budget, id])
    if rating:
        query = "Update Films set rating = ? where id = ?"
        db.sql_do(query, [rating, id])
    if dateFound:
        query = "Update Films set dateFound = ? where id = ?"
        db.sql_do(query, [dateFound, id])


def edit_actor(id, surname=None, name=None, wikiLink=None, genderId=None, dateBirth=None):
    if surname:
        query = "Update Actors set surname = ? where id = ?"
        db.sql_do(query, [surname, id])
    if name:
        query = "Update Films set name = ? where id = ?"
        db.sql_do(query, [name, id])
    if wikiLink:
        query = "Update Films set wikiLink = ? where id = ?"
        db.sql_do(query, [wikiLink, id])
    if genderId:
        query = "Update Films set genderId = ? where id = ?"
        db.sql_do(query, [genderId, id])
    if dateBirth:
        query = "Update Films set dateBirth = ? where id = ?"
        db.sql_do(query, [dateBirth, id])


if __name__ == '__main__':
    while True:
        command = input("Write a command: ")
        match command.split():
            case ["quit"]:
                break
            case ["?"]:
                print("add_actor ; add_actor_kp; edit_actor; del_actor;")
                print("add_film ; add_film _kp; edit_film; del_film;")
            case ["add_actor", id, surname, name, wikiLink, genderId, dateBirth]:
                add_actor(id, surname, name, wikiLink, genderId, dateBirth)
            case ["add_film", id, name, description, budget, rating, dateFound]:
                add_film(id, name, description, budget, rating, dateFound)
            case ["add_film_kp", id]:
                add_film_kp(id)
            case ["add_actor_kp", id]:
                add_actor_kp(id)
            case ["del_actor", id]:
                del_actor(id)
            case ["del_film", id]:
                del_film(id)
            case ["edit_actor", id, surname, name, wikiLink, genderId, dateBirth]:
                edit_actor(id, surname, name, wikiLink, genderId, dateBirth)
            case ["edit_film", id, name, description, budget, rating, dateFound]:
                edit_actor(id, name, description, budget, rating, dateFound)
            case _:
                print(f"Sorry, I couldn't understand {command!r}")
