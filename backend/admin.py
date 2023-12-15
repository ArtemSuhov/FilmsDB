from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from init import db
from db_classes import Film

api_client = KinopoiskApiClient("7a0fcfa4-0ad1-43d2-a148-e3dcb778d11c")

def add_film(id : int):
    request = FilmRequest(id)
    response = api_client.films.send_film_request(request)

    films_count = Film.get_film_count()
    query = "INSERT INTO Films VALUES (?, ?, ?, ?, ?, ?)"
    film = response.film
    print(films_count + 1, str(film.name_ru), str(film.description), 0, float(film.rating_kinopoisk), int(film.year))

    db.sql_do(query, [films_count + 1, str(film.name_ru), str(film.description), 0, float(film.rating_kinopoisk), film.year])

if __name__ == '__main__':
    add_film(507)
