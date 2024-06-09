import logging
from init import db
from typing import List

PAGE_SIZE = 20

class Film:
    def __init__(self, id, name, description, budget, rating, dateFound):
        self.id = id
        self.name = name
        self.description = description
        self.budget = budget
        self.rating = rating
        self.dateFound = dateFound

    def get_genres(self):
        query = "SELECT idGenre FROM FilmsGenres WHERE idFilm = ?"
        data = db.db_select(query, [self.id])

        genre_queries = [("SELECT * FROM Genres WHERE id = ?", (genre_id[0],)) for genre_id in data]
        genre_data = db.sql_do_all(genre_queries)

        genres = []
        for g in genre_data:
            for genre in g:
                genres.append(Genre(*genre))

        return genres

    def get_countries(self):
        query = "SELECT idCountry FROM FilmsCountries WHERE idFilm = ?"
        data = db.db_select(query, [self.id])

        country_queries = [("SELECT * FROM Countries WHERE id = ?", (country_id[0],)) for country_id in data]
        country_data = db.sql_do_all(country_queries)

        countries = []
        for c in country_data:
            for country in c:
                countries.append(Country(*country))

        return countries

    def get_studios(self):
        query = "SELECT idStudio FROM FilmsStudios WHERE idFilm = ?"
        data = db.db_select(query, [self.id])

        studio_queries = [("SELECT * FROM Studios WHERE id = ?", (studio_id[0],)) for studio_id in data]
        studio_data = db.sql_do_all(studio_queries)

        studios = []
        for s in studio_data:
            for studio in s:
                studios.append(Studio(*studio))

        return studios

    @staticmethod
    def full_text_search(query: str):
        full_text_query = "SELECT * FROM Films_fts WHERE Films_fts MATCH ?"
        data = db.db_select(full_text_query, [query])
        films = [Film(*film_data) for film_data in data]
        return films

    @staticmethod
    def get_film_count():
        query = "SELECT COUNT(id) from Films"
        data = db.db_select(query, [])
        return data[0][0] if data else 0

    def get_actors(self):
        query = "SELECT idActor FROM FilmsActors WHERE idFilm = ?"
        data = db.db_select(query, [self.id])

        actor_queries = [("SELECT * FROM Actors WHERE id = ?", (actor_id[0],)) for actor_id in data]
        actor_data = db.sql_do_all(actor_queries)

        actors = []
        for a in actor_data:
            for actor in a:
                actors.append(Actor(*actor))

        return actors

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Films WHERE id = ?"
        data = db.db_select(query, [id])

        if data:
            film_data = data[0]
            return Film(*film_data)

    @staticmethod
    def get_by_name(name: str):
        query = "SELECT * FROM Films WHERE name = ?"
        try:
            data = db.db_select(query, [name])
            if data:
                film_data = data[0]
                return Film(*film_data)
        except Exception as e:
            logging.error(f"Failed to get film by name: {e}")

    @staticmethod
    def get_page(n: int):
        query = "SELECT * FROM Films LIMIT ? OFFSET ?"
        offset = (n - 1) * PAGE_SIZE
        data = db.db_select(query, [PAGE_SIZE, offset])

        films = [Film(*film_data) for film_data in data]
        return films


class Studio:
    def __init__(self, id, name, wikiLink, dateFound):
        self.id = id
        self.name = name
        self.wikiLink = wikiLink
        self.dateFound = dateFound

    def get_films(self):
        query = "SELECT idFilm FROM FilmsStudios WHERE idStudio = ?"
        data = db.db_select(query, [self.id])

        film_queries = [("SELECT * FROM Films WHERE id = ?", (film_id[0],)) for film_id in data]
        film_data = db.sql_do_all(film_queries)

        films = []
        for f in film_data:
            for film in f:
                films.append(Film(*film))

        return films

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Studios WHERE id = ?"
        data = db.db_select(query, [id])
        if data:
            studio_data = data[0]
            return Studio(*studio_data)

    @staticmethod
    def filter_films(genres: List[str], min_rating: float, countries: List[str]):
        query = "SELECT f.* FROM Films f"
        constraints = []
        params = []

        if genres:
            query += " JOIN FilmsGenres fg ON f.id = fg.idFilm"
            query += " JOIN Genres g ON fg.idGenre = g.id"
            constraints.append("g.name IN ({})".format(','.join(['?'] * len(genres))))
            params.extend(genres)

        if min_rating:
            constraints.append("f.rating >= ?")
            params.append(min_rating)

        if countries:
            constraints.append(
                "EXISTS (SELECT 1 FROM FilmsCountries fc JOIN Countries c ON fc.idCountry = c.id WHERE fc.idFilm = f.id AND c.name IN ({}))".format(
                    ','.join(['?'] * len(countries))))
            params.extend(countries)

        if constraints:
            query += " WHERE " + " AND ".join(constraints)

        data = db.db_select(query, tuple(params))
        films = [Film(*film_data) for film_data in data]
        return films


