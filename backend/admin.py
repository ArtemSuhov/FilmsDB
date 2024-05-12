from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from init import db
from db_classes import Film, Genre, Country, Actor
from kinopoisk_unofficial.request.staff.person_request import PersonRequest

api_client = KinopoiskApiClient("7a0fcfa4-0ad1-43d2-a148-e3dcb778d11c")


def add_film_kp(id_kp: int):
    request = FilmRequest(id_kp)
    response = api_client.films.send_film_request(request)

    film = response.film

    query = "INSERT INTO Films (name, description, budget, rating, dateFound) VALUES (?, ?, ?, ?, ?)"
    db.sql_do(query, [film.name_ru, film.description, 1, float(film.rating_kinopoisk), film.year])

    film_id = Film.get_film_count()

    for genre in film.genres:
        genre_bd = Genre.get_by_name(genre.genre)
        if genre_bd:
            genre_id = genre_bd.id
        else:
            db.sql_do("INSERT INTO Genres (name) VALUES (?)", [genre.genre])
            genre_bd = Genre.get_by_name(genre.genre)
            genre_id = genre_bd.id

        db.sql_do("INSERT INTO FilmsGenres VALUES (?, ?)", [film_id, genre_id])

    for country in film.countries:
        country_bd = Country.get_by_name(country.country)
        if country_bd:
            country_id = country_bd.id
        else:
            db.sql_do("INSERT INTO Countries (name) VALUES (?)", [country.country])
            country_bd = Country.get_by_name(country.country)
            country_id = country_bd.id

        db.sql_do("INSERT INTO FilmsCountries VALUES (?, ?)", [film_id, country_id])


def add_actor_kp(id_kp: int):
    request = PersonRequest(id_kp)
    response = api_client.staff.send_person_request(request)

    actor = response
    gender_id = 1 if actor.sex.name == actor.sex.FEMALE else 2

    db.sql_do("INSERT INTO Actors (surname, name, wikiLink, genderId, dateBirth) VALUES (?, ?, ?, ?, ?)",
              [actor.nameRu.split(" ")[1], actor.nameRu.split(" ")[0], "https://ru.wikipedia.org/",
               gender_id, actor.birthday])

    actor_id = Actor.get_actors_count()

    for film in actor.films:
        film_bd = Film.get_by_name(film.name_ru)
        if film_bd:
            film_id = film_bd.id
            db.sql_do("INSERT INTO FilmsActors VALUES (?, ?)", [film_id, actor_id])

    country_bd = Country.get_by_name(actor.birthplace)
    if country_bd:
        country_id = country_bd.id
    else:
        db.sql_do("INSERT INTO Countries (name) VALUES (?)", [actor.birthplace])
        country_bd = Country.get_by_name(actor.birthplace)
        country_id = country_bd.id

    db.sql_do("INSERT INTO ActorsCountries VALUES (?, ?)", [actor_id, country_id])


def del_film(id: int):
    db.sql_do("DELETE FROM Films WHERE id = ?", [id])
    db.sql_do("DELETE FROM FilmsCountries WHERE idFilm = ?", [id])
    db.sql_do("DELETE FROM FilmsGenres WHERE idFilm = ?", [id])
    db.sql_do("DELETE FROM FilmsActors WHERE idFilm = ?", [id])
    db.sql_do("DELETE FROM FilmsStudios WHERE idFilm = ?", [id])


def del_actor(id: int):
    db.sql_do("DELETE FROM Actors WHERE id = ?", [id])
    db.sql_do("DELETE FROM ActorsCountries WHERE idActor = ?", [id])
    db.sql_do("DELETE FROM FilmsActors WHERE idActor = ?", [id])


def add_film(name, description, budget, rating, dateFound):
    db.sql_do("INSERT INTO Films (name, description, budget, rating, dateFound) VALUES (?, ?, ?, ?, ?)",
              [name, description, budget, rating, dateFound])


def add_actor(id, surname, name, wikiLink, genderId, dateBirth):
    db.sql_do("INSERT INTO Actors (surname, name, wikiLink, genderId, dateBirth) VALUES (?, ?, ?, ?, ?)",
              [surname, name, wikiLink, genderId, dateBirth])


def edit_film(id, name=None, description=None, budget=None, rating=None, dateFound=None):
    if name:
        db.sql_do("UPDATE Films SET name = ? WHERE id = ?", [name, id])
    if description:
        db.sql_do("UPDATE Films SET description = ? WHERE id = ?", [description, id])
    if budget:
        db.sql_do("UPDATE Films SET budget = ? WHERE id = ?", [budget, id])
    if rating:
        db.sql_do("UPDATE Films SET rating = ? WHERE id = ?", [rating, id])
    if dateFound:
        db.sql_do("UPDATE Films SET dateFound = ? WHERE id = ?", [dateFound, id])


def edit_actor(id, surname=None, name=None, wikiLink=None, genderId=None, dateBirth=None):
    if surname:
        db.sql_do("UPDATE Actors SET surname = ? WHERE id = ?", [surname, id])
    if name:
        db.sql_do("UPDATE Actors SET name = ? WHERE id = ?", [name, id])
    if wikiLink:
        db.sql_do("UPDATE Actors SET wikiLink = ? WHERE id = ?", [wikiLink, id])
    if genderId:
        db.sql_do("UPDATE Actors SET genderId = ? WHERE id = ?", [genderId, id])
    if dateBirth:
        db.sql_do("UPDATE Actors SET dateBirth = ? WHERE id = ?", [dateBirth, id])


if __name__ == '__main__':
    while True:
        command = input("Write a command: ")
        parts = command.split()
        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        if cmd == "quit":
            break
        elif cmd == "?":
            print("add_actor, add_actor_kp, edit_actor, del_actor")
            print("add_film, add_film_kp, edit_film, del_film")
        elif cmd == "add_actor":
            add_actor(*args)
        elif cmd == "add_film":
            add_film(*args)
        elif cmd == "add_film_kp":
            add_film_kp(*args)
        elif cmd == "add_actor_kp":
            add_actor_kp(*args)
        elif cmd == "del_actor":
            del_actor(*args)
        elif cmd == "del_film":
            del_film(*args)
        elif cmd == "edit_actor":
            edit_actor(*args)
        elif cmd == "edit_film":
            edit_film(*args)
        else:
            print(f"Sorry, I couldn't understand {command!r}")