class Actor:
    def __init__(self, id, surname, name, wikiLink, genderId, dateBirth):
        self.id = id
        self.surname = surname
        self.name = name
        self.wikiLink = wikiLink
        self.genderId = genderId
        self.dateBirth = dateBirth

    def get_countries(self):
        query = "SELECT idCountry FROM ActorsCountries WHERE idActor = ?"
        data = db.db_select(query, [self.id])

        country_queries = [("SELECT * FROM Countries WHERE id = ?", (country_id[0],)) for country_id in data]
        country_data = db.sql_do_all(country_queries)

        countries = []
        for c in country_data:
            for country in c:
                countries.append(Country(*country))

        return countries

    def get_films(self):
        query = "SELECT idFilm FROM FilmsActors WHERE idActor = ?"
        data = db.db_select(query, [self.id])

        film_queries = [("SELECT * FROM Films WHERE id = ?", (film_id[0],)) for film_id in data]
        film_data = db.sql_do_all(film_queries)

        films = []
        for f in film_data:
            for film in f:
                films.append(Film(*film))

        return films

    @staticmethod
    def get_actors_count():
        query = "SELECT COUNT(id) from Actors"
        data = db.db_select(query, [])
        return data[0][0] if data else 0

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Actors WHERE id = ?"
        data = db.db_select(query, [id])
        if data:
            actor_data = data[0]
            return Actor(*actor_data)


class Genre:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_films(self):
        query = "SELECT idFilm FROM FilmsGenres WHERE idGenre = ?"
        data = db.db_select(query, [self.id])

        film_queries = [("SELECT * FROM Films WHERE id = ?", (film_id[0],)) for film_id in data]
        film_data = db.sql_do_all(film_queries)

        films = []
        for f in film_data:
            for film in f:
                films.append(Film(*film))

        return films

    @staticmethod
    def get_by_name(name: str):
        query = "SELECT * FROM Genres WHERE name = ?"
        try:
            data = db.db_select(query, [name])
            if data:
                genre_data = data[0]
                return Genre(*genre_data)
        except Exception as e:
            logging.error(f"Failed to get genre by name: {e}")

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Genres WHERE id = ?"
        data = db.db_select(query, [id])
        if data:
            genre_data = data[0]
            return Genre(*genre_data)

    @staticmethod
    def get_all_genres():
        query = "SELECT * FROM Genres ORDER BY name"
        genres_data = []
        try:
            data = db.db_select(query, [])
            genres_data = [Genre(*genre_data) for genre_data in data]
        except Exception as e:
            logging.error(f"Failed to get all genres: {e}")
        return genres_data


class Country:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_films(self):
        query = "SELECT idFilm FROM FilmsCountries WHERE idCountry = ?"
        data = db.db_select(query, [self.id])

        film_queries = [("SELECT * FROM Films WHERE id = ?", (film_id[0],)) for film_id in data]
        film_data = db.sql_do_all(film_queries)

        films = []
        for f in film_data:
            for film in f:
                films.append(Film(*film))

        return films

    def get_actors(self):
        query = "SELECT idActor FROM ActorsCountries WHERE idCountry = ?"
        data = db.db_select(query, [self.id])

        actor_queries = [("SELECT * FROM Actors WHERE id = ?", (actor_id[0],)) for actor_id in data]
        actor_data = db.sql_do_all(actor_queries)

        actors = []
        for a in actor_data:
            for actor in a:
                actors.append(Actor(*actor))

        return actors

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Countries WHERE id = ?"
        data = db.db_select(query, [id])
        if data:
            country_data = data[0]
            return Country(*country_data)

    @staticmethod
    def get_by_name(name: str):
        query = "SELECT * FROM Countries WHERE name = ?"
        try:
            data = db.db_select(query, [name])
            if data:
                country_data = data[0]
                return Country(*country_data)
        except Exception as e:
            logging.error(f"Failed to get country by name: {e}")

    @staticmethod
    def get_all_countries():
        query = "SELECT * FROM Countries ORDER BY name"
        countries_data = []
        try:
            data = db.db_select(query, [])
            countries_data = [Country(*country_data) for country_data in data]
        except Exception as e:
            logging.error(f"Failed to get all countries: {e}")
        return countries_data


class Gender:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Genders WHERE id = ?"
        data = db.db_select(query, [id])
        if data:
            gender_data = data[0]
            return Gender(*gender_data)
